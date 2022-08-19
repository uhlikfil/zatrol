from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from zatrol.database.dao.quote import QuoteDAO
from zatrol.database.schema import Quote
from zatrol.exceptions import NotFound
from zatrol.services import champion as champion_svc


class QuoteSvc:
    def __init__(self, dao: QuoteDAO = Depends()) -> None:
        self.dao = dao

    async def get_all(self, puuid: str) -> list[Quote]:
        quotes = await self.dao.get_all(puuid)
        if not quotes:
            raise NotFound(f"No quotes found for the summoner {puuid}")
        return quotes

    async def insert_quote(
        self, puuid: str, text: str, champ_restrictions: list[str]
    ) -> None:
        champions = champion_svc.validate_champions(champ_restrictions)
        try:
            await self.dao.create(puuid, text, champions)
        except IntegrityError as error:
            print(error)
            raise NotFound(f"Summoner {puuid} not found")
