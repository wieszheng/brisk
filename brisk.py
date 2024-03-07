# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : brisk.py
@Time     : 2024/3/2 23:56
@Author   : wiesZheng
@Function :
"""
import uvicorn
from config import Settings

if __name__ == "__main__":
    uvicorn.run("main:brisk", host=Settings.APP_HOST,
                port=Settings.APP_PORT, reload=False, forwarded_allow_ips="*")

