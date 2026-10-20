"""
Pirate Kid (Mini Pirate / Юнга) sprite generator.
Generates cute chibi-style pirate child animations for the children spawned after a kiss!
"""

import os
from PIL import Image, ImageDraw

C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (20, 20, 25, 255)
C_WHITE       = (250, 250, 250, 255)
C_SKIN        = (255, 215, 185, 255)
C_BLUSH       = (255, 130, 150, 255)
C_HAIR        = (110, 55, 25, 255)
C_BANDANA     = (225, 35, 45, 255)       # Bright red bandana
C_BANDANA_DOT = (255, 240, 240, 255)
C_SHIRT_BLU   = (45, 130, 210, 255)      # Blue & white stripes
C_SHIRT_WHT   = (245, 245, 245, 255)
C_PANTS       = (40, 50, 75, 255)
C_BOOT        = (75, 45, 30, 255)
C_WOOD_SWORD  = (180, 125, 65, 255)      # Wooden toy sword!
C_WOOD_HILT   = (120, 80, 40, 255)

SIZE = 40  # 40x40 chibi frame


def create_blank():
    return Image.new("RGBA", (SIZE, SIZE), C_TRANSPARENT)


def draw_kid_bandana(d: ImageDraw.ImageDraw, hx, hy):
    """Cute tied pirate bandana with knot and tail on the back"""
    # Bandana cap over head
    d.polygon([
        (hx - 8, hy - 1),
        (hx - 9, hy - 5),
        (hx - 5, hy - 9),
        (hx + 5, hy - 9),
        (hx + 9, hy - 5),
        (hx + 8, hy - 1),
        (hx, hy - 3)
    ], fill=C_BANDANA)
    # Bandana white polka dots
    d.point([(hx - 4, hy - 6), (hx + 2, hy - 7), (hx + 6, hy - 4), (hx - 2, hy - 4)], fill=C_BANDANA_DOT)

    # Tied knot & tails on left
    d.polygon([(hx - 9, hy - 2), (hx - 13, hy), (hx - 12, hy + 4), (hx - 8, hy)], fill=C_BANDANA)
    d.point([(hx - 10, hy - 1)], fill=C_BANDANA_DOT)


def draw_kid_head(d: ImageDraw.ImageDraw, hx, hy, blink=False, mouth="smile"):
    """Cute chubby toddler face with huge eyes and rosy cheeks"""
    # Round toddler face
    d.rectangle([hx - 6, hy - 2, hx + 6, hy + 5], fill=C_SKIN)
    d.line([(hx - 4, hy + 6), (hx + 4, hy + 6)], fill=C_SKIN, width=1)

    # Big round toddler eyes!
    if blink:
        d.line([(hx - 4, hy + 1), (hx - 1, hy + 1)], fill=C_BLACK, width=1)
        d.line([(hx + 1, hy + 1), (hx + 4, hy + 1)], fill=C_BLACK, width=1)
    else:
        # Left eye
        d.rectangle([hx - 4, hy, hx - 1, hy + 3], fill=C_WHITE)
        d.rectangle([hx - 3, hy + 1, hx - 1, hy + 3], fill=C_BLACK)
        d.point([(hx - 3, hy + 1)], fill=C_WHITE)  # Eye sparkle
        # Right eye
        d.rectangle([hx + 1, hy, hx + 4, hy + 3], fill=C_WHITE)
        d.rectangle([hx + 2, hy + 1, hx + 4, hy + 3], fill=C_BLACK)
        d.point([(hx + 2, hy + 1)], fill=C_WHITE)

    # Chubby rosy blush cheeks
    d.rectangle([hx - 6, hy + 3, hx - 4, hy + 4], fill=C_BLUSH)
    d.rectangle([hx + 4, hy + 3, hx + 6, hy + 4], fill=C_BLUSH)

    # Mouth
    if mouth == "smile":
        d.line([(hx - 1, hy + 4), (hx + 1, hy + 4)], fill=C_BLACK, width=1)
    elif mouth == "open":
        d.rectangle([hx - 1, hy + 4, hx + 1, hy + 5], fill=C_BLACK)


