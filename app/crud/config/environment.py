# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : environment
@Time     : 2024-03-22 下午 07:17
@Author   : wies Zheng
@Software : PyCharm
"""
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCRUD
from app.models.environment import Environment
from app.schemas.environment import EnvironmentSchemaBase, UpdateEnvironmentParam


class EnvironmentCRUD(BaseCRUD[Environment, EnvironmentSchemaBase, UpdateEnvironmentParam]):
    async def get_by_name(self, session: AsyncSession, name: str):
        return await self.get_(session, name=name, is_deleted=0)

    async def get_by_id(self, session: AsyncSession, environment_id: int):
        return await self.get_(session, id=environment_id, is_deleted=0)

    async def create(self, session: AsyncSession, obj: EnvironmentSchemaBase, create_uuid: str):
        return await self.create_(session, obj, create_uuid)

    async def update(self, session: AsyncSession, obj: UpdateEnvironmentParam, update_uuid: str):
        return await self.update_(session, obj, update_uuid, id=obj.id)

    async def delete(self, session: AsyncSession, environment_id: int, update_uuid: str):
        return await self.delete_(session, update_uuid, id=environment_id)

    async def get_page_environments(self, session: AsyncSession, page_num: int, page_size: int, **kwargs):
        data, total_count = await self.get_multi_(session,
                                                  offset=(page_num - 1) * page_size,
                                                  limit=page_size,
                                                  sort_columns="name",
                                                  sort_orders="asc",
                                                  is_deleted=0,
                                                  **kwargs)
        return data, total_count


environment_crud = EnvironmentCRUD(Environment)
