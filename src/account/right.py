from fastapi import APIRouter

from models.right import Rights, Rights_Pydantic

router = APIRouter()


@router.get("/account/getRightsList", tags=["account"])
async def get_rights():
    rights = await Rights.filter(parent_id=None).all()
    result = []
    for right in rights:
        result.append({
            "id": right.id,
            "url": right.url,
            "title": right.title,
            "children": await Rights_Pydantic.from_queryset(Rights.filter(parent_id=right.id).all()),
            # "children": [],
            "permission": right.permission,
        })
    return result


@router.put("/account/changeRightPermission", tags=["account"])
async def change_right_permission(id: int):
    right = await Rights.filter(id=id).first()
    if right:
        right.permission = 0 if right.permission == 1 else 1
        await right.save()
        return {
            "msg": "ok",
            "data": None
        }
    return {
        "msg": "error: not found right",
        "data": None
    }
