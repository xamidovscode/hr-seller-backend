from sqlalchemy.ext.asyncio import AsyncSession


class SellerBalanceDetail:
    """
    Seller ning balansi detail ko'rinishda hamma datalar bilan birgalikda

    -------- Faqat bitta seller uchun --------
    """

    def __init__(self, db: AsyncSession, seller_id: int):
        self.db = db

    async def seller_tenants(self):
        pass

    async def supervised_sellers(self):
        pass

    async def seller_requests(self):
        pass

    async def detail_balance(self):
        pass

