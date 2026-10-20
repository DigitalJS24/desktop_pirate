"""
Parrot sprite generator.
Generates dedicated, high-detail pixel-art animations for the pirate's pet parrot companion.
"""

import os
from PIL import Image, ImageDraw

C_TRANSPARENT = (0, 0, 0, 0)
C_BLACK       = (20, 20, 20, 255)
C_WHITE       = (250, 250, 250, 255)
C_RED         = (230, 35, 35, 255)
C_RED_DARK    = (175, 25, 25, 255)
C_GREEN       = (40, 190, 60, 255)
C_GREEN_DARK  = (25, 135, 40, 255)
C_BLUE        = (45, 120, 225, 255)
C_YELLOW      = (255, 215, 25, 255)
C_ORANGE      = (245, 140, 20, 255)
C_FEET        = (160, 130, 90, 255)

SIZE = 36  # Base frame 36x36 pixels


def blank():
    return Image.new("RGBA", (SIZE, SIZE), C_TRANSPARENT)


def draw_perch_frames():
    frames = []
    # 4 frames: bobbing, looking around
    bobs = [0, -1, 0, 1]
    for i, bob in enumerate(bobs):
        im = blank()
        d = ImageDraw.Draw(im)
        cx, cy = 18, 18 + bob

        # Feet gripping branch/shoulder
        d.line([(cx - 3, cy + 8), (cx - 1, cy + 9)], fill=C_FEET, width=2)
        d.line([(cx + 1, cy + 8), (cx + 3, cy + 9)], fill=C_FEET, width=2)

        # Long tropical tail feathers (Red, Blue, Yellow)
        d.line([(cx - 2, cy + 7), (cx - 5, cy + 15)], fill=C_BLUE, width=2)
        d.line([(cx, cy + 7), (cx - 2, cy + 17)], fill=C_RED, width=2)
        d.line([(cx + 2, cy + 7), (cx + 1, cy + 14)], fill=C_YELLOW, width=1)

        # Body (vibrant green + red chest)
        d.rectangle([cx - 4, cy, cx + 4, cy + 7], fill=C_GREEN)
        d.rectangle([cx - 2, cy + 1, cx + 2, cy + 6], fill=C_RED)

        # Folded wing (blue & yellow edge)
        d.polygon([(cx - 3, cy + 1), (cx - 6, cy + 4), (cx - 4, cy + 8)], fill=C_BLUE)
        d.point([(cx - 5, cy + 5), (cx - 4, cy + 6)], fill=C_YELLOW)

        # Head (red with green crest)
        d.rectangle([cx - 3, cy - 6, cx + 3, cy], fill=C_RED)
        # Green head crest feather
        d.polygon([(cx - 1, cy - 6), (cx - 2, cy - 10), (cx + 1, cy - 6)], fill=C_GREEN)

        # Eye
        d.rectangle([cx + 1, cy - 5, cx + 3, cy - 3], fill=C_WHITE)
        d.point([(cx + 2, cy - 4)], fill=C_BLACK)

        # Curved pirate parrot beak (yellow with hooked tip)
        d.polygon([(cx + 3, cy - 4), (cx + 7, cy - 3), (cx + 6, cy - 1), (cx + 3, cy - 2)], fill=C_YELLOW)
        d.point([(cx + 6, cy)], fill=C_ORANGE)  # Hook tip

        frames.append(im)
    return frames


