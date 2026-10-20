"""
Pirate Girl (Piratess) sprite generator.
Generates all pixel-art animation frames for the pirate girl mascot with high detail,
flowing hair, pirate corset, boots, and kiss/romance animations.
"""

import os
from PIL import Image, ImageDraw

# Color Palette for Pirate Girl
C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (25, 20, 25, 255)
C_WHITE       = (250, 248, 245, 255)
C_SKIN        = (252, 208, 175, 255)
C_SKIN_SHADOW = (220, 168, 135, 255)
C_BLUSH       = (245, 120, 135, 255)
C_HAIR        = (150, 60, 25, 255)       # Rich auburn / chestnut
C_HAIR_LIGHT  = (195, 90, 45, 255)
C_HAT         = (40, 25, 35, 255)       # Dark maroon / velvet
C_HAT_GOLD    = (245, 200, 50, 255)
C_FEATHER     = (240, 240, 245, 255)     # White feathered plume
C_CORSET      = (185, 30, 45, 255)      # Ruby velvet corset
C_CORSET_LACE = (250, 215, 60, 255)
C_BLOUSE      = (245, 240, 235, 255)    # Ruffled poet blouse
C_PANTS       = (35, 45, 65, 255)       # Dark navy sailor pants
C_BOOT        = (50, 32, 28, 255)       # Leather boots
C_BOOT_TOP    = (80, 50, 40, 255)
C_STEEL       = (210, 220, 235, 255)
C_GOLD        = (255, 215, 0, 255)
C_HEART       = (255, 75, 120, 255)     # Romantic pink/red hearts
C_HEART_LIGHT = (255, 140, 175, 255)

FRAME_SIZE = 64


def create_blank():
    return Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE), C_TRANSPARENT)


def draw_heart(d: ImageDraw.ImageDraw, hx, hy, size=5):
    """Draw a cute pixel heart"""
    if size <= 5:
        d.polygon([
            (hx, hy + 2), (hx - 3, hy - 1), (hx - 2, hy - 3),
            (hx, hy - 1),
            (hx + 2, hy - 3), (hx + 3, hy - 1)
        ], fill=C_HEART)
        d.point([(hx - 1, hy - 2)], fill=C_HEART_LIGHT)
    else:
        d.polygon([
            (hx, hy + 4), (hx - 4, hy), (hx - 3, hy - 4),
            (hx, hy - 1),
            (hx + 3, hy - 4), (hx + 4, hy)
        ], fill=C_HEART)
        d.point([(hx - 2, hy - 2), (hx - 1, hy - 3)], fill=C_HEART_LIGHT)


def draw_girl_hat(d: ImageDraw.ImageDraw, hx, hy):
    """Stylish corsair captain tricorn with white feather plume & gold rose brooch"""
    # Hat brim
    d.polygon([
        (hx - 13, hy + 3),
        (hx - 16, hy - 2),
        (hx - 10, hy - 5),
        (hx, hy - 7),
        (hx + 10, hy - 5),
        (hx + 16, hy - 2),
        (hx + 13, hy + 3),
        (hx, hy + 1)
    ], fill=C_HAT)
    d.line([(hx - 15, hy - 2), (hx, hy - 7), (hx + 15, hy - 2)], fill=C_HAT_GOLD, width=1)

    # Elegant white feather flowing back
    d.line([(hx - 6, hy - 6), (hx - 12, hy - 12), (hx - 16, hy - 14)], fill=C_FEATHER, width=2)
    d.point([(hx - 17, hy - 15), (hx - 15, hy - 16)], fill=C_FEATHER)

    # Ruby/gold flower brooch
    d.point([(hx, hy - 2)], fill=C_CORSET)
    d.point([(hx - 1, hy - 2), (hx + 1, hy - 2)], fill=C_GOLD)


