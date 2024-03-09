# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:22
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

import jwt
from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.auth.user import UserCRUD
from app.exceptions.request import PermissionException, AuthException
from app.models import async_session
from app.utils.responses import model_to_dict
from app.utils.jwt_ import jwt_decode
from config import Settings

FORBIDDEN = "对不起, 你没有足够的权限"


async def async_get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Permission:
    def __init__(self, role: int = Settings.MEMBER):
        self.role = role

    async def __call__(self, token: str = Header(...)):
        if not token:
            raise Exception("用户信息身份认证失败, 请检查填写的token是否正确")
        try:
            user_info = jwt_decode(token)

            if user_info.get("role", 0) < self.role:
                raise PermissionException(status.HTTP_403_FORBIDDEN, FORBIDDEN)
            user = await UserCRUD.query_user(user_info.get("id"))
            if user is None:
                raise Exception("用户不存在")
            user_info = model_to_dict(user, "password")
            return user_info
        except Exception as e:
            raise AuthException(status.HTTP_403_FORBIDDEN, str(e))


# 节点权限鉴权中间件(装饰器)
# def permission_required(permission: str, log: bool = False):
#     # 用户访问权限
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(request: Request, *args, **kwargs):
#             # 1、获取用户id，如果是超级管理员，则直接放行
#             user = True
#             if user:
#                 return await func(request, *args, **kwargs)
#             # 2、查询该用户的权限，如果存在，则放行，否则抛出异常
#             if permission != "system:login":
#                 raise AppException(HttpResp.NO_PERMISSION)
#
#             if log:
#                 # 记录无权限访问日志
#                 print("记录无权限访问日志")
#
#             # 函数调用
#             return await func(request, *args, **kwargs)
#
#         # 返回
#         return wrapper
#
#     return decorator
