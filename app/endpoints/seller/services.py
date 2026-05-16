from app.resources.services import BaseService



class SellerService(BaseService):

    async def get_seller_tenants(self):
        return {
            'success': True,
        }