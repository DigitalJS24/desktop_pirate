"""
High-Definition Smooth Cartoon Sprite Generator for the Girl (Reference Photo).
Renders smooth anti-aliased 256x256 frames (via 512x512 Lanczos supersampling):
- Silky blonde straight hair parted in center, draping over shoulders
- Expressive face with detailed eyes, eyelashes, and cute expressions
- Heather gray cropped t-shirt exposing midriff and navel
- Red string bracelet on left wrist
- Fitted dark indigo skinny jeans with stonewash highlights & rolled cuffs
- Crisp white sneakers
"""

import os
import math
from PIL import Image, ImageDraw

OUTPUT_SIZE = 256
RENDER_SIZE = 512
SCALE = RENDER_SIZE / OUTPUT_SIZE  # 2.0

# HD Color Palette
C_TRANSPARENT    = (0, 0, 0, 0)
C_BLACK          = (24, 22, 28, 255)
C_WHITE          = (255, 255, 255, 255)

# Skin
C_SKIN           = (254, 228, 210, 255)
C_SKIN_SHADOW    = (234, 194, 170, 255)
C_SKIN_DEEP      = (214, 170, 144, 255)
C_BLUSH          = (255, 148, 160, 180)
C_LIP_PINK       = (232, 105, 120, 255)
C_LIP_DARK       = (185, 60, 78, 255)

# Hair (Blonde from photo)
C_HAIR_BASE      = (206, 174, 128, 255)
C_HAIR_LIGHT     = (242, 222, 184, 255)
C_HAIR_DARK      = (164, 130, 88, 255)
C_HAIR_ROOT      = (135, 102, 65, 255)

# Crop Top
C_TOP            = (218, 222, 228, 255)
C_TOP_LIGHT      = (242, 245, 248, 255)
C_TOP_SHADOW     = (176, 182, 192, 255)

# Jeans
C_JEANS          = (44, 76, 126, 255)
C_JEANS_LIGHT    = (70, 114, 174, 255)
C_JEANS_DARK     = (26, 48, 84, 255)
C_JEANS_CUFF     = (135, 168, 210, 255)
C_JEANS_BUTTON   = (212, 186, 118, 255)

# White Sneakers
C_SNEAKER        = (252, 252, 252, 255)
C_SNEAKER_SOLE   = (216, 220, 226, 255)
C_SNEAKER_DARK   = (180, 186, 194, 255)

# Accessories & Details
C_RED_BRACELET   = (230, 40, 48, 255)
C_NAVEL          = (220, 174, 148, 255)
C_EYE_HAZEL      = (108, 76, 50, 255)
C_HEART          = (255, 75, 120, 255)
C_HEART_LIGHT    = (255, 150, 185, 255)


def create_canvas():
    return Image.new("RGBA", (RENDER_SIZE, RENDER_SIZE), C_TRANSPARENT)


