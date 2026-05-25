from app.core.settings import settings
from app.resources.grpc.tenant_plans.stub import tenant_plans_pb2 as pb2, tenant_plans_pb2_grpc as pb2_grpc
from app.resources.services.base.grpc_base import GrpcClient


class TenantPlansGrpcClient(GrpcClient):

    @property
    def host(self) -> str:
        return settings.HR_CORE_GRPC_HOST

    def _create_stub(self, channel):
        return pb2_grpc.TenantPlanServiceStub(channel)

    async def get_tenant_active_plan(self, tenant_id: int) -> list[dict]:
        stub = await self._get_stub()
        response = await stub.GetTenantActivePlan(pb2.GetTenantActivePlanRequest(tenant_id=tenant_id))
        return [self._message_to_dict(tp) for tp in response.active_plans]

    async def get_tenant_my_data(self, tenant_id: int) -> dict:
        stub = await self._get_stub()
        response = await stub.GetTenantMyData(pb2.GetTenantMyDataRequest(tenant_id=tenant_id))
        return self._message_to_dict(response)

    async def get_tenant_transactions(self, tenant_id: int) -> list[dict]:
        stub = await self._get_stub()
        response = await stub.GetTenantTransactions(pb2.GetTenantTransactionsRequest(tenant_id=tenant_id))
        return [self._message_to_dict(t) for t in response.transactions]

    async def get_tenant_transactions_detail(self, tenant_id: int, date: str = '') -> list[dict]:
        stub = await self._get_stub()
        response = await stub.GetTenantTransactionsDetail(
            pb2.GetTenantTransactionsDetailRequest(tenant_id=tenant_id, date=date)
        )
        return [self._message_to_dict(d) for d in response.details]

    async def get_tenant_paid_amount_sum(
        self, tenant_id: int, from_date: str, to_date: str
    ) -> float:
        stub = await self._get_stub()
        response = await stub.GetTenantPaidAmountSum(
            pb2.TenantPaidSumRequest(
                tenant_id=tenant_id,
                from_date=from_date,
                to_date=to_date,
            )
        )
        return response.paid_amount_sum