from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.settings import settings
from app.endpoints.base_route import base_v1_router
from app.core.db import engine
from app.models.admin import all_views
from app.resources.permissions.admin_auth import AdminAuth

app = FastAPI(
    title='HR SELLER APP',
    description='Seller app for IMB HR',
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY))
for view in all_views:
    admin.add_view(view)

app.include_router(base_v1_router, prefix="/api/v1")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = {}

    for error in exc.errors():
        field = error["loc"][-1]
        errors[field] = error["msg"]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "errors": errors
        }
    )

@app.get("/health")
async def root():
    return {"message": "Hello World"}

