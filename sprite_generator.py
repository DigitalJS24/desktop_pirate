"""
High-Definition Smooth Cartoon Sprite Generator for the Pirate Captain.
Renders smooth anti-aliased 256x256 frames (via 512x512 Lanczos supersampling):
- Tricorn captain hat with curved gold trim, skull emblem, and crimson plume
- Weathered captain face with eye patch, bushy eyebrows, and curled mustache
- Full rich pirate beard with braided highlights
- Crimson velvet pirate coat with gold frogging and brass buttons
- Classic peg leg (wooden with brass collar & iron ferrule) and tall pirate boot
- Steel cutlass with golden basket hilt
"""

import os
import math
from PIL import Image, ImageDraw

OUTPUT_SIZE = 256
RENDER_SIZE = 512

# HD Palette
C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (22, 20, 26, 255)
C_WHITE       = (255, 255, 255, 255)

C_SKIN        = (246, 196, 156, 255)
C_SKIN_SHADOW = (212, 158, 118, 255)
C_BEARD       = (68, 38, 22, 255)
C_BEARD_LIGHT = (98, 58, 34, 255)

C_HAT         = (32, 26, 36, 255)
C_HAT_GOLD    = (245, 195, 55, 255)
C_FEATHER     = (225, 45, 45, 255)

C_COAT        = (185, 35, 45, 255)
C_COAT_DARK   = (135, 22, 30, 255)
C_SHIRT       = (248, 245, 238, 255)
C_BELT        = (45, 30, 22, 255)
C_BUCKLE      = (255, 215, 60, 255)
C_PANTS       = (40, 65, 115, 255)

C_BOOT        = (52, 34, 26, 255)
C_BOOT_FOLD   = (75, 48, 38, 255)
C_WOOD        = (165, 105, 55, 255)
C_STEEL       = (215, 225, 238, 255)
C_STEEL_DARK  = (145, 158, 175, 255)


def create_canvas():
    return Image.new("RGBA", (RENDER_SIZE, RENDER_SIZE), C_TRANSPARENT)


def finalize_frame(im: Image.Image) -> Image.Image:
    return im.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)


