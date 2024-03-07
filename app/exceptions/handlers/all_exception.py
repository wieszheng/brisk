# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : all_exception.py
@Time     : 2024/3/4 23:11
@Author   : wiesZheng
@Function :
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from app.enums.http_response import HttpResponseInfo, HttpResponseEnum


class AppException(Exception):
    """应用异常基类"""

    def __init__(
        self,
        exc_info: HttpResponseInfo,
        *args,
        code: int = None,
        msg: str = None,
        err_msg: str = "",
        echo_exc: bool = False,
        **kwargs,
    ):
        super().__init__()
        _code = code if code is not None else exc_info.code
        _message = msg if msg is not None else exc_info.msg
        self._code = _code or HttpResponseEnum.FAILED.value.code
        self._message = _message or HttpResponseEnum.FAILED.value.msg
        self.err_msg = err_msg
        self.echo_exc = echo_exc
        self.args = args or ()
        self.kwargs = kwargs or {}

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._message

    def __str__(self):
        return "{}: {}".format(self.code, self.msg)


async def all_exception_handler(request: Request, exc: AppException):
    """处理自定义异常"""
    # 根据参数来决定是否保存错误堆栈信息
    if exc.echo_exc:
        pass
        # logger.error(exc, exc_info=True)
    return JSONResponse(
        status_code=200,
        content={
            "code": exc.code,
            "msg": exc.msg,
            "err_msg": exc.err_msg,
            "args": exc.args,
            "kwargs": exc.kwargs,
        },
    )