"""
Girl sprite generator based on the reference photo:
- Blonde straight hair falling over shoulders with center part
- Light gray cropped t-shirt (crop top) exposing midriff
- Red bracelet on left wrist
- Fitted blue skinny denim jeans
- Clean white sneakers
- Cute expressive face
"""

import os
from PIL import Image, ImageDraw

# Color Palette
C_TRANSPARENT    = (0, 0, 0, 0)
C_BLACK          = (25, 22, 28, 255)
C_WHITE          = (255, 255, 255, 255)
C_SKIN           = (253, 226, 206, 255)
C_SKIN_SHADOW    = (232, 192, 168, 255)
C_BLUSH          = (248, 142, 155, 255)

# Hair (Blonde / Ash Honey Blonde from photo)
C_HAIR           = (212, 182, 138, 255)       # Main blonde
C_HAIR_LIGHT     = (238, 218, 180, 255)       # Highlight
C_HAIR_DARK      = (175, 142, 102, 255)       # Depth / shadow
C_HAIR_ROOT      = (148, 115, 80, 255)        # Center part

# Clothing
# Crop Top: Light heather gray / silver
C_TOP            = (218, 221, 226, 255)
C_TOP_LIGHT      = (240, 242, 245, 255)
C_TOP_SHADOW     = (175, 180, 188, 255)

# Jeans: Classic deep indigo denim
C_JEANS          = (42, 78, 132, 255)
C_JEANS_LIGHT    = (68, 112, 175, 255)        # Thigh fading / highlight
C_JEANS_DARK     = (28, 52, 92, 255)          # Creases / side seams
C_JEANS_WAIST    = (190, 165, 110, 255)       # Button / rivet brass

# Shoes: White sneakers
C_SNEAKER        = (252, 252, 252, 255)
C_SNEAKER_SOLE   = (215, 218, 222, 255)
C_SNEAKER_SHADOW = (180, 184, 190, 255)

# Details
C_RED_BRACELET   = (225, 45, 52, 255)         # Red wrist bracelet from photo
C_NAVEL          = (220, 175, 150, 255)       # Cute belly button
C_EYE_HAZEL      = (95, 68, 48, 255)          # Expressive eyes
C_HEART          = (255, 75, 120, 255)
C_HEART_LIGHT    = (255, 145, 180, 255)

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


