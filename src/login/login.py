from fastapi import APIRouter, Cookie, Depends
from pydantic import BaseModel

from dependencies import get_current_user
from models.account import User
from utils import get_rights_list_by_role_utils

router = APIRouter()


@router.get("/getMenuList", tags=["login"], dependencies=[Depends(get_current_user)])
async def get_menu_list(token: str = Cookie(None)):
    # print(token)
    if token is None:
        return {
            "sucess": False,
            "code": 401,
            "msg": "请先登录",
            "data": None,
        }
    user = await User.filter(id=token).first()
    if user is None:
        return {
            "sucess": False,
            "code": 403,
            "msg": "token 无效",
            "data": None,
        }
    # rights = await get_rights_list_by_role_utils(user.role_id)
    return {
        "sucess": True,
        "code": 0,
        "msg": "",
        "data": await get_rights_list_by_role_utils(user.role_id),
    }


class LoginModel(BaseModel):
    username: str
    password: str


@router.post("/login", tags=["login"])
async def login(body: LoginModel):
    user = await User.filter(phone=body.username).filter(password=body.password).first()
    if user is None:
        return {
            "success": True,
            "code": 101,
            "msg": "用户名或密码错误",
            "data": None,
        }
    return {"success": True, "code": 0, "msg": "", "data": {"token": user.id}}
