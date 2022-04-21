from fastapi import Cookie, HTTPException, status

from models.account import User


async def get_current_user(token: str = Cookie(None)):
    user_obj = await User.filter(id=token).first()
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": 401,
                "msg": "身份信息失效，请重新登录",
                "data": None,
                "success": False,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_obj
