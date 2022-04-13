from fastapi import APIRouter, Depends
from dependencies import oauth2_scheme


router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users(common: dict = Depends(oauth2_scheme)):
    print(common)
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
