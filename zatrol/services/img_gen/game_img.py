import io

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from zatrol.services import riot_client
from zatrol.settings import Settings


def create_img(
    champion_key: int,
    kills: int,
    deaths: int,
    assists: int,
    won: bool,
) -> bytes:
    champ_icon = Image.open(io.BytesIO(riot_client.get_champion_icon(champion_key)))
    bg_w, bg_h, border_size = _bg_size(champ_icon)
    bg_img = Image.new("RGB", (bg_w, bg_h), color="#272a30")
    bg_img.paste(champ_icon, (border_size, border_size))
    draw = ImageDraw.Draw(bg_img)
    # outcome (Defeat / Victory) text
    out_font = _font("RobotoCondensed-Bold.ttf", champ_icon.height // 3)
    out_text = "Victory" if won else "Defeat"
    out_pos = bg_w - border_size - out_font.getsize(out_text)[0], border_size
    out_col = "#30d9d3" if won else "#ff574e"
    draw.text(out_pos, out_text, out_col, out_font)
    # KDA text
    kda_font = _font("RobotoCondensed-Bold.ttf", champ_icon.height // 4)
    kda_text = f"{(kills + assists) / deaths:.2f} KDA"
    kda_pos = (2 * border_size + champ_icon.width, bg_h // 2)
    kda_col = "#828790"
    draw.text(kda_pos, kda_text, kda_col, kda_font)
    # score text
    score_font = _font("RobotoCondensed-Regular.ttf", champ_icon.height // 5)
    score_text = f"{kills} / {deaths} / {assists}"
    score_pos = kda_pos[0], bg_h - border_size - score_font.getsize(score_text)[1]
    draw.text(score_pos, score_text, kda_col, score_font)
    # save image
    byte_arr = io.BytesIO()
    bg_img.save(byte_arr, format="PNG")
    return byte_arr.getvalue()


def _bg_size(img: Image) -> tuple[int, int, int]:
    w, h = img.size
    bg_h = int(h * 1.5)
    border_size = (bg_h - h) // 2
    bg_w = int(w * 2.25 + 2 * border_size)
    return bg_w, bg_h, border_size


def _font(font_name: str, wanted_height: int) -> FreeTypeFont:
    font_path = str(Settings.path.RESOURCES / "fonts" / font_name)

    for i in range(1, 256):
        font = ImageFont.truetype(font_path, i)
        height = font.getsize("Test string 123/45")[1]
        if height == wanted_height:
            return font
    return font  # wanted size not found, return the largest possible
