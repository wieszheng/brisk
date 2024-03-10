# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : address.py
@Time     : 2024/3/10 14:53
@Author   : wiesZheng
@Function :
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis import async_get_session, Permission
from app.crud.config.address import AddressCRUD
from app.schemas.address import AddressPayload
from app.utils.responses import Success, Fail, model_to_dict, SuccessExtra
from config import Settings

router = APIRouter(prefix="/config", tags=["环境配置"])


@router.post("/gateway", summary="新增网关地址", description="添加网关地址，只有组长可以操作")
async def create_gateway(payload: AddressPayload, user_info=Depends(Permission(Settings.MANAGER))):

    try:
        res = await AddressCRUD.register_address(payload, user_info.get("id"))
        return Success(data=res, total="1")
    except Exception as e:
        return Fail(msg=f"添加地址失败：{str(e)}")


@router.get("/gateway", summary="id查询网关地址")
async def get_gateway(address_id: str):
    try:
        res = await AddressCRUD.get_address(address_id)
        return Success(data=res)
    except Exception as e:
        return Fail(msg=f"查询失败：{str(e)}")


@router.get("/gateways", summary="获取网关地址列表")
async def get_gateways(session: AsyncSession = Depends(async_get_session)):
    try:
        data, total = await AddressCRUD.get_gateway_list_all(session)
        return Success(data=data, total=total)
    except Exception as e:
        return Fail(msg=f"查询失败：{str(e)}")


@router.get("/gateways/page", summary="分页获取网关地址列表")
async def get_gateway_page():
    pass


@router.put("/gateway", summary="修改网关地址")
async def update_gateway():
    pass


@router.delete("/gateway", summary="删除网关地址")
async def delete_gateway():
    pass
