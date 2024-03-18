# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:03
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCRUD
from app.models.user import User
from app.schemas.user import UserPayload, UserBody, UserUpdateForm
from app.utils.password import add_salt
from config import Settings


class UserCRUD(BaseCRUD[User, UserPayload, UserUpdateForm]):

    async def create(self,
                     session: AsyncSession,
                     obj: UserPayload):
        obj.password = add_salt(password=obj.password)
        dict_obj = obj.model_dump()
        dict_obj.update({"last_login_at": datetime.now()})
        count = self.count_(session=session)
        print(count)
        if count == 0:
            dict_obj.update({"role": Settings.ADMIN})
        print(dict_obj)
        new_user = self.model(**dict_obj)
        session.add(new_user)
        return new_user

    async def get_by_name(self,
                          session: AsyncSession,
                          name: str):
        return await self.get_(session, username=name, is_deleted=0)

    async def get_by_email(self,
                           session: AsyncSession,
                           email: str):
        return await self.get_(session, email=email, is_deleted=0)

    async def get_by_id(self,
                        session: AsyncSession,
                        user_id: str):
        return await self.get_(session, id=user_id, is_deleted=0)


user_crud = UserCRUD(User)
