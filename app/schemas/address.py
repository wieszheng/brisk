# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : address.py
@Time     : 2024/3/10 14:56
@Author   : wiesZheng
@Function :
"""
from datetime import datetime

from pydantic import BaseModel, validator


class AddressPayload(BaseModel):
    env: int = None
    name: str = ''
    gateway: str = ''


class AddressOut(BaseModel):
    id: int
    env: int
    name: str
    gateway: str
    create_time: datetime
    update_time: datetime
    create_user: str
    update_user: str
    is_deleted: int
