from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


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


class Roles(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, null=False, unique=True, description='角色名称')
    is_delete = fields.BooleanField(default=False, description='是否删除')
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')

    class PydanticMeta:
        computed: list[str] = []
        exclude = ['create_time', 'update_time', 'is_delete']


Roles_Pydantic = pydantic_model_creator(Roles, name="Roles")


class RoleRight(Model):

    id = fields.IntField(pk=True)
    role = fields.ForeignKeyField('models.Roles', related_name='role', description='角色id')
    right = fields.ForeignKeyField('models.Rights', related_name='right', description='权限id')
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')

    class Meta:
        table = 'role_right'

    class PydanticMeta:
        computed: list[str] = []
        exclude = ['create_time', 'update_time']


RoleRight_Pydantic = pydantic_model_creator(RoleRight, name="RoleRights")
