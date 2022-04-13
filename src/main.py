#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from fastapi import FastAPI

# from .dependencies import get_query_token, get_token_header
from account import right

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


# app.include_router(right.router)
# app.include_router(items.router)
app.include_router(
    right.router,
    prefix="/api",
    tags=["account"],
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
)
