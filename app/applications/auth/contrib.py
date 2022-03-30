from datetime import timedelta, datetime
from typing import Optional
import jwt
from fastapi.security import OAuth2PasswordRequestForm

from app.applications.auth.schemas import CredentialsSchema
from app.applications.auth.utils.password import verify_and_update_password
from app.applications.users.models import User
from app.conf.settings import settings


async def authenticate(credentials: OAuth2PasswordRequestForm) -> Optional[User]:
    user = await User.get_by_username(credentials.username)
    if user is None:
        return None

    verified, updated_password_hash = verify_and_update_password(credentials.password, user.password_hash)
    if not verified:
        return None

    user.last_login = datetime.utcnow()
    if updated_password_hash is not None:
        user.password_hash = updated_password_hash
    await user.save()

    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.CRYPT_ALGORITHM)
    return encoded_jwt
