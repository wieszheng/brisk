# -*- coding: utf-8 -*-

"""
@Version  : Python3.8
@FileName : environment
@Time     : 2024/3/24 18:27
@Author   : wiesZheng
@Software : PyCharm
"""
from app.crud.config.environment import environment_crud
from app.models import async_session
from app.schemas.environment import EnvironmentSchemaBase, UpdateEnvironmentParam


class EnvironmentService:

    @staticmethod
    async def create_environment(obj: EnvironmentSchemaBase, create_uuid: str):
        async with async_session() as session:
            async with session.begin():
                environment_name = await environment_crud.get_by_name(session, obj.name)
                if environment_name:
                    raise Exception("环境名称已存在,请修改")
                await environment_crud.create(session, obj, create_uuid)

    @staticmethod
    async def update_environment(obj: UpdateEnvironmentParam, update_uuid: str):
        async with async_session() as session:
            async with session.begin():
                environment_id = await environment_crud.get_by_id(session, obj.id)
                if environment_id:
                    raise Exception("该环境环境不存在,请检查")
                rowcount = await environment_crud.update(session, obj, update_uuid)
                return rowcount

    @staticmethod
    async def get_page_environment(page_num: int, page_size: int, name: str):
        if page_num == 0 or page_size == 0:
            raise ValueError("输入数值必须大于0")
        async with async_session() as session:
            if name:
                data, total_count = await environment_crud.get_page_users(session, page_num, page_size,
                                                                          name__rlike=name)
                return data, total_count
            data, total_count = await environment_crud.get_page_users(session, page_num, page_size)
            return data, total_count
