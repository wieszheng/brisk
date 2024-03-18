# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : user
@Time     : 2024-03-18 下午 04:37
@Author   : wies Zheng
@Software : PyCharm
"""
from datetime import datetime

from app.crud.auth.user import user_crud
from app.models import async_session
from app.schemas.user import UserPayload
from app.utils.password import hash_psw
from config import Settings


class UserService:
    @staticmethod
    async def create_user(payload: UserPayload):
        async with async_session() as session:
            name = await user_crud.get_by_name(session=session, name=payload.username)
            if name:
                raise Exception("用户名已存在,请修改")
            email = await user_crud.get_by_email(session=session, email=payload.email)
            if email:
                raise Exception("邮箱已存在,请修改")
            return await user_crud.create(session=session, obj=payload)

    # @staticmethod
    # async def create_user(payload: UserPayload, async_session: AsyncSession):
    #     users = await async_session.execute(
    #         select(User).where(or_(User.username == payload.username, User.email == payload.email)))
    #     counts = await async_session.execute(select(func.count(User.id)))
    #     if users.scalars().first():
    #         raise Exception("用户名或邮箱已存在,请修改")
    #
    #     payload.password = hash_psw(password=payload.password)
    #     user = User(**payload.model_dump())
    #     user.last_login_at = datetime.now()
    #     # 如果用户数量为0 则注册为超管
    #     if counts.scalars().first() == 0:
    #         user.role = Settings.ADMIN
    #
    #     async_session.add(user)
    #     await async_session.commit()
    #     await async_session.refresh(user)
    #     return user
    # @staticmethod
    # async def login(payload: UserBody, async_session: AsyncSession):
    #     query = await async_session.execute(select(User).where(
    #         and_(User.username == payload.username,
    #              User.deleted_at == 0)))
    #     user = query.scalars().first()
    #     if user is None:
    #         raise Exception("用户名错误")
    #     if not verify_psw(payload.password, user.password):
    #         raise Exception("密码错误")
    #     if not user.is_valid:
    #         raise Exception("您的账号已被封禁, 请联系管理员")
    #
    #     user.last_login_at = datetime.now()
    #     await async_session.refresh(user)
    #     return user
    #
    # @staticmethod
    # async def query_user(user_id: int):
    #     async with async_session() as session:
    #         query = await session.execute(select(User).where(and_(User.id == user_id)))
    #         return query.scalars().first()
    #
    # @staticmethod
    # async def list_users(async_session: AsyncSession):
    #     query = await async_session.execute(select(User))
    #     return query.scalars().all()
    #
    # @staticmethod
    # async def page_list_users(async_session: AsyncSession,
    #                           pageNum: int,
    #                           pageSize: int,
    #                           keywords: str):
    #     if pageNum == 0 or pageSize == 0:
    #         raise ValueError("输入数值必须大于0")
    #
    #     search = [User.deleted_at == 0]
    #     if keywords:
    #         search.append(User.name.like("%{}%".format(keywords)))
    #     query = await async_session.execute(select(User).where(*search))
    #     data = await async_session.execute(select(User).where(*search).offset((pageNum - 1) * pageSize).limit(pageSize))
    #
    #     return data.scalars().all(), len(query.scalars().all())
    #
    # @staticmethod
    # async def update_user(update_data: UserUpdateForm, user_id: int, async_session: AsyncSession):
    #     query = await async_session.execute(select(User).where(and_(User.id == update_data.id)))
    #     user = query.scalars().first()
    #     if not user:
    #         raise Exception("该用户不存在, 请检查")
    #     if isinstance(update_data, dict):
    #         update_data = update_data
    #     else:
    #         update_data = update_data.model_dump(exclude_unset=True)
    #
    #     update_data["updated_at"] = datetime.now()
    #     update_data["update_user"] = user_id
    #     stmt = update(User).where(and_(User.id == update_data.get("id"))).values(update_data)
    #
    #     await async_session.execute(stmt)
    #     await async_session.commit()
