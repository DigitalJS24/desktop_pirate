"""
Minion sprite generator.
Generates pixel-art animation frames for cute yellow Minions who appear after pirate kisses!
"""

import os
from PIL import Image, ImageDraw

C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (20, 20, 25, 255)
C_WHITE       = (250, 250, 250, 255)
C_YELLOW      = (255, 220, 15, 255)      # Iconic Minion Yellow
C_YELLOW_SHAD = (225, 185, 10, 255)
C_OVERALLS    = (45, 95, 165, 255)       # Denim blue
C_OVERALLS_DK = (30, 65, 120, 255)
C_GOGGLES     = (185, 195, 205, 255)     # Silver metallic
C_GOGGLES_DK  = (130, 140, 150, 255)
C_STRAP       = (35, 35, 40, 255)        # Black strap
C_EYE_BROWN   = (125, 75, 40, 255)
C_GLOVE       = (30, 30, 35, 255)
C_BOOT        = (30, 30, 35, 255)
C_BANANA      = (255, 235, 30, 255)      # Yellow Banana!
C_BANANA_TIP  = (85, 140, 35, 255)       # Greenish stem

SIZE = 40


def create_blank():
    return Image.new("RGBA", (SIZE, SIZE), C_TRANSPARENT)


def draw_banana(d: ImageDraw.ImageDraw, bx, by, angle="up"):
    """Draws a cute curved yellow banana"""
    if angle == "up":
        d.line([(bx, by + 4), (bx + 2, by + 1), (bx + 2, by - 3), (bx + 1, by - 5)], fill=C_BANANA, width=2)
        d.point([(bx, by - 5)], fill=C_BANANA_TIP)
    elif angle == "forward":
        d.line([(bx, by), (bx + 3, by - 2), (bx + 6, by - 1), (bx + 8, by + 2)], fill=C_BANANA, width=2)
        d.point([(bx + 8, by + 3)], fill=C_BANANA_TIP)