def draw_girl_head(d: ImageDraw.ImageDraw, hx, hy, blink=False, blush=False, mouth="smile", hair_blow=0):
    """
    Draw face and blonde hair matching the photo:
    - Long blonde straight hair falling over shoulders
    - Center parting
    - Expressive face: delicate eyes, cute mouth ('smile', 'kiss', 'open' / surprised 'o')
    """
    # 1. Back hair volume
    d.rectangle([hx - 7, hy - 6, hx + 7, hy + 8], fill=C_HAIR)
    d.polygon([
        (hx - 7, hy + 5),
        (hx - 8 + hair_blow, hy + 17),
        (hx - 5 + hair_blow, hy + 19),
        (hx - 4, hy + 8)
    ], fill=C_HAIR)
    d.polygon([
        (hx + 4, hy + 8),
        (hx + 5 - hair_blow, hy + 19),
        (hx + 8 - hair_blow, hy + 17),
        (hx + 7, hy + 5)
    ], fill=C_HAIR)

    # Hair shading/depth
    d.line([(hx - 8 + hair_blow, hy + 10), (hx - 8 + hair_blow, hy + 17)], fill=C_HAIR_DARK)
    d.line([(hx + 8 - hair_blow, hy + 10), (hx + 8 - hair_blow, hy + 17)], fill=C_HAIR_DARK)

    # 2. Face skin base
    d.rectangle([hx - 5, hy - 2, hx + 5, hy + 6], fill=C_SKIN)
    d.line([(hx - 3, hy + 7), (hx + 3, hy + 7)], fill=C_SKIN) # Chin
    d.line([(hx - 1, hy + 8), (hx + 1, hy + 8)], fill=C_SKIN_SHADOW) # Jaw tip

    # 3. Top of head / Hair roots & center parting
    d.rectangle([hx - 6, hy - 7, hx + 6, hy - 3], fill=C_HAIR)
    d.line([(hx - 5, hy - 7), (hx + 5, hy - 7)], fill=C_HAIR_LIGHT)
    d.point([(hx, hy - 7), (hx, hy - 6), (hx, hy - 5)], fill=C_HAIR_ROOT) # Center part

    # Front bangs framing face (straight down sides)
    d.line([(hx - 5, hy - 3), (hx - 5, hy + 14)], fill=C_HAIR_LIGHT, width=1)
    d.line([(hx - 6, hy), (hx - 6, hy + 16)], fill=C_HAIR, width=1)

    d.line([(hx + 5, hy - 3), (hx + 5, hy + 14)], fill=C_HAIR_LIGHT, width=1)
    d.line([(hx + 6, hy), (hx + 6, hy + 16)], fill=C_HAIR, width=1)

    # Eyebrows
    d.line([(hx - 4, hy), (hx - 2, hy)], fill=C_HAIR_DARK)
    d.line([(hx + 2, hy), (hx + 4, hy)], fill=C_HAIR_DARK)

    # 4. Eyes
    if blink:
        d.line([(hx - 4, hy + 2), (hx - 2, hy + 2)], fill=C_BLACK, width=1)
        d.line([(hx + 2, hy + 2), (hx + 4, hy + 2)], fill=C_BLACK, width=1)
    else:
        # Left eye
        d.rectangle([hx - 4, hy + 2, hx - 2, hy + 3], fill=C_WHITE)
        d.point([(hx - 3, hy + 2)], fill=C_EYE_HAZEL)
        d.point([(hx - 4, hy + 1)], fill=C_BLACK) # Eyelash
        # Right eye
        d.rectangle([hx + 2, hy + 2, hx + 4, hy + 3], fill=C_WHITE)
        d.point([(hx + 3, hy + 2)], fill=C_EYE_HAZEL)
        d.point([(hx + 4, hy + 1)], fill=C_BLACK) # Eyelash

    # Cute nose
    d.point([(hx, hy + 4)], fill=C_SKIN_SHADOW)

    # Cheeks / Blush
    if blush:
        d.rectangle([hx - 4, hy + 4, hx - 3, hy + 5], fill=C_BLUSH)
        d.rectangle([hx + 3, hy + 4, hx + 4, hy + 5], fill=C_BLUSH)
    else:
        d.point([(hx - 4, hy + 5)], fill=C_BLUSH)
        d.point([(hx + 4, hy + 5)], fill=C_BLUSH)

    # 5. Mouth (from photo: cute surprised 'o' or smile / kiss)
    if mouth == "smile":
        d.line([(hx - 1, hy + 6), (hx + 1, hy + 6)], fill=(210, 80, 95, 255))
    elif mouth == "kiss":
        d.rectangle([hx - 1, hy + 5, hx + 1, hy + 6], fill=(230, 60, 85, 255))
        d.point([(hx, hy + 6)], fill=C_BLUSH)
    elif mouth == "open": # Surprised 'o' from photo!
        d.rectangle([hx - 1, hy + 5, hx + 1, hy + 7], fill=C_BLACK)
        d.point([(hx, hy + 6)], fill=(180, 50, 60, 255))
        d.line([(hx - 1, hy + 5), (hx + 1, hy + 5)], fill=(225, 100, 110, 255))


