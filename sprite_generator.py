"""
High-Definition Smooth Cartoon Sprite Generator for Donald Trump.
Renders smooth anti-aliased 256x256 frames (via 512x512 Lanczos supersampling):
- Iconic golden-blonde swept-back hairstyle with signature volume
- Tailored dark navy blue suit jacket (open) with matching trousers
- Signature long bright red tie hanging below belt line
- Crisp white collared dress shirt with collar points
- Polished black leather dress shoes
- Signature gestures: Pointing finger forward ('You're fired!'), swagger walk, fist pump celebration
"""

import os
import math
from PIL import Image, ImageDraw

OUTPUT_SIZE = 256
RENDER_SIZE = 512

# HD Palette
C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (20, 20, 24, 255)
C_WHITE       = (255, 255, 255, 255)

# Skin & Tan
C_SKIN        = (250, 204, 168, 255)
C_SKIN_SHADOW = (226, 166, 126, 255)
C_TAN_BLUSH   = (238, 154, 108, 150)

# Signature Hair
C_HAIR        = (246, 210, 88, 255)
C_HAIR_LIGHT  = (255, 238, 142, 255)
C_HAIR_DARK   = (208, 158, 48, 255)

# Suit & Clothing
C_SUIT        = (22, 34, 56, 255)
C_SUIT_LIGHT  = (38, 56, 90, 255)
C_SUIT_DARK   = (12, 20, 36, 255)

C_SHIRT       = (255, 255, 255, 255)
C_SHIRT_SHAD  = (220, 224, 232, 255)

C_TIE         = (228, 28, 45, 255)
C_TIE_DARK    = (175, 18, 32, 255)
C_TIE_LIGHT   = (248, 65, 82, 255)

C_BELT        = (18, 18, 22, 255)
C_BUCKLE      = (215, 220, 230, 255)

C_SHOE        = (18, 18, 22, 255)
C_SHOE_SOLE   = (38, 38, 42, 255)


def create_canvas():
    return Image.new("RGBA", (RENDER_SIZE, RENDER_SIZE), C_TRANSPARENT)


def finalize_frame(im: Image.Image) -> Image.Image:
    return im.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)