def draw_kid_torso(d: ImageDraw.ImageDraw, tx, ty):
    """Striped sailor shirt (blue & white)"""
    for i in range(7):
        col = C_SHIRT_BLU if (i // 2) % 2 == 0 else C_SHIRT_WHT
        d.line([(tx - 5, ty + i), (tx + 5, ty + i)], fill=col, width=1)


def draw_toy_sword(d: ImageDraw.ImageDraw, sx, sy, angle="down"):
    """Cute wooden toy pirate sword"""
    d.line([(sx - 2, sy), (sx + 2, sy)], fill=C_WOOD_HILT, width=1)
    if angle == "down":
        d.line([(sx, sy), (sx + 2, sy + 6)], fill=C_WOOD_SWORD, width=2)
    elif angle == "up":
        d.line([(sx, sy), (sx + 3, sy - 7)], fill=C_WOOD_SWORD, width=2)
    elif angle == "forward":
        d.line([(sx, sy), (sx + 7, sy - 1)], fill=C_WOOD_SWORD, width=2)


def draw_kid_legs(d: ImageDraw.ImageDraw, cx, cy, l_off=(0, 0), r_off=(0, 0)):
    """Cute little toddler legs & boots"""
    lx = cx - 3 + l_off[0]
    ly = cy + l_off[1]
    d.rectangle([lx - 1, ly, lx + 1, ly + 2], fill=C_PANTS)
    d.rectangle([lx - 2, ly + 3, lx + 1, ly + 5], fill=C_BOOT)

    rx = cx + 3 + r_off[0]
    ry = cy + r_off[1]
    d.rectangle([rx - 1, ry, rx + 1, ry + 2], fill=C_PANTS)
    d.rectangle([rx - 1, ry + 3, rx + 2, ry + 5], fill=C_BOOT)


def gen_kid_idle():
    frames = []
    bobs = [0, -1, 0, 1]
    for i, bob in enumerate(bobs):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 19 + bob

        draw_kid_legs(d, 20, 29)
        draw_kid_torso(d, cx, cy + 3)
        draw_toy_sword(d, cx + 5, cy + 6, angle="down")
        draw_kid_head(d, cx, cy - 4, blink=(i == 2))
        draw_kid_bandana(d, cx, cy - 6)
        frames.append(im)
    return frames


def gen_kid_walk():
    frames = []
    w_data = [
        (0, 2, 0, -2, -1, "down"),
        (-1, 1, -1, -1, 0, "down"),
        (-2, -2, 0, 2, -1, "forward"),
        (0, -2, -1, 2, 0, "down"),
        (-1, -1, 0, 1, -1, "down"),
        (-2, 1, -1, -1, 0, "forward"),
    ]
    for i, (bob, ldx, ldy, rdx, rdy, s_ang) in enumerate(w_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 19 + bob

        draw_kid_legs(d, 20, 29, (ldx, ldy), (rdx, rdy))
        draw_kid_torso(d, cx, cy + 3)
        draw_toy_sword(d, cx + 5, cy + 6, angle=s_ang)
        draw_kid_head(d, cx, cy - 4, blink=False)
        draw_kid_bandana(d, cx, cy - 6)
        frames.append(im)
    return frames


def gen_kid_run():
    frames = []
    r_data = [
        (-2, 3, -1, -3, -2),
        (1, 1, 0, -1, -1),
        (-2, -3, -2, 3, -1),
        (1, -1, -1, 1, 0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(r_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 21, 19 + bob

        draw_kid_legs(d, 20, 29, (ldx, ldy), (rdx, rdy))
        draw_kid_torso(d, cx, cy + 3)
        draw_toy_sword(d, cx + 6, cy + 4, angle="forward")
        draw_kid_head(d, cx, cy - 4, mouth="open")
        draw_kid_bandana(d, cx - 1, cy - 6)
        frames.append(im)
    return frames


def gen_kid_jump():
    frames = []
    # Up
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    draw_kid_legs(d0, 20, 28, (-1, -3), (1, -3))
    draw_kid_torso(d0, 20, 17)
    draw_toy_sword(d0, 26, 15, angle="up")
    draw_kid_head(d0, 20, 10, mouth="open")
    draw_kid_bandana(d0, 20, 8)
    frames.append(im0)

    # Peak
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    draw_kid_legs(d1, 20, 27, (-2, -4), (2, -4))
    draw_kid_torso(d1, 20, 16)
    draw_toy_sword(d1, 26, 13, angle="up")
    draw_kid_head(d1, 20, 9, mouth="smile")
    draw_kid_bandana(d1, 20, 7)
    frames.append(im1)
    return frames


def gen_kid_fall():
    frames = []
    for i in range(2):
        im = create_blank()
        d = ImageDraw.Draw(im)
        draw_kid_legs(d, 20, 28, (-2, -1), (2, -1))
        draw_kid_torso(d, 20, 19)
        draw_toy_sword(d, 25, 21, angle="down")
        draw_kid_head(d, 20, 11, mouth="open")
        draw_kid_bandana(d, 20, 8)
        frames.append(im)
    return frames


def gen_kid_cheer():
    """Jumping for joy with toy sword held high!"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 18 + (0 if i % 2 == 0 else -2)

        draw_kid_legs(d, 20, 29)
        draw_kid_torso(d, cx, cy + 3)
        draw_toy_sword(d, cx + 5, cy + 2, angle="up")
        draw_kid_head(d, cx, cy - 4, mouth="open")
        draw_kid_bandana(d, cx, cy - 6)
        frames.append(im)
    return frames


def gen_kid_dragged():
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 19
        draw_kid_legs(d, 20, 29, (-2 if i % 2 == 0 else 2, -2), (2 if i % 2 == 0 else -2, 1))
        draw_kid_torso(d, cx, cy + 3)
        draw_toy_sword(d, cx + 6, cy + 5, angle="forward" if i % 2 == 0 else "up")
        draw_kid_head(d, cx, cy - 4, mouth="open")
        draw_kid_bandana(d, cx, cy - 7)
        frames.append(im)
    return frames


def gen_kid_sleep():
    frames = []
    for i in range(3):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 24

        d.rectangle([cx - 5, cy + 5, cx + 5, cy + 8], fill=C_PANTS)
        d.rectangle([cx - 6, cy + 6, cx - 4, cy + 8], fill=C_BOOT)
        d.rectangle([cx + 4, cy + 6, cx + 6, cy + 8], fill=C_BOOT)

        draw_kid_torso(d, cx, cy)
        draw_toy_sword(d, cx - 6, cy + 7, angle="forward")
        draw_kid_head(d, cx, cy - 5, blink=True, mouth="smile")
        draw_kid_bandana(d, cx, cy - 7)

        d.text((cx + 7, cy - 12 - i * 2), "z", fill=C_WHITE)
        frames.append(im)
    return frames


def generate_all_kid_sprites(output_dir="assets/sprites/kid"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "idle": gen_kid_idle(),
        "walk": gen_kid_walk(),
        "run": gen_kid_run(),
        "jump": gen_kid_jump(),
        "fall": gen_kid_fall(),
        "cheer": gen_kid_cheer(),
        "dragged": gen_kid_dragged(),
        "sleep": gen_kid_sleep(),
    }

    for name, frames in animations.items():
        for idx, fr in enumerate(frames):
            p_r = os.path.join(output_dir, f"{name}_right_{idx}.png")
            fr.save(p_r)

            fr_l = fr.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{name}_left_{idx}.png")
            fr_l.save(p_l)

    print(f"Pirate kid sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_kid_sprites()

