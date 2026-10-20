"""
Pixel-art sprite generator for Desktop Pirate.
Generates all pirate animation frames with high detail, transparency, and personality.
"""

import os
from PIL import Image, ImageDraw

# Color Palette (Rich retro pirate colors)
C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (25, 20, 20, 255)
C_WHITE       = (245, 245, 245, 255)
C_SKIN        = (240, 192, 148, 255)
C_SKIN_SHADOW = (205, 153, 110, 255)
C_BEARD       = (75, 45, 25, 255)
C_BEARD_LIGHT = (110, 68, 38, 255)
C_HAT         = (32, 28, 36, 255)
C_HAT_GOLD    = (235, 185, 45, 255)
C_FEATHER     = (220, 40, 40, 255)
C_SHIRT_RED   = (210, 45, 45, 255)
C_SHIRT_WHITE = (235, 235, 230, 255)
C_VEST        = (58, 38, 28, 255)
C_VEST_LIGHT  = (85, 56, 42, 255)
C_BELT        = (35, 25, 20, 255)
C_BUCKLE      = (245, 210, 60, 255)
C_PANTS       = (35, 60, 110, 255)
C_BOOT        = (40, 28, 22, 255)
C_WOOD        = (150, 95, 45, 255)
C_WOOD_TIP    = (90, 55, 25, 255)
C_STEEL       = (200, 210, 225, 255)
C_STEEL_DARK  = (130, 145, 160, 255)
C_GOLD        = (255, 215, 0, 255)
C_GOLD_SHADOW = (200, 160, 0, 255)
C_PARROT_GRN  = (40, 180, 60, 255)
C_PARROT_RED  = (230, 40, 40, 255)
C_PARROT_YEL  = (250, 210, 30, 255)
C_SLASH       = (240, 245, 255, 200)

FRAME_SIZE = 64  # Base frame 64x64 pixels


def create_blank():
    return Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE), C_TRANSPARENT)


def draw_hat(d: ImageDraw.ImageDraw, hx, hy, tilt=0):
    """Draw pirate tricorn hat with golden trim and skull/crossbones"""
    # Hat brim base
    d.polygon([
        (hx - 14, hy + 4),
        (hx - 18, hy - 2),
        (hx - 12, hy - 4),
        (hx, hy - 7),
        (hx + 12, hy - 4),
        (hx + 18, hy - 2),
        (hx + 14, hy + 4),
        (hx, hy + 2)
    ], fill=C_HAT)
    
    # Gold trim along hat crest
    d.line([(hx - 17, hy - 2), (hx - 11, hy - 4), (hx, hy - 7), (hx + 11, hy - 4), (hx + 17, hy - 2)], fill=C_HAT_GOLD, width=1)
    
    # Red feather on left
    d.line([(hx - 8, hy - 5), (hx - 14, hy - 11), (hx - 16, hy - 15)], fill=C_FEATHER, width=2)
    d.point([(hx - 17, hy - 16), (hx - 15, hy - 17)], fill=C_FEATHER)

    # Mini skull / jolly roger center
    d.rectangle([hx - 2, hy - 3, hx + 2, hy - 1], fill=C_WHITE)
    d.point([(hx - 1, hy - 2), (hx + 1, hy - 2)], fill=C_BLACK)
    d.point([(hx, hy)], fill=C_WHITE)