def draw_girl_head(d: ImageDraw.ImageDraw, hx, hy, blink=False, blush=False, mouth="smile", hair_blow=0):
    """Draw female pirate face: delicate features, blush, long auburn flowing hair"""
    # Long flowing hair in background
    d.polygon([
        (hx - 7, hy + 2),
        (hx - 9 + hair_blow, hy + 12),
        (hx - 6 + hair_blow, hy + 18),
        (hx - 3, hy + 12)
    ], fill=C_HAIR)
    d.polygon([
        (hx + 3, hy + 12),
        (hx + 6 - hair_blow, hy + 18),
        (hx + 9 - hair_blow, hy + 12),
        (hx + 7, hy + 2)
    ], fill=C_HAIR)

    # Face skin
    d.rectangle([hx - 5, hy, hx + 5, hy + 7], fill=C_SKIN)
    d.point([(hx - 5, hy), (hx + 5, hy), (hx - 5, hy + 7), (hx + 5, hy + 7)], fill=C_SKIN_SHADOW)
    # Tapered chin
    d.line([(hx - 2, hy + 8), (hx + 2, hy + 8)], fill=C_SKIN, width=1)

    # Nose
    d.point([(hx, hy + 4)], fill=C_SKIN_SHADOW)

    # Eyes: big, expressive pirate eyes with eyelashes
    if blink:
        d.line([(hx - 4, hy + 3), (hx - 2, hy + 3)], fill=C_BLACK, width=1)
        d.line([(hx + 2, hy + 3), (hx + 4, hy + 3)], fill=C_BLACK, width=1)
    else:
        # Left eye
        d.rectangle([hx - 4, hy + 2, hx - 2, hy + 4], fill=C_WHITE)
        d.point([(hx - 3, hy + 3)], fill=C_BLACK)
        d.point([(hx - 4, hy + 1)], fill=C_BLACK)  # Eyelash
        # Right eye
        d.rectangle([hx + 2, hy + 2, hx + 4, hy + 4], fill=C_WHITE)
        d.point([(hx + 3, hy + 3)], fill=C_BLACK)
        d.point([(hx + 4, hy + 1)], fill=C_BLACK)  # Eyelash

    # Rosy blush cheeks!
    if blush:
        d.rectangle([hx - 5, hy + 4, hx - 3, hy + 5], fill=C_BLUSH)
        d.rectangle([hx + 3, hy + 4, hx + 5, hy + 5], fill=C_BLUSH)
    else:
        d.point([(hx - 4, hy + 5)], fill=C_BLUSH)
        d.point([(hx + 4, hy + 5)], fill=C_BLUSH)

    # Gold hoop earring on side
    d.point([(hx - 6, hy + 4)], fill=C_GOLD)

    # Mouth
    if mouth == "smile":
        d.line([(hx - 1, hy + 6), (hx + 1, hy + 6)], fill=C_CORSET, width=1)
    elif mouth == "kiss":
        # Pouted kissy lips
        d.rectangle([hx - 1, hy + 5, hx + 1, hy + 6], fill=C_CORSET)
        d.point([(hx, hy + 6)], fill=C_BLUSH)
    elif mouth == "open":
        d.rectangle([hx - 1, hy + 6, hx + 1, hy + 7], fill=C_BLACK)

    # Front hair bangs / curls framing face
    d.line([(hx - 5, hy), (hx - 3, hy + 2)], fill=C_HAIR_LIGHT, width=1)
    d.line([(hx + 5, hy), (hx + 3, hy + 2)], fill=C_HAIR_LIGHT, width=1)


