from fastapi import APIRouter

from models.right import Rights, Rights_Pydantic

router = APIRouter()


@router.get("/getMenuList", tags=["login"])
async def get_menu_list():
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
                )
                # "permission": right.permission,
            }
        )
    return result
