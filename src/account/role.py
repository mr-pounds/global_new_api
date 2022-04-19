from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from models.account import Rights, RoleRight, Roles, Roles_Pydantic

router = APIRouter()


@router.get(
    "/account/getRoleList",
    tags=["account"],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_role_list():
    return {
        "success": True,
        "code": 0,
        "msg": "",
        "data": await Roles_Pydantic.from_queryset(Roles.filter(is_delete=0).all()),
    }


class AddRoleModel(BaseModel):
    name: str
    desc: str
    right_list: list[int]


@router.post("/account/addRole", tags=["account"])
async def add_role(body: AddRoleModel):
    role = await Roles.filter(is_delete=0).filter(name=body.name).first()
    if role is not None:
        return {"code": 101, "msg": "error: role name is exist", "data": None}
    role = await Roles.create(name=body.name, desc=body.desc if body.desc else "")
    for right in body.right_list:
        await RoleRight.create(role=role, right=await Rights.filter(id=right).first())
    return {"code": 0, "msg": "ok", "data": None}


@router.get(
    "/account/getRightsByRoleId",
    tags=["account"],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_rights_by_role_id(id: int = None):
    role = await Roles.filter(id=id).first()
    if role:
        return {
            "success": True,
            "code": 0,
            "msg": "",
            "data": {
                "id": role.id,
                "name": role.name,
                "desc": role.desc,
                "rightList": [
                    item["right_id"]
                    for item in await RoleRight.filter(role_id=id).values("right_id")
                ],
            },
        }
    return {"success": False, "code": 404, "msg": "无此角色", "data": None}


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
    return {"msg": "ok", "data": None, "code": 0, "success": True}


@router.delete("/account/delRole", tags=["account"])
async def del_role(id: int):
    deleted_count = await Roles.filter(id=id).update(is_delete=1)
    await RoleRight.filter(role=id).delete()
    if not deleted_count:
        return {"success": False, "msg": "error: not found role", "data": None}
    return {"success": True, "msg": "ok", "data": None}
