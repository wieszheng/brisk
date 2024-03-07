# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : http_exception.py
@Time     : 2024/3/3 22:28
@Author   : wiesZheng
@Function :
"""
from fastapi import Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse
from app.enums.http_response import HttpResponseEnum


# from fastapi.exceptions import HTTPException


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理非自定义的响应状态异常
    以json形式返回
    """
    # 通过响应状态码获取对应的响应信息
    exc_msg = HttpResponseEnum.use_code_get_enum_msg(exc.status_code)
    # 构建响应信息
    response_dict: dict = {
        "status_code": exc.status_code,
        "content": {"code": exc.status_code, "msg": exc_msg, "data": exc.detail},
    }
    # 如果有改变headers, 则传入headers
    if exc.headers:
        response_dict["headers"] = exc.headers
    return JSONResponse(**response_dict)
