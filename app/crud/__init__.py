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

from sqlalchemy import Select, desc, asc, select, Row, func, inspect, update, delete
from sqlalchemy.exc import ArgumentError

from app.models import async_engine, Base, async_session
from typing import TypeVar, Optional, Any, Union, Callable, Type, List, Dict
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.models.base import BBaseModel
from app.utils.log import Log


async def init_create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
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


class BaseCrud:
    __log__ = Log("BaseCrud")
    __model__: Type[BBaseModel] = None
    is_deleted_column: str = "is_deleted",
    deleted_at_column: str = "deleted_at",

    @classmethod
    def _parse_filters(cls, **kwargs):
        filters = []
        for k, v in kwargs.items():
            if "__" in k:
                field_name, op = k.rsplit("__", 1)
                column = getattr(cls.__model__, field_name, None)
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
                column = getattr(cls.__model__, k, None)
                if column is not None:
                    filters.append(column == v)

        return filters

    @classmethod
    def _apply_sorting(cls,
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
                column = getattr(cls.__model__, column_name, None)
                if not column:
                    raise ArgumentError(f"无效的列名: {column_name}")

                order = validated_sort_orders[idx]
                stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

        return stmt

    @classmethod
    def _extract_matching_columns_from_schema(cls,
                                              model: Type[BBaseModel],
                                              schema: Optional[Union[Type[BaseModel], list]]):
        column_list = list(model.__table__.columns)
        if schema is not None:
            if isinstance(schema, list):
                schema_fields = schema
            else:
                schema_fields = schema.model_fields.keys()

            column_list = []
            for column_name in schema_fields:
                if hasattr(model, column_name):
                    column_list.append(getattr(model, column_name))

        return column_list

    @classmethod
    @connect(True)
    async def create(cls,
                     model: BBaseModel,
                     session: AsyncSession = None):

        # object_dict = obj.model_dump()
        #
        # model_object = cls.__model__(**object_dict)
        session.add(model)
        await session.flush()
        session.expunge(model)
        return model

    @classmethod
    @connect()
    async def get(cls,
                  session: AsyncSession = None,
                  schema_to_select: Optional[Type[BaseModel]] = None,
                  **kwargs: Any):
        to_select = cls._extract_matching_columns_from_schema(
            model=cls.__model__,
            schema=schema_to_select)

        filters = cls._parse_filters(**kwargs)
        stmt = select(*to_select).filter(*filters)
        db_row = await session.execute(stmt)
        result: Row = db_row.first()
        if result is not None:
            out: dict = dict(result._mapping)
            return out
        return None

    @classmethod
    @connect()
    async def exists(cls,
                     session: AsyncSession,
                     **kwargs: Any):
        filters = cls._parse_filters(**kwargs)
        stmt = select(cls.__model__).filter(*filters).limit(1)

        result = await session.execute(stmt)
        return result.first() is not None

    @classmethod
    @connect()
    async def count(cls,
                    session: AsyncSession,
                    **kwargs: Any):
        filters = cls._parse_filters(**kwargs)
        if filters:
            count_query = select(func.count()).select_from(cls.__model__).filter(*filters)
        else:
            count_query = select(func.count()).select_from(cls.__model__)

        total_count: int = await session.scalar(count_query)
        return total_count

    @classmethod
    @connect()
    async def get_multi(
            cls,
            session: AsyncSession,
            offset: int = 0,
            limit: int = 100,
            schema_to_select: Optional[Type[BaseModel]] = None,
            sort_columns: Optional[Union[str, List[str]]] = None,
            sort_orders: Optional[Union[str, List[str]]] = None,
            **kwargs: Any):
        if limit < 0 or offset < 0:
            raise ValueError("限制和偏移量必须为非负")

        to_select = cls._extract_matching_columns_from_schema(
            model=cls.__model__,
            schema=schema_to_select)
        filters = cls._parse_filters(**kwargs)
        stmt = select(*to_select).filter(*filters)

        if sort_columns:
            stmt = cls._apply_sorting(stmt, sort_columns, sort_orders)

        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        data = [dict(row) for row in result.mappings()]
        total_count = await cls.count(session=session, **kwargs)
        return data, total_count

    @classmethod
    @connect()
    async def update(
            cls,
            session: AsyncSession,
            object: Union[UpdateSchemaType, Dict[str, Any]],
            allow_multiple: bool = False,
            **kwargs: Any):
        total_count = await cls.count(session=session, **kwargs)
        if not allow_multiple and total_count > 1:
            raise ValueError(
                f"需要一条要更新的记录，找到 {total_count}"
            )

        if isinstance(object, dict):
            update_data = object
        else:
            update_data = object.model_dump(exclude_unset=True)

        if "update_time" in update_data.keys():
            update_data["update_time"] = datetime.now()

        model_columns = {column.name for column in inspect(cls.__model__).c}
        extra_fields = set(update_data) - model_columns
        if extra_fields:
            raise ValueError(f"提供了额外字段: {extra_fields}")

        filters = cls._parse_filters(**kwargs)
        stmt = update(cls.__model__).filter(*filters).values(update_data)

        await session.execute(stmt)
        await session.commit()

    @classmethod
    @connect()
    async def db_delete(cls,
                        session: AsyncSession,
                        allow_multiple: bool = False,
                        **kwargs: Any):
        total_count = await cls.count(session=session, **kwargs)
        if not allow_multiple and total_count > 1:
            raise ValueError(
                f"应该有一条记录要删除，但找到 {total_count}."
            )

        filters = cls._parse_filters(**kwargs)
        stmt = delete(cls.__model__).filter(*filters)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    @connect()
    async def delete(cls,
                     session: AsyncSession,
                     db_row: Optional[Row] = None,
                     allow_multiple: bool = False,
                     **kwargs: Any):
        filters = cls._parse_filters(**kwargs)
        if db_row:
            if hasattr(db_row, cls.is_deleted_column):
                is_deleted_col = getattr(cls.__model__, cls.is_deleted_column)
                deleted_at_col = getattr(cls.__model__, cls.deleted_at_column, None)

                update_values = {
                    is_deleted_col: True,
                    deleted_at_col: datetime.now(),
                }
                update_stmt = (
                    update(cls.__model__).filter(*filters).values(**update_values)
                )
                await session.execute(update_stmt)
            else:
                await session.delete(db_row)
                await session.commit()

        total_count = await cls.count(session, **kwargs)
        if total_count == 0:
            raise ValueError("找不到要删除的记录")
        if not allow_multiple and total_count > 1:
            raise ValueError(
                f"应该有一条记录要删除，但找到 {total_count}"
            )

        if cls.is_deleted_column in cls.__model__.__table__.columns:
            update_stmt = (
                update(cls.__model__)
                .filter(*filters)
                .values(is_deleted=True, deleted_at=datetime.now())
            )
            await session.execute(update_stmt)
        else:
            delete_stmt = delete(cls.__model__).filter(*filters)
            await session.execute(delete_stmt)

        await session.commit()
