# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : http
@Time     : 2024-03-22 上午 11:45
@Author   : wies Zheng
@Software : PyCharm
"""
from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class RespFmt(Enum):
    """http响应格式"""
    JSON = "json"
    BYTES = "bytes"
    TEXT = "text"