def draw_trump(d: ImageDraw.ImageDraw, cx=256, cy=245,
               leg_l_off=(0, 0), leg_r_off=(0, 0),
               arm_pose="walk", eye_blink=False,
               mouth="speech", hair_blow=0, lean_x=0, tie_swing=0):
    """
    Renders Donald Trump on 512x512 canvas.
    """
    hx = cx + lean_x
    hy = cy - 110

    # =========================================================================
    # 1. LEGS (Navy Trousers & Black Dress Shoes)
    # =========================================================================
    jy = cy + 45

    # Left Leg
    lx = cx - 24 + leg_l_off[0] * 3
    ly = jy + 18 + leg_l_off[1] * 3
    d.polygon([
        (cx - 36, jy), (cx - 10, jy),
        (lx + 8, ly + 145), (lx - 18, ly + 145)
    ], fill=C_SUIT)
    d.line([(cx - 24, jy), (lx - 5, ly + 140)], fill=C_SUIT_LIGHT, width=3) # Crease line
    # Left Black Dress Shoe
    d.polygon([
        (lx - 26, ly + 142), (lx + 12, ly + 142),
        (lx + 18, ly + 158), (lx - 28, ly + 158)
    ], fill=C_SHOE)
    d.line([(lx - 28, ly + 158), (lx + 18, ly + 158)], fill=C_SHOE_SOLE, width=3)

    # Right Leg
    rx = cx + 24 + leg_r_off[0] * 3
    ry = jy + 18 + leg_r_off[1] * 3
    d.polygon([
        (cx + 10, jy), (cx + 36, jy),
        (rx + 18, ry + 145), (rx - 8, ry + 145)
    ], fill=C_SUIT)
    d.line([(cx + 24, jy), (rx + 5, ry + 140)], fill=C_SUIT_LIGHT, width=3) # Crease line
    # Right Black Dress Shoe
    d.polygon([
        (rx - 12, ry + 142), (rx + 26, ry + 142),
        (rx + 28, ry + 158), (rx - 18, ry + 158)
    ], fill=C_SHOE)
    d.line([(rx - 18, ry + 158), (rx + 28, ry + 158)], fill=C_SHOE_SOLE, width=3)

    # =========================================================================
    # 2. TORSO (White Shirt, Belt, Long Red Tie, Open Navy Suit Jacket)
    # =========================================================================
    ty = hy + 60
    # White dress shirt base
    d.rounded_rectangle([hx - 38, ty, hx + 38, ty + 85], radius=6, fill=C_SHIRT)

    # White collar
    d.polygon([(hx - 24, ty - 8), (hx - 5, ty + 16), (hx - 18, ty + 12)], fill=C_SHIRT)
    d.polygon([(hx + 24, ty - 8), (hx + 5, ty + 16), (hx + 18, ty + 12)], fill=C_SHIRT)
    d.line([(hx - 24, ty - 8), (hx - 5, ty + 16)], fill=C_SHIRT_SHAD, width=2)
    d.line([(hx + 24, ty - 8), (hx + 5, ty + 16)], fill=C_SHIRT_SHAD, width=2)

    # Belt
    d.rectangle([hx - 38, ty + 72, hx + 38, ty + 84], fill=C_BELT)
    d.rectangle([hx - 8, ty + 72, hx + 8, ty + 84], fill=C_BUCKLE)

    # Signature Long Red Tie (hanging down past belt line!)
    ts = tie_swing * 2
    d.polygon([
        (hx - 7, ty + 10), (hx + 7, ty + 10),
        (hx + 10 + ts, ty + 95), (hx + ts, ty + 108), (hx - 10 + ts, ty + 95)
    ], fill=C_TIE)
    d.line([(hx - 7, ty + 12), (hx - 9 + ts, ty + 94)], fill=C_TIE_DARK, width=2)
    d.line([(hx + 5, ty + 12), (hx + 7 + ts, ty + 94)], fill=C_TIE_LIGHT, width=2)

    # Open Navy Suit Jacket (left & right flaps)
    d.polygon([
        (hx - 58, ty), (hx - 24, ty),
        (hx - 16, ty + 86), (hx - 60, ty + 88)
    ], fill=C_SUIT)
    d.polygon([
        (hx + 24, ty), (hx + 58, ty),
        (hx + 60, ty + 88), (hx + 16, ty + 86)
    ], fill=C_SUIT)
    # Suit lapels
    d.line([(hx - 24, ty), (hx - 16, ty + 46)], fill=C_SUIT_LIGHT, width=4)
    d.line([(hx + 24, ty), (hx + 16, ty + 46)], fill=C_SUIT_LIGHT, width=4)

    # Arms
    if arm_pose == "walk":
        # Left arm swinging back
        d.line([(hx - 50, ty + 12), (hx - 75, ty + 75)], fill=C_SUIT, width=18)
        d.ellipse([hx - 85, ty + 72, cx - 68, ty + 88], fill=C_SKIN)

        # Right arm swinging forward
        d.line([(hx + 50, ty + 12), (hx + 78, ty + 75)], fill=C_SUIT, width=18)
        d.ellipse([hx + 68, ty + 72, cx + 85, ty + 88], fill=C_SKIN)

    elif arm_pose == "point":
        # The iconic finger point from photo!
        # Left arm relaxed
        d.line([(hx - 50, ty + 12), (hx - 72, ty + 70)], fill=C_SUIT, width=18)
        d.ellipse([hx - 82, ty + 68, hx - 66, ty + 84], fill=C_SKIN)

        # Right arm pointing forward
        d.line([(hx + 50, ty + 12), (hx + 105, ty + 4)], fill=C_SUIT, width=18)
        d.rectangle([hx + 104, ty - 3, hx + 112, ty + 11], fill=C_SHIRT) # White cuff
        d.ellipse([hx + 110, ty - 4, hx + 128, ty + 12], fill=C_SKIN) # Fist
        d.line([(hx + 122, ty + 4), (hx + 155, ty + 2)], fill=C_SKIN, width=6) # Pointing finger!

    elif arm_pose == "fist_pump":
        # Double fist pump celebration / dance!
        d.line([(hx - 50, ty + 12), (hx - 70, ty - 25)], fill=C_SUIT, width=18)
        d.ellipse([hx - 78, ty - 40, hx - 62, ty - 24], fill=C_SKIN)

        d.line([(hx + 50, ty + 12), (hx + 70, ty - 25)], fill=C_SUIT, width=18)
        d.ellipse([hx + 62, ty - 40, hx + 78, ty - 24], fill=C_SKIN)

    elif arm_pose == "dragged":
        # Flailing arms while being carried by mouse!
        d.line([(hx - 50, ty + 12), (hx - 80, ty - 40)], fill=C_SUIT, width=18)
        d.ellipse([hx - 92, ty - 52, hx - 72, ty - 34], fill=C_SKIN)

        d.line([(hx + 50, ty + 12), (hx + 80, ty - 40)], fill=C_SUIT, width=18)
        d.ellipse([hx + 72, ty - 52, hx + 92, ty - 34], fill=C_SKIN)

    elif arm_pose == "up":
        # Climbing borders
        d.line([(hx - 50, ty + 12), (hx - 62, ty - 60)], fill=C_SUIT, width=18)
        d.line([(hx + 50, ty + 12), (hx + 62, ty - 60)], fill=C_SUIT, width=18)

    # =========================================================================
    # 3. HEAD & FACE
    # =========================================================================
    d.rounded_rectangle([hx - 32, hy - 20, hx + 32, hy + 45], radius=18, fill=C_SKIN)
    d.polygon([(hx - 30, hy + 20), (hx, hy + 50), (hx + 30, hy + 20)], fill=C_SKIN) # Jaw

    # Tan / Bronzer contour
    d.ellipse([hx - 28, hy + 10, hx - 12, hy + 26], fill=C_TAN_BLUSH)
    d.ellipse([hx + 12, hy + 10, hx + 28, hy + 26], fill=C_TAN_BLUSH)

    # Eyes
    for side in [-1, 1]:
        ex = hx + side * 15
        ey = hy + 5
        if eye_blink:
            d.line([(ex - 7, ey), (ex + 7, ey)], fill=C_BLACK, width=2)
        else:
            d.ellipse([ex - 7, ey - 4, ex + 7, ey + 4], fill=C_WHITE)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(85, 125, 175, 255)) # Blue eyes
            d.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=C_BLACK)
            # Squint contour
            d.line([(ex - 8, ey - 4), (ex + 8, ey - 4)], fill=C_SKIN_SHADOW, width=2)
            # Blonde eyebrows
            d.arc([ex - 9, ey - 14, ex + 9, ey - 6], start=190, end=350, fill=C_HAIR_DARK, width=4)

    # Nose
    d.polygon([(hx, hy + 10), (hx - 4, hy + 24), (hx + 4, hy + 24)], fill=C_SKIN_SHADOW)

    # Mouth
    if mouth == "speech":
        d.rounded_rectangle([hx - 8, hy + 30, hx + 8, hy + 38], radius=4, fill=(195, 75, 80, 255))
        d.line([(hx - 6, hy + 33), (hx + 6, hy + 33)], fill=C_WHITE, width=2)
    elif mouth == "smile":
        d.arc([hx - 10, hy + 24, hx + 10, hy + 40], start=20, end=160, fill=(185, 60, 68, 255), width=3)
    elif mouth == "kiss":
        d.rounded_rectangle([hx - 6, hy + 30, hx + 6, hy + 38], radius=4, fill=(215, 60, 75, 255))

    # =========================================================================
    # 4. SIGNATURE HAIR (Golden-blonde swept-back volume)
    # =========================================================================
    hb = hair_blow * 2
    d.rounded_rectangle([hx - 42, hy - 45, hx + 42, hy - 8], radius=16, fill=C_HAIR)
    d.polygon([
        (hx - 42, hy - 30), (hx - 50 + hb, hy - 40),
        (hx - 30 + hb, hy - 55), (hx + 10 + hb, hy - 58),
        (hx + 45 + hb, hy - 42), (hx + 42, hy - 15),
        (hx + 30, hy - 25), (hx - 10, hy - 35)
    ], fill=C_HAIR)
    # Sweeping hair lines & highlights
    d.arc([hx - 45 + hb, hy - 52, hx + 45 + hb, hy - 10], start=180, end=350, fill=C_HAIR_LIGHT, width=6)
    d.line([(hx - 35 + hb, hy - 38), (hx + 35 + hb, hy - 45)], fill=C_HAIR_LIGHT, width=4)
    d.line([(hx - 25 + hb, hy - 28), (hx + 38 + hb, hy - 32)], fill=C_HAIR_LIGHT, width=3)
    d.line([(hx - 40, hy - 20), (hx - 36, hy + 5)], fill=C_HAIR_DARK, width=4) # Sideburn left
    d.line([(hx + 40, hy - 20), (hx + 36, hy + 5)], fill=C_HAIR_DARK, width=4) # Sideburn right


