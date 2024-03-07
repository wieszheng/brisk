# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : config.py
@Time     : 2024/3/2 23:56
@Author   : wiesZheng
@Function :
"""
import os
from functools import lru_cache
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ROOT = os.path.dirname(os.path.abspath(__file__))


class AppConfigSettings(BaseSettings):
    LOG_DIR: ClassVar = os.path.join(ROOT, 'logs')
    # LOG_NAME: ClassVar = os.path.join(LOG_DIR, 'log.log')

    # 服务配置信息
    APP_NAME: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int

    # 数据库配置
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # SalAlchemy配置
    ASYNC_DATABASE_URI: str

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

    # 其他
    BANNER: str = """
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


@lru_cache
def getAppConfig():
    """ 获取项目配置 """
    runenv = os.environ.get("APP_ENV", "")
    envfile = os.path.join(ROOT, "conf", ".env")
    if runenv != "":
        # 当是其他环境时，如测试环境: 加载 .env.test 正式环境: 加载.env.prod
        envfile = f".env.{runenv}"
    load_dotenv(envfile)
    return AppConfigSettings()


Settings = getAppConfig()
