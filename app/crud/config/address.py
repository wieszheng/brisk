# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : address.py
@Time     : 2024/3/10 15:00
@Author   : wiesZheng
@Function :
"""
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models.address import Address
from app.schemas.address import AddressPayload, AddressOut


class AddressCRUD(BaseCrud):
    __model__ = Address

    @classmethod
    async def register_address(cls, payload: AddressPayload,
                               user_id: str):
        model = Address(**payload.model_dump(),
                        create_user=user_id)
        return await cls.create(model=model)

    @classmethod
    async def get_address(cls, address_id: str):
        return await cls.get(schema_to_select=AddressOut,
                             return_as_model=False,
                             id=address_id)

    @classmethod
    async def get_gateway_list_all(cls, async_session: AsyncSession):
        query = await async_session.execute(select(Address).where(and_(Address.is_deleted == 0)))
        data = query.scalars().all()
        return data, len(data)
