#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import login
# from .dependencies import get_query_token, get_token_header
from account import right, role, user
from setting import DB_PATH

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(title="tortoise-fastapi")

# 导入 account 相关的接口
app.include_router(
    right.router,
    prefix="/api",
    tags=["account"],
)

app.include_router(
    role.router,
    prefix="/api",
    tags=["account"],
)

app.include_router(
    user.router,
    prefix="/api",
    tags=["account"],
)

# 导入登录相关的接口
app.include_router(
    login.router,
    prefix="/api",
    tags=["login"],
)

register_tortoise(
    app,
    db_url="sqlite://" + DB_PATH,
    modules={"models": ["models.account"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
