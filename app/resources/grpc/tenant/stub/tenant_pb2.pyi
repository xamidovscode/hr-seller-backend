from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetTenantsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTenantsByIdsRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ids: _Optional[_Iterable[int]] = ...) -> None: ...

class GetTenantByIdRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetTenantsBalanceStatusRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ids: _Optional[_Iterable[int]] = ...) -> None: ...

class MonthlyTransResponse(_message.Message):
    __slots__ = ("id", "month", "debt_amount", "paid_amount", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DEBT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PAID_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    month: str
    debt_amount: float
    paid_amount: float
    status: str
    def __init__(self, id: _Optional[int] = ..., month: _Optional[str] = ..., debt_amount: _Optional[float] = ..., paid_amount: _Optional[float] = ..., status: _Optional[str] = ...) -> None: ...

class TenantResponse(_message.Message):
    __slots__ = ("id", "name", "schema_name", "created_on", "activated_at", "deadline", "on_trial", "is_active", "is_deleted", "empl_count", "active_plan_amount", "monthly_trans", "is_personal", "personal_amount")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    ACTIVATED_AT_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    ON_TRIAL_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    IS_DELETED_FIELD_NUMBER: _ClassVar[int]
    EMPL_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_TRANS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    schema_name: str
    created_on: str
    activated_at: str
    deadline: str
    on_trial: bool
    is_active: bool
    is_deleted: bool
    empl_count: int
    active_plan_amount: int
    monthly_trans: _containers.RepeatedCompositeFieldContainer[MonthlyTransResponse]
    is_personal: bool
    personal_amount: float
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., schema_name: _Optional[str] = ..., created_on: _Optional[str] = ..., activated_at: _Optional[str] = ..., deadline: _Optional[str] = ..., on_trial: bool = ..., is_active: bool = ..., is_deleted: bool = ..., empl_count: _Optional[int] = ..., active_plan_amount: _Optional[int] = ..., monthly_trans: _Optional[_Iterable[_Union[MonthlyTransResponse, _Mapping]]] = ..., is_personal: bool = ..., personal_amount: _Optional[float] = ...) -> None: ...

class GetTenantsResponse(_message.Message):
    __slots__ = ("tenants",)
    TENANTS_FIELD_NUMBER: _ClassVar[int]
    tenants: _containers.RepeatedCompositeFieldContainer[TenantResponse]
    def __init__(self, tenants: _Optional[_Iterable[_Union[TenantResponse, _Mapping]]] = ...) -> None: ...

class TenantsBalanceStatusResponse(_message.Message):
    __slots__ = ("must_paid_amount", "not_paid_amount", "paid_amount")
    MUST_PAID_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    NOT_PAID_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PAID_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    must_paid_amount: float
    not_paid_amount: float
    paid_amount: float
    def __init__(self, must_paid_amount: _Optional[float] = ..., not_paid_amount: _Optional[float] = ..., paid_amount: _Optional[float] = ...) -> None: ...
