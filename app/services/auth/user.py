# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : user
@Time     : 2024-03-18 下午 04:37
@Author   : wies Zheng
@Software : PyCharm
"""
from app.crud.auth.user import user_crud
from app.models import async_session
from app.schemas.user import RegisterUserParam, UserSchemaBase, UpdateUserParam
from app.utils.jwt_ import jwt_encode
from app.utils.password import verify_psw
from config import Settings


class UserService:
    @staticmethod
    async def create_user(obj: RegisterUserParam):
        async with async_session() as session:
            async with session.begin():
                if not obj.password:
                    raise ValueError("密码为空")
                username = await user_crud.get_by_username(session, obj.username)
                if username:
                    raise Exception("用户名已存在,请修改")
                nickname = await user_crud.get_by_nickname(session, obj.nickname)
                if nickname:
                    raise Exception("昵称已存在,请修改")
                email = await user_crud.get_by_email(session, obj.email)
                if email:
                    raise Exception("邮箱已存在,请修改")
                await user_crud.create(session, obj)

    @staticmethod
    async def login(obj: UserSchemaBase):
        async with async_session() as session:
            async with session.begin():
                current_user = await user_crud.get_by_username(session, obj.username)
                if not current_user:
                    raise Exception("用户不存在")
                elif not verify_psw(obj.password, current_user.password):
                    raise Exception("密码错误")
                elif not current_user.is_valid:
                    raise Exception("用户已锁定, 登陆失败")
                new_current_user = current_user.to_dict("password")
                access_token = jwt_encode(new_current_user)
                await user_crud.update_login_time(session, obj.username)
                return access_token, new_current_user

    @staticmethod
    async def update_user(obj: UpdateUserParam, uuid: str):
        async with async_session() as session:
            async with session.begin():
                current_user = await user_crud.get_by_id(session, obj.id)
                if not current_user:
                    raise Exception("该用户不存在，请检查")
                rowcount = await user_crud.update_userinfo(session, obj, uuid)
                return rowcount

    @staticmethod
    async def delete_user(user_id: int, uuid: str):
        async with async_session() as session:
            async with session.begin():
                current_user = await user_crud.get_by_id(session, user_id)
                if not current_user:
                    raise Exception("该用户不存在，请检查")
                if current_user.role == Settings.ADMIN:
                    raise Exception("不能删除超级管理员")
                rowcount = await user_crud.delete(session, user_id, uuid)
                return rowcount

    @staticmethod
    async def update_user_avatar(user_id: int, avatar_url: str):
        async with async_session() as session:
            async with session.begin():
                rowcount = await user_crud.update_avatar(session, user_id, avatar_url)
                return rowcount

    @staticmethod
    async def get_users(username: str):
        async with async_session() as session:
            if username:
                data, total_count = await user_crud.get_all_users(session, username__rlike=username)
                list_user = [u.to_dict("password") for u in data]
                return list_user, total_count
            data, total_count = await user_crud.get_all_users(session)
            list_user = [u.to_dict("password") for u in data]
            return list_user, total_count

    @staticmethod
    async def get_page_users(page_num: int, page_size: int, username: str):
        if page_num == 0 or page_size == 0:
            raise ValueError("输入数值必须大于0")
        async with async_session() as session:
            if username:
                data, total_count = await user_crud.get_page_users(session, page_num, page_size,
                                                                   username__rlike=username)
                list_user = [u.to_dict("password") for u in data]
                return list_user, total_count
            data, total_count = await user_crud.get_page_users(session, page_num, page_size)
            list_user = [u.to_dict("password") for u in data]
            return list_user, total_count