def draw_fly_frames():
    frames = []
    # 4 frames: wings up, forward, down, glide
    wing_states = ["up", "mid", "down", "glide"]
    for i, state in enumerate(wing_states):
        im = blank()
        d = ImageDraw.Draw(im)
        cx, cy = 18, 18

        # Tail streaming behind in flight
        d.line([(cx - 5, cy + 2), (cx - 14, cy + 4)], fill=C_RED, width=2)
        d.line([(cx - 4, cy + 3), (cx - 12, cy + 7)], fill=C_BLUE, width=2)
        d.line([(cx - 4, cy + 1), (cx - 13, cy + 2)], fill=C_YELLOW, width=1)

        # Body horizontal/streamlined
        d.rectangle([cx - 5, cy - 2, cx + 4, cy + 3], fill=C_GREEN)
        d.rectangle([cx - 2, cy - 1, cx + 3, cy + 2], fill=C_RED)

        # Tucked feet
        d.point([(cx - 2, cy + 4), (cx, cy + 4)], fill=C_FEET)

        # Head thrust forward
        d.rectangle([cx + 3, cy - 4, cx + 8, cy + 1], fill=C_RED)
        d.polygon([(cx + 5, cy - 4), (cx + 4, cy - 7), (cx + 7, cy - 4)], fill=C_GREEN)
        d.point([(cx + 6, cy - 3)], fill=C_WHITE)
        d.point([(cx + 7, cy - 3)], fill=C_BLACK)
        # Beak forward
        d.polygon([(cx + 8, cy - 3), (cx + 12, cy - 2), (cx + 10, cy), (cx + 8, cy - 1)], fill=C_YELLOW)

        # Wings flapping!
        if state == "up":
            # Wings raised high
            d.polygon([(cx - 2, cy - 2), (cx + 1, cy - 12), (cx + 6, cy - 2)], fill=C_BLUE)
            d.polygon([(cx - 1, cy - 2), (cx + 2, cy - 10), (cx + 5, cy - 2)], fill=C_YELLOW)
            d.polygon([(cx, cy - 2), (cx + 3, cy - 8), (cx + 4, cy - 2)], fill=C_RED)
        elif state == "mid":
            # Wings outstretched
            d.polygon([(cx - 4, cy - 2), (cx + 2, cy - 7), (cx + 7, cy - 1)], fill=C_BLUE)
            d.polygon([(cx - 3, cy - 1), (cx + 2, cy - 5), (cx + 6, cy)], fill=C_YELLOW)
        elif state == "down":
            # Wings pushed down
            d.polygon([(cx - 2, cy + 1), (cx + 2, cy + 10), (cx + 6, cy + 1)], fill=C_BLUE)
            d.polygon([(cx - 1, cy + 1), (cx + 2, cy + 8), (cx + 5, cy + 1)], fill=C_YELLOW)
        elif state == "glide":
            # Flat banking glide
            d.polygon([(cx - 5, cy - 1), (cx + 1, cy - 4), (cx + 6, cy - 1)], fill=C_BLUE)
            d.line([(cx - 4, cy - 1), (cx + 5, cy - 1)], fill=C_YELLOW, width=1)

        frames.append(im)
    return frames


def draw_squawk_frames():
    frames = []
    for i in range(2):
        im = blank()
        d = ImageDraw.Draw(im)
        cx, cy = 18, 17 + (0 if i == 0 else -1)

        d.line([(cx - 3, cy + 8), (cx - 1, cy + 9)], fill=C_FEET, width=2)
        d.line([(cx + 1, cy + 8), (cx + 3, cy + 9)], fill=C_FEET, width=2)
        d.line([(cx - 2, cy + 7), (cx - 5, cy + 15)], fill=C_BLUE, width=2)
        d.line([(cx, cy + 7), (cx - 2, cy + 17)], fill=C_RED, width=2)

        d.rectangle([cx - 4, cy, cx + 4, cy + 7], fill=C_GREEN)
        d.rectangle([cx - 2, cy + 1, cx + 2, cy + 6], fill=C_RED)

        # Flapped wing
        d.polygon([(cx - 3, cy + 1), (cx - 8, cy - 2), (cx - 4, cy + 7)], fill=C_BLUE)
        d.point([(cx - 6, cy + 1)], fill=C_YELLOW)

        # Head tilted up squawking
        d.rectangle([cx - 3, cy - 6, cx + 3, cy], fill=C_RED)
        d.polygon([(cx - 1, cy - 6), (cx - 3, cy - 11), (cx + 1, cy - 6)], fill=C_GREEN)

        d.rectangle([cx + 1, cy - 5, cx + 3, cy - 3], fill=C_WHITE)
        d.point([(cx + 2, cy - 4)], fill=C_BLACK)

        # WIDE OPEN BEAK
        d.polygon([(cx + 3, cy - 5), (cx + 8, cy - 6), (cx + 4, cy - 3)], fill=C_YELLOW)
        d.polygon([(cx + 3, cy - 2), (cx + 7, cy), (cx + 4, cy + 1)], fill=C_YELLOW)
        d.point([(cx + 3, cy - 3), (cx + 4, cy - 3)], fill=C_BLACK)  # Inside mouth

        # Sound notes / squawk wave marks!
        if i == 1:
            d.point([(cx + 9, cy - 6), (cx + 11, cy - 8)], fill=C_YELLOW)
            d.point([(cx + 10, cy - 2)], fill=C_ORANGE)

        frames.append(im)
    return frames


def generate_parrot_sprites(output_dir="assets/sprites/parrot"):
    os.makedirs(output_dir, exist_ok=True)
    sets = {
        "perch": draw_perch_frames(),
        "fly": draw_fly_frames(),
        "squawk": draw_squawk_frames(),
    }

    for name, frames in sets.items():
        for idx, fr in enumerate(frames):
            # Facing right
            p_r = os.path.join(output_dir, f"{name}_right_{idx}.png")
            fr.save(p_r)

            # Facing left
            fr_l = fr.transpose(Image.FLIP_LEFT_RIGHT)
            p_l = os.path.join(output_dir, f"{name}_left_{idx}.png")
            fr_l.save(p_l)

    print(f"Parrot sprites generated successfully in {output_dir}!")


if __name__ == "__main__":
    generate_parrot_sprites()