def draw_girl_torso(d: ImageDraw.ImageDraw, tx, ty, width=12, arm_pose="down"):
    """
    Draw cropped light gray t-shirt, exposed midriff & arms:
    - Loose light gray crop top
    - Exposed belly with navel
    - Bare arms
    - Red bracelet on left wrist!
    """
    hw = width // 2

    # 1. Light gray crop top
    d.rectangle([tx - hw, ty + 1, tx + hw, ty + 7], fill=C_TOP)
    d.line([(tx - hw + 1, ty + 1), (tx + hw - 1, ty + 1)], fill=C_TOP_LIGHT) # Collar/neckline
    # Loose hem at bottom of crop top
    d.line([(tx - hw, ty + 7), (tx + hw, ty + 7)], fill=C_TOP_SHADOW)

    # Neck
    d.rectangle([tx - 2, ty - 1, tx + 2, ty + 1], fill=C_SKIN)

    # 2. Exposed midriff (bare skin between crop top and jeans!)
    d.rectangle([tx - hw + 2, ty + 8, tx + hw - 2, ty + 11], fill=C_SKIN)
    d.point([(tx, ty + 9)], fill=C_NAVEL) # Navel / belly button!
    d.line([(tx - hw + 2, ty + 8), (tx - hw + 2, ty + 11)], fill=C_SKIN_SHADOW)
    d.line([(tx + hw - 2, ty + 8), (tx + hw - 2, ty + 11)], fill=C_SKIN_SHADOW)

    # 3. Arms & hands
    if arm_pose == "down":
        # Left arm (viewer's left) - bare skin from short sleeve
        d.rectangle([tx - hw - 2, ty + 2, tx - hw, ty + 4], fill=C_TOP) # Short sleeve
        d.rectangle([tx - hw - 2, ty + 5, tx - hw, ty + 12], fill=C_SKIN) # Bare arm
        d.rectangle([tx - hw - 2, ty + 13, tx - hw, ty + 14], fill=C_SKIN_SHADOW) # Hand

        # Right arm (viewer's right, her left arm with red bracelet!)
        d.rectangle([tx + hw, ty + 2, tx + hw + 2, ty + 4], fill=C_TOP) # Short sleeve
        d.rectangle([tx + hw, ty + 5, tx + hw + 2, ty + 11], fill=C_SKIN) # Bare arm
        # Red bracelet from the photo!
        d.line([(tx + hw, ty + 12), (tx + hw + 2, ty + 12)], fill=C_RED_BRACELET)
        d.rectangle([tx + hw, ty + 13, tx + hw + 2, ty + 14], fill=C_SKIN_SHADOW) # Hand

    elif arm_pose == "run":
        # Pumping arms in run
        d.rectangle([tx - hw - 2, ty + 2, tx - hw, ty + 4], fill=C_TOP)
        d.line([(tx - hw - 1, ty + 5), (tx - hw - 4, ty + 9)], fill=C_SKIN, width=2)
        d.rectangle([tx + hw, ty + 2, tx + hw + 2, ty + 4], fill=C_TOP)
        d.line([(tx + hw + 1, ty + 5), (tx + hw + 4, ty + 9)], fill=C_SKIN, width=2)
        d.point([(tx + hw + 4, ty + 9)], fill=C_RED_BRACELET)

    elif arm_pose == "up":
        # Arms raised in joy / climbing
        d.rectangle([tx - hw - 2, ty + 1, tx - hw, ty + 3], fill=C_TOP)
        d.line([(tx - hw - 1, ty + 1), (tx - hw - 3, ty - 6)], fill=C_SKIN, width=2)
        d.rectangle([tx + hw, ty + 1, tx + hw + 2, ty + 3], fill=C_TOP)
        d.line([(tx + hw + 1, ty + 1), (tx + hw + 3, ty - 6)], fill=C_SKIN, width=2)
        d.point([(tx + hw + 3, ty - 4)], fill=C_RED_BRACELET)


