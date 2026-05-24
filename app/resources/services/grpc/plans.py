from app.core.settings import settings
from app.resources.grpc.plans.stubs import plans_pb2, plans_pb2_grpc
from app.resources.services.base.grpc_base import GrpcClient


class PlansGrpcClient(GrpcClient):

    @property
    def host(self) -> str:
        return settings.HR_CORE_GRPC_HOST

    def _create_stub(self, channel):
        return plans_pb2_grpc.PlansServiceStub(channel)

    async def list_plans(self):
        stub = await self._get_stub()
        response = await stub.GetPlansList(plans_pb2.GetPlansRequest())
        return [self._message_to_dict(t) for t in response.plans]
