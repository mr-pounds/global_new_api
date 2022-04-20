from fastapi import APIRouter, Cookie
from pydantic import BaseModel

from models.account import Rights, Rights_Pydantic, User

router = APIRouter()


@router.get("/getMenuList", tags=["login"])
async def get_menu_list(token: str = Cookie(None)):
    # print(token)
    rights = await Rights.filter(parent_id=None).filter(permission=1).all()
    result = []
    for right in rights:
        result.append(
            {
                "id": right.id,
                "url": right.url,
                "title": right.title,
                "children": await Rights_Pydantic.from_queryset(
                    Rights.filter(parent_id=right.id).filter(permission=1).all()
                ),
            }
        )
    return result


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
