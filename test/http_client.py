# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : http_client
@Time     : 2024-03-22 下午 12:29
@Author   : wies Zheng
@Software : PyCharm
"""
import asyncio

from loguru import logger

from app.core.client import AsyncHttpClient
from app.enums.http import RespFmt


async def async_http_client_demo():
    logger.debug("async_http_client_demo")
    url = "http://www.baidu.com"

    # 调用
    data = await AsyncHttpClient().get(url, resp_fmt=RespFmt.TEXT)
    # logger.debug(data)


async def main():
    """
    该函数是一个异步函数，在函数内部使用asyncio.gather方法并发地执行两个async_http_client_demo函数和一个
    async_http_client_demo函数。asyncio.gather方法会等待所有协程完成并返回结果。
    """
    await asyncio.gather(*[async_http_client_demo(), async_http_client_demo()])
    await async_http_client_demo()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
