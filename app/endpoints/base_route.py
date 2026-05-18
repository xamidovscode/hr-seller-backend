from fastapi import APIRouter

from app.endpoints.auth.routers import router as auth_router
from app.endpoints.admin.users.routers import router as users_router
from app.endpoints.admin.tenants.routers import tenants_router, tenant_detail_router, monthly_trans_router
from app.endpoints.seller.routers import router as seller_router

admin_router = APIRouter(prefix="/admin")
admin_router.include_router(users_router)
admin_router.include_router(tenants_router)
admin_router.include_router(tenant_detail_router)
admin_router.include_router(monthly_trans_router)

seller_api_router = APIRouter(prefix="/seller")
seller_api_router.include_router(seller_router)

base_v1_router = APIRouter()
base_v1_router.include_router(auth_router)
base_v1_router.include_router(admin_router)
base_v1_router.include_router(seller_api_router)

