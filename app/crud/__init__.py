# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:25
@Author   : wiesZheng
@Function :
"""
from app.models import async_engine, Base
from typing import TypeVar, Optional, Any, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


async def init_create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseCrud:

    def __init__(self, model):
        self.model = model

    def _parse_filters(self, **kwargs):
        filters = []
        for k, v in kwargs.items():
            if "__" in k:
                field_name, op = k.rsplit("__", 1)
                column = getattr(self.model, field_name, None)
                if column is not None:
                    raise ValueError(f"column 为空: {field_name}")

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

    async def create(self,
                     db: AsyncSession,
                     obj: CreateSchemaType
                     ) -> ModelType:

        object_dict = obj.model_dump()
        db_object = self.model(**object_dict)
        db.add(db_object)
        await db.commit()
        return db_object

    async def get(self,
                  db: AsyncSession,
                  schema_to_select: Optional[type(BaseModel)] = None,
                  return_as_model: bool = False,
                  **kwargs: Any
                  ) -> Optional[Union[dict, BaseModel]]:
        pass
