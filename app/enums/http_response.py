# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : http_response.py
@Time     : 2024/3/3 22:39
@Author   : wiesZheng
@Function :
"""
from dataclasses import dataclass
from enum import Enum, unique
from functools import lru_cache


@dataclass
class HttpResponseInfo:
    code: int
    msg: str


@unique
class HttpResponseEnum(Enum):
    """HTTP响应枚举"""

    # 2xx(成功状态码)
    SUCCESS = HttpResponseInfo(200, "请求成功")
    CREATE = HttpResponseInfo(201, "请求成功, 服务端创建了一个新资源")
    NOT_CONTENT = HttpResponseInfo(204, "请求成功, 但响应不包含任何数据")

    # 3xx(重定向错误码)
    MOVED_PERMANENTLY = HttpResponseInfo(301, "资源永久移动到新位置")
    FOUND = HttpResponseInfo(302, "资源暂时移动到新位置")
    NOT_MODIFY = HttpResponseInfo(304, "客户端缓存仍然有效")

    # 4xx(客户端错误码)
    BAD_REQUEST = HttpResponseInfo(400, "请求无效或无法被服务端理解")
    NOT_AUTH = HttpResponseInfo(401, "用户未登录")
    NOT_PERMISSION = HttpResponseInfo(403, "当前用户身份无相关操作权限")
    NOT_FOUND = HttpResponseInfo(404, "请求接口不存在")
    REQUEST_METHOD_ERROR = HttpResponseInfo(405, "请求方法错误")
    LOCKED_REQUEST_ERROR = HttpResponseInfo(
        423, "请求失败, 请稍后重试"
    )  # 不允许并发请求
    TOO_MANY_REQUEST_ERROR = HttpResponseInfo(429, "请求过于频繁, 请稍后重试")

    # 5xx(服务端错误码)
    SERVER_ERROR = HttpResponseInfo(500, "服务错误, 无法完成请求")
    SERVER_UNAVAILABLE = HttpResponseInfo(503, "服务过载或正在维护")
    SERVER_TIMEOUT = HttpResponseInfo(504, "因服务侧原因导致的请求超时")

    # 自定义错误码
    FAILED = HttpResponseInfo(600, "请求失败")
    REQUEST_ACCESS_TOKEN_EXPIRED = HttpResponseInfo(601, "请求的access_token参数已过期")
    REQUEST_REFRESH_TOKEN_EXPIRED = HttpResponseInfo(
        602, "请求的refresh_token参数已过期"
    )
    REQUEST_PARAMS_VALID_ERROR = HttpResponseInfo(606, "请求参数校验错误")
    REQUEST_REPEATED = HttpResponseInfo(900, "重复请求, 请稍后重试")
    DEMO_DENY = HttpResponseInfo(901, "演示模式, 禁止写操作")

    @classmethod
    @lru_cache
    def get_code_msg_dict_cache(cls):
        """以缓存的方式返回响应状态码与响应信息的映射
        Returns:
            dict[int, str]: 响应状态码与响应信息的映射
        """
        result = {}
        for item in cls:
            result[item.value.code] = item.value.msg
        return result

    @classmethod
    def use_code_get_enum_msg(cls, code: int) -> str:
        """通过响应状态码获取对应的响应信息
        Args:
            code: 响应状态码

        Returns:
            str: 响应信息
        """
        mapping = cls.get_code_msg_dict_cache()
        return mapping[code]
