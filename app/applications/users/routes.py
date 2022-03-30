from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.applications.auth.deps import get_current_user, get_current_active_user, get_current_active_superuser
from app.applications.auth.utils.password import get_password_hash
from app.applications.users.models import User
from app.applications.users.schemas import BaseUserOut, BaseUserCreate, BaseUserUpdate
from app.conf.settings import settings

router = APIRouter()


@router.post("/create", response_model=BaseUserOut, status_code=201)
async def create_user(
        *,
        user_in: BaseUserCreate,
        # current_user: User = Depends(get_current_active_superuser),
):
    if await User.get_by_username(username=user_in.username):
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.", )

    db_user = BaseUserCreate(**user_in.create_update_dict())
    created_user = await User.create(db_user)
    return created_user


@router.get('/me', response_model=BaseUserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.put("/me", response_model=BaseUserOut)
async def update_user_me(
        user_in: BaseUserUpdate,
        user: User = Depends(get_current_active_user)
):
    if user_in.password is not None:
        user.password_hash = get_password_hash(user_in.password)
    await user.update_from_dict(user_in.dict(exclude={'password'}, exclude_unset=True))
    await user.save()
    return user


@router.get("/", response_model=List[BaseUserOut], dependencies=[Depends(get_current_active_superuser)])
async def read_users(
        skip: int = 0,
        limit: int = 100
):
    return await User.all().limit(limit).offset(skip)
