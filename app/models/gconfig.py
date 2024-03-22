# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : gconfig
@Time     : 2024-03-22 下午 05:49
@Author   : wies Zheng
@Software : PyCharm
"""
from sqlalchemy import Column, INT, String, UniqueConstraint, TEXT, BOOLEAN

from app.models.base import BaseTable


class GlobalConfig(BaseTable):
    __tablename__ = 'brisk_global_config'

    __table_args__ = (
        UniqueConstraint('env', 'key'),
    )
    id = Column(INT, primary_key=True, comment="主键id")
    env = Column(INT)
    key = Column(String(16))
    value = Column(TEXT)
    key_type = Column(INT, nullable=False, comment="0: string 1: json 2: yaml")
    enable = Column(BOOLEAN, default=True)

    __fields__ = (env, key)
    __tag__ = '全局变量'
    __alias__ = dict(env='环境', key='名称', key_type='类型', value='值')
