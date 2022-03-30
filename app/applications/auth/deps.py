from typing import Optional

import jwt
from fastapi import Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from app.applications.auth.schemas import JWTTokenPayload
from app.applications.users.models import User
from app.conf.settings import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_ROUTE_PREFIX}/auth/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)) -> Optional[User]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.CRYPT_ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await User.get(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_active_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return current_user
