# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : client
@Time     : 2024-03-22 上午 11:41
@Author   : wies Zheng
@Software : PyCharm
"""
from datetime import timedelta
import asyncio

import httpx

from app.enums.http import RespFmt, HttpMethod


class AsyncHttpClient:

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None, resp_fmt: RespFmt = RespFmt.JSON):
        """构造异步HTTP客户端"""
        self.default_timeout = timeout
        self.default_headers = headers or {}
        self.default_resp_fmt = resp_fmt
        self.client = httpx.AsyncClient()
        self.response: httpx.Response

    async def _request(
            self,
            method: HttpMethod, url: str,
            params: dict = None, data: dict = None,
            timeout: timedelta = None, **kwargs
    ):
        """内部请求实现方法

        创建客户端会话,构造并发送HTTP请求,返回响应对象

        Args:
            method: HttpMethod 请求方法, 'GET', 'POST' 等
            url: 请求URL
            params: 请求查询字符串参数字典
            data: 请求体数据字典
            timeout: 超时时间,单位秒
            kwargs: 其他关键字参数

        Returns:
            httpx.Response: HTTP响应对象
        """
        timeout = timeout or self.default_timeout
        headers = self.default_headers or {}
        self.response = await self.client.request(
            method=method.value,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout.total_seconds(),
            **kwargs
        )
        return self.response

    def _parse_response(self, resp_fmt: RespFmt = None):
        """解析响应

        Args:
            resp_fmt: 响应格式

        Returns:
            resp Union[dict, bytes, str]
        """
        resp_fmt = resp_fmt or self.default_resp_fmt
        resp_content_mapping = {
            RespFmt.JSON: self.json,
            RespFmt.BYTES: self.bytes,
            RespFmt.TEXT: self.text,
        }
        resp_func = resp_content_mapping.get(resp_fmt)
        return resp_func()

    def json(self):
        return self.response.json()

    def bytes(self):
        return self.response.content

    def text(self):
        return self.response.text

    async def get(self, url: str, params: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """GET请求

        Args:
            url: 请求URL
            params: 请求查询字符串参数字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict or bytes
        """

        await self._request(HttpMethod.GET, url, params=params, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    async def post(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """POST请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict or bytes
        """
        await self._request(HttpMethod.POST, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    async def put(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """PUT请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict
        """
        await self._request(HttpMethod.PUT, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    async def delete(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """DELETE请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict
        """
        await self._request(HttpMethod.DELETE, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)