# =========================================================================
# ANIMATION SETS
# =========================================================================

def gen_idle():
    """Standing confident, pointing finger forward (from photo) / thumbs up!"""
    frames = []
    bobs = [0, -2, 0, 2]
    for i, bob in enumerate(bobs):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=245 + bob,
                   arm_pose="point" if i % 2 == 0 else "walk",
                   eye_blink=(i == 2),
                   mouth="speech" if i == 0 else "smile")
        frames.append(finalize_frame(im))
    return frames


def gen_walk():
    """Iconic White House lawn swagger stride from photo!"""
    frames = []
    walk_data = [
        (0,   4,  0,  -4, -1,  2),
        (-2,  2, -1,  -2,  0,  0),
        (-4, -2,  0,   2, -1, -2),
        (0,  -4, -1,   4,  0, -2),
        (-2, -2,  0,   2, -1,  0),
        (-4,  2, -1,  -2,  0,  2),
    ]
    for i, (bob, ldx, ldy, rdx, rdy, t_swing) in enumerate(walk_data):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=245 + bob,
                   leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                   arm_pose="point" if i == 0 else "walk",
                   tie_swing=t_swing)
        frames.append(finalize_frame(im))
    return frames


def gen_run():
    """Brisk jog chasing the girl!"""
    frames = []
    run_data = [
        (-4,  6, -3, -6, -4,  4),
        (2,   3,  0, -3, -1,  0),
        (-4, -6, -4,  6, -3, -4),
        (2,  -3, -1,  3,  0,  0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy, t_swing) in enumerate(run_data):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=245 + bob,
                   leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                   arm_pose="walk", tie_swing=t_swing, hair_blow=-3)
        frames.append(finalize_frame(im))
    return frames


