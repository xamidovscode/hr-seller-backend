from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

from app.models.choices import RequestConditions
from .schemas import SellerRequestCreateSchema, SellerRequestUpdateSchema, SellerRequestFilterSchema
from .services import seller_request_service

router = APIRouter(prefix="/requests", tags=["Admin | Seller Requests"])


@router.get('/list/')
async def list_requests(
    service: seller_request_service,
    seller_id: Optional[int] = Query(default=None),
    condition: Optional[RequestConditions] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
):
    filters = SellerRequestFilterSchema(
        seller_id=seller_id,
        condition=condition,
        date_from=date_from,
        date_to=date_to,
    )
    return await service.list(filters=filters)


@router.get('/{pk}/')
async def get_request(pk: int, service: seller_request_service):
    return await service.detail(pk=pk)


@router.post('/create/')
async def create_request(schema: SellerRequestCreateSchema, service: seller_request_service):
    return await service.create(schema=schema)


@router.patch('/{pk}/')
async def update_request(pk: int, schema: SellerRequestUpdateSchema, service: seller_request_service):
    return await service.patch(pk=pk, schema=schema)


@router.delete('/{pk}/')
async def delete_request(pk: int, service: seller_request_service):
    return await service.delete(pk=pk)
