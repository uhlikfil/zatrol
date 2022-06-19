import base64
import random
from pathlib import Path

from sa_decor import with_connection

from zatrol.config import Config
from zatrol.database import db_api
from zatrol.exception import NotFound
from zatrol.model.db_schema import Game, Quote
from zatrol.services.img_gen import final_img

BACKGROUNDS = None
QUOTE_FONTS = None


def init():
    global BACKGROUNDS, QUOTE_FONTS
    BACKGROUNDS = [str(path) for path in (Config.path.resources / "bg").glob("*.jpg")]
    QUOTE_FONTS = [
        str(path) for path in (Config.path.resources / "fonts" / "quote").glob("*.ttf")
    ]


@with_connection()
def generate(puuid: str, quote: Quote = None, game: Game = None, *, connection) -> str:
    summoner = db_api.select_summoner(connection, puuid)
    if not summoner:
        raise NotFound(f"Summoner '{puuid}' not registered")

    quote = db_api.select_random_quote(connection, puuid)
    if not quote:
        msg = f"No registered quotes found for the summoner '{summoner.summoner_name}'"
        raise NotFound(msg)
    game = db_api.select_random_game(connection, puuid, quote.champ_restrictions)

    if not game:
        msg = f"The summoner '{summoner.summoner_name}' has no interesting games for {quote.champ_restrictions}"
        raise NotFound(msg)

    img_data = final_img.generate(
        quote.text,
        game.img_data,
        random.choice(BACKGROUNDS),
        random.choice(QUOTE_FONTS),
        summoner.summoner_name,
        game.champion,
    )
    return base64.b64encode(img_data).decode()
