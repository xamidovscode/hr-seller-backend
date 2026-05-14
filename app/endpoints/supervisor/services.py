from typing import Any

from sqlalchemy import select

from app.resources.services import BaseService
from app.models import users


class SupervisorService(BaseService):

    async def get_supervisors_by_seller_id(self, seller_id: int) -> Any:

        seller = self.get_object_or_404(
            select(users.User).where(users.User.id == seller_id)
        )

        assistants = self.get_all(
            select(users.Supervisor).where(users.Supervisor.supervisor == seller)
        )

        return {
            'success': True,
        }

supers_service = SupervisorService.annotated('db')
