import io
import random

from PIL import Image, ImageDraw, ImageFont

BORDER = 50
TEXT_CENTER_REPEAT = 20


def generate(text: str, score, background):
    bg_img = Image.open(background)
    draw = ImageDraw.Draw(bg_img)
    bg_w, bg_h = bg_img.size
    bg_h_half = bg_h // 2
    # text
    font = ImageFont.truetype("fonts/SaucerBB.ttf", 50)
    t_size = font.getsize(text)
    t_coords = _get_rand_pos(*t_size, bg_w, bg_h_half)
    while abs(t_coords[1] - bg_h_half // 2) < TEXT_CENTER_REPEAT:
        t_coords = _get_rand_pos(*t_size, bg_w, bg_h_half)  # too close to y center
    # lost LP
    lp_coords = _mirror(t_coords, t_size, (bg_w, bg_h_half))
    lp_loss = random.randint(12, 20)
    # score image
    score_img = Image.open(score).resize((bg_w // 2, bg_h_half // 2))
    img_x, img_y = _get_rand_pos(*score_img.size, bg_w, bg_h_half)
    img_y += bg_h_half
    # draw it
    draw.text(lp_coords, f"-{lp_loss} LP", fill=(255, 0, 0, 255), font=font)
    draw.text(t_coords, text, font=font)
    bg_img.paste(score_img, (img_x, img_y))
    return bg_img


def _get_rand_pos(obj_w: int, obj_h: int, bg_w: int, bg_h: int) -> tuple[int, int]:
    max_x = bg_w - BORDER - obj_w
    x = random.randint(BORDER, max_x)
    max_y = bg_h - BORDER - obj_h
    y = random.randint(BORDER, max_y)
    return x, y


def _mirror(
    coords: tuple[int, int], size: tuple[int, int], bg_size: tuple[int, int]
) -> tuple[int, int]:
    obj_c = _get_center(coords, size)
    bg_c = _get_center((0, 0), bg_size)
    return _mirror_coord(obj_c[0], bg_c[0]), _mirror_coord(obj_c[1], bg_c[1])


def _mirror_coord(pos: int, center: int) -> int:
    move = abs(pos - center) * 2
    if pos > center:
        return pos - move
    return pos + move


def _get_center(coords: tuple[int, int], size: tuple[int, int]) -> tuple[int, int]:
    return coords[0] + size[0] // 2, coords[1] + size[1] // 2


if __name__ == "__main__":
    with open("score/1.png", "rb") as score_f:
        score_data = score_f.read()
        img = generate("co s tim mam delat", io.BytesIO(score_data), "bg/summ_rift.jpg")
        img.save("test.png")
