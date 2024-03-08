# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:03
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from sqlalchemy import or_, select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import async_session
from app.models.user import User
from app.schemas.user import UserPayload, UserBody
from app.utils.password import hash_psw, verify_psw
from config import Settings


class UserCRUD:
    @staticmethod
    async def create_user(payload: UserPayload, async_session: AsyncSession):
        users = await async_session.execute(
            select(User).where(or_(User.username == payload.username, User.email == payload.email)))
        counts = await async_session.execute(select(func.count(User.id)))
        if users.scalars().first():
            raise Exception("用户名或邮箱已存在,请修改")

        payload.password = hash_psw(password=payload.password)
        user = User(**payload.model_dump())
        user.last_login_at = datetime.now()
        # 如果用户数量为0 则注册为超管
        if counts.scalars().first() == 0:
            user.role = Settings.ADMIN

        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)
        return user

    @staticmethod
    async def login(payload: UserBody, async_session: AsyncSession):
        query = await async_session.execute(select(User).where(
            and_(User.username == payload.username,
                 User.deleted_at == 0)))
        user = query.scalars().first()
        if user is None:
            raise Exception("用户名错误")
        if not verify_psw(payload.password, user.password):
            raise Exception("密码错误")
        if not user.is_valid:
            raise Exception("您的账号已被封禁, 请联系管理员")

        user.last_login_at = datetime.now()
        await async_session.refresh(user)
        return user

    @staticmethod
    async def query_user(user_id: int):
        async with async_session() as session:
            query = await session.execute(select(User).where(and_(User.id == user_id)))
            return query.scalars().first()
