from fastapi import APIRouter, Depends
from dependencies import get_current_user


router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users(current_user: dict = Depends(get_current_user)):
    print(current_user)
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
