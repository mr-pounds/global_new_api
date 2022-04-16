from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from models.right import Rights, RoleRight, Roles, Roles_Pydantic

from .utils import get_rights_list as get_rights_list_utils
from .utils import get_rights_list_by_role as get_rights_list_by_role_utils

router = APIRouter()


@router.get("/account/getRightsList", tags=["account"])
async def get_rights_list():
    result = await get_rights_list_utils()
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "list": result,
            "total": len(result),
        },
    }


@router.put("/account/changeRightPermission", tags=["account"])
async def change_right_permission(id: int):
    right = await Rights.filter(id=id).first()
    if right:
        right.permission = 0 if right.permission == 1 else 1
        await right.save()
        return {"msg": "ok", "data": None}
    return {"msg": "error: not found right", "data": None}


@router.get(
    "/account/getRoleList",
    tags=["account"],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_role_list():
    return await Roles_Pydantic.from_queryset(Roles.filter(is_delete=0).all())


class AddRoleModel(BaseModel):
    name: str
    desc: str
    right_list: list[int]


@router.post("/account/addRole", tags=["account"])
async def add_role(body: AddRoleModel):
    role = await Roles.filter(is_delete=0).filter(name=body.name).first()
    if role is not None:
        return {"code": 101, "msg": "error: role name is exist", "data": None}
    role = await Roles.create(name=body.name, desc=body.desc)
    for right in body.right_list:
        await RoleRight.create(role=role, right=await Rights.filter(id=right).first())
    return {"code": 0, "msg": "ok", "data": None}


@router.get(
    "/account/getRightsByRoleId",
    tags=["account"],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_rights_by_role_id(id: Optional[int] = None):
    if id is None:
        return await get_rights_list_utils(set_permission=0)
    return await get_rights_list_by_role_utils(id)


class RoleModel(BaseModel):
    id: int
    name: str
    desc: str
    right_list: list[int]


@router.put("/account/updateRole", tags=["account"])
async def update_role(body: RoleModel):
    # 删除多余的权限
    role = await Roles.filter(id=body.id).first()
    role.name = body.name
    role.desc = body.desc
    await role.save()
    await RoleRight.filter(role=body.id).filter(
        right_id__not_in=body.right_list
    ).delete()
    # 获取已创建的权限
    had_right_map = (
        await RoleRight.filter(role=body.id)
        .filter(right_id__in=body.right_list)
        .values("right_id")
    )
    had_right_list = [right["right_id"] for right in had_right_map]
    for right in body.right_list:
        if right not in had_right_list:
            await RoleRight.create(role_id=body.id, right_id=right)
    return {"msg": "ok", "data": None}


@router.delete("/account/delRole", tags=["account"])
async def del_role(id: int):
    deleted_count = await Roles.filter(id=id).update(is_delete=1)
    await RoleRight.filter(role=id).delete()
    if not deleted_count:
        return {"msg": "error: not found role", "data": None}
    return {"msg": "ok", "data": None}
