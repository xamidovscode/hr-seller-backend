from sqladmin import ModelView
from app.models import User, Supervisor, SellerRequest, SellerTransactions, MonthlyTransaction, Tenant


class UserAdmin(ModelView, model=User):
    icon = "fa-solid fa-user"
    name = "Foydalanuvchi"
    name_plural = "Foydalanuvchilar"
    column_list = [
        User.id, User.full_name, User.username,
        User.role, User.is_active, User.percentage, User.duration
    ]
    column_searchable_list = [User.username, User.full_name, User.phone]
    column_sortable_list = [User.id, User.full_name, User.role, User.is_active]
    form_excluded_columns = [User.password]


class SupervisorAdmin(ModelView, model=Supervisor):
    icon = "fa-solid fa-user-tie"
    name = "Supervisor"
    name_plural = "Supervisorlar"
    column_list = [
        Supervisor.id, Supervisor.supervisor_id, Supervisor.seller_id,
        Supervisor.from_date, Supervisor.to_date, Supervisor.percentage
    ]
    column_sortable_list = [Supervisor.id, Supervisor.from_date, Supervisor.to_date]


class SellerRequestAdmin(ModelView, model=SellerRequest):
    icon = "fa-solid fa-file-invoice"
    name = "Seller So'rovi"
    name_plural = "Seller So'rovlari"
    column_list = [
        SellerRequest.id, SellerRequest.amount,
        SellerRequest.date, SellerRequest.condition,
        SellerRequest.seller_transaction_id,
    ]
    column_sortable_list = [SellerRequest.id, SellerRequest.date, SellerRequest.amount]


class SellerTransactionsAdmin(ModelView, model=SellerTransactions):
    icon = "fa-solid fa-money-bill-transfer"
    name = "Seller Tranzaksiya"
    name_plural = "Seller Tranzaksiyalari"
    column_list = [
        SellerTransactions.id, SellerTransactions.seller_id,
        SellerTransactions.amount, SellerTransactions.model,
        SellerTransactions.instance_id, SellerTransactions.type,
    ]
    column_sortable_list = [SellerTransactions.id, SellerTransactions.amount]


class MonthlyTransactionAdmin(ModelView, model=MonthlyTransaction):
    icon = "fa-solid fa-calendar-days"
    name = "Oylik Tranzaksiya"
    name_plural = "Oylik Tranzaksiyalar"
    column_list = [
        MonthlyTransaction.id, MonthlyTransaction.tenant_id,
        MonthlyTransaction.service_id, MonthlyTransaction.month,
        MonthlyTransaction.amount, MonthlyTransaction.seller_trans_id,
    ]
    column_sortable_list = [MonthlyTransaction.id, MonthlyTransaction.month, MonthlyTransaction.amount]


class TenantAdmin(ModelView, model=Tenant):
    icon = "fa-solid fa-building"
    name = "Tenant"
    name_plural = "Tenantlar"
    column_list = [
        Tenant.id, Tenant.tenant_id, Tenant.type,
        Tenant.from_date, Tenant.to_date,
        Tenant.percentage, Tenant.seller_id,
    ]
    column_sortable_list = [Tenant.id, Tenant.from_date, Tenant.to_date]


all_views = [
    UserAdmin,
    SupervisorAdmin,
    SellerRequestAdmin,
    SellerTransactionsAdmin,
    MonthlyTransactionAdmin,
    TenantAdmin,
]