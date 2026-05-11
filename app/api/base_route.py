from fastapi import APIRouter
from app.api import auth, sellers, tenants

base_v1_router = APIRouter()
base_v1_router.include_router(sellers.router, tags=["sellers"])
base_v1_router.include_router(auth.router, tags=["auth"])
base_v1_router.include_router(tenants.router, tags=["tenants"])
