# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : base.py
@Time     : 2024/3/14 23:07
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BBaseModel
from typing import TypeVar, Optional, Any, Union, Callable, Type, List, Dict

ModelType = TypeVar('ModelType', bound=BBaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase:
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

    async def get_(self,
                   session: AsyncSession,
                   **kwargs: Any):
        filters = self._parse_filters(**kwargs)
        result = await session.execute(select(self.model).filter(*filters).limit(1))
        return result.first() is not None

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
