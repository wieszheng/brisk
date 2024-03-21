# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : base.py
@Time     : 2024/3/3 22:12
@Author   : wiesZheng
@Function :
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, func, String, DateTime, BIGINT
from app.models import Base


class PrimaryUUIdMixin:
    uuid = Column(String(36), default=str(uuid.uuid4()), comment="uuid")


class TimestampMixin:
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(BIGINT, nullable=False, default=0)


class OperateMixin:
    created_user = Column(String(36), nullable=True, comment="创建人")
    updated_user = Column(String(36), nullable=True, comment="更新人")


class TombstoneMixin:
    is_deleted = Column(BIGINT, nullable=False, default=0, comment="0: 未删除 1: 已删除")


class BBaseModel(Base,
                 TimestampMixin, PrimaryUUIdMixin,
                 OperateMixin, TombstoneMixin):
    __abstract__ = True

    def to_dict(self):
        """ 数据模型对象转字典 """
        data_dict = dict()
        base_dict = self.__dict__
        for k, v in base_dict.items():
            if str(k).startswith('_'):
                # 前缀带下划线不要
                continue
            if str(k).endswith('_time') and isinstance(v, datetime):
                # 时间字段转成时间戳
                # k = k[:-4] + 'ts'
                data_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S") if v else None
                continue

            data_dict[k] = v
        return data_dict


'''
          ```python
            {
                "id": 1,
                "name": "John Doe",
                "username": "john_doe",
                "email": "johndoe@example.com",
                "hashed_password": "hashed_password_example",
                "profile_image_url": "https://profileimageurl.com/default.jpg",
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-02T12:00:00",
                "deleted_at": null,
                "is_deleted": false,
                "is_superuser": false,
                "tier_id": 2,
                "tier_name": "Premium",
                "tier_created_at": "2022-12-01T10:00:00",
                "tier_updated_at": "2023-01-01T11:00:00"
            }
            ```
'''