def draw_head(d: ImageDraw.ImageDraw, hx, hy, blink=False, eye_dir=0, mouth="neutral"):
    """Draw pirate face: skin, eye patch, working eye, bushy beard & mustache"""
    # Head skin
    d.rectangle([hx - 6, hy, hx + 6, hy + 8], fill=C_SKIN)
    d.point([(hx - 6, hy), (hx + 6, hy), (hx - 6, hy + 8), (hx + 6, hy + 8)], fill=C_SKIN_SHADOW)
    
    # Nose
    d.rectangle([hx - 1, hy + 3, hx + 1, hy + 4], fill=C_SKIN_SHADOW)

    # Left eye: Eye patch (black strap and patch)
    d.line([(hx - 7, hy + 1), (hx + 6, hy + 4)], fill=C_BLACK, width=1)
    d.rectangle([hx - 4, hy + 2, hx - 2, hy + 4], fill=C_BLACK)

    # Right eye: Living eye
    if blink:
        d.line([(hx + 2, hy + 3), (hx + 4, hy + 3)], fill=C_BLACK, width=1)
    else:
        d.rectangle([hx + 2, hy + 2, hx + 4, hy + 4], fill=C_WHITE)
        pupil_x = hx + 3 + eye_dir
        pupil_x = max(hx + 2, min(hx + 4, pupil_x))
        d.point([(pupil_x, hy + 3)], fill=C_BLACK)
    
    # Eyebrows (thick, bushy pirate brows)
    d.line([(hx - 5, hy + 1), (hx - 2, hy + 1)], fill=C_BEARD, width=1)
    d.line([(hx + 2, hy + 1), (hx + 5, hy + 1)], fill=C_BEARD, width=1)

    # Bushy mustache & beard
    d.rectangle([hx - 6, hy + 5, hx + 6, hy + 6], fill=C_BEARD)
    d.line([(hx - 5, hy + 5), (hx + 5, hy + 5)], fill=C_BEARD_LIGHT, width=1)
    
    # Full pirate beard hanging down
    d.polygon([
        (hx - 5, hy + 7),
        (hx + 5, hy + 7),
        (hx + 4, hy + 11),
        (hx, hy + 13),
        (hx - 4, hy + 11)
    ], fill=C_BEARD)
    d.line([(hx - 2, hy + 8), (hx, hy + 12), (hx + 2, hy + 8)], fill=C_BEARD_LIGHT, width=1)

    # Mouth
    if mouth == "smile":
        d.line([(hx - 1, hy + 6), (hx + 2, hy + 6)], fill=C_BLACK, width=1)
        d.point([(hx + 1, hy + 6)], fill=C_WHITE)  # Gold/white tooth
    elif mouth == "open":
        d.rectangle([hx - 1, hy + 6, hx + 2, hy + 7], fill=C_BLACK)
        d.point([(hx - 1, hy + 6)], fill=C_GOLD)   # Gold tooth!
    elif mouth == "shock":
        d.rectangle([hx, hy + 6, hx + 1, hy + 8], fill=C_BLACK)


