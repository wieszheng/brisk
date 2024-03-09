# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : responses.py
@Time     : 2024/3/3 22:37
@Author   : wiesZheng
@Function :
"""
import datetime
from datetime import datetime as datetime_type
import decimal
import json

import typing
from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.ext.declarative import DeclarativeMeta


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 如果对象具有keys和__getitem__属性，则返回对象的字典表示
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            return dict(obj)
        # 如果对象是datetime.datetime类型，则将其转换为字符串格式
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # 如果对象是datetime.date类型，则将其转换为字符串格式
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # 如果对象是datetime.time类型，则将其转换为ISO格式字符串
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        # 如果对象是decimal.Decimal类型，则将其转换为浮点数
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        # 如果对象是bytes类型，则将其转换为UTF-8编码的字符串
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        # 如果对象的类是DeclarativeMeta类型，则将其序列化为JSON
        elif isinstance(obj.__class__, DeclarativeMeta):
            # 如果是查询返回所有的那种models类型的，需要处理些
            # 将SqlAlchemy结果序列化为JSON--查询全部的时候的处理返回
            return self.default({i.name: getattr(obj, i.name) for i in obj.__table__.columns})
        # 如果对象是字典类型，则递归处理其中的值
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    if isinstance(obj[k], (datetime.datetime, datetime.date, DeclarativeMeta)):
                        obj[k] = self.default(obj[k])
                    else:
                        obj[k] = obj[k]
                except TypeError:
                    obj[k] = None
            return obj
        # 默认情况下，使用JSONEncoder的默认处理方式
        return json.JSONEncoder.default(self, obj)


class ApiResponse(JSONResponse):
    # 定义返回响应码--如果不指定的话则默认都是返回200
    http_status_code = 200
    # 默认成功
    api_code = 0
    # 默认Node.如果是必选的，去掉默认值即可
    data: Optional[Dict[str, Any]] = None  # 结果可以是{} 或 []
    msg = '成功'

    def __init__(self, http_status_code=None, api_code=None, data=None, msg=None, **options):
        self.msg = msg or self.msg
        self.api_code = api_code or self.api_code
        self.http_status_code = http_status_code or self.http_status_code
        self.data = data or self.data

        # 返回内容体
        body = dict(
            msg=self.msg,
            code=self.api_code,
            data=self.data,

        )
        super(ApiResponse, self).__init__(status_code=self.http_status_code, content=body, **options)

    # 这个render会自动调用，如果这里需要特殊的处理的话，可以重写这个地方
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CJsonEncoder
        ).encode("utf-8")


class Success(JSONResponse):
    def __init__(
            self,
            code: int = 200,
            msg: Optional[str] = "OK",
            data: Optional[Any] = None,
            **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


class Fail(JSONResponse):
    def __init__(
            self,
            code: int = 400,
            msg: Optional[str] = None,
            data: Optional[Any] = None,
            **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


class SuccessExtra(JSONResponse):
    def __init__(
            self,
            code: int = 200,
            msg: Optional[str] = "OK",
            data: Optional[Any] = None,
            total: int = 0,
            page: int = 1,
            page_size: int = 20,
            **kwargs,
    ):
        content = {
            "code": code,
            "msg": msg,
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


def model_to_dict(obj, *ignore: str):
    if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
        return dict(obj)
    elif isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, datetime.time):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, bytes):
        return str(obj, encoding='utf-8')
    elif isinstance(obj.__class__, DeclarativeMeta):
        data = model_to_dict({i.name: getattr(obj, i.name).strftime("%Y-%m-%d %H:%M:%S") if isinstance(
            getattr(obj, i.name), datetime_type) else getattr(obj, i.name)
                              for i in obj.__table__.columns if i.name not in ignore})
        return data
    elif isinstance(obj, dict):
        for k in obj:
            try:
                if isinstance(obj[k], (datetime.datetime, datetime.date, DeclarativeMeta)):
                    obj[k] = model_to_dict(obj[k])
                else:
                    obj[k] = obj[k]
            except TypeError:
                obj[k] = None
        return obj
    return obj
