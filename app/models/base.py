# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : base.py
@Time     : 2024/3/3 22:12
@Author   : wiesZheng
@Function :
"""
from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")