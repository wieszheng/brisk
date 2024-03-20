# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : general
@Time     : 2024-03-20 下午 06:12
@Author   : wies Zheng
@Software : PyCharm
"""
from pydantic import BaseModel, field_validator


class PageParamSchema(BaseModel):
    pageNum: int = 0
    pageSize: int = 10

    @field_validator("pageNum", "pageSize")
    def validate_page_num(cls, v):
        if v == 0:
            raise ValueError("pageNum and pageSize 输入数值必须大于0")
        return v
