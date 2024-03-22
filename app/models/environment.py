# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : environment
@Time     : 2024-03-22 下午 05:41
@Author   : wies Zheng
@Software : PyCharm
"""
from sqlalchemy import Column, INT, String, UniqueConstraint
from app.models.base import BaseTable


class Environment(BaseTable):
    __tablename__ = 'brisk_environment'

    __table_args__ = (
        UniqueConstraint('name'),
    )
    id = Column(INT, primary_key=True)
    name = Column(String(32))
    remarks = Column(String(128))

    __fields__ = (name,)
    __tag__ = '环境'
    __alias__ = dict(name='环境名称', remarks='备注信息')
