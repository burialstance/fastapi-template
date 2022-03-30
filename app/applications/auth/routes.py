from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.applications.auth.contrib import authenticate, create_access_token
from app.applications.auth.schemas import CredentialsSchema, JWTToken
from app.conf.settings import settings

router = APIRouter()



@router.post("/access-token", response_model=JWTToken)
async def login_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires),
        "token_type": "bearer",
    }