from enum import IntEnum

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Rights(Model):

    id = fields.IntField(pk=True, source_field="rowid")
    url = fields.CharField(
        max_length=60, null=False, unique=True, index=True, description="前端路由地址"
    )
    title = fields.CharField(max_length=30, null=False, description="前端显示的名称")
    permission = fields.IntField(default=1, null=False, description="是否启用")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    parent_id = fields.IntField(null=True, description="父级id")

    class PydanticMeta:
        computed: list[str] = []
        exclude = ["create_time", "update_time", "parent_id"]


Rights_Pydantic = pydantic_model_creator(Rights, name="Rights")


class Roles(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, null=False, unique=True, description="角色名称")
    desc = fields.CharField(max_length=200, description="角色描述")
    is_delete = fields.BooleanField(default=False, description="是否删除")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class PydanticMeta:
        computed: list[str] = []
        exclude = ["create_time", "update_time", "is_delete"]


Roles_Pydantic = pydantic_model_creator(Roles, name="Roles")


class RoleRight(Model):

    id = fields.IntField(pk=True)
    role = fields.ForeignKeyField(
        "models.Roles", related_name="role", description="角色id"
    )
    right = fields.ForeignKeyField(
        "models.Rights", related_name="right", description="权限id"
    )
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "role_right"

    class PydanticMeta:
        computed: list[str] = []
        exclude = ["create_time", "update_time"]


Region = IntEnum("Region", ("全国", "北京", "上海", "广州", "深圳"))


class User(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, null=False, description="用户名")
    password = fields.CharField(max_length=60, null=False, description="密码")
    phone = fields.CharField(max_length=11, null=False, unique=True, description="手机号")
    region = fields.IntEnumField(Region, null=False, description="地区")
    role = fields.ForeignKeyField(
        "models.Roles", related_name="role_id", description="角色id"
    )
    is_delete = fields.BooleanField(default=False, description="是否删除")
    is_effect = fields.BooleanField(default=True, description="是否生效")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "user"
        order = ["id"]

    def region_name(self):
        return Region(self.region).name

    @staticmethod
    def get_region_list():
        return [i.name for i in Region]

    class PydanticMeta:
        computed: list[str] = ["region_name"]
        exclude = ["create_time", "update_time", "is_delete", "password"]


User_Pydantic = pydantic_model_creator(User, name="User")
