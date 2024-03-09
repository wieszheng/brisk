# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:21
@Author   : wiesZheng
@Function :
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserPayload(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr


class UserBody(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: str
    name: str
    username: str
    phone: str
    role: int
    email: EmailStr


class UserList(BaseModel):
    total: int
    data: List[User]


class UserUpdateForm(BaseModel):
    id: str
    name: str = None
    username: str = None
    phone: str = None
    role: int = None
    email: EmailStr = None
    is_valid: bool = None