def draw_girl_legs(d: ImageDraw.ImageDraw, cx, cy, l_off=(0, 0), r_off=(0, 0)):
    """
    Draw blue skinny denim jeans and white sneakers:
    - High-waist denim with waistband button
    - Tight fitted jeans
    - Rolled cuffs at ankle
    - White sneakers with gray soles
    """
    # Waistband / belt area of jeans
    d.rectangle([cx - 5, cy, cx + 5, cy + 2], fill=C_JEANS)
    d.point([(cx, cy + 1)], fill=C_JEANS_WAIST) # Brass button

    # Left leg (viewer's left)
    lx = cx - 3 + l_off[0]
    ly = cy + 2 + l_off[1]
    # Denim thigh & calf
    d.rectangle([lx - 1, ly, lx + 2, ly + 8], fill=C_JEANS)
    d.line([(lx, ly + 1), (lx, ly + 7)], fill=C_JEANS_LIGHT) # Wash fade
    d.line([(lx - 1, ly), (lx - 1, ly + 8)], fill=C_JEANS_DARK) # Inseam
    # Jean cuff
    d.line([(lx - 1, ly + 8), (lx + 2, ly + 8)], fill=(125, 155, 195, 255))
    # Ankle skin peek
    d.line([(lx - 1, ly + 9), (lx + 2, ly + 9)], fill=C_SKIN)
    # White sneaker
    d.rectangle([lx - 2, ly + 10, lx + 2, ly + 12], fill=C_SNEAKER)
    d.point([(lx, ly + 10)], fill=C_SNEAKER_SHADOW) # Laces
    d.line([(lx - 2, ly + 13), (lx + 3, ly + 13)], fill=C_SNEAKER_SOLE) # Sole

    # Right leg (viewer's right)
    rx = cx + 3 + r_off[0]
    ry = cy + 2 + r_off[1]
    d.rectangle([rx - 2, ry, rx + 1, ry + 8], fill=C_JEANS)
    d.line([(rx, ry + 1), (rx, ry + 7)], fill=C_JEANS_LIGHT)
    d.line([(rx + 1, ry), (rx + 1, ry + 8)], fill=C_JEANS_DARK)
    # Jean cuff
    d.line([(rx - 2, ry + 8), (rx + 1, ry + 8)], fill=(125, 155, 195, 255))
    # Ankle skin peek
    d.line([(rx - 2, ry + 9), (rx + 1, ry + 9)], fill=C_SKIN)
    # White sneaker
    d.rectangle([rx - 2, ry + 10, rx + 2, ry + 12], fill=C_SNEAKER)
    d.point([(rx, ry + 10)], fill=C_SNEAKER_SHADOW)
    d.line([(rx - 3, ry + 13), (rx + 2, ry + 13)], fill=C_SNEAKER_SOLE)


# =========================================================================
# ANIMATION SETS
# =========================================================================

def gen_idle():
    frames = []
    bobs = [0, -1, 0, 1]
    for i, bob in enumerate(bobs):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 26 + bob

        draw_girl_legs(d, 32, 40)
        draw_girl_torso(d, cx, cy + 2, arm_pose="down")
        draw_girl_head(d, cx, cy - 8, blink=(i == 2), blush=False,
                       mouth="open" if i == 0 else "smile",
                       hair_blow=(1 if i % 2 == 0 else -1))
        frames.append(im)
    return frames


