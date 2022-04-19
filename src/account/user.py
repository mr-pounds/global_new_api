from fastapi import APIRouter
from pydantic import BaseModel

from models.account import Roles, Roles_Pydantic, User

router = APIRouter()


@router.get("/account/getUserList", tags=["account"])
async def get_user_list():
    objs = await User.filter(is_delete=0).prefetch_related("role").all()
    # print(objs[0].role.name)
    user_list = [
        {
            "id": obj.id,
            "name": obj.name,
            "phone": obj.phone,
            "region": obj.region.name,
            "region_id": obj.region,
            "role": obj.role.name,
            "role_id": obj.role.id,
            "is_effect": obj.is_effect,
        }
        for obj in objs
    ]
    return {
        "success": True,
        "code": 0,
        "msg": "",
        "data": {
            "userList": user_list,
            "regionList": User.get_region_list(),
            "roleList": await Roles_Pydantic.from_queryset(
                Roles.filter(is_delete=0).all()
            ),
        },
    }


class AddUser(BaseModel):
    name: str
    password: str
    phone: str
    region: int
    role: int


@router.post("/account/addUser", tags=["account"])
async def add_user(user: AddUser):
    user_obj = await User.filter(phone=user.phone).first()
    # print(user_obj.id)
    if user_obj is not None:
        return {
            "success": True,
            "code": 101,
            "msg": "该手机号已被注册",
            "data": None,
        }
    await User.create(
        name=user.name,
        password=user.password,
        phone=user.phone,
        region=user.region,
        role_id=user.role,
    )
    return {
        "success": True,
        "code": 0,
        "msg": "",
        "data": None,
    }


class UpdateUser(BaseModel):
    id: int
    name: str
    phone: str
    region: int
    role: int


@router.post("/account/updateUser", tags=["account"])
async def update_user(user: UpdateUser):
    user_obj = await User.filter(id=user.id).first()
    if user_obj is None:
        return {
            "success": True,
            "code": 404,
            "msg": "用户不存在",
            "data": None,
        }
    user_obj.name = user.name
    user_obj.region = user.region
    user_obj.role_id = user.role
    await user_obj.save()
    return {
        "success": True,
        "code": 0,
        "msg": "",
        "data": None,
    }


@router.delete("/account/delUser", tags=["account"])
async def delete_user(id: int):
    user_obj = await User.filter(id=id).first()
    if user_obj is None:
        return {
            "success": True,
            "code": 404,
            "msg": "用户不存在",
            "data": None,
        }
    user_obj.is_delete = 1
    await user_obj.save()
    return {
        "success": True,
        "code": 0,
        "msg": "",
        "data": None,
    }


@router.put("/account/changeUserEffect", tags=["account"])
async def change_user_effect(id: int):
    user_obj = await User.filter(id=id).first()
    if user_obj is None:
        return {
            "success": True,
            "code": 404,
            "msg": "用户不存在",
            "data": None,
        }
    user_obj.is_effect = 0 if user_obj.is_effect else 1
    await user_obj.save()
    return {
        "success": True,
        "code": 0,
        "msg": "",
        "data": None,
    }
