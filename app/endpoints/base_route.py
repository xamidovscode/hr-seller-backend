from fastapi import APIRouter, Depends

from app.endpoints.auth.routers import router as auth_router
from app.endpoints.admin.users.routers import router as users_router
from app.endpoints.admin.plans.routers import router as plans_router
from app.endpoints.admin.salaries.routers import router as salaries_router
from app.endpoints.admin.requests.routers import router as requests_router
from app.endpoints.admin.tenants.routers import (
    tenants_router,
    tenant_detail_router,
    telegram_chat_router,
)
from app.endpoints.seller.routers import router as seller_router
from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles

_admin = [Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]
_seller = [Depends(require_roles(UserRoles.seller, ))]

admin_router = APIRouter(prefix="/admin", dependencies=_admin)
admin_router.include_router(users_router)
admin_router.include_router(tenants_router)
admin_router.include_router(tenant_detail_router)
admin_router.include_router(telegram_chat_router)
admin_router.include_router(plans_router)
admin_router.include_router(salaries_router)
admin_router.include_router(requests_router)

seller_api_router = APIRouter(prefix="/seller", dependencies=_seller)
seller_api_router.include_router(seller_router)

base_v1_router = APIRouter()
base_v1_router.include_router(auth_router)
base_v1_router.include_router(admin_router)
base_v1_router.include_router(seller_api_router)

