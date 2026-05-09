from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.api.base_route import base_v1_router
from app.core.db import engine
from app.models.admin import all_views

app = FastAPI(
    title='HR SELLER APP',
    description='Seller app for IMB HR',
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

admin = Admin(app, engine)
for view in all_views:
    admin.add_view(view)

app.include_router(base_v1_router, prefix="/api/v1")


@app.get("/health")
async def root():
    return {"message": "Hello World"}

