"""
High-Definition Smooth Cartoon Sprite Generator for the Minions.
Renders smooth anti-aliased 256x256 frames (via 512x512 Lanczos supersampling):
- Iconic yellow capsule body with curved shading
- Polished silver goggles with glass reflections and black rubber strap
- Expressive brown eye with highlight catchlights
- Classic denim blue overalls with pocket and metal buttons
- Black gloves and shoes
- Bright yellow curved Banana (BANANA!)
"""

import os
from PIL import Image, ImageDraw

OUTPUT_SIZE = 256
RENDER_SIZE = 512

C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (22, 22, 26, 255)
C_WHITE       = (255, 255, 255, 255)

C_YELLOW      = (255, 220, 25, 255)
C_YELLOW_SHAD = (220, 180, 15, 255)
C_YELLOW_LGT  = (255, 238, 90, 255)

C_DENIM       = (45, 95, 165, 255)
C_DENIM_LGT   = (70, 125, 200, 255)
C_DENIM_DK    = (30, 65, 120, 255)

C_GOGGLES     = (200, 208, 218, 255)
C_GOGGLES_DK  = (140, 150, 162, 255)
C_STRAP       = (35, 35, 42, 255)
C_EYE_BROWN   = (125, 75, 40, 255)

C_GLOVE       = (32, 32, 38, 255)
C_BOOT        = (32, 32, 38, 255)

C_BANANA      = (255, 235, 30, 255)
C_BANANA_TIP  = (85, 140, 35, 255)


def create_canvas():
    return Image.new("RGBA", (RENDER_SIZE, RENDER_SIZE), C_TRANSPARENT)


def finalize_frame(im: Image.Image) -> Image.Image:
    return im.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)


def draw_banana(d: ImageDraw.ImageDraw, bx, by, angle="up"):
    if angle == "up":
        d.line([(bx, by + 30), (bx + 16, by + 5), (bx + 16, by - 25), (bx + 5, by - 45)], fill=C_BANANA, width=14)
        d.ellipse([bx + 2, by - 52, bx + 10, by - 42], fill=C_BANANA_TIP)
    elif angle == "forward":
        d.line([(bx - 20, by), (bx + 10, by - 15), (bx + 40, by - 10), (bx + 60, by + 15)], fill=C_BANANA, width=14)
        d.ellipse([bx + 58, by + 12, bx + 66, by + 22], fill=C_BANANA_TIP)


