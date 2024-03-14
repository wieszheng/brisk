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


class PrimaryIdMixin:
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), comment="主键id")


class TimestampMixin:
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")


class OperateMixin:
    create_user = Column(String(36), nullable=False, comment="创建人")
    update_user = Column(String(36), nullable=True, comment="更新人")


class TombstoneMixin:
    is_deleted = Column(BIGINT, nullable=False, default=0, comment="0: 未删除 1: 已删除")


class BBaseModel(Base,
                 TimestampMixin, PrimaryIdMixin,
                 OperateMixin, TombstoneMixin):
    __abstract__ = True
