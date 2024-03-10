# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:26
@Author   : wiesZheng
@Function :
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,\
    async_sessionmaker, async_scoped_session
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Settings

# 定义数据库URL
async_database_url = f"mysql+aiomysql://{Settings.MYSQL_USER}:{Settings.MYSQL_PASSWORD}" \
                     f"@{Settings.MYSQL_HOST}:{Settings.MYSQL_PORT}/{Settings.MYSQL_DATABASE}?charset=utf8mb4"
# 创建异步引擎
async_engine = create_async_engine(async_database_url, echo=True, pool_size=50, pool_recycle=1500)

# 使用Declarative Base定义模型
Base = declarative_base()

# 初始化Session工厂
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    # autoflush=False,
    expire_on_commit=False
)
