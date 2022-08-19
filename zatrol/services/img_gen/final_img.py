import io
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

WRAP_CHAR_COUNT = 16
FONT_SIZE_LARGE = 50
FONT_SIZE_SMALL = 24

BORDER_EDGE = 16
BORDER = 64


def generate(
    text: str,
    game_img: bytes,
    summoner_name: str,
    champion: str,
    bg_path: str,
    font_path: str,
) -> io.BytesIO:
    bg_img = Image.open(bg_path)
    bg_halfbox = (bg_img.width, bg_img.height // 2)
    # text
    text = "\n".join(textwrap.wrap(text, WRAP_CHAR_COUNT))
    signature = f"-{summoner_name}\nas {champion}"
    text_font = ImageFont.truetype(font_path, FONT_SIZE_LARGE)
    sign_font = ImageFont.truetype(font_path, FONT_SIZE_SMALL)
    text_size = text_font.getsize_multiline(text)
    sign_size = sign_font.getsize_multiline(signature)
    text_pos = _get_rand_pos(text_size, bg_halfbox)
    sign_pos = (text_pos[0] + text_size[0] - sign_size[0], text_pos[1] + text_size[1])
    # score image
    score_img = Image.open(io.BytesIO(game_img))
    score_img_size = _resize_keep_aspect_ratio(score_img.size, int(bg_img.width / 1.5))
    score_img = score_img.resize(score_img_size)
    img_x, img_y = _get_rand_pos(score_img.size, bg_halfbox)
    img_y += bg_img.height // 2  # move to the bottom half
    # draw borders
    draw = ImageDraw.Draw(bg_img, "RGBA")
    draw.rectangle(
        (
            BORDER_EDGE,
            BORDER_EDGE,
            bg_img.width - BORDER_EDGE,
            bg_img.height - BORDER_EDGE,
        ),
        fill=(0, 0, 0, 0),
        outline=(0, 0, 0, 128),
        width=BORDER - 2 * BORDER_EDGE,
    )
    # draw objects
    draw.multiline_text(text_pos, text, font=text_font, align="left")
    draw.multiline_text(sign_pos, signature, font=sign_font, align="right")
    bg_img.paste(score_img, (img_x, img_y))
    # save image
    byte_arr = io.BytesIO()
    bg_img.save(byte_arr, format="PNG")
    byte_arr.seek(0)
    return byte_arr


def _get_rand_pos(
    obj_size: tuple[int, int], bg_size: tuple[int, int]
) -> tuple[int, int]:
    max_x = bg_size[0] - BORDER - obj_size[0]
    x = random.randint(BORDER, max_x)
    max_y = bg_size[1] - BORDER - obj_size[1]
    y = random.randint(BORDER, max_y)
    return x, y


def _resize_keep_aspect_ratio(
    orig_size: tuple[int, int], wanted_width: int
) -> tuple[int, int]:
    ratio = wanted_width / orig_size[0]
    return wanted_width, int(orig_size[1] * ratio)
