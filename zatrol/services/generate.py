import base64
import random
from pathlib import Path

from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.services.img_gen import final_img

BACKGROUNDS = None
QUOTE_FONTS = None


def init():
    global BACKGROUNDS, QUOTE_FONTS
    BACKGROUNDS = [
        str(path) for path in Path(Config.img_gen.assets_dir, "bg").glob("*.jpg")
    ]
    QUOTE_FONTS = [
        str(path)
        for path in Path(Config.img_gen.assets_dir, "fonts", "quote").glob("*.ttf")
    ]


def generate(puuid: str) -> str:
    with cm.session_mkr() as sess:
        player = db_api.select_player(sess, puuid)
        quote = db_api.select_random_quote(sess, puuid)
        if not (player and quote):
            raise FileNotFoundError(f"No quotes found for the player '{puuid}'")
        game = db_api.select_random_game(sess, puuid, quote.champ_restrictions)

    if not game:
        raise FileNotFoundError(f"The player '{player.summoner_name}' has no interesting games")  # fmt: skip

    img_data = final_img.generate(
        quote.text,
        game.img_data,
        random.choice(BACKGROUNDS),
        random.choice(QUOTE_FONTS),
        player.summoner_name,
        game.champion,
    )
    with open(f"last_generated.png", "wb+") as f:
        f.write(img_data)
    return base64.b64encode(img_data).decode()