def draw_minion(d: ImageDraw.ImageDraw, cx=256, cy=245,
                leg_l_off=(0, 0), leg_r_off=(0, 0),
                arm_pose="banana", mouth="smile", eye_blink=False, bob=0):
    mx = cx
    my = cy + bob

    # 1. Shoes & Legs
    lx = mx - 28 + leg_l_off[0] * 3
    ly = my + 70 + leg_l_off[1] * 3
    d.rounded_rectangle([lx - 12, ly, lx + 12, ly + 25], radius=6, fill=C_DENIM_DK)
    d.rounded_rectangle([lx - 18, ly + 20, lx + 14, ly + 36], radius=7, fill=C_BOOT)

    rx = mx + 28 + leg_r_off[0] * 3
    ry = my + 70 + leg_r_off[1] * 3
    d.rounded_rectangle([rx - 12, ry, rx + 12, ry + 25], radius=6, fill=C_DENIM_DK)
    d.rounded_rectangle([rx - 14, ry + 20, rx + 18, ry + 36], radius=7, fill=C_BOOT)

    # 2. Iconic Yellow Capsule Body
    # Top dome
    d.pieslice([mx - 65, my - 130, mx + 65, my], 180, 360, fill=C_YELLOW)
    # Middle cylinder
    d.rectangle([mx - 65, my - 65, mx + 65, my + 60], fill=C_YELLOW)
    # Bottom round
    d.pieslice([mx - 65, my - 10, mx + 65, my + 80], 0, 180, fill=C_YELLOW)

    # Hair sprouts on top!
    d.line([(mx - 15, my - 125), (mx - 25, my - 155)], fill=C_BLACK, width=4)
    d.line([(mx, my - 130), (mx, my - 165)], fill=C_BLACK, width=4)
    d.line([(mx + 15, my - 125), (mx + 25, my - 155)], fill=C_BLACK, width=4)

    # 3. Denim Overalls
    d.rounded_rectangle([mx - 64, my + 10, mx + 64, my + 75], radius=16, fill=C_DENIM)
    # Front bib
    d.rectangle([mx - 42, my - 15, mx + 42, my + 30], fill=C_DENIM)
    # Straps
    d.line([(mx - 60, my - 5), (mx - 38, my - 15)], fill=C_DENIM_DK, width=12)
    d.line([(mx + 60, my - 5), (mx + 38, my - 15)], fill=C_DENIM_DK, width=12)
    # Silver buttons on straps
    d.ellipse([mx - 44, my - 18, mx - 34, my - 8], fill=C_GOGGLES)
    d.ellipse([mx + 34, my - 18, mx + 44, my - 8], fill=C_GOGGLES)
    # Front pocket with 'G' logo circle
    d.rounded_rectangle([mx - 20, my + 15, mx + 20, my + 45], radius=6, outline=C_DENIM_DK, width=3)
    d.ellipse([mx - 10, my + 22, mx + 10, my + 38], fill=C_BLACK)
    d.ellipse([mx - 6, my + 26, mx + 6, my + 34], fill=C_YELLOW)

    # 4. Goggles & Eye
    gy = my - 45
    # Black rubber strap
    d.rectangle([mx - 65, gy - 12, mx + 65, gy + 12], fill=C_STRAP)
    # Silver metal goggles outer rim
    d.ellipse([mx - 42, gy - 42, mx + 42, gy + 42], fill=C_GOGGLES)
    d.ellipse([mx - 34, gy - 34, mx + 34, gy + 34], fill=C_GOGGLES_DK)
    # Inner lens white
    d.ellipse([mx - 30, gy - 30, mx + 30, gy + 30], fill=C_WHITE)

    if eye_blink:
        d.line([(mx - 25, gy), (mx + 25, gy)], fill=C_BLACK, width=5)
    else:
        # Brown iris
        d.ellipse([mx - 18, gy - 18, mx + 18, gy + 18], fill=C_EYE_BROWN)
        # Black pupil
        d.ellipse([mx - 10, gy - 10, mx + 10, gy + 10], fill=C_BLACK)
        # Specular shine
        d.ellipse([mx - 12, gy - 14, mx - 4, gy - 6], fill=C_WHITE)
        d.point([(mx + 6, gy + 6)], fill=C_WHITE)

    # 5. Mouth
    if mouth == "banana":
        # Joyful open mouth shouting BANANA!
        d.pieslice([mx - 25, gy + 40, mx + 25, gy + 80], 0, 180, fill=(75, 20, 25, 255))
        d.ellipse([mx - 18, gy + 50, mx + 18, gy + 62], fill=C_WHITE) # Upper teeth
    elif mouth == "smile":
        d.arc([mx - 22, gy + 38, mx + 22, gy + 68], start=20, end=160, fill=C_BLACK, width=4)

    # 6. Arms & Banana
    if arm_pose == "banana":
        # Left arm holding banana up high!
        d.line([(mx - 55, my), (mx - 85, my - 45)], fill=C_YELLOW, width=16)
        d.ellipse([mx - 95, my - 55, mx - 75, my - 35], fill=C_GLOVE)
        draw_banana(d, mx - 85, my - 45, angle="up")
        # Right arm down
        d.line([(mx + 55, my), (mx + 75, my + 35)], fill=C_YELLOW, width=16)
        d.ellipse([mx + 68, my + 30, mx + 84, my + 46], fill=C_GLOVE)
    elif arm_pose == "celebrate":
        d.line([(mx - 55, my), (mx - 85, my - 55)], fill=C_YELLOW, width=16)
        d.ellipse([mx - 95, my - 65, mx - 75, my - 45], fill=C_GLOVE)
        d.line([(mx + 55, my), (mx + 85, my - 55)], fill=C_YELLOW, width=16)
        d.ellipse([mx + 75, my - 65, mx + 95, my - 45], fill=C_GLOVE)
        draw_banana(d, mx, my - 130, angle="forward")
    elif arm_pose == "down":
        d.line([(mx - 55, my), (mx - 75, my + 35)], fill=C_YELLOW, width=16)
        d.ellipse([mx - 84, my + 30, mx - 68, my + 46], fill=C_GLOVE)
        d.line([(mx + 55, my), (mx + 75, my + 35)], fill=C_YELLOW, width=16)
        d.ellipse([mx + 68, my + 30, mx + 84, my + 46], fill=C_GLOVE)


