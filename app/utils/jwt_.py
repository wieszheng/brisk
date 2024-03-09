# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : jwt_.py
@Time     : 2024/3/6 21:48
@Author   : wiesZheng
@Function :
"""

from datetime import datetime, timedelta
from uuid import uuid1
import jwt
from typing import Any, Dict, Union
import pytz
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel

from config import Settings

# 设置时区
ChinaTimeZone = pytz.timezone("Asia/Shanghai")
# token过期
TokenErrorTimeOut = "TokenTimeOut"
# token非法
TokenErrorInvalid = "TokenInvalid"


class jwt_token_body(BaseModel):
    jti: str  # 签发唯一编号
    iss: str  # 签发人
    iat: datetime  # 签发时间
    exp: datetime  # 过期时间
    data: Any  # 业务数据


def jwt_encode(payload: Dict[Any, Union[str, Any]]):
    # 当前UTC时间
    current_time = datetime.now(ChinaTimeZone)
    jwt_body = jwt_token_body(
        jti=current_time.strftime("%Y%m%d%H%M%f"),
        iss=Settings.JWT_ISS,
        iat=current_time,
        exp=current_time + timedelta(minutes=Settings.JWT_EXPIRED),
        data=payload
    )
    new_data = dict({
        "jti": current_time.strftime("%Y%m%d%H%M%f"),
        "iss": Settings.JWT_ISS,
        "iat": current_time,
        "exp": current_time + timedelta(minutes=Settings.JWT_EXPIRED)},
        **payload)
    # 生成并返回jwt
    return jwt.encode(new_data,
                      key=Settings.JWT_SECRET_KEY,
                      algorithm=Settings.JWT_ALGORITHM)


def jwt_decode(token: str):
    try:
        return jwt.decode(
            token,
            key=Settings.JWT_SECRET_KEY,
            algorithms=[Settings.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise Exception("登录状态已过期, 请重新登录")
    except InvalidTokenError:
        raise Exception("Token不合法, 请重新登录")
    except Exception:
        raise Exception("登录状态校验失败, 请重新登录")
