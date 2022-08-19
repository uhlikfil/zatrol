from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from zatrol.database.dao import BaseDAO
from zatrol.database.schema import Quote


class QuoteDAO(BaseDAO):
    async def create(self, puuid: str, text: str, champs: list[str] = []) -> None:
        vals = {Quote.puuid: puuid, Quote.text: text, Quote.champ_restrictions: champs}
        stmt = insert(Quote).values(vals).on_conflict_do_nothing()
        await self.connection.execute(stmt)

    async def get_all(
        self, puuid: str, limit: int = None, offset: int = None
    ) -> list[Quote]:
        stmt = select(Quote).where(Quote.puuid == puuid).limit(limit).offset(offset)
        result = await self.connection.execute(stmt)
        return result.fetchall()

    async def get(self, quote_id: int) -> Quote:
        stmt = select(Quote).where(Quote.id == quote_id)
        result = await self.connection.execute(stmt)
        return result.one_or_none()

    async def get_random(self, puuid: str) -> Quote:
        stmt = select(Quote).where(Quote.puuid == puuid)
        stmt = stmt.order_by(func.random()).limit(1)
        result = await self.connection.execute(stmt)
        return result.one_or_none()
