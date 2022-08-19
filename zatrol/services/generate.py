import io
import random
from typing import Union

from fastapi import Depends

from zatrol.database.dao.game import GameDAO
from zatrol.database.dao.quote import QuoteDAO
from zatrol.database.dao.summoner import SummonerDAO
from zatrol.exceptions import NotFound
from zatrol.services.img_gen import final_img
from zatrol.settings import Settings


class GenerateSvc:
    BACKGROUNDS = [str(path) for path in (Settings.path.RESOURCES / "bg").glob("*.jpg")]
    QUOTE_FONTS = [
        str(path)
        for path in (Settings.path.RESOURCES / "fonts" / "quote").glob("*.ttf")
    ]

    def __init__(
        self,
        game_dao: GameDAO = Depends(),
        quote_dao: QuoteDAO = Depends(),
        summoner_dao: SummonerDAO = Depends(),
    ) -> None:
        self.game_dao = game_dao
        self.quote_dao = quote_dao
        self.summoner_dao = summoner_dao

    async def generate(self, puuid: str, quote_id: int, game_id: int) -> io.BytesIO:
        summoner = await self.summoner_dao.get(puuid)
        if not summoner:
            raise NotFound(f"Summoner {puuid} not registered")

        quote = (
            await self.quote_dao.get_random(puuid)
            if quote_id is None
            else await self.quote_dao.get(quote_id)
        )
        if not quote:
            msg = (
                f"No registered quotes found for the summoner {summoner.summoner_name}"
                if quote_id is None
                else f"Quote with ID {quote_id} does not exist"
            )
            raise NotFound(msg)

        game = (
            await self.game_dao.get_random(puuid, quote.champ_restrictions)
            if game_id is None
            else await self.game_dao.get(game_id)
        )
        if not game:
            msg = (
                f"The summoner {summoner.summoner_name} has no interesting games for {quote.champ_restrictions}"
                if quote_id is None
                else f"Game with ID {game_id} does not exist"
            )
            raise NotFound(msg)

        return final_img.generate(
            quote.text,
            game.img_data,
            summoner.summoner_name,
            game.champion,
            bg_path=random.choice(self.BACKGROUNDS),
            font_path=random.choice(self.QUOTE_FONTS),
        )
