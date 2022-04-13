from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO(Zheng Zhizhan, 2022-04-13 21:21:01)：看文档把用户认证部分写完
