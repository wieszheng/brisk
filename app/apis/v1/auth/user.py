# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:24
@Author   : wiesZheng
@Function :
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.apis import async_get_session, Permission
from app.schemas.user import RegisterUserParam, UpdateUserParam, UserSchemaBase
from app.services.auth.user import UserService
from app.utils.jwt_ import jwt_encode
from app.utils.responses import Success, Fail, model_to_dict
from config import Settings

router = APIRouter(prefix="/users", tags=["用户接口"])


@router.post("/login", summary="用户登录")
async def login(obj: UserSchemaBase):
    try:
        access_token, current_user = await UserService.login(obj)
        return Success(data=current_user, token=access_token)
    except Exception as e:
        return Fail(msg=str(e))


@router.post("/", summary="新增用户")
async def register(obj: RegisterUserParam):
    try:
        await UserService.create_user(obj)
        return Success()
    except Exception as e:
        return Fail(msg=str(e))


@router.get("/me", summary="获取当前登录用户信息")
async def register(user_info=Depends(Permission(Settings.MEMBER))):
    return Success(data=user_info)


@router.get("/list", summary="用户列表")
async def list_user(username: str = None):
    try:
        data, total = await UserService.get_users(username)
        return Success(data=data, total=total)
    except Exception as e:
        return Fail(msg=str(e))


@router.get("/page", summary="用户分页列表")
async def page(pageNum: int = 1, pageSize: int = 10):
    try:
        data, total = await UserService.get_page_users(pageNum, pageSize)
        return Success(data=data, total=total,
                       pagenum=pageNum,
                       pagesize=pageSize)
    except Exception as e:
        return Fail(msg=str(e))


@router.put("/update", summary="修改用户")
async def update(update_data: UpdateUserParam,
                 user_info=Depends(Permission(Settings.ADMIN))):
    try:
        await UserService.update_user(update_data, user_info.get("uuid"))
        return Success()
    except Exception as e:
        return Fail(msg=str(e))


@router.delete("/id", summary="删除用户")
async def delete(user_id: int, user_info=Depends(Permission(Settings.ADMIN))):
    try:
        await UserService.delete_user(user_id, user_info.get("uuid"))
        return Success()
    except Exception as e:
        return Fail(msg=str(e))


@router.patch("/password/{user_id}", summary="修改用户密码")
async def page(user_id: int):
    return {"msg": user_id}


@router.put("/avatar", summary="修改用户头像")
async def update_avatar(user_id: int, avatar_url: str):
    try:
        await UserService.update_user_avatar(user_id, avatar_url)
        return Success()
    except Exception as e:
        return Fail(msg=str(e))
