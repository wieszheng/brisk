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

    async def get_by_id(self, session: AsyncSession, id: int):
        return await self.get_(session, id=id, is_deleted=0)

    async def create(self,
                     session: AsyncSession,
                     obj: EnvironmentSchemaBase,
                     user_id: str):
        return await self.create_(session, obj, user_id)


environment_crud = EnvironmentCRUD(Environment)
