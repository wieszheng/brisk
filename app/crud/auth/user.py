# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:03
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from sqlalchemy import update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCRUD
from app.models.user import User
from app.schemas.user import RegisterUserParam, UpdateUserParam
from app.utils.password import hash_psw
from config import Settings


class UserCRUD(BaseCRUD[User, RegisterUserParam, UpdateUserParam]):

    async def create(self,
                     session: AsyncSession,
                     obj: RegisterUserParam):
        obj.password = hash_psw(password=obj.password)
        dict_obj = obj.model_dump()
        dict_obj.update({"last_login_at": datetime.now()})
        count = await self.count_(session=session)
        if count == 0:
            dict_obj.update({"role": Settings.ADMIN})
        new_user = self.model(**dict_obj)
        session.add(new_user)

    async def get_by_username(self,
                              session: AsyncSession,
                              username: str):
        return await self.get_(session, username=username, is_deleted=0)

    async def get_by_nickname(self,
                              session: AsyncSession,
                              nickname: str):
        return await self.get_(session, nickname=nickname, is_deleted=0)

    async def get_by_email(self,
                           session: AsyncSession,
                           email: str):
        return await self.get_(session, email=email, is_deleted=0)

    async def get_by_id(self,
                        session: AsyncSession,
                        user_id: str):
        return await self.get_(session, id=user_id, is_deleted=0)

    async def update_login_time(self,
                                session: AsyncSession,
                                username: str):
        user = await session.execute(
            update(self.model).where(and_(self.model.username == username)).values(last_login_at=datetime.now())
        )
        return user.rowcount


user_crud = UserCRUD(User)
