# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : address.py
@Time     : 2024/3/10 14:43
@Author   : wiesZheng
@Function :
"""
from sqlalchemy import Column, INT, String, UniqueConstraint
from app.models.base import BaseTable


class Address(BaseTable):

    __tablename__ = 'brisk_address'

    __table_args__ = (
        UniqueConstraint('env', 'name'),
    )
    id = Column(INT, primary_key=True, comment='主键id')
    env = Column(INT, comment='对应环境')
    name = Column(String(32), comment="网关名称")
    gateway = Column(String(128), comment="网关地址")

    __fields__ = (name, env, gateway)
    __tag__ = '网关'
    __alias__ = dict(name='网关名称', env='环境', gateway='网关地址')
