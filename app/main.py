from fastapi import FastAPI
from app.api.base_route import base_v1_router


app = FastAPI(
    title='HR SELLER APP',
    description='Seller app for IMB HR',
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.include_router(base_v1_router, prefix="/api/v1")


@app.get("/health")
async def root():
    return {"message": "Hello World"}