def draw_minion_body(d: ImageDraw.ImageDraw, cx, cy, height=22, width=14):
    """Pill-shaped iconic yellow Minion body"""
    # Top dome
    d.pieslice([cx - width // 2, cy - height // 2, cx + width // 2, cy - height // 2 + 10], 180, 360, fill=C_YELLOW)
    # Middle cylinder
    d.rectangle([cx - width // 2, cy - height // 2 + 4, cx + width // 2, cy + height // 2 - 4], fill=C_YELLOW)
    # Bottom round
    d.pieslice([cx - width // 2, cy + height // 2 - 10, cx + width // 2, cy + height // 2], 0, 180, fill=C_YELLOW)

    # Hair sprouts on head!
    d.line([(cx - 2, cy - height // 2), (cx - 4, cy - height // 2 - 3)], fill=C_BLACK, width=1)
    d.line([(cx + 1, cy - height // 2), (cx + 3, cy - height // 2 - 3)], fill=C_BLACK, width=1)
    d.point([(cx, cy - height // 2 - 4)], fill=C_BLACK)


def draw_goggles_and_eyes(d: ImageDraw.ImageDraw, cx, gy, blink=False, one_eye=False):
    """Silver goggles with black strap and brown eyes"""
    # Black strap across head
    d.line([(cx - 8, gy), (cx + 8, gy)], fill=C_STRAP, width=3)

    if one_eye:
        # One large center eye
        d.ellipse([cx - 5, gy - 5, cx + 5, gy + 5], fill=C_GOGGLES, outline=C_GOGGLES_DK)
        if blink:
            d.line([(cx - 3, gy), (cx + 3, gy)], fill=C_BLACK, width=1)
        else:
            d.ellipse([cx - 3, gy - 3, cx + 3, gy + 3], fill=C_WHITE)
            d.ellipse([cx - 1, gy - 2, cx + 2, gy + 1], fill=C_EYE_BROWN)
            d.point([(cx, gy - 1)], fill=C_BLACK)
            d.point([(cx + 1, gy - 2)], fill=C_WHITE)  # Sparkle
    else:
        # Two eyes
        # Left eye goggle
        d.ellipse([cx - 6, gy - 4, cx - 1, gy + 4], fill=C_GOGGLES, outline=C_GOGGLES_DK)
        # Right eye goggle
        d.ellipse([cx, gy - 4, cx + 5, gy + 4], fill=C_GOGGLES, outline=C_GOGGLES_DK)

        if blink:
            d.line([(cx - 5, gy), (cx - 2, gy)], fill=C_BLACK, width=1)
            d.line([(cx + 1, gy), (cx + 4, gy)], fill=C_BLACK, width=1)
        else:
            # Left eye
            d.ellipse([cx - 5, gy - 3, cx - 2, gy + 3], fill=C_WHITE)
            d.point([(cx - 3, gy)], fill=C_EYE_BROWN)
            d.point([(cx - 4, gy)], fill=C_BLACK)
            d.point([(cx - 3, gy - 1)], fill=C_WHITE)

            # Right eye
            d.ellipse([cx + 1, gy - 3, cx + 4, gy + 3], fill=C_WHITE)
            d.point([(cx + 2, gy)], fill=C_EYE_BROWN)
            d.point([(cx + 3, gy)], fill=C_BLACK)
            d.point([(cx + 2, gy - 1)], fill=C_WHITE)


def draw_mouth(d: ImageDraw.ImageDraw, mx, my, mode="smile"):
    if mode == "smile":
        d.line([(mx - 3, my), (mx + 3, my)], fill=C_BLACK, width=1)
        d.point([(mx - 3, my - 1), (mx + 3, my - 1)], fill=C_BLACK)
    elif mode == "open":
        # Big open happy laughing mouth showing white teeth!
        d.rectangle([mx - 3, my - 1, mx + 3, my + 2], fill=C_BLACK)
        d.line([(mx - 2, my - 1), (mx + 2, my - 1)], fill=C_WHITE, width=1)  # Teeth
    elif mode == "banana":
        d.ellipse([mx - 2, my - 1, mx + 2, my + 3], fill=C_BLACK)


def draw_overalls(d: ImageDraw.ImageDraw, cx, oy):
    """Blue denim overalls with straps and front pocket"""
    # Overalls bib
    d.rectangle([cx - 5, oy, cx + 5, oy + 7], fill=C_OVERALLS)
    # Side pants
    d.rectangle([cx - 7, oy + 3, cx + 7, oy + 8], fill=C_OVERALLS)

    # Straps
    d.line([(cx - 6, oy - 2), (cx - 4, oy + 1)], fill=C_OVERALLS_DK, width=2)
    d.line([(cx + 6, oy - 2), (cx + 4, oy + 1)], fill=C_OVERALLS_DK, width=2)
    # Black buttons
    d.point([(cx - 4, oy + 1), (cx + 4, oy + 1)], fill=C_BLACK)

    # Pocket in center
    d.rectangle([cx - 2, oy + 3, cx + 2, oy + 6], fill=C_OVERALLS_DK)
    d.point([(cx, oy + 4)], fill=C_BLACK)  # Emblem


def draw_minion_legs(d: ImageDraw.ImageDraw, cx, cy, l_off=(0, 0), r_off=(0, 0)):
    # Left boot
    lx = cx - 3 + l_off[0]
    ly = cy + l_off[1]
    d.rectangle([lx - 1, ly, lx + 1, ly + 2], fill=C_OVERALLS)
    d.rectangle([lx - 2, ly + 2, lx + 1, ly + 4], fill=C_BOOT)

    # Right boot
    rx = cx + 3 + r_off[0]
    ry = cy + r_off[1]
    d.rectangle([rx - 1, ry, rx + 1, ry + 2], fill=C_OVERALLS)
    d.rectangle([rx - 1, ry + 2, rx + 2, ry + 4], fill=C_BOOT)


# =========================================================================
# ANIMATION SETS
# =========================================================================

def gen_minion_idle():
    frames = []
    bobs = [0, -1, 0, 1]
    for i, bob in enumerate(bobs):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 19 + bob

        draw_minion_legs(d, 20, 29)
        draw_minion_body(d, cx, cy)
        draw_overalls(d, cx, cy + 3)
        draw_goggles_and_eyes(d, cx, cy - 3, blink=(i == 2))
        draw_mouth(d, cx, cy + 3, mode="smile")

        # Hands & Banana
        d.rectangle([cx + 6, cy + 4, cx + 8, cy + 6], fill=C_GLOVE)
        draw_banana(d, cx + 7, cy + 3, angle="up")
        d.rectangle([cx - 8, cy + 4, cx - 6, cy + 6], fill=C_GLOVE)

        frames.append(im)
    return frames


def gen_minion_walk():
    frames = []
    steps = [
        (0, 2, 0, -2, -1),
        (-1, 1, -1, -1, 0),
        (-2, -2, 0, 2, -1),
        (0, -2, -1, 2, 0),
        (-1, -1, 0, 1, -1),
        (-2, 1, -1, -1, 0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(steps):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 19 + bob

        draw_minion_legs(d, 20, 29, (ldx, ldy), (rdx, rdy))
        draw_minion_body(d, cx, cy)
        draw_overalls(d, cx, cy + 3)
        draw_goggles_and_eyes(d, cx, cy - 3)
        draw_mouth(d, cx, cy + 3, mode="smile")

        # Swaying hands & Banana
        d.rectangle([cx + 6, cy + 4 + (1 if i % 2 == 0 else -1), cx + 8, cy + 6], fill=C_GLOVE)
        draw_banana(d, cx + 7, cy + 2, angle="forward")
        d.rectangle([cx - 8, cy + 4 - (1 if i % 2 == 0 else -1), cx - 6, cy + 6], fill=C_GLOVE)

        frames.append(im)
    return frames


def gen_minion_run():
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        bob = -2 if i % 2 == 0 else 1
        cx, cy = 21, 19 + bob

        draw_minion_legs(d, 20, 29, (3 if i % 2 == 0 else -3, -1), (-3 if i % 2 == 0 else 3, -1))
        draw_minion_body(d, cx, cy)
        draw_overalls(d, cx, cy + 3)
        draw_goggles_and_eyes(d, cx, cy - 3)
        draw_mouth(d, cx, cy + 3, mode="open")  # Shouting BANANA!

        # Hands flailing in air!
        d.rectangle([cx + 6, cy - 2, cx + 8, cy], fill=C_GLOVE)
        draw_banana(d, cx + 7, cy - 4, angle="up")
        d.rectangle([cx - 8, cy - 2, cx - 6, cy], fill=C_GLOVE)

        frames.append(im)
    return frames


def gen_minion_jump():
    frames = []
    # Up
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    draw_minion_legs(d0, 20, 27, (-1, -2), (1, -2))
    draw_minion_body(d0, 20, 16)
    draw_overalls(d0, 20, 19)
    draw_goggles_and_eyes(d0, 20, 13)
    draw_mouth(d0, 20, 19, mode="open")
    d0.rectangle([26, 11, 28, 13], fill=C_GLOVE)
    draw_banana(d0, 27, 9, angle="up")
    d0.rectangle([12, 11, 14, 13], fill=C_GLOVE)
    frames.append(im0)

    # Peak
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    draw_minion_legs(d1, 20, 26, (-2, -3), (2, -3))
    draw_minion_body(d1, 20, 15)
    draw_overalls(d1, 20, 18)
    draw_goggles_and_eyes(d1, 20, 12)
    draw_mouth(d1, 20, 18, mode="open")
    d1.rectangle([26, 9, 28, 11], fill=C_GLOVE)
    draw_banana(d1, 27, 7, angle="up")
    d1.rectangle([12, 9, 14, 11], fill=C_GLOVE)
    frames.append(im1)
    return frames


def gen_minion_fall():
    frames = []
    for i in range(2):
        im = create_blank()
        d = ImageDraw.Draw(im)
        draw_minion_legs(d, 20, 28, (-2, -1), (2, -1))
        draw_minion_body(d, 20, 18)
        draw_overalls(d, 20, 21)
        draw_goggles_and_eyes(d, 20, 15)
        draw_mouth(d, 20, 21, mode="banana")  # "O" mouth!
        d.rectangle([26, 17, 28, 19], fill=C_GLOVE)
        draw_banana(d, 27, 16, angle="up")
        d.rectangle([12, 17, 14, 19], fill=C_GLOVE)
        frames.append(im)
    return frames


def gen_minion_cheer():
    """Jumping up and shouting 'BANANA!' while waving it happily!"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        bob = -3 if i % 2 == 0 else 0
        cx, cy = 20, 18 + bob

        draw_minion_legs(d, 20, 29)
        draw_minion_body(d, cx, cy)
        draw_overalls(d, cx, cy + 3)
        draw_goggles_and_eyes(d, cx, cy - 3)
        draw_mouth(d, cx, cy + 3, mode="open")

        # Both hands raised triumphantly in the air!
        d.rectangle([cx + 6, cy - 4, cx + 8, cy - 2], fill=C_GLOVE)
        draw_banana(d, cx + 7, cy - 7, angle="up")
        d.rectangle([cx - 8, cy - 4, cx - 6, cy - 2], fill=C_GLOVE)

        frames.append(im)
    return frames


def gen_minion_dragged():
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 19

        # Dangling legs kicking
        draw_minion_legs(d, 20, 29, (-2 if i % 2 == 0 else 2, -2), (2 if i % 2 == 0 else -2, 1))
        draw_minion_body(d, cx, cy)
        draw_overalls(d, cx, cy + 3)
        draw_goggles_and_eyes(d, cx, cy - 3)
        draw_mouth(d, cx, cy + 3, mode="banana")

        # Hands flailing
        d.rectangle([cx + 6, cy + 2, cx + 8, cy + 4], fill=C_GLOVE)
        draw_banana(d, cx + 7, cy + 1, angle="up")
        d.rectangle([cx - 8, cy + 2, cx - 6, cy + 4], fill=C_GLOVE)

        frames.append(im)
    return frames


def gen_minion_sleep():
    frames = []
    for i in range(3):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 20, 23

        d.rectangle([cx - 6, cy + 6, cx + 6, cy + 8], fill=C_BOOT)
        draw_minion_body(d, cx, cy)
        draw_overalls(d, cx, cy + 2)
        draw_goggles_and_eyes(d, cx, cy - 3, blink=True)
        draw_mouth(d, cx, cy + 3, mode="smile")

        # Banana sleeping under arm
        draw_banana(d, cx - 6, cy + 3, angle="forward")

        d.text((cx + 7, cy - 14 - i * 2), "z", fill=C_YELLOW)
        frames.append(im)
    return frames


def generate_all_minion_sprites(output_dir="assets/sprites/minion"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "idle": gen_minion_idle(),
        "walk": gen_minion_walk(),
        "run": gen_minion_run(),
        "jump": gen_minion_jump(),
        "fall": gen_minion_fall(),
        "cheer": gen_minion_cheer(),
        "dragged": gen_minion_dragged(),
        "sleep": gen_minion_sleep(),
    }

    for name, frames in animations.items():
        for idx, fr in enumerate(frames):
            p_r = os.path.join(output_dir, f"{name}_right_{idx}.png")
            fr.save(p_r)

            fr_l = fr.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{name}_left_{idx}.png")
            fr_l.save(p_l)

    print(f"Minion sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_minion_sprites()

