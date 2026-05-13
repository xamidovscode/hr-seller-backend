import grpc
from app.resources.grpc.tenant import tenant_pb2_grpc
from app.resources.grpc.tenant import tenant_pb2
from app.core.settings import settings


def get_tenants():
    channel = grpc.insecure_channel(settings.HR_CORE_GRPC_HOST)
    stub = tenant_pb2_grpc.TenantServiceStub(channel)
    response = stub.GetTenants(tenant_pb2.GetTenantsRequest())
    return response.tenants