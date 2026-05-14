from typing import Any

from sqlalchemy import select, func, and_

from app.models.choices import TransTypes
from app.resources.services import BaseService
from app.models import users, transactions


class SupervisorService(BaseService):

    async def get_supervisors_by_seller_id(self, seller_id: int) -> Any:

        seller = await self.get_object_or_404(
            select(users.User).where(users.User.id == seller_id)
        )

        assistants = await self.execute(
            select(
                users.Supervisor,
                func.coalesce(func.sum(transactions.SellerTransactions.amount), 0).label('income'),
            )
            .outerjoin(
                transactions.SellerTransactions,
                and_(
                    transactions.SellerTransactions.seller_id == users.Supervisor.seller_id,
                    transactions.SellerTransactions.month >= users.Supervisor.from_date,
                    transactions.SellerTransactions.month <= users.Supervisor.to_date,
                    transactions.SellerTransactions.type == TransTypes.INCOME
                )
            )
            .where(users.Supervisor.supervisor_id == seller_id)
            .group_by(users.Supervisor.id)
        )

        assistants_data = [
            {
                'id': row.Supervisor.id,
                'seller_id': row.Supervisor.seller_id,
                'from_date': row.Supervisor.from_date,
                'to_date': row.Supervisor.to_date,
                'percentage': row.Supervisor.percentage,
                'amount_portion': row.income * (row.Supervisor.percentage / 100),
            }
            for row in assistants.mappings().all()
        ]

        return {
            'id': seller.id,
            'username': seller.username,
            'full_name': seller.full_name,
            'password': seller.password,
            'phone': seller.phone,
            'role': seller.role,
            'is_active': seller.is_active,
            'percentage': seller.percentage,
            'duration': seller.duration,
            'assistants': assistants_data,
        }

supers_service = SupervisorService.annotated('db')
