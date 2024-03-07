# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : __init__.py.py
@Time     : 2024/3/3 0:19
@Author   : wiesZheng
@Function :
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from app.apis.v1 import v1
from app.exceptions.register import register_global_exceptions_handler
from config import Settings, ROOT

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
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
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
