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

from app.crud import BaseCRUD
from app.models.address import Address
from app.schemas.address import AddressPayload, AddressOut, UpdateAddressParam


class AddressCRUD(BaseCRUD):
    model = Address

    async def create(self,
                     session: AsyncSession,
                     obj: AddressPayload,
                     user_id: str):
        return await self.create_(session, obj, user_id)

    async def update(self,
                     session: AsyncSession,
                     obj: UpdateAddressParam,
                     user_id: str):
        return await self.update_(session, obj, user_id)

    async def delete(self,
                     session: AsyncSession,
                     address_id: str):
        return await self.delete_(session, id=address_id)

    async def get_by_name(self,
                          session: AsyncSession,
                          address_name: str):
        return await self.get_(session, name=address_name, is_deleted=0)

    async def get_by_env(self,
                         session: AsyncSession,
                         address_env: str):
        return await self.get_(session, env=address_env, is_deleted=0)

    async def get_by_id(self,
                        session: AsyncSession,
                        address_id: str):
        return await self.get_(session, id=address_id, is_deleted=0)

    async def get_all(self,
                      session: AsyncSession):
        query = await session.execute(select(self.model).where(and_(Address.is_deleted == 0)))
        data = query.scalars().all()
        return data, len(data)


address_crud = AddressCRUD()
