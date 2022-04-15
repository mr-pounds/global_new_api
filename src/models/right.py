from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

# from setting import DB_PATH


class Rights(Model):

    id = fields.IntField(pk=True, source_field='rowid')
    url = fields.CharField(max_length=60, null=False, unique=True, index=True, description='前端路由地址')
    title = fields.CharField(max_length=30, null=False, description='前端显示的名称')
    permission = fields.IntField(default=1, null=False, description='是否启用')
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')
    parent_id = fields.IntField(null=True, description='父级id')

    class PydanticMeta:
        computed: list[str] = []
        exclude = ['create_time', 'update_time', 'parent_id']


Rights_Pydantic = pydantic_model_creator(Rights, name="Rights")
# Menus_Pydantic = pydantic_model_creator(Rights, name="Menus")
# RightsIn_Pydantic = pydantic_model_creator(Rights, name="RightsIn", exclude_readonly=True)
