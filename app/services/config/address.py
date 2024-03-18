# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : address.py
@Time     : 2024/3/17 23:12
@Author   : wiesZheng
@Function :
"""
from app.crud.config.address import address_crud
from app.models import async_session


class AddressService:
    @staticmethod
    async def get_select(*,
                         id: str = None,
                         name: str = None):
        async with async_session() as session:
            if id:
                return await address_crud.get_by_id(session, id)

            if name:
                return await address_crud.get_by_name(session, name)
