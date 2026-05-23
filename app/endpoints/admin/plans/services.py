from app.resources.services import BaseService
from app.resources.services.grpc import PlansGrpcClient

_plans_grpc = PlansGrpcClient()


class PlansService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._plans_grpc = _plans_grpc

    async def plans_list(self):
        return await self._plans_grpc.list_plans()


plans_service = PlansService.annotated('db')