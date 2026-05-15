from app.core.settings import settings
from app.resources.grpc.tenant_plans import plans_pb2, plans_pb2_grpc
from app.resources.services.base.grpc_base import GrpcClient


class PlansGrpcClient(GrpcClient):

    @property
    def host(self) -> str:
        return settings.HR_CORE_GRPC_HOST  # ertaga boshqa host bo'lsa — shu yerda o'zgartiring

    def _create_stub(self, channel):
        return plans_pb2_grpc.TenantPlanServiceStub(channel)

    async def get_tenant_active_plan(self, tenant_id: int) -> list[dict]:
        stub = await self._get_stub()
        response = await stub.GetTenantActivePlan(
            plans_pb2.GetTenantActivePlanRequest(tenant_id=tenant_id)
        )
        return [self._message_to_dict(tp) for tp in response.active_plans]