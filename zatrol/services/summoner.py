from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from zatrol.database.dao.summoner import SummonerDAO
from zatrol.database.schema import Summoner
from zatrol.exceptions import AlreadyExists, NotFound
from zatrol.model.region import Region
from zatrol.services import riot_client


class SummonerSvc:
    def __init__(self, dao: SummonerDAO = Depends()) -> None:
        self.dao = dao

    async def get_all(self) -> list[Summoner]:
        return await self.dao.get_all()

    async def insert_summoner(self, region: Region, summoner_name: str) -> str:
        puuid = self.summoner_name_to_puuid(region, summoner_name)
        try:
            return await self.dao.create(puuid, region, summoner_name)
        except IntegrityError:
            raise AlreadyExists(f"Summoner {summoner_name} #{region.value} has already been registered before")  # fmt: skip

    @staticmethod
    def summoner_name_to_puuid(region: Region, summoner_name: str) -> str:
        puuid = riot_client.get_puuid(region, summoner_name)
        if not puuid:
            raise NotFound(f"Summoner {summoner_name} not found in the {region.value} region")  # fmt: skip
        return puuid
