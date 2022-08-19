import base64
import random
from pathlib import Path

from zatrol.config import Config
from zatrol.database import connection as cm
from zatrol.database import db_api
from zatrol.services.img_gen import final_img

BACKGROUNDS = None
QUOTE_FONTS = None


def init():
    global BACKGROUNDS, QUOTE_FONTS
    BACKGROUNDS = [
        str(path) for path in Path(Config.services.assets_dir, "bg").glob("*.jpg")
    ]
    QUOTE_FONTS = [
        str(path)
        for path in Path(Config.services.assets_dir, "fonts", "quote").glob("*.ttf")
    ]


def generate(puuid: str) -> str:
    with cm.session_mkr() as sess:
        summoner = db_api.select_summoner(sess, puuid)
        if not summoner:
            raise FileNotFoundError(f"Summoner '{puuid}' not registered")
        quote = db_api.select_random_quote(sess, puuid)
        if not quote:
            raise FileNotFoundError(f"No registered quotes found for the summoner '{summoner.summoner_name}'")  # fmt: skip
        game = db_api.select_random_game(sess, puuid, quote.champ_restrictions)

    if not game:
        raise FileNotFoundError(f"The summoner '{summoner.summoner_name}' has no interesting games for {quote.champ_restrictions}")  # fmt: skip

    img_data = final_img.generate(
        quote.text,
        game.img_data,
        random.choice(BACKGROUNDS),
        random.choice(QUOTE_FONTS),
        summoner.summoner_name,
        game.champion,
    )
    return base64.b64encode(img_data).decode()
