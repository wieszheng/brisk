# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 1:24
@Author   : wiesZheng
@Function :
"""
from fastapi import APIRouter
from app.apis.v1.auth import user

v1 = APIRouter(prefix="/v1")
# 定义路由列表
RegisterRouterList = [
    user,
]

for item in RegisterRouterList:
    v1.include_router(item.router)
