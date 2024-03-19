# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 1:21
@Author   : wiesZheng
@Function :
"""
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserSchemaBase(BaseModel):
    username: str
    password: str


class RegisterUserParam(UserSchemaBase):
    nickname: str = None
    email: EmailStr


class CustomPhoneNumber(PhoneNumber):
    default_region_code = 'CN'


class UserInfoSchemaBase(BaseModel):
    id: int
    username: str
    nickname: str
    email: EmailStr
    phone: str = None


class UpdateUserParam(UserInfoSchemaBase):
    role: int = None
    is_valid: bool = None
