# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : base.py
@Time     : 2024/3/3 22:12
@Author   : wiesZheng
@Function :
"""
import uuid
from sqlalchemy import Column, func, String, DateTime, BIGINT
from app.models import Base


class PrimaryUUIdMixin:
    uuid = Column(String(36), primary_key=True, default=str(uuid.uuid4()), comment="uuid")


class TimestampMixin:
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(BIGINT, nullable=False, default=0)


class OperateMixin:
    create_user = Column(String(36), nullable=False, comment="创建人")
    update_user = Column(String(36), nullable=True, comment="更新人")


class TombstoneMixin:
    is_deleted = Column(BIGINT, nullable=False, default=0, comment="0: 未删除 1: 已删除")


class BBaseModel(Base,
                 TimestampMixin, PrimaryUUIdMixin,
                 OperateMixin, TombstoneMixin):
    __abstract__ = True


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
