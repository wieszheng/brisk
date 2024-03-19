# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:25
@Author   : wiesZheng
@Function :
"""
from datetime import datetime
from functools import wraps

from sqlalchemy import Select, desc, asc, select, func, update, delete, Join, inspect
from sqlalchemy.exc import ArgumentError

from app.models import async_engine, Base, async_session
from typing import TypeVar, Optional, Any, Union, Type, List, Dict, Callable, Generic

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BBaseModel
from app.utils.log import Log


async def init_create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


ModelType = TypeVar('ModelType', bound=BBaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
Transaction = TypeVar("Transaction", bool, Callable)


def connect(transaction: Transaction = False):
    """
    自动创建session装饰器
    """
    if callable(transaction):
        @wraps(transaction)
        async def wrap(cls, *args, **kwargs):
            try:
                session: AsyncSession = kwargs.pop("session", None)
                if session is not None:
                    return await transaction(cls, *args, session=session, **kwargs)
                async with async_session() as ss:
                    return await transaction(cls, *args, session=ss, **kwargs)
            except Exception as e:
                cls.__log__.error(f"操作Model: {cls.__model__.__name__}失败: {e}")
                raise f"操作数据库失败: {e}"

        return wrap

    def decorator(func):
        @wraps(func)
        async def wrapper(cls, *args, **kwargs):
            try:
                session: AsyncSession = kwargs.pop("session", None)
                nb = kwargs.get("not_begin")
                if session is not None:
                    if transaction and not nb:
                        async with session.begin():
                            return await func(cls, *args, session=session, **kwargs)
                    return await func(cls, *args[1:], session=session, **kwargs)
                async with async_session() as ss:
                    if transaction and not nb:
                        async with ss.begin():
                            return await func(cls, *args, session=ss, **kwargs)
                    return await func(cls, *args, session=ss, **kwargs)
            except Exception as e:
                cls.__log__.error(f"操作Model: {cls.__model__.__name__}失败: {e}")
                raise f"操作数据失败: {str(e)}"

        return wrapper

    return decorator


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    __log__ = Log("BaseCRUD")

    def __init__(self,
                 model: Type[ModelType],
                 is_deleted_column: str = "is_deleted",
                 deleted_at_column: str = "deleted_at"):
        self.model = model
        self.is_deleted_column = is_deleted_column
        self.deleted_at_column = deleted_at_column

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
            update_data.update({'updated_user': user_id})
        if "updated_at" in update_data.keys():
            update_data["updated_at"] = datetime.now()
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
                      user_id: str,
                      **kwargs: Any):

        filters = self._parse_filters(**kwargs)
        update_stmt = update(self.model).filter(*filters).values(is_deleted=1, updated_user=user_id)
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
                         limit: int = 10,
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

    async def get_joined_(self,
                          session: AsyncSession,
                          join_model: Type[ModelType],
                          join_prefix: Optional[str] = None,
                          join_on: Optional[Union[Join, None]] = None,
                          join_type: str = "left",
                          **kwargs: Any):
        primary_select = list(self.model.__table__.columns)
        # join_select = []
        # columns = list(join_model.__table__.columns)
        join_select = inspect(join_model).c

        if join_type == "left":
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == "inner":
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(f"无效的连接类型：{join_type}。只有“左”或“内”有效。")

        filters = self._parse_filters(**kwargs)
        if filters:
            stmt = stmt.filter(*filters)

        result = await session.execute(stmt)
        if result:
            return result.scalars().first()

        return None
