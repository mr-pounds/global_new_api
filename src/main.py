#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib

from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

# from .dependencies import get_query_token, get_token_header
import account
import dependencies
import login
from setting import DB_PATH

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(title='tortoise-fastapi')


class Status(BaseModel):
    message: str


app.include_router(dependencies.router)
# app.include_router(items.router)
app.include_router(
    account.router,
    prefix="/api",
    tags=["account"],
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
)

app.include_router(
    login.router,
    prefix="/api",
    tags=["login"],
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
)

register_tortoise(
    app,
    db_url="sqlite://" + DB_PATH,
    modules={"models": ["models.right"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