def draw_pirate_captain(d: ImageDraw.ImageDraw, cx=256, cy=245,
                        leg_l_off=(0, 0), leg_r_off=(0, 0),
                        arm_pose="down", mouth="smirk", eye_blink=False,
                        hat_tilt=0, lean_x=0):
    hx = cx + lean_x
    hy = cy - 110

    # =========================================================================
    # 1. LEGS (Boot on Left, Peg Leg on Right)
    # =========================================================================
    jy = cy + 45
    d.rectangle([cx - 45, jy, cx + 45, jy + 25], fill=C_PANTS)

    # Left Leg: Tall Leather Boot
    lx = cx - 25 + leg_l_off[0] * 3
    ly = jy + 18 + leg_l_off[1] * 3
    d.polygon([(lx - 18, ly), (lx + 12, ly), (lx + 10, ly + 95), (lx - 20, ly + 95)], fill=C_BOOT)
    d.rounded_rectangle([lx - 24, ly, lx + 16, ly + 32], radius=6, fill=C_BOOT_FOLD)
    d.rounded_rectangle([lx - 26, ly + 90, lx + 14, ly + 108], radius=6, fill=(35, 22, 16, 255)) # Foot

    # Right Leg: Peg Leg (Wooden peg + brass collar + iron tip)
    rx = cx + 25 + leg_r_off[0] * 3
    ry = jy + 18 + leg_r_off[1] * 3
    d.polygon([(rx - 14, ry), (rx + 14, ry), (rx + 10, ry + 22), (rx - 10, ry + 22)], fill=C_PANTS)
    # Brass knee collar
    d.rounded_rectangle([rx - 10, ry + 20, rx + 10, ry + 32], radius=4, fill=C_HAT_GOLD)
    # Wooden peg
    d.polygon([(rx - 5, ry + 32), (rx + 5, ry + 32), (rx + 3, ry + 100), (rx - 3, ry + 100)], fill=C_WOOD)
    # Iron tip
    d.rounded_rectangle([rx - 4, ry + 98, rx + 4, ry + 108], radius=2, fill=(80, 85, 95, 255))

    # =========================================================================
    # 2. TORSO & PIRATE COAT
    # =========================================================================
    ty = hy + 65
    d.rounded_rectangle([hx - 54, ty, hx + 54, ty + 85], radius=14, fill=C_COAT)
    # White ruffled shirt center
    d.polygon([(hx - 22, ty), (hx + 22, ty), (hx, ty + 50)], fill=C_SHIRT)
    d.line([(hx, ty + 10), (hx, ty + 45)], fill=(210, 205, 195, 255), width=2) # shirt ruffle

    # Gold buttons & braid
    for by in [ty + 18, ty + 38, ty + 58]:
        d.ellipse([hx - 32, by - 5, hx - 22, by + 5], fill=C_HAT_GOLD)
        d.ellipse([hx + 22, by - 5, hx + 32, by + 5], fill=C_HAT_GOLD)
        d.line([(hx - 27, by), (hx - 12, by)], fill=C_HAT_GOLD, width=3)
        d.line([(hx + 12, by), (hx + 27, by)], fill=C_HAT_GOLD, width=3)

    # Belt & Large Golden Buckle
    d.rectangle([hx - 52, ty + 70, hx + 52, ty + 92], fill=C_BELT)
    d.rounded_rectangle([hx - 20, ty + 66, hx + 20, ty + 96], radius=4, outline=C_BUCKLE, width=5)

    # Cutlass / Saber on hip
    d.line([(hx + 42, ty + 40), (hx + 82, ty + 130)], fill=C_STEEL, width=7)
    d.line([(hx + 44, ty + 40), (hx + 80, ty + 125)], fill=C_WHITE, width=2) # highlight
    d.ellipse([hx + 36, ty + 34, hx + 52, ty + 50], fill=C_HAT_GOLD) # Basket hilt

    # Arms
    if arm_pose == "down":
        d.polygon([(hx - 52, ty + 8), (hx - 74, ty + 40), (hx - 58, ty + 48), (hx - 48, ty + 30)], fill=C_COAT)
        d.rounded_rectangle([hx - 70, ty + 44, hx - 52, ty + 115], radius=8, fill=C_COAT)
        d.rounded_rectangle([hx - 68, ty + 115, hx - 54, ty + 130], radius=5, fill=C_SKIN) # Hand

        d.polygon([(hx + 52, ty + 8), (hx + 74, ty + 40), (hx + 58, ty + 48), (hx + 48, ty + 30)], fill=C_COAT)
        d.rounded_rectangle([hx + 52, ty + 44, hx + 70, ty + 115], radius=8, fill=C_COAT)
        d.rounded_rectangle([hx + 54, ty + 115, hx + 68, ty + 130], radius=5, fill=C_SKIN) # Hand

    elif arm_pose == "cutlass_swing":
        # Left arm back
        d.rounded_rectangle([hx - 72, ty + 20, hx - 54, ty + 95], radius=8, fill=C_COAT)
        # Right arm swinging cutlass forward!
        d.line([(hx + 50, ty + 20), (hx + 105, ty - 20)], fill=C_COAT, width=16)
        d.line([(hx + 105, ty - 20), (hx + 160, ty - 60)], fill=C_STEEL, width=8) # Raised blade!
        d.ellipse([hx + 95, ty - 30, hx + 115, ty - 10], fill=C_HAT_GOLD)

    elif arm_pose == "up":
        # Cheering / climbing
        d.line([(hx - 54, ty + 20), (hx - 65, ty - 65)], fill=C_COAT, width=16)
        d.line([(hx + 54, ty + 20), (hx + 65, ty - 65)], fill=C_COAT, width=16)

    # =========================================================================
    # 3. HEAD & FACE
    # =========================================================================
    d.rounded_rectangle([hx - 36, hy - 25, hx + 36, hy + 45], radius=20, fill=C_SKIN)

    # Eye patch on left eye
    d.line([(hx - 36, hy - 5), (hx + 36, hy + 15)], fill=C_BLACK, width=3)
    d.ellipse([hx - 28, hy - 4, hx - 10, hy + 14], fill=C_BLACK)

    # Right eye
    if eye_blink:
        d.line([(hx + 10, hy + 5), (hx + 28, hy + 5)], fill=C_BLACK, width=3)
    else:
        d.ellipse([hx + 10, hy - 2, hx + 28, hy + 12], fill=C_WHITE)
        d.ellipse([hx + 14, hy, hx + 24, hy + 10], fill=(70, 95, 140, 255)) # Iris
        d.ellipse([hx + 17, hy + 3, hx + 21, hy + 7], fill=C_BLACK)
        d.ellipse([hx + 15, hy + 2, hx + 18, hy + 5], fill=C_WHITE) # Catchlight
        d.line([(hx + 8, hy - 8), (hx + 30, hy - 4)], fill=C_BEARD, width=5) # Bushy eyebrow

    # Nose
    d.polygon([(hx, hy + 8), (hx - 6, hy + 20), (hx + 6, hy + 20)], fill=C_SKIN_SHADOW)

    # Curled Mustache
    d.polygon([(hx, hy + 24), (hx - 36, hy + 28), (hx - 42, hy + 18), (hx - 20, hy + 22)], fill=C_BEARD)
    d.polygon([(hx, hy + 24), (hx + 36, hy + 28), (hx + 42, hy + 18), (hx + 20, hy + 22)], fill=C_BEARD)

    # Beard
    d.polygon([
        (hx - 35, hy + 25), (hx - 30, hy + 75),
        (hx, hy + 96),
        (hx + 30, hy + 75), (hx + 35, hy + 25)
    ], fill=C_BEARD)
    d.line([(hx - 15, hy + 42), (hx - 10, hy + 78)], fill=C_BEARD_LIGHT, width=3)
    d.line([(hx + 15, hy + 42), (hx + 10, hy + 78)], fill=C_BEARD_LIGHT, width=3)

    # =========================================================================
    # 4. TRICORN HAT WITH GOLD TRIM & PLUME
    # =========================================================================
    t = hat_tilt
    d.polygon([
        (hx - 80 + t, hy - 15),
        (hx - 95 + t, hy - 45),
        (hx - 60 + t, hy - 75),
        (hx + t, hy - 95),
        (hx + 60 + t, hy - 75),
        (hx + 95 + t, hy - 45),
        (hx + 80 + t, hy - 15),
        (hx + t, hy - 25)
    ], fill=C_HAT)
    d.line([
        (hx - 92 + t, hy - 43), (hx - 58 + t, hy - 73),
        (hx + t, hy - 93),
        (hx + 58 + t, hy - 73), (hx + 92 + t, hy - 43)
    ], fill=C_HAT_GOLD, width=5)

    # Crimson feather plume
    d.polygon([
        (hx - 30 + t, hy - 70), (hx - 70 + t, hy - 130),
        (hx - 100 + t, hy - 110), (hx - 55 + t, hy - 65)
    ], fill=C_FEATHER)

    # Skull brooch
    d.ellipse([hx - 8 + t, hy - 45, hx + 8 + t, hy - 32], fill=(245, 245, 245, 255))
    d.ellipse([hx - 4 + t, hy - 41, hx - 1 + t, hy - 37], fill=C_BLACK)
    d.ellipse([hx + 1 + t, hy - 41, hx + 4 + t, hy - 37], fill=C_BLACK)


