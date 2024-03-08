# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : request.py
@Time     : 2024/3/6 23:55
@Author   : wiesZheng
@Function :
"""
from fastapi import HTTPException


class AuthException(HTTPException):
    pass


class PermissionException(HTTPException):
    pass