def gen_walk():
    frames = []
    walk_data = [
        (0,  2,  0, -2, -1),
        (-1, 1, -1, -1,  0),
        (-2,-1,  0,  1, -1),
        (0, -2, -1,  2,  0),
        (-1,-1,  0,  1, -1),
        (-2, 1, -1, -1,  0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(walk_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 26 + bob

        draw_girl_legs(d, 32, 40, (ldx, ldy), (rdx, rdy))
        draw_girl_torso(d, cx, cy + 2, arm_pose="down")
        draw_girl_head(d, cx, cy - 8, blink=False,
                       mouth="smile",
                       hair_blow=(2 if i % 2 == 0 else -1))
        frames.append(im)
    return frames


def gen_run():
    """Playful sprint fleeing from the pirate!"""
    frames = []
    run_data = [
        (-2,  4, -2, -4, -3),
        (1,   2,  0, -2, -1),
        (-2, -4, -3,  4, -2),
        (1,  -2, -1,  2,  0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(run_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 33, 26 + bob

        draw_girl_legs(d, 32, 40, (ldx, ldy), (rdx, rdy))
        draw_girl_torso(d, cx, cy + 2, arm_pose="run")
        # Hair flying behind in sprint!
        draw_girl_head(d, cx, cy - 8, mouth="open", hair_blow=-5)
        frames.append(im)
    return frames


def gen_jump():
    frames = []
    # Frame 0: leap
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    cx, cy = 32, 22
    draw_girl_legs(d0, 32, 40, (-2, -4), (2, -5))
    draw_girl_torso(d0, cx, cy + 2, arm_pose="up")
    draw_girl_head(d0, cx, cy - 8, mouth="open", hair_blow=-3)
    frames.append(im0)

    # Frame 1: peak
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    cx, cy = 32, 20
    draw_girl_legs(d1, 32, 40, (-3, -6), (3, -6))
    draw_girl_torso(d1, cx, cy + 2, arm_pose="up")
    draw_girl_head(d1, cx, cy - 8, mouth="smile", hair_blow=-4)
    frames.append(im1)
    return frames


def gen_fall():
    frames = []
    for i in range(2):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 25
        draw_girl_legs(d, 32, 40, (-3, -2), (3, -2))
        draw_girl_torso(d, cx, cy + 2, arm_pose="up")
        draw_girl_head(d, cx, cy - 8, mouth="open", hair_blow=3)
        frames.append(im)
    return frames


def gen_land():
    frames = []
    # Frame 0: squat
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    draw_girl_legs(d0, 32, 42, (-2, 1), (2, 1))
    draw_girl_torso(d0, 32, 30, arm_pose="down")
    draw_girl_head(d0, 32, 20, mouth="smile")
    frames.append(im0)

    # Frame 1: recover
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    draw_girl_legs(d1, 32, 40)
    draw_girl_torso(d1, 32, 28, arm_pose="down")
    draw_girl_head(d1, 32, 18, mouth="smile")
    frames.append(im1)
    return frames


def gen_kiss():
    """Sweet romantic kiss: leaning forward, pouted lips, rosy blush, floating hearts!"""
    frames = []
    kiss_data = [
        (2, "smile", True,  None, 0),
        (4, "kiss",  True,  -8,   4),
        (5, "kiss",  True,  -14,  6),
        (3, "smile", True,  -20,  5),
    ]
    for i, (lx, mouth, blush, hy, hsize) in enumerate(kiss_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32 + lx, 26

        draw_girl_legs(d, 32, 40, (0, 0), (lx, 0))
        draw_girl_torso(d, cx, cy + 2, arm_pose="down")

        if hy is not None:
            draw_heart(d, cx + 8, cy + hy, size=hsize)

        draw_girl_head(d, cx, cy - 8, blink=True, blush=blush, mouth=mouth, hair_blow=-2)
        frames.append(im)
    return frames


def gen_blush():
    """Giggling / blowing kiss with heart floating up"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 26

        draw_girl_legs(d, 32, 40)
        draw_girl_torso(d, cx, cy + 2, arm_pose="down")

        # Hand blowing kiss
        d.line([(cx + 4, cy + 6), (cx + 9, cy + 1)], fill=C_SKIN, width=2)
        d.point([(cx + 8, cy + 3)], fill=C_RED_BRACELET)
        draw_heart(d, cx + 12 + i * 2, cy - 2 - i * 3, size=4)

        draw_girl_head(d, cx, cy - 8, blink=(i % 2 == 1), blush=True,
                       mouth="kiss" if i == 0 else "smile")
        frames.append(im)
    return frames


def gen_climb():
    """Climbing wall/border"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 26 + (1 if i % 2 == 0 else -1)

        draw_girl_legs(d, 32, 40, (-1, -2 if i % 2 == 0 else 2), (2, 2 if i % 2 == 0 else -2))
        draw_girl_torso(d, cx, cy + 2, arm_pose="up")
        draw_girl_head(d, cx, cy - 8, mouth="smile")
        frames.append(im)
    return frames


def gen_dragged():
    """Being carried by mouse: wide surprised 'o' expression just like photo!"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 26

        draw_girl_legs(d, 32, 40, (-2 if i % 2 == 0 else 2, -2), (2 if i % 2 == 0 else -2, 1))
        draw_girl_torso(d, cx, cy + 2, arm_pose="up")
        draw_girl_head(d, cx, cy - 8, blink=False, blush=True, mouth="open", hair_blow=3)
        frames.append(im)
    return frames


def gen_sleep():
    """Resting peacefully"""
    frames = []
    for i in range(3):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 32

        # Sitting comfortably
        d.rectangle([cx - 5, cy + 6, cx + 5, cy + 9], fill=C_JEANS)
        d.rectangle([cx - 7, cy + 8, cx - 4, cy + 11], fill=C_SNEAKER)
        d.rectangle([cx + 4, cy + 8, cx + 7, cy + 11], fill=C_SNEAKER)

        draw_girl_torso(d, cx, cy - 2, arm_pose="down")
        draw_girl_head(d, cx, cy - 10, blink=True, blush=True, mouth="smile")

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

    print(f"Girl sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_piratess_sprites()