def draw_girl_torso(d: ImageDraw.ImageDraw, tx, ty, width=12, height=13):
    """White ruffled poet blouse under a fitted ruby corset with gold laces"""
    # White ruffled blouse shoulders
    d.rectangle([tx - width // 2, ty, tx + width // 2, ty + 4], fill=C_BLOUSE)

    # Ruby corset
    d.polygon([
        (tx - width // 2, ty + 3),
        (tx + width // 2, ty + 3),
        (tx + width // 2 - 1, ty + height),
        (tx - width // 2 + 1, ty + height)
    ], fill=C_CORSET)

    # Gold criss-cross laces in center
    d.line([(tx - 1, ty + 4), (tx + 1, ty + 6)], fill=C_CORSET_LACE, width=1)
    d.line([(tx + 1, ty + 4), (tx - 1, ty + 6)], fill=C_CORSET_LACE, width=1)
    d.line([(tx - 1, ty + 7), (tx + 1, ty + 9)], fill=C_CORSET_LACE, width=1)
    d.line([(tx + 1, ty + 7), (tx - 1, ty + 9)], fill=C_CORSET_LACE, width=1)

    # Golden sash & belt at waist
    d.line([(tx - width // 2 + 1, ty + height), (tx + width // 2 - 1, ty + height)], fill=C_GOLD, width=1)


def draw_girl_legs(d: ImageDraw.ImageDraw, cx, cy, l_off=(0, 0), r_off=(0, 0)):
    """Navy tight sailor trousers and tall folded leather pirate boots"""
    # Left leg
    lx = cx - 3 + l_off[0]
    ly = cy + l_off[1]
    d.rectangle([lx - 1, ly, lx + 1, ly + 5], fill=C_PANTS)
    d.rectangle([lx - 2, ly + 5, lx + 2, ly + 9], fill=C_BOOT)
    d.line([(lx - 2, ly + 5), (lx + 2, ly + 5)], fill=C_BOOT_TOP, width=1)

    # Right leg
    rx = cx + 3 + r_off[0]
    ry = cy + r_off[1]
    d.rectangle([rx - 1, ry, rx + 1, ry + 5], fill=C_PANTS)
    d.rectangle([rx - 2, ry + 5, rx + 2, ry + 9], fill=C_BOOT)
    d.line([(rx - 2, ry + 5), (rx + 2, ry + 5)], fill=C_BOOT_TOP, width=1)


# =========================================================================
# ANIMATION SETS
# =========================================================================

def gen_idle():
    frames = []
    bobs = [0, -1, 0, 1]
    for i, bob in enumerate(bobs):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28 + bob

        draw_girl_legs(d, 32, 44)
        draw_girl_torso(d, cx, cy + 4)
        # Slender rapier at side
        d.line([(cx + 6, cy + 8), (cx + 8, cy + 15)], fill=C_STEEL, width=1)
        d.point([(cx + 6, cy + 8)], fill=C_GOLD)

        draw_girl_head(d, cx, cy - 8, blink=(i == 2), blush=False, hair_blow=(1 if i % 2 == 0 else -1))
        draw_girl_hat(d, cx, cy - 10)
        frames.append(im)
    return frames


def gen_walk():
    frames = []
    walk_data = [
        (0, 3, 0, -3, -1),
        (-1, 1, -1, -1, 0),
        (-2, -2, 0, 2, -1),
        (0, -3, -1, 3, 0),
        (-1, -1, 0, 1, -1),
        (-2, 2, -1, -2, 0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(walk_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28 + bob

        draw_girl_legs(d, 32, 44, (ldx, ldy), (rdx, rdy))
        draw_girl_torso(d, cx, cy + 4)
        d.line([(cx + 6, cy + 8), (cx + 8, cy + 15)], fill=C_STEEL, width=1)

        draw_girl_head(d, cx, cy - 8, blink=False, hair_blow=(2 if i % 2 == 0 else -1))
        draw_girl_hat(d, cx, cy - 10)
        frames.append(im)
    return frames


def gen_run():
    """Playful sprint when running away from pirate!"""
    frames = []
    run_data = [
        (-2, 5, -2, -5, -3),
        (1, 2, 0, -2, -1),
        (-2, -5, -3, 5, -2),
        (1, -2, -1, 2, 0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(run_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 33, 28 + bob

        draw_girl_legs(d, 32, 44, (ldx, ldy), (rdx, rdy))
        draw_girl_torso(d, cx, cy + 4)
        # Hair flying behind in sprint
        draw_girl_head(d, cx, cy - 8, mouth="open", hair_blow=-5)
        draw_girl_hat(d, cx - 1, cy - 10)
        frames.append(im)
    return frames


def gen_jump():
    frames = []
    # Frame 0: leap
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    cx, cy = 32, 24
    draw_girl_legs(d0, 32, 44, (-2, -4), (2, -5))
    draw_girl_torso(d0, cx, cy + 4)
    draw_girl_head(d0, cx, cy - 8, mouth="smile", hair_blow=-3)
    draw_girl_hat(d0, cx, cy - 11)
    frames.append(im0)

    # Frame 1: peak
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    cx, cy = 32, 22
    draw_girl_legs(d1, 32, 44, (-3, -6), (3, -6))
    draw_girl_torso(d1, cx, cy + 4)
    draw_girl_head(d1, cx, cy - 8, mouth="smile", hair_blow=-4)
    draw_girl_hat(d1, cx, cy - 12)
    frames.append(im1)
    return frames


def gen_fall():
    frames = []
    for i in range(2):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 27
        draw_girl_legs(d, 32, 44, (-4, -2), (4, -2))
        draw_girl_torso(d, cx, cy + 4)
        draw_girl_head(d, cx, cy - 8, mouth="open", hair_blow=3)
        draw_girl_hat(d, cx, cy - 12)
        frames.append(im)
    return frames


def gen_land():
    frames = []
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    draw_girl_legs(d0, 32, 46, (-3, 1), (3, 1))
    draw_girl_torso(d0, 32, 34)
    draw_girl_head(d0, 32, 24, mouth="smile")
    draw_girl_hat(d0, 32, 22)
    frames.append(im0)

    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    draw_girl_legs(d1, 32, 44)
    draw_girl_torso(d1, 32, 32)
    draw_girl_head(d1, 32, 20, mouth="smile")
    draw_girl_hat(d1, 32, 18)
    frames.append(im1)
    return frames


def gen_kiss():
    """Kiss animation: leaning forward, lips pouted, blushing, hearts floating!"""
    frames = []
    kiss_data = [
        # (lean_x, mouth, blush, heart_y, heart_size)
        (2, "smile", True, None, 0),
        (4, "kiss",  True, -8, 4),
        (5, "kiss",  True, -14, 6),
        (3, "smile", True, -20, 5),
    ]
    for i, (lx, mouth, blush, hy, hsize) in enumerate(kiss_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32 + lx, 28

        draw_girl_legs(d, 32, 44, (0, 0), (lx, 0))
        draw_girl_torso(d, cx, cy + 4)

        # Floating romantic heart!
        if hy is not None:
            draw_heart(d, cx + 8, cy + hy, size=hsize)

        draw_girl_head(d, cx, cy - 8, blink=True, blush=blush, mouth=mouth, hair_blow=-2)
        draw_girl_hat(d, cx, cy - 10)
        frames.append(im)
    return frames


def gen_blush():
    """Giggling / blowing a kiss with heart floating up"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28

        draw_girl_legs(d, 32, 44)
        draw_girl_torso(d, cx, cy + 4)

        # Hand blowing kiss
        d.line([(cx + 4, cy + 8), (cx + 9, cy + 3)], fill=C_SKIN, width=2)
        draw_heart(d, cx + 12 + i * 2, cy - 2 - i * 3, size=4)

        draw_girl_head(d, cx, cy - 8, blink=(i % 2 == 1), blush=True, mouth="kiss" if i == 0 else "smile")
        draw_girl_hat(d, cx, cy - 10)
        frames.append(im)
    return frames


def gen_climb():
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28 + (1 if i % 2 == 0 else -1)

        draw_girl_legs(d, 32, 44, (-1, -2 if i % 2 == 0 else 2), (2, 2 if i % 2 == 0 else -2))
        draw_girl_torso(d, cx, cy + 4)
        # Arms climbing
        d.rectangle([cx + 5, cy + 1, cx + 9, cy + 3], fill=C_SKIN)

        draw_girl_head(d, cx, cy - 8, mouth="smile")
        draw_girl_hat(d, cx, cy - 10)
        frames.append(im)
    return frames


def gen_dragged():
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28

        draw_girl_legs(d, 32, 44, (-3 if i % 2 == 0 else 2, -2), (3 if i % 2 == 0 else -2, 1))
        draw_girl_torso(d, cx, cy + 4)
        draw_girl_head(d, cx, cy - 8, blink=False, blush=True, mouth="open", hair_blow=3)
        draw_girl_hat(d, cx, cy - 11)
        frames.append(im)
    return frames


def gen_sleep():
    frames = []
    for i in range(3):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 36

        # Sitting gracefully
        d.rectangle([cx - 6, cy + 8, cx + 6, cy + 12], fill=C_PANTS)
        d.rectangle([cx - 8, cy + 9, cx - 6, cy + 12], fill=C_BOOT)
        d.rectangle([cx + 6, cy + 9, cx + 8, cy + 12], fill=C_BOOT)

        draw_girl_torso(d, cx, cy)
        draw_girl_head(d, cx, cy - 8, blink=True, blush=True, mouth="smile")
        draw_girl_hat(d, cx, cy - 7)

        # Floating heart + Z
        d.text((cx + 10, cy - 14 - i * 2), "z", fill=C_HEART_LIGHT)
        if i >= 1:
            draw_heart(d, cx + 18, cy - 18 - i * 2, size=4)
        frames.append(im)
    return frames


def generate_all_piratess_sprites(output_dir="assets/sprites/piratess"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "idle": gen_idle(),
        "walk": gen_walk(),
        "run": gen_run(),
        "jump": gen_jump(),
        "fall": gen_fall(),
        "land": gen_land(),
        "kiss": gen_kiss(),
        "blush": gen_blush(),
        "climb_wall": gen_climb(),
        "dragged": gen_dragged(),
        "sleep": gen_sleep(),
    }

    for anim_name, frames in animations.items():
        for idx, frame in enumerate(frames):
            p_r = os.path.join(output_dir, f"{anim_name}_right_{idx}.png")
            frame.save(p_r)

            frame_l = frame.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{anim_name}_left_{idx}.png")
            frame_l.save(p_l)

    print(f"Piratess sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_piratess_sprites()

