# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:24
@Author   : wiesZheng
@Function :
"""
from typing import Any, TypeVar, Generic

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.crud.auth.user import UserCRUD
from app.apis import async_get_session, model_to_dict, Permission
from app.schemas.user import UserPayload, User, UserBody
from app.utils.jwt_ import jwt_decode, jwt_encode
from config import Settings

router = APIRouter(prefix="/users", tags=["用户接口"])


# 定义通用响应模型，其中Data为泛型
T = TypeVar("T")


class APIResponseModel(BaseModel, Generic[T]):
    msg: str
    data: T = None


@router.post("/", response_model=APIResponseModel[User], summary="新增用户")
async def register(payload: UserPayload, db: AsyncSession = Depends(async_get_session)):
    try:
        user = await UserCRUD.create_user(payload, db)
        return {"msg": "OK", "data": user}
    except Exception as e:
        return {"msg": str(e)}


@router.get("/me", response_model=APIResponseModel[User], summary="获取当前登录用户信息")
async def register(payload: UserPayload, db: AsyncSession = Depends(async_get_session)):
    raise "Register"


@router.post("/login", summary="登录")
async def login(payload: UserBody, db: AsyncSession = Depends(async_get_session)):
    try:
        user = await UserCRUD.login(payload, db)
        user = model_to_dict(user, "password")
        token = jwt_encode(user)
        return {"msg": "OK", "data": user, "token": token}
    except Exception as e:
        return {"msg": str(e)}


@router.get("/page", summary="用户分页列表")
async def page(user_info=Depends(Permission(Settings.ADMIN))):
    return {"msg": user_info}