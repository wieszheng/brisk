# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Version  : Python 3.8.10
@FileName : log
@Time     : 2024-03-08 下午 12:45
@Author   : wies Zheng
@Software : PyCharm
"""
import inspect
import os
from loguru import logger
from config import Settings


class Log:
    def __init__(self, name: str = "brisk"):
        # 如果目录不存在则创建
        if not os.path.exists(Settings.LOG_DIR):
            os.mkdir(Settings.LOG_DIR)
        self.business = name

    def info(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Settings.LOG_INFO, func=func, line=line,
                    business=self.business, filename=file_name).debug(message)

    def error(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Settings.LOG_ERROR, func=func, line=line,
                    business=self.business, filename=file_name).error(message)

    def warning(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Settings.LOG_INFO, func=func, line=line,
                    business=self.business, filename=file_name).warning(message)

    def debug(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Settings.LOG_INFO, func=func, line=line,
                    business=self.business, filename=file_name).debug(message)

    def exception(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Settings.LOG_ERROR, func=func, line=line,
                    business=self.business, filename=file_name).exception(message)
