# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:19
@Author   : wiesZheng
@Function :
"""
import logging
import os
import sys
from pprint import pformat

from fastapi import FastAPI
from loguru._defaults import LOGURU_FORMAT
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from app.apis.v1 import v1
from app.exceptions.register import register_global_exceptions_handler
from config import Settings, ROOT
from loguru import logger

brisk = FastAPI(
    title=Settings.APP_NAME,
    version=Settings.APP_VERSION,
    docs_url=None)
brisk.mount("/static", StaticFiles(directory=f"{ROOT}/static"), name="static")


@brisk.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=Settings.APP_NAME + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.png"
    )


# 注册自定义错误处理器
register_global_exceptions_handler(brisk)
# 加载路由
brisk.include_router(v1, prefix="/api")

brisk.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的来源，可以是字符串、字符串列表，或通配符 "*"
    allow_credentials=True,  # 是否允许携带凭证（例如，使用 HTTP 认证、Cookie 等）
    allow_methods=["*"],  # 允许的 HTTP 方法，可以是字符串、字符串列表，或通配符 "*"
    allow_headers=["*"],  # 允许的 HTTP 头信息，可以是字符串、字符串列表，或通配符 "*"
    expose_headers=["*"],  # 允许前端访问的额外响应头，可以是字符串、字符串列表
)


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict):
    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"
    format_string += "{exception}\n"
    return format_string


def make_filter(name):
    # 过滤操作，当日志要选择对应的日志文件的时候，通过filter进行筛选
    def filter_(record):
        return record["extra"].get("name") == name

    return filter_


def init_logging():
    # loggers = (
    #     logging.getLogger(name)
    #     for name in logging.root.manager.loggerDict
    #     if name.startswith("uvicorn")
    # )
    logger_names = ("uvicorn.access", "uvicorn.error", "uvicorn")
    for name in logger_names:
        logging.getLogger(name).handlers = [InterceptHandler()]

    info = os.path.join(Settings.LOG_DIR, f"{Settings.LOG_INFO}.log")
    error = os.path.join(Settings.LOG_DIR, f"{Settings.LOG_ERROR}.log")
    # 配置loguru的日志句柄，sink代表输出的目标
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
            # {"sink": info, "level": logging.DEBUG, "rotation": "500 MB", "encoding": 'utf-8'},
            # {"sink": error, "level": logging.WARNING, "serialize": True, "rotation": "500 MB", "encoding": 'utf-8'}
        ]
    )
    logger.add(info, enqueue=True, rotation="20 MB", level="DEBUG", encoding='utf-8')
    logger.add(error, enqueue=True, rotation="10 MB", level="WARNING", encoding='utf-8')
    logger.debug('日志系统已加载')

    return logger
