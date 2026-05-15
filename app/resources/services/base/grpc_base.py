import grpc.aio
from abc import ABC, abstractmethod

from google.protobuf.json_format import MessageToDict


class GrpcService(ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._channel = None
        self._stub = None

    @property
    @abstractmethod
    def host(self) -> str: ...

    @abstractmethod
    def _create_stub(self, channel: grpc.aio.Channel): ...

    async def get_stub(self):
        if self._stub is None:
            self._channel = grpc.aio.insecure_channel(self.host)
            self._stub = self._create_stub(self._channel)
        return self._stub

    async def close(self):
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None

    @staticmethod
    def _message_to_dict(tenant) -> dict:
        return MessageToDict(tenant, preserving_proto_field_name=True)

