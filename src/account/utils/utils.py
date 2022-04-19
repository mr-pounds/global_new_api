from models.account import Rights, RoleRight


async def get_rights_list(
    parent_id: int | None = None,
    set_permission: int | None = None,
    filter: bool = False,
    permission_include: list | None = None,
) -> list[dict]:
    """_summary_

    Args:
        parent_id (int | None, optional): 获取子权限列表. Defaults to None.
        set_permission (int | None, optional): 将权限改为指定项, 0 为禁用, 1 为启用. Defaults to None.
        filter (bool):是否将 permission 为 0 的权限项过滤掉. Defaults to False.
        permission_include (list | None, optional): 启用的权限项. Defaults to None.

    Returns:
        list[dict]: _description_
    """

    result = []
    if filter:
        rights = await Rights.filter(parent_id=parent_id).filter(permission=1).all()
    else:
        rights = await Rights.filter(parent_id=parent_id).all()

    for right in rights:
        children = await get_rights_list(
            parent_id=right.id,
            set_permission=set_permission,
            permission_include=permission_include,
        )
        permission = right.permission if set_permission is None else set_permission
        if permission_include is not None:
            permission = 1 if right.id in permission_include else 0
        if filter and permission == 0:
            continue
        result.append(
            {
                "id": right.id,
                "url": right.url,
                "title": right.title,
                "permission": permission,
                "children": None if len(children) == 0 else children,
            }
        )
    return result


async def get_rights_list_by_role(role_id: int) -> list[dict]:
    """_summary_

    Args:
        role_id (int): _description_

    Returns:
        list[dict]: _description_
    """

    rights_map = await RoleRight.filter(role=role_id).values("right_id")
    rights_list = [right["right_id"] for right in rights_map]
    # print(rights_list)
    return await get_rights_list(permission_include=rights_list)
