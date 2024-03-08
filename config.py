# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : config.py
@Time     : 2024/3/2 23:56
@Author   : wiesZheng
@Function :
"""
import argparse
import os
from functools import lru_cache
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ROOT = os.path.dirname(os.path.abspath(__file__))


class AppConfigSettings(BaseSettings):
    LOG_DIR: ClassVar = os.path.join(ROOT, 'logs')

    # 服务配置信息
    APP_NAME: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int
    APP_ENV: str

    # 数据库配置
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # SalAlchemy配置
    ASYNC_DATABASE_URI: str

    # 日志配置
    LOG_ERROR: str
    LOG_INFO: str
    DEBUG: bool

    # 用户权限
    MEMBER: int
    MANAGER: int
    ADMIN: int

    # jwt配置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRED: int
    JWT_ISS: str

    # 密码加密配置
    BCRYPT_ROUNDS: int  # bcrypt迭代次数,越大耗时越长(好在python的bcrypt是C库)

BANNER = """
                                  \`-,                             
                                  |   `\                           
                                  |     \                          
                               __/.- - -.\,__                      
                          _.-'`              `'"'--..,__           
                      .-'`                              `'--.,_    
                   .'`   _                         _ ___       `)  
                 .'   .'` `'-.                    (_`  _`)  _.-'   
               .'    '--.     '.                 .-.`"`@ .-'""-,   
      .------~'     ,.---'      '-._      _.'   /   `'--':::.-'   
    /`        '   /`  _,..-----.,__ `''''`/    ;__,..--''--'`      
    `'--.,__ '    |-'`             `'---'|     |                   
            `\    \                       \   /                    
             |     |                       '-'                     
              \    |                                               
               `\  |                                               
                 \/  

        """


def parseCliArgument():
    """ 解析命令行参数 """
    import sys
    if "uvicorn" in sys.argv[0]:
        # 使用uvicorn启动时，命令行参数只能按照uvicorn的文档来，不能传自定义参数，否则报错
        return
    # 使用 argparse 定义命令行参数
    parser = argparse.ArgumentParser(description="命令行参数")
    parser.add_argument("--env", type=str, default="", help="运行环境")
    # 解析命令行参数
    args = parser.parse_args()
    # 设置环境变量
    # uvicorn模式启动，读取的.env*里面的APP_ENV
    os.environ["APP_ENV"] = args.env


@lru_cache
def getAppConfig():
    """ 获取项目配置 """
    parseCliArgument()
    runenv = os.environ.get("APP_ENV", "")
    envfile = ".env"
    if runenv != "":
        # 当是其他环境时，如测试环境: 加载 .env.test 正式环境: 加载.env.prod
        envfile = f".env.{runenv}"
    load_dotenv(os.path.join(ROOT, "conf", envfile))
    return AppConfigSettings()


Settings = getAppConfig()


