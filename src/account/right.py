from fastapi import APIRouter, Depends

from dependencies import get_current_user
from models.account import Rights
from utils import get_rights_list_utils

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/account/getRightsList", tags=["account"])
async def get_rights_list():
    result = await get_rights_list_utils()
    return {
        "success": True,
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
