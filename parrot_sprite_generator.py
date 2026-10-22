"""
High-Definition Smooth Cartoon Sprite Generator for the Pirate's Pet Parrot.
Renders smooth anti-aliased 256x256 frames (via 512x512 Lanczos supersampling):
- Vibrant scarlet macaw with golden wing bars and royal blue flight feathers
- Expressive eye with white cheek patch and curved pirate beak
- Flowing tail feathers and cute claws
- Fluid flapping and perching cycles
"""

import os
from PIL import Image, ImageDraw

OUTPUT_SIZE = 256
RENDER_SIZE = 512

C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (20, 20, 25, 255)
C_WHITE       = (255, 255, 255, 255)
C_RED         = (235, 38, 42, 255)
C_RED_DARK    = (175, 24, 28, 255)
C_YELLOW      = (255, 215, 30, 255)
C_BLUE        = (42, 115, 225, 255)
C_BLUE_DARK   = (26, 75, 155, 255)
C_BEAK        = (248, 242, 225, 255)
C_BEAK_TIP    = (75, 75, 80, 255)
C_FEET        = (170, 140, 100, 255)


def create_canvas():
    return Image.new("RGBA", (RENDER_SIZE, RENDER_SIZE), C_TRANSPARENT)


def finalize_frame(im: Image.Image) -> Image.Image:
    return im.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)


def draw_parrot(d: ImageDraw.ImageDraw, cx=256, cy=240,
                wing_state="folded", bob=0, flap_y=0, beak_open=False):
    px = cx
    py = cy + bob

    # 1. Long Tropical Tail Feathers
    d.polygon([(px - 15, py + 30), (px - 50, py + 160), (px - 35, py + 160), (px - 5, py + 35)], fill=C_BLUE)
    d.polygon([(px - 8, py + 30), (px - 38, py + 180), (px - 22, py + 180), (px + 2, py + 35)], fill=C_RED)
    d.polygon([(px, py + 30), (px - 20, py + 145), (px - 10, py + 145), (px + 8, py + 35)], fill=C_YELLOW)

    # 2. Feet / Claws
    d.rounded_rectangle([px - 20, py + 52, px - 6, py + 68], radius=4, fill=C_FEET)
    d.rounded_rectangle([px + 2, py + 52, px + 16, py + 68], radius=4, fill=C_FEET)

    # 3. Body (Plump round scarlet chest)
    d.ellipse([px - 45, py - 35, px + 40, py + 55], fill=C_RED)
    d.arc([px - 45, py - 35, px + 40, py + 55], start=45, end=135, fill=C_RED_DARK, width=6)

    # 4. Wings
    if wing_state == "folded":
        # Folded wing (blue + yellow bar)
        d.polygon([(px - 20, py - 20), (px + 15, py - 10), (px - 15, py + 45), (px - 42, py + 15)], fill=C_BLUE)
        d.polygon([(px - 18, py - 18), (px + 10, py - 8), (px - 5, py + 15), (px - 30, py + 5)], fill=C_YELLOW)
        d.arc([(px - 20, py - 20), (px - 15, py + 45)], start=0, end=180, fill=C_BLUE_DARK, width=3)
    elif wing_state == "up":
        # Wings flapped high up
        d.polygon([(px - 15, py - 20), (px - 110, py - 120 + flap_y), (px - 50, py - 30), (px - 10, py + 10)], fill=C_BLUE)
        d.polygon([(px - 15, py - 20), (px - 90, py - 100 + flap_y), (px - 45, py - 25), (px - 10, py + 5)], fill=C_YELLOW)

        d.polygon([(px + 15, py - 20), (px + 110, py - 120 + flap_y), (px + 50, py - 30), (px + 10, py + 10)], fill=C_BLUE)
        d.polygon([(px + 15, py - 20), (px + 90, py - 100 + flap_y), (px + 45, py - 25), (px + 10, py + 5)], fill=C_YELLOW)
    elif wing_state == "down":
        # Wings flapped downward
        d.polygon([(px - 15, py - 10), (px - 120, py + 45 + flap_y), (px - 60, py + 30), (px - 10, py + 20)], fill=C_BLUE)
        d.polygon([(px - 15, py - 10), (px - 95, py + 30 + flap_y), (px - 50, py + 20), (px - 10, py + 15)], fill=C_YELLOW)

        d.polygon([(px + 15, py - 10), (px + 120, py + 45 + flap_y), (px + 60, py + 30), (px + 10, py + 20)], fill=C_BLUE)
        d.polygon([(px + 15, py - 10), (px + 95, py + 30 + flap_y), (px + 50, py + 20), (px + 10, py + 15)], fill=C_YELLOW)

    # 5. Head & Crest
    d.ellipse([px - 30, py - 85, px + 35, py - 20], fill=C_RED)
    # Tropical crest feather on top
    d.polygon([(px - 15, py - 80), (px - 10, py - 125), (px + 10, py - 85)], fill=C_YELLOW)
    d.polygon([(px + 2, py - 82), (px + 8, py - 118), (px + 22, py - 82)], fill=C_RED)

    # White cheek patch
    d.ellipse([px + 2, py - 65, px + 30, py - 35], fill=C_WHITE)

    # Eye
    d.ellipse([px + 10, py - 58, px + 24, py - 44], fill=C_BLACK)
    d.ellipse([px + 13, py - 56, px + 18, py - 51], fill=C_WHITE) # catchlight

    # Curved Ivory Beak
    if beak_open:
        d.polygon([(px + 25, py - 60), (px + 58, py - 45), (px + 45, py - 35), (px + 25, py - 40)], fill=C_BEAK)
        d.polygon([(px + 25, py - 35), (px + 48, py - 25), (px + 40, py - 18), (px + 25, py - 25)], fill=C_BEAK_TIP)
    else:
        d.polygon([(px + 25, py - 60), (px + 62, py - 42), (px + 50, py - 22), (px + 25, py - 35)], fill=C_BEAK)
        d.point([(px + 52, py - 24)], fill=C_BEAK_TIP) # Hook tip


