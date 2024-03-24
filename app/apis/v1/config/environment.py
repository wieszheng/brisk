# -*- coding: utf-8 -*-

"""
@Version  : Python3.8
@FileName : environment
@Time     : 2024/3/24 18:39
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Depends

from app.apis import Permission
from app.schemas.environment import EnvironmentSchemaBase, UpdateEnvironmentParam
from app.services.config.environment import EnvironmentService
from app.utils.responses import Fail, Success
from config import Settings

router = APIRouter(prefix="/config", tags=["环境配置"])


@router.post("/environment", summary="新增环境", description="添加对应环境地址")
async def create_environment(obj: EnvironmentSchemaBase, user_info=Depends(Permission(Settings.MANAGER))):
    try:
        await EnvironmentService.create_environment(obj, user_info.get("uuid"))
        return Success()
    except Exception as e:
        return Fail(msg=str(e))