# =========================================================================
# ANIMATION SETS
# =========================================================================

def gen_idle():
    frames = []
    bobs = [0, -2, 0, 2]
    for i, bob in enumerate(bobs):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256, cy=245 + bob, eye_blink=(i == 2))
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
        draw_pirate_captain(d, cx=256, cy=245 + bob,
                            leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                            hat_tilt=(-2 if i % 2 == 0 else 2))
        frames.append(finalize_frame(im))
    return frames


def gen_run():
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
        draw_pirate_captain(d, cx=256, cy=245 + bob,
                            leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                            arm_pose="cutlass_swing" if i % 2 == 0 else "down",
                            hat_tilt=-4)
        frames.append(finalize_frame(im))
    return frames


def gen_jump():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_pirate_captain(d0, cx=256, cy=220, leg_l_off=(-3, -5), leg_r_off=(3, -5), arm_pose="up", hat_tilt=-3)
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_pirate_captain(d1, cx=256, cy=200, leg_l_off=(-4, -8), leg_r_off=(4, -8), arm_pose="up", hat_tilt=-5)
    frames.append(finalize_frame(im1))
    return frames


def gen_fall():
    frames = []
    for i in range(2):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256, cy=235, leg_l_off=(-4, -2), leg_r_off=(4, -2), arm_pose="up", hat_tilt=3)
        frames.append(finalize_frame(im))
    return frames


def gen_land():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_pirate_captain(d0, cx=256, cy=260, leg_l_off=(-3, 2), leg_r_off=(3, 2), arm_pose="down")
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_pirate_captain(d1, cx=256, cy=245, arm_pose="down")
    frames.append(finalize_frame(im1))
    return frames


def gen_climb():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256, cy=245 + (2 if i % 2 == 0 else -2),
                            leg_l_off=(-2, -3 if i % 2 == 0 else 3),
                            leg_r_off=(3, 3 if i % 2 == 0 else -3),
                            arm_pose="up")
        frames.append(finalize_frame(im))
    return frames


def gen_dragged():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256, cy=245,
                            leg_l_off=(-3 if i % 2 == 0 else 3, -3),
                            leg_r_off=(3 if i % 2 == 0 else -3, 2),
                            arm_pose="up", hat_tilt=5)
        frames.append(finalize_frame(im))
    return frames


def gen_attack():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256 + (i * 4), cy=245, arm_pose="cutlass_swing")
        frames.append(finalize_frame(im))
    return frames


def gen_celebrate():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256, cy=245 - (i * 2), arm_pose="up", hat_tilt=(-4 if i % 2 == 0 else 4))
        frames.append(finalize_frame(im))
    return frames


def gen_sleep():
    frames = []
    for i in range(3):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_pirate_captain(d, cx=256, cy=265, eye_blink=True, hat_tilt=8)
        d.text((290, 80 - i * 10), "Z", fill=C_HAT_GOLD)
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

    print(f"HD Pirate Captain sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_sprites()
