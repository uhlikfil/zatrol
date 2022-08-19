from sqlalchemy import func, insert, select

from zatrol.database.dao import BaseDAO
from zatrol.database.schema import Game


class GameDAO(BaseDAO):
    async def create(self, puuid: str, img_data: bytes, champion: str) -> None:
        vals = {
            Game.puuid: puuid,
            Game.img_data: img_data,
            Game.champion: champion,
        }
        stmt = insert(Game).values(vals)
        await self.connection.execute(stmt)

    async def get_random(self, puuid: str) -> Game:
        stmt = select(Game).where(Game.puuid == puuid)
        stmt = stmt.order_by(func.random()).limit(1)
        result = await self.connection.execute(stmt)
        return result.one_or_none()
