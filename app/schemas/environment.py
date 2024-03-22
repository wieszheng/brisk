# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : environment
@Time     : 2024-03-22 下午 07:20
@Author   : wies Zheng
@Software : PyCharm
"""
from pydantic import BaseModel


class EnvironmentSchemaBase(BaseModel):
    name: str
    remarks: str


class UpdateEnvironmentParam(EnvironmentSchemaBase):
    id: int
