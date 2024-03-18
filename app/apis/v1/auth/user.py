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

from app.crud.auth.user import UserCRUD
from app.apis import async_get_session, Permission
from app.schemas.user import UserPayload, UserBody, UserUpdateForm
from app.services.auth.user import UserService
from app.utils.jwt_ import jwt_encode
from app.utils.responses import Success, Fail, model_to_dict, SuccessExtra
from config import Settings

router = APIRouter(prefix="/users", tags=["用户接口"])


@router.post("/login", summary="用户登录")
async def login(payload: UserBody, db: AsyncSession = Depends(async_get_session)):
    pass


@router.post("/", summary="新增用户")
async def register(payload: UserPayload):
    try:
        user = await UserService.create_user(payload)
        user = model_to_dict(user, "password")
        token = jwt_encode(user)
        return Success(msg="注册成功", data=user, token=token)
    except Exception as e:
        return Fail(msg=str(e))


@router.get("/me", summary="获取当前登录用户信息")
async def register(user_info=Depends(Permission(Settings.MEMBER))):
    return Success(data=user_info)


@router.get("/list", summary="用户列表")
async def page(db: AsyncSession = Depends(async_get_session)):
    pass


@router.get("/page", summary="用户分页列表")
async def page(pageNum: int, pageSize: int, keywords: str = None,
               db: AsyncSession = Depends(async_get_session)):
    pass


@router.put("/update", summary="修改用户")
async def update(update_data: UserUpdateForm,
                 db: AsyncSession = Depends(async_get_session),
                 user_info=Depends(Permission(Settings.ADMIN))):
    pass


@router.delete("/id", summary="删除用户")
async def page(user_id: int):
    return {"msg": user_id}


@router.patch("/password/{user_id}", summary="修改用户密码")
async def page(user_id: int):
    return {"msg": user_id}


@router.patch("/avatar/{user_id}", summary="修改用户头像")
async def page(user_id: int):
    return {"msg": user_id}
