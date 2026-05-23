from app.core.settings import settings
from app.resources.services import BaseService
from app.resources.services.grpc import PlansGrpcClient
from .schemas import PlanBulkUpdateSchema

_plans_grpc = PlansGrpcClient()


class PlansService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._plans_grpc = _plans_grpc

    async def plans_list(self):
        return await self._plans_grpc.list_plans()

    async def update_plan(self, schema: PlanBulkUpdateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/plans/update/'
        data = schema.dict()
        await self.httpx_post(url=url, data=data)
        return {
            'success': True,
        }


plans_service = PlansService.annotated('db')