def gen_idle():
    frames = []
    bobs = [0, -2, 0, 2]
    for i, bob in enumerate(bobs):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=245 + bob, arm_pose="banana", mouth="smile", eye_blink=(i == 2))
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
        draw_minion(d, cx=256, cy=245 + bob,
                    leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                    arm_pose="banana", mouth="smile")
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
        draw_minion(d, cx=256, cy=245 + bob,
                    leg_l_off=(ldx, ldy), leg_r_off=(rdx, rdy),
                    arm_pose="celebrate", mouth="banana")
        frames.append(finalize_frame(im))
    return frames


def gen_banana():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=245 - (i * 3), arm_pose="banana", mouth="banana")
        frames.append(finalize_frame(im))
    return frames


def gen_celebrate():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=245 - (i * 4), arm_pose="celebrate", mouth="banana")
        frames.append(finalize_frame(im))
    return frames


def gen_jump():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_minion(d0, cx=256, cy=220, leg_l_off=(-3, -5), leg_r_off=(3, -5), arm_pose="celebrate", mouth="banana")
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_minion(d1, cx=256, cy=200, leg_l_off=(-4, -8), leg_r_off=(4, -8), arm_pose="celebrate", mouth="banana")
    frames.append(finalize_frame(im1))
    return frames


def gen_fall():
    frames = []
    for i in range(2):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=235, leg_l_off=(-4, -2), leg_r_off=(4, -2), arm_pose="celebrate", mouth="banana")
        frames.append(finalize_frame(im))
    return frames


def gen_land():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_minion(d0, cx=256, cy=260, leg_l_off=(-3, 2), leg_r_off=(3, 2), arm_pose="down", mouth="smile")
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_minion(d1, cx=256, cy=245, arm_pose="banana", mouth="smile")
    frames.append(finalize_frame(im1))
    return frames


def gen_climb():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=245 + (2 if i % 2 == 0 else -2),
                    leg_l_off=(-2, -3 if i % 2 == 0 else 3),
                    leg_r_off=(3, 3 if i % 2 == 0 else -3),
                    arm_pose="celebrate", mouth="banana")
        frames.append(finalize_frame(im))
    return frames


def gen_dragged():
    frames = []
    for i in range(4):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=245,
                    leg_l_off=(-3 if i % 2 == 0 else 3, -3),
                    leg_r_off=(3 if i % 2 == 0 else -3, 2),
                    arm_pose="celebrate", mouth="banana")
        frames.append(finalize_frame(im))
    return frames


def gen_sleep():
    frames = []
    for i in range(3):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_minion(d, cx=256, cy=265, arm_pose="down", eye_blink=True, mouth="smile")
        d.text((290, 80 - i * 10), "z", fill=C_YELLOW)
        frames.append(finalize_frame(im))
    return frames


def generate_all_minion_sprites(output_dir="assets/sprites/minion"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "idle": gen_idle(),
        "walk": gen_walk(),
        "run": gen_run(),
        "jump": gen_jump(),
        "fall": gen_fall(),
        "land": gen_land(),
        "climb_wall": gen_climb(),
        "celebrate": gen_celebrate(),
        "dragged": gen_dragged(),
        "banana": gen_banana(),
        "sleep": gen_sleep(),
    }

    for anim_name, frames in animations.items():
        for idx, frame in enumerate(frames):
            p_r = os.path.join(output_dir, f"{anim_name}_right_{idx}.png")
            frame.save(p_r)

            frame_l = frame.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{anim_name}_left_{idx}.png")
            frame_l.save(p_l)

    print(f"HD Minion sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_all_minion_sprites()
