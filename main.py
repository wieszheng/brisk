# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : main.py
@Time     : 2024/3/2 23:55
@Author   : wiesZheng
@Function :
"""
import asyncio

from app import brisk, init_logging
from app.crud import init_create_table
from config import BANNER, Settings

logger = init_logging()
logger.bind(name=None).opt(ansi=True).success(f"brisk is running at <red>{Settings.APP_NAME}</red>")
logger.bind(name=None).success(BANNER)


@brisk.on_event('startup')
async def init_database():
    """初始化数据库，建表"""
    try:
        asyncio.create_task(init_create_table())
        logger.bind(name=None).success("database and tables created success.        ✔")
    except Exception as e:
        logger.bind(name=None).error(f"database and tables  created failed.        ❌")
        raise e


@brisk.on_event("shutdown")
async def shutdown():
    pass
