from fastapi import APIRouter
from .users.routes import router as users_router
from .auth.routes import router as auth_router


router = APIRouter()

router.include_router(users_router, prefix='/users', tags=['users'])
router.include_router(auth_router, prefix='/auth', tags=['auth'])