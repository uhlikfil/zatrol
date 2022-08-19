from sqlalchemy import func, insert, select

from zatrol.database.dao import BaseDAO
from zatrol.database.schema import Game


class GameDAO(BaseDAO):
    async def create(self, puuid: str, img_data: bytes, champion: str) -> int:
        vals = {
            Game.puuid: puuid,
            Game.img_data: img_data,
            Game.champion: champion,
        }
        stmt = insert(Game).values(vals)
        result = await self.connection.execute(stmt)
        return result.inserted_primary_key[0]

    async def get(self, game_id: int) -> Game:
        stmt = select(Game).where(Game.id == game_id)
        result = await self.connection.execute(stmt)
        return result.one_or_none()

    async def get_random(self, puuid: str, champions: list[str] = None) -> Game:
        stmt = select(Game).where(Game.puuid == puuid)
        if champions:
            stmt = stmt.where(Game.champion.in_(champions))
        stmt = stmt.order_by(func.random()).limit(1)
        result = await self.connection.execute(stmt)
        return result.one_or_none()
