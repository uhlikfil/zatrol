from sqlalchemy import insert, select, update

from zatrol.database.dao import BaseDAO
from zatrol.database.schema import Summoner
from zatrol.model.region import Region


class SummonerDAO(BaseDAO):
    async def create(self, puuid: str, region: Region, summoner_name: str) -> None:
        vals = {
            Summoner.puuid: puuid,
            Summoner.region: region,
            Summoner.summoner_name: summoner_name,
        }
        stmt = insert(Summoner).values(vals)
        await self.connection.execute(stmt)

    async def get_all(self, limit: int = None, offset: int = None) -> list[Summoner]:
        stmt = select(Summoner).limit(limit).offset(offset)
        result = await self.connection.execute(stmt)
        return result.fetchall()

    async def get(self, puuid: str) -> Summoner:
        stmt = select(Summoner).where(Summoner.puuid == puuid)
        result = await self.connection.execute(stmt)
        return result.one_or_none()

    async def update(
        self,
        puuid: str,
        new_region: Region = None,
        new_name: str = None,
        last_match: str = None,
    ) -> None:
        vals = {}
        if new_region:
            vals[Summoner.region] = new_region
        if new_name:
            vals[Summoner.summoner_name] = new_name
        if last_match:
            vals[Summoner.last_match] = last_match
        stmt = update(Summoner).where(Summoner.puuid == puuid).values(vals)
        await self.connection.execute(stmt)
