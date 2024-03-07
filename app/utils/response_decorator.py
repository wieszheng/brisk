# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : response_decorator.py
@Time     : 2024/3/3 13:04
@Author   : wiesZheng
@Function :
"""
import inspect
from typing import List, Callable, Any, Generic, TypeVar, Optional

from fastapi import APIRouter
from fastapi.openapi.models import Response
from pydantic import BaseModel

from pydantic.v1.generics import GenericModel
# from pydantic.v1.generics import GenericModel, Generic
# from pydantic.v1.types import T

def success_response(msg: str, data=''):
    new_body = {'success': True, 'msg': msg, 'data': data}
    return new_body


T = TypeVar('T')  # 通用类型变量


class APIResponse(BaseModel, Generic[T]):
    success: bool
    msg: str
    data: T = None


def validate_methods(methods: List[str]) -> bool:
    """验证HTTP方法列表是否合法"""
    valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]
    return all(method in valid_methods for method in methods)


def route(
        router: APIRouter,
        path: str,
        methods: List[str],
        response_model: Optional[Any] = None,
        **options):
    if not validate_methods(methods):
        raise ValueError("不合法的HTTP方法列表")

    common_response_model = APIResponse[response_model] if response_model else None

    def wrapper(func: Callable[..., Any]):
        async def decorator(*args, **kwargs):

            try:
                response = await func(*args, **kwargs)
            except Exception as e:
                # 这里可以添加更具体的异常处理，以及错误日志记录
                print(f"函数{func.__name__}执行出错：{str(e)}")
                raise
            if isinstance(response, Response):
                return response
            return success_response("OK", response)

        signature = inspect.signature(func)
        decorator.__signature__ = signature
        decorator.__name__ = func.__name__
        decorator.__doc__ = func.__doc__
        router.add_api_route(
            path,
            endpoint=decorator,
            response_model=common_response_model,
            methods=methods,
            **options
        )
        return decorator

    return wrapper