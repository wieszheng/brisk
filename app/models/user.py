# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 0:52
@Author   : wiesZheng
@Function :
"""

from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, INT, BIGINT, Boolean
import uuid
from app.models.base import BaseTable


class User(BaseTable):

    __tablename__ = "brisk_users"

    id = Column(INT, primary_key=True, comment="主键id")
    username = Column(String(16), unique=True, index=True)
    nickname = Column(String(16), nullable=False, index=True)
    email = Column(String(32), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=False)
    role = Column(INT, default=0, comment="0: 普通用户 1: 组长 2: 超级管理员")
    phone = Column(String(12), unique=True)
    last_login_at = Column(DateTime)
    avatar = Column(String(128), nullable=True, default="http://154.8.177.173:9002/will/pic5.png")
    is_valid = Column(Boolean, nullable=False, default=True, comment="是否合法")
