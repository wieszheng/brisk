# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : validation_exception.py
@Time     : 2024/3/3 23:04
@Author   : wiesZheng
@Function :
"""
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.enums.http_response import HttpResponseEnum


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    处理参数验证的异常
    """
    response_info_enum = HttpResponseEnum.REQUEST_PARAMS_VALID_ERROR.value
    # 剥离出第一个错误信息的msg
    err_msg = exc.errors()[0].get("msg", "")
    # errs = exc.errors()
    # resp = HttpResp.PARAMS_VALID_ERROR
    # if errs and errs[0].get('type', '').startswith('type_error.'):
    #     resp = HttpResp.PARAMS_TYPE_ERROR
    return JSONResponse(
        status_code=HttpResponseEnum.SUCCESS.value.code,
        content={
            "code": response_info_enum.code,
            "msg": response_info_enum.msg,
            "err_msg": err_msg,
        },
    )