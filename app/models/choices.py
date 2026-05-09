from enum import Enum, IntEnum

class UserRoles(str, Enum):
    admin = 'admin'
    seller = 'seller'
    super_admin = 'super_admin'

class TenantTypes(str, Enum):
    IMB_EDU = 'imb_edu'
    IMB_HR = 'imb_hr'

class TransTypes(IntEnum):
    INCOME = 1
    EXPENSE = -1

class RequestConditions(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'

