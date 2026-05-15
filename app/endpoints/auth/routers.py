from fastapi import APIRouter

from . import schemas
from .services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/")
async def login(schema: schemas.LoginSchema, auth_service: AuthService.annotated('db')):
    return await auth_service.login(schema)


@router.get("/profile/")
async def get_profile(auth_service: AuthService.annotated('db', 'user')):
    return await auth_service.get_profile()