# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:25
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from sqlalchemy import Select, desc, asc, select, func, update, delete
from sqlalchemy.exc import ArgumentError

from app.models import async_engine, Base
from typing import TypeVar, Optional, Any, Union, Type, List, Dict

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BBaseModel


async def init_create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


ModelType = TypeVar('ModelType', bound=BBaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCRUD:
    model: Type[ModelType]

    def _parse_filters(self, **kwargs):
        filters = []
        for k, v in kwargs.items():
            if "__" in k:
                field_name, op = k.rsplit("__", 1)
                column = getattr(self.model, field_name, None)
                if column is not None:
                    raise ValueError(f"无效的筛选器列: {field_name}")

                if op == "gt":
                    filters.append(column > v)
                elif op == "lt":
                    filters.append(column < v)
                elif op == "gte":
                    filters.append(column >= v)
                elif op == "lte":
                    filters.append(column <= v)
                elif op == "ne":
                    filters.append(column != v)
            else:
                column = getattr(self.model, k, None)
                if column is not None:
                    filters.append(column == v)

        return filters

    def _apply_sorting(self,
                       stmt: Select,
                       sort_columns: Union[str, List[str]],
                       sort_orders: Optional[Union[str, List[str]]] = None):

        if sort_orders and not sort_columns:
            raise ValueError("提供的排序顺序没有相应的排序列")

        if sort_columns:
            if not isinstance(sort_columns, list):
                sort_columns = [sort_columns]

            if sort_orders:
                if not isinstance(sort_orders, list):
                    sort_orders = [sort_orders] * len(sort_columns)
                if len(sort_columns) != len(sort_orders):
                    raise ValueError(
                        "sort_columns和sort_order的长度必须匹配"
                    )

                for idx, order in enumerate(sort_orders):
                    if order not in ["asc", "desc"]:
                        raise ValueError(
                            f"排序顺序无效: {order}，只允许使用“asc”或“desc”"
                        )

            validated_sort_orders = (
                ["asc"] * len(sort_columns) if not sort_orders else sort_orders
            )

            for idx, column_name in enumerate(sort_columns):
                column = getattr(self.model, column_name, None)
                if not column:
                    raise ArgumentError(f"无效的列名: {column_name}")

                order = validated_sort_orders[idx]
                stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

        return stmt

    async def get_(self,
                   session: AsyncSession,
                   **kwargs: Any):
        filters = self._parse_filters(**kwargs)
        result = await session.execute(select(self.model).filter(*filters).limit(1))
        return result.scalars().first()

    async def create_(self,
                      session: AsyncSession,
                      obj: CreateSchemaType,
                      user_id: str = None):
        object_dict = obj.model_dump()
        if user_id:
            create_data = self.model(**object_dict, create_user=user_id)
        else:
            create_data = self.model(**object_dict)
        session.add(create_data)
        await session.commit()
        return create_data

    async def update_(self,
                      session: AsyncSession,
                      obj: Union[UpdateSchemaType, Dict[str, Any]],
                      user_id: str = None,
                      **kwargs: Any):

        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.model_dump(exclude_unset=True)
        if user_id:
            update_data.update({'update_user': user_id})
        if "update_time" in update_data.keys():
            update_data["update_time"] = datetime.now()
        filters = self._parse_filters(**kwargs)
        stmt = update(self.model).filter(*filters).values(update_data)
        result = await session.execute(stmt)
        return result.rowcount

    async def delete_db(self,
                        session: AsyncSession,
                        **kwargs: Any):
        filters = self._parse_filters(**kwargs)
        stmt = delete(self.model).filter(*filters)
        result = await session.execute(stmt)
        return result.rowcount

    async def delete_(self,
                      session: AsyncSession,
                      **kwargs: Any):
        filters = self._parse_filters(**kwargs)
        update_stmt = update(self.model).filter(*filters).values(is_deleted=1)
        result = await session.execute(update_stmt)
        return result.rowcount

    async def count_(self,
                     session: AsyncSession,
                     **kwargs: Any):
        filters = self._parse_filters(**kwargs)
        if filters:
            count_query = select(func.count()).select_from(self.model).filter(*filters)
        else:
            count_query = select(func.count()).select_from(self.model)

        total_count = await session.scalar(count_query)
        return total_count

    async def get_multi_(self,
                         session: AsyncSession,
                         offset: int = 0,
                         limit: int = 100,
                         sort_columns: Optional[Union[str, List[str]]] = None,
                         sort_orders: Optional[Union[str, List[str]]] = None,
                         **kwargs: Any):

        if limit < 0 or offset < 0:
            raise ValueError("限制和偏移量必须为非负")
        filters = self._parse_filters(**kwargs)
        stmt = select(self.model).filter(*filters)
        if sort_columns:
            stmt = self._apply_sorting(stmt, sort_columns, sort_orders)
        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        data = [dict(row) for row in result.mappings()]
        total_count = await self.count_(session=session, **kwargs)
        return data, total_count
