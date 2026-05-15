from google.protobuf.json_format import MessageToDict

from app.resources.grpc.tenant import tenant_pb2_grpc, tenant_pb2
from app.core.settings import settings
from app.resources.services.base.grpc_base import GrpcService


def _tenant_to_dict(tenant) -> dict:
    return MessageToDict(tenant, preserving_proto_field_name=True)


class TenantGrpcService(GrpcService):

    @property
    def host(self) -> str:
        return settings.HR_CORE_GRPC_HOST

    def _create_stub(self, channel):
        return tenant_pb2_grpc.TenantServiceStub(channel)

    async def get_grpc_tenants(self):
        stub = await self.get_stub()
        response = await stub.GetTenants(tenant_pb2.GetTenantsRequest())
        return [_tenant_to_dict(t) for t in response.tenants]

    async def get_grpc_tenants_by_ids(self, ids: list[int]):
        stub = await self.get_stub()
        response = await stub.GetTenantsByIds(tenant_pb2.GetTenantsByIdsRequest(ids=ids))
        return [_tenant_to_dict(t) for t in response.tenants]

    async def get_grpc_tenant_by_id(self, pk: int):
        stub = await self.get_stub()
        response = await stub.GetTenantById(tenant_pb2.GetTenantByIdRequest(id=pk))
        return _tenant_to_dict(response)