def gen_jump():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_trump(d0, cx=256, cy=220, leg_l_off=(-3, -5), leg_r_off=(3, -5), arm_pose="fist_pump", tie_swing=-4)
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_trump(d1, cx=256, cy=200, leg_l_off=(-4, -8), leg_r_off=(4, -8), arm_pose="fist_pump", tie_swing=4)
    frames.append(finalize_frame(im1))
    return frames


def gen_fall():
    frames = []
    for i in range(2):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=235, leg_l_off=(-4, -2), leg_r_off=(4, -2), arm_pose="dragged", tie_swing=6)
        frames.append(finalize_frame(im))
    return frames


def gen_land():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_trump(d0, cx=256, cy=260, leg_l_off=(-3, 2), leg_r_off=(3, 2), arm_pose="walk", mouth="smile")
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_trump(d1, cx=256, cy=245, arm_pose="point", mouth="speech")
    frames.append(finalize_frame(im1))
    return frames


def gen_climb():
    """Climbing screen borders/windows ('We will build a wall!')"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=245 + (2 if i % 2 == 0 else -2),
                   leg_l_off=(-2, -3 if i % 2 == 0 else 3),
                   leg_r_off=(3, 3 if i % 2 == 0 else -3),
                   arm_pose="up")
        frames.append(finalize_frame(im))
    return frames


def gen_dragged():
    """Dragged by user ('Excuse me! Total fake news!')"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=245,
                   leg_l_off=(-3 if i % 2 == 0 else 3, -3),
                   leg_r_off=(3 if i % 2 == 0 else -3, 2),
                   arm_pose="dragged", hair_blow=4, mouth="speech")
        frames.append(finalize_frame(im))
    return frames


def gen_attack():
    """The iconic Pointing Finger ('You're fired! 🫵')"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256 + (i * 3), cy=245, arm_pose="point", mouth="speech")
        frames.append(finalize_frame(im))
    return frames


def gen_celebrate():
    """Double fist pump rally dance!"""
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=245 - (i * 3), arm_pose="fist_pump", mouth="smile")
        frames.append(finalize_frame(im))
    return frames


def gen_sleep():
    """Resting peacefully ('Big rally tomorrow...')"""
    frames = []
    for i in range(3):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_trump(d, cx=256, cy=265, arm_pose="walk", eye_blink=True, mouth="smile")
        d.text((290, 80 - i * 10), "Z", fill=(246, 210, 88, 255))
        frames.append(finalize_frame(im))
    return frames


def generate_all_sprites(output_dir="assets/sprites"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "idle": gen_idle(),
        "walk": gen_walk(),
        "run": gen_run(),
        "jump": gen_jump(),
        "fall": gen_fall(),
        "land": gen_land(),
        "climb_wall": gen_climb(),
        "climb_ceiling": gen_climb(),
        "dragged": gen_dragged(),
        "attack": gen_attack(),
        "celebrate": gen_celebrate(),
        "sleep": gen_sleep(),
    }

    for anim_name, frames in animations.items():
        for idx, frame in enumerate(frames):
            p_r = os.path.join(output_dir, f"{anim_name}_right_{idx}.png")
            frame.save(p_r)

            frame_l = frame.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{anim_name}_left_{idx}.png")
            frame_l.save(p_l)

    print(f"Donald Trump HD sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_sprites()