def gen_perched():
    frames = []
    bobs = [0, -3, 0, 3]
    for i, bob in enumerate(bobs):
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_parrot(d, cx=256, cy=240, wing_state="folded", bob=bob, beak_open=(i == 1))
        frames.append(finalize_frame(im))
    return frames


def gen_flying():
    frames = []
    flaps = [("up", -10), ("up", 10), ("down", -10), ("down", 10)]
    for state, fy in flaps:
        im = create_canvas()
        d = ImageDraw.Draw(im)
        draw_parrot(d, cx=256, cy=240, wing_state=state, flap_y=fy)
        frames.append(finalize_frame(im))
    return frames


def gen_taking_off():
    frames = []
    im0 = create_canvas()
    d0 = ImageDraw.Draw(im0)
    draw_parrot(d0, cx=256, cy=245, wing_state="folded", bob=4)
    frames.append(finalize_frame(im0))

    im1 = create_canvas()
    d1 = ImageDraw.Draw(im1)
    draw_parrot(d1, cx=256, cy=235, wing_state="up", flap_y=-15)
    frames.append(finalize_frame(im1))
    return frames


def generate_parrot_sprites(output_dir="assets/sprites/parrot"):
    os.makedirs(output_dir, exist_ok=True)
    animations = {
        "perched": gen_perched(),
        "flying": gen_flying(),
        "taking_off": gen_taking_off(),
        "icon": gen_perched(),
        "returning": gen_flying(),
        "dragged": gen_flying(),
    }

    for anim_name, frames in animations.items():
        for idx, frame in enumerate(frames):
            p_r = os.path.join(output_dir, f"{anim_name}_right_{idx}.png")
            frame.save(p_r)

            frame_l = frame.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{anim_name}_left_{idx}.png")
            frame_l.save(p_l)

    print(f"HD Parrot sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_parrot_sprites()
