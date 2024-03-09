# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : user.py
@Time     : 2024/3/3 0:52
@Author   : wiesZheng
@Function :
"""
from app.models import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, INT, BIGINT, Boolean
import uuid


class User(Base):
    __tablename__ = "brisk_users"
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(16), unique=True, index=True)
    name = Column(String(16), nullable=False, index=True)
    email = Column(String(32), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=False)
    role = Column(INT, default=0, comment="0: 普通用户 1: 组长 2: 超级管理员")
    phone = Column(String(12), unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    deleted_at = Column(BIGINT, nullable=False, default=0)
    update_user = Column(String(36), nullable=True)  # 修改人
    last_login_at = Column(DateTime)
    avatar = Column(String(128), nullable=True, default="http://154.8.177.173:9002/will/pic5.png")
    # 管理员可以禁用某个用户
    is_valid = Column(Boolean, nullable=False, default=True, comment="是否合法")

