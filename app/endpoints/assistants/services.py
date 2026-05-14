from typing import Any

from sqlalchemy import select

from app.resources.services import BaseService
from app.models import users


class SupervisorService(BaseService):

    async def get_supervisors_by_seller_id(self, seller_id: int) -> Any:

        seller = await self.get_object_or_404(
            select(users.User).where(users.User.id == seller_id)
        )

        assistants = await self.get_all(
            select(users.Supervisor)
            .where(users.Supervisor.supervisor_id == seller.id)
        )

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
            'assistants': assistants,
        }

supers_service = SupervisorService.annotated('db')
