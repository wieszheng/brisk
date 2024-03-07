# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : main.py
@Time     : 2024/3/2 23:55
@Author   : wiesZheng
@Function :
"""
import asyncio

from app import brisk
from app.crud import init_create_table


@brisk.on_event('startup')
async def init_database():
    """初始化数据库，建表"""
    try:
        asyncio.create_task(init_create_table())
        print("database and tables created success.        ✔")
    except Exception as e:
        print(f"database and tables  created failed.        ❌\nerror: {e}")
        raise


@brisk.on_event("shutdown")
async def shutdown():
    pass
