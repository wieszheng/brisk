# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:03
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCRUD
from app.models.user import User
from app.schemas.user import RegisterUserParam, UpdateUserParam
from app.utils.password import hash_psw
from config import Settings


class UserCRUD(BaseCRUD[User, RegisterUserParam, UpdateUserParam]):

    async def create(self, session: AsyncSession, obj: RegisterUserParam):
        obj.password = hash_psw(password=obj.password)
        user_dict = obj.model_dump()
        user_dict.update({"last_login_at": datetime.now()})
        count = await self.count_(session=session)
        if count == 0:
            user_dict.update({"role": Settings.ADMIN})
        new_user = self.model(**user_dict)
        session.add(new_user)

    async def get_by_username(self, session: AsyncSession, username: str):
        return await self.get_(session, username=username, is_deleted=0)

    async def get_by_nickname(self, session: AsyncSession, nickname: str):
        return await self.get_(session, nickname=nickname, is_deleted=0)

    async def get_by_email(self, session: AsyncSession, email: str):
        return await self.get_(session, email=email, is_deleted=0)

    async def get_by_id(self, session: AsyncSession, user_id: int):
        return await self.get_(session, id=user_id, is_deleted=0)

    async def update_login_time(self, session: AsyncSession, username: str):
        update_data = {
            "last_login_at": datetime.now()
        }
        rowcount = await self.update_(session, update_data, username=username)
        return rowcount

    async def update_userinfo(self, session: AsyncSession, obj: UpdateUserParam, update_uuid: str):
        rowcount = await self.update_(session, obj, update_uuid, id=obj.id)
        return rowcount

    async def delete(self, session: AsyncSession, user_id: int, update_uuid: str):
        return await self.delete_(session, update_uuid, id=user_id)

    async def update_avatar(self, session: AsyncSession, user_id: int, avatar_url: str):
        update_data = {
            "avatar": avatar_url
        }
        rowcount = await self.update_(session, update_data, id=user_id)
        return rowcount

    async def get_all_users(self, session: AsyncSession, **kwargs):
        filters = self._parse_filters(is_deleted=0, **kwargs)
        stmt = select(self.model).filter(*filters)
        result = await session.execute(stmt)
        data = result.scalars().all()
        return data, len(data)

    async def get_page_users(self, session: AsyncSession, pageNum: int, pageSize: int, **kwargs):
        data, total_count = await self.get_multi_(session,
                                                  offset=(pageNum - 1) * pageSize,
                                                  limit=pageSize,
                                                  sort_columns="username",
                                                  sort_orders="asc",
                                                  is_deleted=0,
                                                  **kwargs)
        return data, total_count


user_crud = UserCRUD(User)