def draw_torso(d: ImageDraw.ImageDraw, tx, ty, width=14, height=14):
    """Draw pirate sailor shirt (red & white stripes) with open dark captain vest"""
    # Base red/white striped shirt
    for i in range(height):
        strip_col = C_SHIRT_RED if (i // 2) % 2 == 0 else C_SHIRT_WHITE
        d.line([(tx - width // 2, ty + i), (tx + width // 2, ty + i)], fill=strip_col, width=1)
    
    # Open captain leather vest on sides
    vest_w = 3
    d.rectangle([tx - width // 2, ty, tx - width // 2 + vest_w, ty + height - 3], fill=C_VEST)
    d.rectangle([tx + width // 2 - vest_w, ty, tx + width // 2, ty + height - 3], fill=C_VEST)
    d.line([(tx - width // 2 + 1, ty), (tx - width // 2 + 1, ty + height - 3)], fill=C_VEST_LIGHT, width=1)
    d.line([(tx + width // 2 - 1, ty), (tx + width // 2 - 1, ty + height - 3)], fill=C_VEST_LIGHT, width=1)

    # Wide pirate leather belt & gold buckle
    belt_y = ty + height - 3
    d.rectangle([tx - width // 2, belt_y, tx + width // 2, belt_y + 3], fill=C_BELT)
    # Shiny gold buckle in the center
    d.rectangle([tx - 2, belt_y, tx + 2, belt_y + 3], fill=C_BUCKLE)
    d.point([(tx, belt_y + 1)], fill=C_BELT)


def draw_parrot(d: ImageDraw.ImageDraw, px, py, flap=False):
    """Cute tropical parrot sitting on pirate's shoulder"""
    # Body (green)
    d.rectangle([px - 2, py - 3, px + 2, py + 2], fill=C_PARROT_GRN)
    # Red head
    d.rectangle([px - 2, py - 6, px + 1, py - 3], fill=C_PARROT_RED)
    # Yellow beak
    d.point([(px - 3, py - 4), (px - 4, py - 4)], fill=C_PARROT_YEL)
    # Eye
    d.point([(px - 1, py - 5)], fill=C_BLACK)
    # Wing
    if flap:
        d.polygon([(px + 1, py - 3), (px + 4, py - 7), (px + 2, py)], fill=C_PARROT_YEL)
    else:
        d.polygon([(px, py - 1), (px + 3, py + 1), (px, py + 3)], fill=C_PARROT_YEL)
    # Tail
    d.line([(px, py + 2), (px + 1, py + 6)], fill=C_PARROT_RED, width=1)


def draw_cutlass(d: ImageDraw.ImageDraw, sx, sy, angle_mode="down"):
    """Draw curved pirate steel cutlass / saber"""
    # Golden guard & hilt
    d.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=C_BUCKLE)
    
    if angle_mode == "down":
        # Blade pointing down-right
        d.line([(sx, sy), (sx + 2, sy + 6), (sx + 4, sy + 11)], fill=C_STEEL, width=2)
        d.point([(sx + 5, sy + 10), (sx + 6, sy + 9)], fill=C_STEEL)  # Curved tip
        d.line([(sx + 1, sy + 1), (sx + 3, sy + 7)], fill=C_STEEL_DARK, width=1)
    elif angle_mode == "slash":
        # Blade swinging forward / horizontal
        d.line([(sx, sy), (sx + 7, sy - 2), (sx + 14, sy - 1)], fill=C_STEEL, width=2)
        d.point([(sx + 14, sy - 2), (sx + 15, sy - 3)], fill=C_STEEL)
    elif angle_mode == "up":
        # Blade held triumphantly up
        d.line([(sx, sy), (sx + 2, sy - 7), (sx + 3, sy - 13)], fill=C_STEEL, width=2)
        d.point([(sx + 4, sy - 14), (sx + 5, sy - 13)], fill=C_STEEL)


def draw_legs_and_feet(d: ImageDraw.ImageDraw, cx, cy, left_leg_offset=(0, 0), right_leg_offset=(0, 0), peg_is_right=True):
    """
    Draw left leg (normal leg with pirate boot) and right leg (wooden peg leg!).
    Offsets allow walk, run, jump, and climb animations.
    """
    # Left leg (sailor blue pants + boot)
    lx = cx - 4 + left_leg_offset[0]
    ly = cy + left_leg_offset[1]
    # Pants
    d.rectangle([lx - 2, ly, lx + 1, ly + 6], fill=C_PANTS)
    # Black leather boot with cuff
    d.rectangle([lx - 2, ly + 6, lx + 2, ly + 10], fill=C_BOOT)
    d.line([(lx - 3, ly + 9), (lx + 2, ly + 9)], fill=C_BLACK, width=1)  # Boot sole

    # Right leg (wooden peg leg!)
    rx = cx + 4 + right_leg_offset[0]
    ry = cy + right_leg_offset[1]
    if peg_is_right:
        # Pants cuff
        d.rectangle([rx - 2, ry, rx + 1, ry + 3], fill=C_PANTS)
        # Wooden peg tapering down to point
        d.polygon([(rx - 1, ry + 3), (rx + 1, ry + 3), (rx, ry + 10)], fill=C_WOOD)
        d.point([(rx, ry + 10)], fill=C_WOOD_TIP)  # Metal tip on peg leg
    else:
        # Both boots if needed
        d.rectangle([rx - 2, ry, rx + 1, ry + 6], fill=C_PANTS)
        d.rectangle([rx - 2, ry + 6, rx + 2, ry + 10], fill=C_BOOT)


# =========================================================================
# ANIMATION FRAMES BUILDERS
# =========================================================================

def generate_idle_frames():
    frames = []
    # 4 frames idle: slight breathing bob, eye blink on frame 2, parrot flap on frame 3
    bobs = [0, -1, 0, 1]
    for i, bob in enumerate(bobs):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28 + bob

        # Parrot on left shoulder
        draw_parrot(d, cx - 8, cy + 2, flap=(i == 3))

        # Legs (planted firmly on ground, ground is around y=56)
        draw_legs_and_feet(d, 32, 44, left_leg_offset=(0, 0), right_leg_offset=(0, 0))

        # Torso
        draw_torso(d, cx, cy + 5)

        # Cutlass at side
        draw_cutlass(d, cx + 7, cy + 10, angle_mode="down")

        # Head & Hat
        blink = (i == 2)
        draw_head(d, cx, cy - 8, blink=blink, mouth="smile" if i == 0 else "neutral")
        draw_hat(d, cx, cy - 10)

        frames.append(im)
    return frames


def generate_walk_frames():
    frames = []
    # 6 frames walking cycle with distinctive peg-leg clack and limp!
    # Frame 0: Left boot steps forward
    # Frame 1: Body lifts up as weight moves onto boot
    # Frame 2: Peg leg swings forward
    # Frame 3: Peg leg strikes ground with distinct sharp impact
    # Frame 4: Push off peg leg
    # Frame 5: Return swing
    walk_data = [
        # (bob, left_leg_dx, left_leg_dy, right_leg_dx, right_leg_dy, saber_angle)
        ( 0,  3,  0, -3, -2, "down"),
        (-2,  1, -1, -2, -1, "down"),
        (-1, -2,  0,  1, -2, "down"),
        ( 1, -3,  0,  3,  0, "slash"),  # Peg leg strikes
        ( 0, -1, -2,  1,  0, "down"),
        (-1,  1, -1, -1, -1, "down"),
    ]

    for i, (bob, ldx, ldy, rdx, rdy, s_angle) in enumerate(walk_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28 + bob

        # Parrot
        draw_parrot(d, cx - 8, cy + 2, flap=(i % 2 == 1))

        # Legs
        draw_legs_and_feet(d, 32, 44, left_leg_offset=(ldx, ldy), right_leg_offset=(rdx, rdy))

        # Torso
        draw_torso(d, cx, cy + 5)

        # Cutlass swinging with stride
        draw_cutlass(d, cx + 7, cy + 10, angle_mode=s_angle)

        # Head & Hat
        draw_head(d, cx, cy - 8, blink=False, mouth="smile" if (i % 2 == 0) else "neutral")
        draw_hat(d, cx, cy - 10)

        frames.append(im)
    return frames


def generate_run_frames():
    frames = []
    # 4 fast frames running
    run_data = [
        (-2,  5, -2, -5, -4),
        ( 1,  2,  0, -2, -1),
        (-2, -5, -4,  5, -2),
        ( 1, -2, -1,  2,  0),
    ]
    for i, (bob, ldx, ldy, rdx, rdy) in enumerate(run_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 34, 28 + bob  # Leaning slightly forward

        draw_parrot(d, cx - 8, cy + 2, flap=True)
        draw_legs_and_feet(d, 32, 44, left_leg_offset=(ldx, ldy), right_leg_offset=(rdx, rdy))
        draw_torso(d, cx, cy + 5)
        draw_cutlass(d, cx + 8, cy + 8, angle_mode="slash")
        draw_head(d, cx, cy - 8, mouth="open")
        draw_hat(d, cx - 1, cy - 10)

        frames.append(im)
    return frames


def generate_jump_frames():
    frames = []
    # Frame 0: Rising up, arms and cutlass thrust up
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    cx, cy = 32, 24
    draw_parrot(d0, cx - 8, cy, flap=True)
    draw_legs_and_feet(d0, 32, 44, left_leg_offset=(-2, -4), right_leg_offset=(2, -5))
    draw_torso(d0, cx, cy + 5)
    draw_cutlass(d0, cx + 8, cy + 2, angle_mode="up")
    draw_head(d0, cx, cy - 8, mouth="open")
    draw_hat(d0, cx, cy - 11)
    frames.append(im0)

    # Frame 1: Peak of jump
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    cx, cy = 32, 22
    draw_parrot(d1, cx - 8, cy - 2, flap=True)
    draw_legs_and_feet(d1, 32, 44, left_leg_offset=(-3, -6), right_leg_offset=(3, -6))
    draw_torso(d1, cx, cy + 5)
    draw_cutlass(d1, cx + 8, cy + 1, angle_mode="up")
    draw_head(d1, cx, cy - 8, mouth="smile")
    draw_hat(d1, cx, cy - 12)
    frames.append(im1)

    return frames


def generate_fall_frames():
    frames = []
    # 2 frames falling: flailing, hat slightly detached/flying up
    for i, flap in enumerate([False, True]):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 27

        draw_parrot(d, cx - 9, cy - 2, flap=True)
        # Legs flailing outwards
        draw_legs_and_feet(d, 32, 43, left_leg_offset=(-5, -3 if flap else -1), right_leg_offset=(5, -1 if flap else -3))
        draw_torso(d, cx, cy + 4)
        draw_cutlass(d, cx + 9, cy + 6, angle_mode="slash" if flap else "down")
        draw_head(d, cx, cy - 8, mouth="shock")
        # Hat floating slightly above head
        draw_hat(d, cx + (1 if flap else -1), cy - 13)
        frames.append(im)
    return frames


def generate_land_frames():
    frames = []
    # Frame 0: Squashed impact
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    cx, cy = 32, 34  # Squashed down
    draw_parrot(d0, cx - 8, cy + 2, flap=False)
    draw_legs_and_feet(d0, 32, 46, left_leg_offset=(-4, 1), right_leg_offset=(4, 1))
    draw_torso(d0, cx, cy + 4, width=16, height=11)
    draw_cutlass(d0, cx + 8, cy + 11, angle_mode="down")
    draw_head(d0, cx, cy - 7, mouth="shock")
    draw_hat(d0, cx, cy - 8)
    frames.append(im0)

    # Frame 1: Recovering
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    cx, cy = 32, 30
    draw_parrot(d1, cx - 8, cy + 2, flap=False)
    draw_legs_and_feet(d1, 32, 44, left_leg_offset=(-2, 0), right_leg_offset=(2, 0))
    draw_torso(d1, cx, cy + 5)
    draw_cutlass(d1, cx + 7, cy + 10, angle_mode="down")
    draw_head(d1, cx, cy - 8, mouth="smile")
    draw_hat(d1, cx, cy - 10)
    frames.append(im1)

    return frames


def generate_climb_wall_frames():
    """Climbing up/down the monitor edge like rigging on a ship"""
    frames = []
    # 4 frames climbing
    steps = [
        (0, -2, 2, -3),
        (-2, 2, -1, 1),
        (0, 3, -3, 2),
        (2, -1, 1, -2),
    ]
    for i, (bob, ldy, rdy, hand_y) in enumerate(steps):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28 + bob

        draw_parrot(d, cx - 7, cy + 2, flap=(i % 2 == 1))
        # Reaching legs against vertical wall
        draw_legs_and_feet(d, 32, 44, left_leg_offset=(-1, ldy), right_leg_offset=(3, rdy))
        draw_torso(d, cx, cy + 5)
        # Reaching arm/hand holding rope
        d.rectangle([cx + 6, cy + 4 + hand_y, cx + 11, cy + 6 + hand_y], fill=C_SKIN)
        # Cutlass sheathed or held in mouth/teeth!
        d.line([(cx - 7, cy + 1), (cx + 8, cy + 1)], fill=C_STEEL, width=2)
        d.point([(cx + 9, cy), (cx + 10, cy - 1)], fill=C_STEEL)  # Tip
        d.point([(cx - 8, cy + 1)], fill=C_BUCKLE)

        # Head looking up
        draw_head(d, cx, cy - 8, mouth="smile")
        draw_hat(d, cx, cy - 11)

        frames.append(im)
    return frames


def generate_climb_ceiling_frames():
    """Hanging and crawling upside-down across the top of screen"""
    frames = []
    # 4 frames hanging upside down by boots/hands
    for i in range(4):
        # We can take a climb frame and rotate or draw upside down
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 34  # Head down, feet up

        # Boots reaching up to ceiling (y ~ 10)
        leg_offset = 2 if i % 2 == 0 else -2
        # Feet grabbing top edge
        d.rectangle([cx - 5 + leg_offset, 12, cx - 1 + leg_offset, 16], fill=C_BOOT)
        d.polygon([(cx + 3 - leg_offset, 12), (cx + 5 - leg_offset, 12), (cx + 4 - leg_offset, 17)], fill=C_WOOD)
        # Pants
        d.rectangle([cx - 5 + leg_offset, 16, cx - 1 + leg_offset, 22], fill=C_PANTS)
        d.rectangle([cx + 2 - leg_offset, 17, cx + 5 - leg_offset, 22], fill=C_PANTS)

        # Torso upside down
        draw_torso(d, cx, 23, width=14, height=12)

        # Cutlass swinging down
        draw_cutlass(d, cx + 7, 30, angle_mode="down")

        # Head upside down or tilted looking down
        draw_head(d, cx, 36, mouth="open" if i % 2 == 0 else "smile")
        draw_hat(d, cx, 44)

        frames.append(im)
    return frames


def generate_dragged_frames():
    frames = []
    # 4 frames when user drags the pirate with mouse cursor:
    # Pirate is suspended by the collar/hat, kicking and protesting comically!
    kick_data = [
        (-4, -2, 4, 1, "shock"),
        (-2, 1, 3, -3, "open"),
        (3, -3, -3, 0, "shock"),
        (4, 0, -4, -2, "open"),
    ]
    for i, (ldx, ldy, rdx, rdy, mouth) in enumerate(kick_data):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 28

        # Parrot flying panicked above pirate
        draw_parrot(d, cx - 10, cy - 8, flap=True)

        # Dangling legs kicking wildly
        draw_legs_and_feet(d, 32, 44, left_leg_offset=(ldx, ldy), right_leg_offset=(rdx, rdy))

        # Stretched torso
        draw_torso(d, cx, cy + 5, width=13, height=15)

        # Cutlass waving frantically
        draw_cutlass(d, cx + 9, cy + 7, angle_mode="slash" if i % 2 == 0 else "up")

        # Head pulled upward
        draw_head(d, cx, cy - 8, mouth=mouth)
        # Hat pulled from above (like by cursor collar)
        draw_hat(d, cx, cy - 11)

        frames.append(im)
    return frames


def generate_attack_frames():
    frames = []
    # 4 frames: Cutlass slash attack animation with sword swoosh effect!
    # Frame 0: Windup
    im0 = create_blank()
    d0 = ImageDraw.Draw(im0)
    cx, cy = 30, 28
    draw_parrot(d0, cx - 8, cy + 2, flap=False)
    draw_legs_and_feet(d0, 32, 44, left_leg_offset=(-3, 0), right_leg_offset=(3, 0))
    draw_torso(d0, cx, cy + 5)
    draw_cutlass(d0, cx - 6, cy + 4, angle_mode="up")  # Cocked back
    draw_head(d0, cx, cy - 8, mouth="smile")
    draw_hat(d0, cx, cy - 10)
    frames.append(im0)

    # Frame 1: Forward Slash with white blade arc!
    im1 = create_blank()
    d1 = ImageDraw.Draw(im1)
    cx, cy = 34, 29
    draw_parrot(d1, cx - 8, cy + 2, flap=True)
    draw_legs_and_feet(d1, 32, 44, left_leg_offset=(-2, 0), right_leg_offset=(4, 0))
    draw_torso(d1, cx, cy + 5)
    draw_cutlass(d1, cx + 8, cy + 6, angle_mode="slash")
    # Swoosh arc
    d1.arc([cx + 4, cy - 8, cx + 26, cy + 18], start=280, end=70, fill=C_SLASH, width=3)
    draw_head(d1, cx, cy - 8, mouth="open")
    draw_hat(d1, cx, cy - 10)
    frames.append(im1)

    # Frame 2: Slash follow-through
    im2 = create_blank()
    d2 = ImageDraw.Draw(im2)
    cx, cy = 35, 29
    draw_parrot(d2, cx - 8, cy + 2, flap=True)
    draw_legs_and_feet(d2, 32, 44, left_leg_offset=(-2, 0), right_leg_offset=(4, 0))
    draw_torso(d2, cx, cy + 5)
    draw_cutlass(d2, cx + 10, cy + 9, angle_mode="slash")
    d2.arc([cx + 6, cy - 6, cx + 28, cy + 16], start=310, end=90, fill=C_SLASH, width=2)
    draw_head(d2, cx, cy - 8, mouth="open")
    draw_hat(d2, cx, cy - 10)
    frames.append(im2)

    # Frame 3: Recovery
    im3 = create_blank()
    d3 = ImageDraw.Draw(im3)
    cx, cy = 32, 28
    draw_parrot(d3, cx - 8, cy + 2, flap=False)
    draw_legs_and_feet(d3, 32, 44, left_leg_offset=(-1, 0), right_leg_offset=(2, 0))
    draw_torso(d3, cx, cy + 5)
    draw_cutlass(d3, cx + 7, cy + 8, angle_mode="down")
    draw_head(d3, cx, cy - 8, mouth="smile")
    draw_hat(d3, cx, cy - 10)
    frames.append(im3)

    return frames


def generate_celebrate_frames():
    """Pirate cheering with gold coin / bottle of rum!"""
    frames = []
    for i in range(4):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 26 + (0 if i % 2 == 0 else -2)

        draw_parrot(d, cx - 8, cy + 2, flap=True)
        draw_legs_and_feet(d, 32, 44, left_leg_offset=(-2, 0), right_leg_offset=(2, 0))
        draw_torso(d, cx, cy + 5)

        # Hand holding shiny golden treasure coin up high!
        coin_y = cy - 6 if i % 2 == 0 else cy - 9
        d.ellipse([cx + 8, coin_y, cx + 16, coin_y + 8], fill=C_GOLD, outline=C_GOLD_SHADOW)
        d.point([(cx + 12, coin_y + 3), (cx + 12, coin_y + 4)], fill=C_WHITE)  # Sparkle

        # Arm reaching up
        d.line([(cx + 5, cy + 7), (cx + 10, coin_y + 6)], fill=C_SKIN, width=2)

        # Head looking up at gold
        draw_head(d, cx, cy - 8, mouth="open")
        draw_hat(d, cx, cy - 10)

        frames.append(im)
    return frames


def generate_sleep_frames():
    """Sitting down, snoozing with Zzz bubbles"""
    frames = []
    for i in range(3):
        im = create_blank()
        d = ImageDraw.Draw(im)
        cx, cy = 32, 36  # Sitting low

        # Parrot sleeping on shoulder with head tucked
        d.rectangle([cx - 8, cy - 2, cx - 4, cy + 3], fill=C_PARROT_GRN)
        d.point([(cx - 7, cy - 3), (cx - 6, cy - 3)], fill=C_PARROT_RED)

        # Legs stretched out sitting on floor
        d.rectangle([cx - 8, cy + 10, cx + 8, cy + 14], fill=C_PANTS)
        d.rectangle([cx - 10, cy + 10, cx - 8, cy + 14], fill=C_BOOT)
        d.point([(cx + 9, cy + 12), (cx + 10, cy + 12)], fill=C_WOOD)

        # Slumped torso
        draw_torso(d, cx, cy, width=14, height=12)

        # Cutlass resting on floor
        d.line([(cx - 12, cy + 13), (cx + 2, cy + 13)], fill=C_STEEL, width=2)
        d.point([(cx + 3, cy + 12)], fill=C_STEEL)

        # Head nodding down (hat pulled over eyes)
        draw_head(d, cx, cy - 8, blink=True, mouth="neutral")
        draw_hat(d, cx, cy - 7)  # Hat tilted down over eyes

        # "Zzz" floating up
        z_y = cy - 14 - (i * 2)
        d.text((cx + 10, z_y), "z", fill=C_WHITE)
        if i >= 1:
            d.text((cx + 14, z_y - 5), "Z", fill=C_WHITE)
        if i >= 2:
            d.text((cx + 18, z_y - 10), "Z", fill=C_HAT_GOLD)

        frames.append(im)
    return frames


def generate_all_sprites(output_dir="assets/sprites"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "idle": generate_idle_frames(),
        "walk": generate_walk_frames(),
        "run": generate_run_frames(),
        "jump": generate_jump_frames(),
        "fall": generate_fall_frames(),
        "land": generate_land_frames(),
        "climb_wall": generate_climb_wall_frames(),
        "climb_ceiling": generate_climb_ceiling_frames(),
        "dragged": generate_dragged_frames(),
        "attack": generate_attack_frames(),
        "celebrate": generate_celebrate_frames(),
        "sleep": generate_sleep_frames(),
    }

    saved_info = {}
    for anim_name, frames in animations.items():
        saved_info[anim_name] = []
        for idx, frame in enumerate(frames):
            # Save normal (facing right)
            filename_right = f"{anim_name}_right_{idx}.png"
            path_right = os.path.join(output_dir, filename_right)
            frame.save(path_right)

            # Save flipped (facing left)
            frame_left = frame.transpose(Image.FLIP_LEFT_RIGHT)
            filename_left = f"{anim_name}_left_{idx}.png"
            path_left = os.path.join(output_dir, filename_left)
            frame_left.save(path_left)

            saved_info[anim_name].append({
                "right": path_right,
                "left": path_left
            })

    print(f"Successfully generated {len(animations)} animation sets in {output_dir}!")
    return saved_info


if __name__ == "__main__":
    generate_all_sprites()