def draw_smooth_heart(d: ImageDraw.ImageDraw, hx, hy, size=16):
    """Draw smooth anti-aliased romantic heart"""
    s = size
    # Two top circles
    d.ellipse([hx - s, hy - s, hx, hy], fill=C_HEART)
    d.ellipse([hx, hy - s, hx + s, hy], fill=C_HEART)
    # Bottom triangle
    d.polygon([(hx - s, hy - s // 2), (hx + s, hy - s // 2), (hx, hy + s)], fill=C_HEART)
    # Highlight shine
    d.ellipse([hx - s // 2, hy - s * 0.7, hx - s // 4, hy - s * 0.3], fill=C_HEART_LIGHT)


def draw_girl(d: ImageDraw.ImageDraw, cx=256, cy=240,
              leg_l_off=(0, 0), leg_r_off=(0, 0),
              arm_pose="down", blink=False, blush=False,
              mouth="smile", hair_blow=0, lean_x=0):
    """
    Renders high-definition girl character at (cx, cy) on 512x512 canvas.
    """
    hx = cx + lean_x
    hy = cy - 110

    # =========================================================================
    # 1. BACKGROUND HAIR
    # =========================================================================
    # Back hair volume falling past shoulders
    hb = hair_blow * 3
    d.rounded_rectangle([hx - 58, hy - 52, hx + 58, hy + 130], radius=38, fill=C_HAIR_BASE)
    d.polygon([
        (hx - 58, hy + 30),
        (hx - 65 + hb, hy + 175),
        (hx - 26 + hb, hy + 185),
        (hx - 22, hy + 80)
    ], fill=C_HAIR_BASE)
    d.polygon([
        (hx + 58, hy + 30),
        (hx + 65 - hb, hy + 175),
        (hx + 26 - hb, hy + 185),
        (hx + 22, hy + 80)
    ], fill=C_HAIR_BASE)

    # Hair shading/highlights
    d.line([(hx - 55 + hb, hy + 60), (hx - 50 + hb, hy + 170)], fill=C_HAIR_DARK, width=4)
    d.line([(hx + 55 - hb, hy + 60), (hx + 50 - hb, hy + 170)], fill=C_HAIR_DARK, width=4)

    # =========================================================================
    # 2. LEGS & JEANS & SNEAKERS
    # =========================================================================
    jy = cy + 22
    # Waistband of jeans
    d.rounded_rectangle([cx - 40, jy, cx + 40, jy + 24], radius=6, fill=C_JEANS)
    d.ellipse([cx - 4, jy + 7, cx + 4, jy + 15], fill=C_JEANS_BUTTON)

    # Left Leg (viewer's left)
    lx = cx - 22 + leg_l_off[0] * 3
    ly = jy + 18 + leg_l_off[1] * 3
    d.polygon([
        (lx - 16, ly), (lx - 12, ly + 145),
        (lx + 10, ly + 145), (lx + 14, ly)
    ], fill=C_JEANS)
    # Thigh wash highlight
    d.rounded_rectangle([lx - 9, ly + 15, lx + 5, ly + 105], radius=6, fill=C_JEANS_LIGHT)
    # Side seam
    d.line([(lx - 15, ly), (lx - 12, ly + 145)], fill=C_JEANS_DARK, width=2)
    # Rolled denim cuff
    d.rounded_rectangle([lx - 13, ly + 142, lx + 11, ly + 152], radius=4, fill=C_JEANS_CUFF)
    # Ankle skin peek
    d.rectangle([lx - 8, ly + 152, lx + 6, ly + 158], fill=C_SKIN)
    # White Sneaker
    d.rounded_rectangle([lx - 16, ly + 156, lx + 12, ly + 180], radius=8, fill=C_SNEAKER)
    d.rounded_rectangle([lx - 18, ly + 174, lx + 14, ly + 182], radius=4, fill=C_SNEAKER_SOLE)
    d.line([(lx - 8, ly + 160), (lx + 2, ly + 160)], fill=C_SNEAKER_DARK, width=2) # Laces
    d.line([(lx - 6, ly + 166), (lx + 4, ly + 166)], fill=C_SNEAKER_DARK, width=2)

    # Right Leg (viewer's right)
    rx = cx + 22 + leg_r_off[0] * 3
    ry = jy + 18 + leg_r_off[1] * 3
    d.polygon([
        (rx - 14, ry), (rx - 10, ry + 145),
        (rx + 12, ry + 145), (rx + 16, ry)
    ], fill=C_JEANS)
    # Thigh wash highlight
    d.rounded_rectangle([rx - 5, ry + 15, rx + 9, ry + 105], radius=6, fill=C_JEANS_LIGHT)
    # Side seam
    d.line([(rx + 15, ry), (rx + 12, ry + 145)], fill=C_JEANS_DARK, width=2)
    # Rolled denim cuff
    d.rounded_rectangle([rx - 11, ry + 142, rx + 13, ry + 152], radius=4, fill=C_JEANS_CUFF)
    # Ankle skin peek
    d.rectangle([rx - 6, ry + 152, rx + 8, ry + 158], fill=C_SKIN)
    # White Sneaker
    d.rounded_rectangle([rx - 12, ry + 156, rx + 16, ry + 180], radius=8, fill=C_SNEAKER)
    d.rounded_rectangle([rx - 14, ry + 174, rx + 18, ry + 182], radius=4, fill=C_SNEAKER_SOLE)
    d.line([(rx - 2, ry + 160), (rx + 8, ry + 160)], fill=C_SNEAKER_DARK, width=2) # Laces
    d.line([(rx - 4, ry + 166), (rx + 6, ry + 166)], fill=C_SNEAKER_DARK, width=2)

    # =========================================================================
    # 3. MIDRIFF & CROP TOP & ARMS
    # =========================================================================
    ty = hy + 65
    # Exposed midriff (bare skin between crop top and jeans!)
    d.rounded_rectangle([hx - 36, ty + 68, hx + 36, ty + 116], radius=6, fill=C_SKIN)
    # Delicate navel
    d.ellipse([hx - 3, ty + 90, hx + 3, ty + 97], fill=C_NAVEL)
    d.point([(hx, ty + 93)], fill=C_SKIN_SHADOW)

    # Light gray crop top
    d.rounded_rectangle([hx - 48, ty, hx + 48, ty + 70], radius=10, fill=C_TOP)
    # Neck cutout
    d.ellipse([hx - 18, ty - 6, hx + 18, ty + 14], fill=C_SKIN)
    d.arc([hx - 18, ty - 6, hx + 18, ty + 14], start=0, end=180, fill=C_TOP_LIGHT, width=3)
    # Bottom hem shadow of crop top
    d.line([(hx - 48, ty + 70), (hx + 48, ty + 70)], fill=C_TOP_SHADOW, width=4)

    # Neck
    d.rectangle([hx - 14, hy + 35, hx + 14, hy + 75], fill=C_SKIN)
    d.line([(hx - 12, hy + 48), (hx + 12, hy + 48)], fill=C_SKIN_SHADOW, width=2) # Chin shadow

    # Arms
    if arm_pose == "down":
        # Left arm (viewer's left)
        d.polygon([(hx - 48, ty + 8), (hx - 68, ty + 36), (hx - 54, ty + 44), (hx - 44, ty + 28)], fill=C_TOP)
        d.rounded_rectangle([hx - 64, ty + 44, hx - 48, ty + 138], radius=8, fill=C_SKIN)
        # Right arm (viewer's right, her left arm with red bracelet!)
        d.polygon([(hx + 48, ty + 8), (hx + 68, ty + 36), (hx + 54, ty + 44), (hx + 44, ty + 28)], fill=C_TOP)
        d.rounded_rectangle([hx + 48, ty + 44, hx + 64, ty + 138], radius=8, fill=C_SKIN)
        # Red bracelet from the photo!
        d.rectangle([hx + 47, ty + 128, hx + 65, ty + 133], fill=C_RED_BRACELET)

    elif arm_pose == "run":
        # Left arm pumping forward
        d.polygon([(hx - 48, ty + 8), (hx - 68, ty + 36), (hx - 54, ty + 44), (hx - 44, ty + 28)], fill=C_TOP)
        d.line([(hx - 58, ty + 40), (hx - 78, ty + 100)], fill=C_SKIN, width=14)
        # Right arm pumping back
        d.polygon([(hx + 48, ty + 8), (hx + 68, ty + 36), (hx + 54, ty + 44), (hx + 44, ty + 28)], fill=C_TOP)
        d.line([(hx + 58, ty + 40), (hx + 78, ty + 100)], fill=C_SKIN, width=14)
        d.line([(hx + 70, ty + 90), (hx + 82, ty + 95)], fill=C_RED_BRACELET, width=4)

    elif arm_pose == "up":
        # Arms raised in joy / climbing / caught
        d.polygon([(hx - 48, ty + 8), (hx - 66, ty - 6), (hx - 52, ty - 12), (hx - 42, ty + 18)], fill=C_TOP)
        d.line([(hx - 58, ty), (hx - 68, ty - 75)], fill=C_SKIN, width=14)
        d.polygon([(hx + 48, ty + 8), (hx + 66, ty - 6), (hx + 52, ty - 12), (hx + 42, ty + 18)], fill=C_TOP)
        d.line([(hx + 58, ty), (hx + 68, ty - 75)], fill=C_SKIN, width=14)
        d.line([(hx + 60, ty - 65), (hx + 74, ty - 65)], fill=C_RED_BRACELET, width=4)

    elif arm_pose == "kiss_hand":
        # Blowing kiss gesture
        d.polygon([(hx - 48, ty + 8), (hx - 68, ty + 36), (hx - 54, ty + 44), (hx - 44, ty + 28)], fill=C_TOP)
        d.rounded_rectangle([hx - 64, ty + 44, hx - 48, ty + 138], radius=8, fill=C_SKIN)
        # Hand near mouth
        d.polygon([(hx + 48, ty + 8), (hx + 68, ty + 36), (hx + 54, ty + 44), (hx + 44, ty + 28)], fill=C_TOP)
        d.line([(hx + 56, ty + 36), (hx + 28, ty - 15)], fill=C_SKIN, width=14)
        d.line([(hx + 36, ty - 5), (hx + 46, ty)], fill=C_RED_BRACELET, width=4)

    # =========================================================================
    # 4. FACE & EYES & EXPRESSION
    # =========================================================================
    # Face oval
    d.rounded_rectangle([hx - 38, hy - 36, hx + 38, hy + 46], radius=24, fill=C_SKIN)
    d.polygon([(hx - 36, hy + 20), (hx, hy + 58), (hx + 36, hy + 20)], fill=C_SKIN)

    # Cheeks / Blush
    if blush:
        d.ellipse([hx - 34, hy + 12, hx - 12, hy + 28], fill=(255, 145, 160, 200))
        d.ellipse([hx + 12, hy + 12, hx + 34, hy + 28], fill=(255, 145, 160, 200))
    else:
        d.ellipse([hx - 32, hy + 14, hx - 14, hy + 26], fill=(255, 165, 175, 120))
        d.ellipse([hx + 14, hy + 14, hx + 32, hy + 26], fill=(255, 165, 175, 120))

    # Eyes
    for side in [-1, 1]:
        ex = hx + side * 18
        ey = hy + 8

        if blink:
            # Closed eye with curved smiling lashes
            d.arc([ex - 10, ey - 6, ex + 10, ey + 8], start=20, end=160, fill=C_BLACK, width=3)
            d.line([(ex + side * 8, ey + 4), (ex + side * 12, ey + 1)], fill=C_BLACK, width=2)
        else:
            # Almond eye sclera
            d.ellipse([ex - 10, ey - 8, ex + 10, ey + 8], fill=C_WHITE)
            # Hazel iris
            d.ellipse([ex - 6, ey - 7, ex + 6, ey + 7], fill=C_EYE_HAZEL)
            # Dark pupil
            d.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=C_BLACK)
            # Specular catchlight shine
            d.ellipse([ex - 4, ey - 6, ex - 1, ey - 3], fill=C_WHITE)
            d.point([(ex + 2, ey + 2)], fill=C_WHITE)
            # Upper eyeliner & delicate lashes
            d.arc([ex - 11, ey - 10, ex + 11, ey + 4], start=190, end=350, fill=C_BLACK, width=3)
            d.line([(ex + side * 10, ey - 5), (ex + side * 14, ey - 9)], fill=C_BLACK, width=2)

        # Eyebrows
        d.arc([ex - 10, ey - 18, ex + 10, ey - 10], start=200, end=340, fill=C_HAIR_DARK, width=3)

    # Cute nose
    d.polygon([(hx, hy + 18), (hx - 3, hy + 24), (hx + 3, hy + 24)], fill=C_SKIN_SHADOW)

    # Mouth
    if mouth == "open":  # Surprised 'o' from photo!
        d.rounded_rectangle([hx - 7, hy + 32, hx + 7, hy + 46], radius=6, fill=(55, 20, 25, 255))
        d.ellipse([hx - 5, hy + 33, hx + 5, hy + 37], fill=C_WHITE) # Upper teeth
        d.arc([hx - 8, hy + 30, hx + 8, hy + 47], start=0, end=360, fill=C_LIP_PINK, width=2)
    elif mouth == "smile":
        d.arc([hx - 10, hy + 26, hx + 10, hy + 42], start=20, end=160, fill=C_LIP_DARK, width=3)
        d.line([(hx - 9, hy + 34), (hx + 9, hy + 34)], fill=C_LIP_PINK, width=2)
    elif mouth == "kiss":
        # Puckered sweet lips
        d.rounded_rectangle([hx - 6, hy + 32, hx + 6, hy + 42], radius=4, fill=C_LIP_PINK)
        d.ellipse([hx - 3, hy + 35, hx + 3, hy + 39], fill=C_LIP_DARK)

    # =========================================================================
    # 5. FOREGROUND HAIR (Bangs, center part & drapes over shoulders)
    # =========================================================================
    # Center parting at top
    d.arc([hx - 50, hy - 50, hx + 50, hy], start=180, end=0, fill=C_HAIR_LIGHT, width=8)
    d.line([(hx, hy - 48), (hx, hy - 32)], fill=C_HAIR_ROOT, width=3)

    # Left drape falling over shoulder & chest
    d.polygon([
        (hx - 45, hy - 25),
        (hx - 52 + hb, hy + 155),
        (hx - 28 + hb, hy + 170),
        (hx - 25, hy + 30)
    ], fill=C_HAIR_BASE)
    d.line([(hx - 42 + hb, hy - 10), (hx - 40 + hb, hy + 160)], fill=C_HAIR_LIGHT, width=4)

    # Right drape falling over shoulder & chest
    d.polygon([
        (hx + 45, hy - 25),
        (hx + 52 - hb, hy + 155),
        (hx + 28 - hb, hy + 170),
        (hx + 25, hy + 30)
    ], fill=C_HAIR_BASE)
    d.line([(hx + 42 - hb, hy - 10), (hx + 40 - hb, hy + 160)], fill=C_HAIR_LIGHT, width=4)


# =========================================================================
# ANIMATION SETS (512x512 rendered, downsampled with Lanczos to 256x256)
# =========================================================================

def finalize_frame(im: Image.Image) -> Image.Image:
    """Downsample with high-quality Lanczos filter to 256x256"""
    return im.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)


def gen_idle():
    frames = []
    bobs = [0, -2, 0, 2]
    for i, bob in enumerate(bobs):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=240 + bob,
                  arm_pose="down",
                  blink=(i == 2), blush=False,
                  mouth="open" if i == 0 else "smile",
                  hair_blow=(1 if i % 2 == 0 else -1))
        frames.append(finalize_frame(im))
    return frames


def gen_walk():
    frames = []
    walk_data = [
        (0,  3,  0, -3, -1),
        (-2, 1, -1, -1,  0),
        (-4,-2,  0,  2, -1),
        (0, -3, -1,  3,  0),
        (-2,-1,  0,  1, -1),
        (-4, 2, -1, -2,  0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(walk_data):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=240 + bob,
                  leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                  arm_pose="down", blink=False,
                  mouth="smile",
                  hair_blow=(2 if i % 2 == 0 else -1))
        frames.append(finalize_frame(im))
    return frames


def gen_run():
    """Dynamic sprint when playfully fleeing from pirate!"""
    frames = []
    run_data = [
        (-4,  6, -3, -6, -4),
        (2,   3,  0, -3, -1),
        (-4, -6, -4,  6, -3),
        (2,  -3, -1,  3,  0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(run_data):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=240 + bob,
                  leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                  arm_pose="run", mouth="open",
                  hair_blow=-6)
        frames.append(finalize_frame(im))
    return frames


def gen_jump():
    frames = []
    # Leap
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_girl(d0, cx=256, cy=220,
              leg_l_off=(-3, -5), leg_r_off=(3, -6),
              arm_pose="up", mouth="open", hair_blow=-4)
    frames.append(finalize_frame(im0))

    # Peak
    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_girl(d1, cx=256, cy=200,
              leg_l_off=(-4, -8), leg_r_off=(4, -8),
              arm_pose="up", mouth="smile", hair_blow=-5)
    frames.append(finalize_frame(im1))
    return frames


def gen_fall():
    frames = []
    for i in range(2):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=235,
                  leg_l_off=(-4, -2), leg_r_off=(4, -2),
                  arm_pose="up", mouth="open", hair_blow=4)
        frames.append(finalize_frame(im))
    return frames


def gen_land():
    frames = []
    # Squat
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_girl(d0, cx=256, cy=260,
              leg_l_off=(-3, 2), leg_r_off=(3, 2),
              arm_pose="down", mouth="smile")
    frames.append(finalize_frame(im0))

    # Recover
    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_girl(d1, cx=256, cy=240, arm_pose="down", mouth="smile")
    frames.append(finalize_frame(im1))
    return frames


def gen_kiss():
    """Sweet romantic kiss: leaning forward, rosy blush, pouted lips, glowing floating hearts!"""
    frames = []
    kiss_data = [
        (4,  "smile", True,  None, 0),
        (10, "kiss",  True,  -20,  18),
        (14, "kiss",  True,  -45,  24),
        (8,  "smile", True,  -65,  20),
    ]
    for i, (lx, mouth, blush, hy, hsize) in enumerate(kiss_data):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256 + lx, cy=240,
                  leg_l_off=(0, 0), leg_r_off=(lx // 3, 0),
                  arm_pose="down", blink=True, blush=blush,
                  mouth=mouth, hair_blow=-3, lean_x=lx)

        if hy is not None:
            draw_smooth_heart(d, 256 + lx + 35, 130 + hy, size=hsize)

        frames.append(finalize_frame(im))
    return frames


def gen_blush():
    """Giggling / blowing kiss with heart floating up"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=240,
                  arm_pose="kiss_hand" if i < 2 else "down",
                  blink=(i % 2 == 1), blush=True,
                  mouth="kiss" if i == 0 else "smile")
        draw_smooth_heart(d, 290 + i * 8, 110 - i * 15, size=14)
        frames.append(finalize_frame(im))
    return frames


def gen_climb():
    """Climbing desktop borders/windows"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=240 + (2 if i % 2 == 0 else -2),
                  leg_l_off=(-2, -3 if i % 2 == 0 else 3),
                  leg_r_off=(3, 3 if i % 2 == 0 else -3),
                  arm_pose="up", mouth="smile")
        frames.append(finalize_frame(im))
    return frames


def gen_dragged():
    """Carried by mouse: wide surprised 'o' expression matching reference photo!"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_girl(d, cx=256, cy=240,
                  leg_l_off=(-3 if i % 2 == 0 else 3, -3),
                  leg_r_off=(3 if i % 2 == 0 else -3, 2),
                  arm_pose="up", blink=False, blush=True,
                  mouth="open", hair_blow=5)
        frames.append(finalize_frame(im))
    return frames


def gen_sleep():
    """Resting gracefully on desktop"""
    frames = []
    for i in range(3):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        # Sitting position
        draw_girl(d, cx=256, cy=265,
                  leg_l_off=(-4, 2), leg_r_off=(4, 2),
                  arm_pose="down", blink=True, blush=True,
                  mouth="smile")
        # Floating Z and small heart
        d.text((290, 80 - i * 10), "z", fill=(255, 170, 195, 255))
        if i >= 1:
            draw_smooth_heart(d, 320, 60 - i * 10, size=10)
        frames.append(finalize_frame(im))
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

    print(f"HD Smooth Girl sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_piratess_sprites()
