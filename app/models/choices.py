from enum import Enum, IntEnum

class UserRoles(str, Enum):
    admin = 'admin'
    seller = 'seller'
    super_admin = 'super_admin'

class TenantTypes(str, Enum):
    IMB_EDU = 'IMB_EDU'
    IMB_HR = 'IMB_HR'

class TransTypes(IntEnum):
    INCOME = 1
    EXPENSE = -1

class RequestConditions(str, Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'

