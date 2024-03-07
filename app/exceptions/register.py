# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : register.py
@Time     : 2024/3/3 22:45
@Author   : wiesZheng
@Function :
"""
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from .handlers.all_exception import AppException, all_exception_handler
from .handlers.http_exception import http_exception_handler
from .handlers.validation_exception import validation_exception_handler


def register_global_exceptions_handler(app: FastAPI):
    """ 统一注册自定义错误处理器 """

    # 非自定义的响应状态异常处理/错误处理StarletteHTTPException
    app.add_exception_handler(HTTPException, handler=http_exception_handler)
    # 注册参数验证错误,并覆盖模式RequestValidationError
    app.add_exception_handler(RequestValidationError, handler=validation_exception_handler)
    # 处理自定义异常
    app.add_exception_handler(AppException, handler=all_exception_handler)
