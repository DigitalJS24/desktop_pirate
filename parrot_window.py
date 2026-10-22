"""
Parrot Companion Window.
An autonomous feathered pet that sits on the pirate's shoulder,
flies around the screen, perches on desktop icons, and returns when the pirate whistles!
"""

import os
import random
import math
import time
from enum import Enum
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QPointF
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication

from speech_bubble import SpeechBubble
from sound_manager import SoundManager
from utils import get_asset_path


class ParrotState(Enum):
    PERCHED = "perched"          # On pirate's shoulder
    TAKING_OFF = "taking_off"    # Launching into the air
    FLYING = "flying"            # Flying across screen
    PERCHED_ICON = "icon"        # Resting on a desktop shortcut icon
    RETURNING = "returning"      # Flying back to pirate after call
    DRAGGED = "dragged"          # Carried by user


class ParrotWindow(QWidget):
    def __init__(self, pirate, sound_mgr=None, scale=1.75):
        super().__init__()
        self.pirate = pirate
        self.sound = sound_mgr or SoundManager()
        self.scale = scale
        self.base_size = 36
        self.w = int(self.base_size * self.scale)
        self.h = int(self.base_size * self.scale)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(self.w, self.h)

        # Bubble for parrot speech
        self.bubble = SpeechBubble()

        # Position and flight dynamics
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.flight_speed = 5.5
        self.facing = "right"

        # State machine
        self.state = ParrotState.PERCHED
        self.state_time = 0.0
        self.next_flight_cooldown = random.uniform(25.0, 45.0)
        self.perch_on_icon_duration = random.uniform(8.0, 15.0)

        # Dragging
        self.is_dragging = False
        self.drag_offset = QPoint(0, 0)
        self.drag_start = QPoint(0, 0)

        # Animation frames
        self.frames = {}
        self.frame_idx = 0
        self.load_sprites()

        # Timers
        self.tick_timer = QTimer(self)
        self.tick_timer.setInterval(30)
        self.tick_timer.timeout.connect(self._tick)
        self.tick_timer.start()

        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(120)
        self.anim_timer.timeout.connect(self._anim_tick)
        self.anim_timer.start()

        # Update initial shoulder position
        self.update_shoulder_position()

    def set_scale(self, new_scale: float):
        self.scale = new_scale
        self.w = int(self.base_size * self.scale)
        self.h = int(self.base_size * self.scale)
        self.resize(self.w, self.h)
        self.load_sprites()
        self.update()

    def load_sprites(self):
        self.frames.clear()
        sp_dir = get_asset_path("sprites", "parrot")

        for anim in ["perch", "fly", "squawk"]:
            self.frames[anim] = {"left": [], "right": []}
            idx = 0
            while True:
                r_file = os.path.join(sp_dir, f"{anim}_right_{idx}.png")
                l_file = os.path.join(sp_dir, f"{anim}_left_{idx}.png")
                if not os.path.exists(r_file):
                    break
                pix_r = QPixmap(r_file).scaled(
                    self.w, self.h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                pix_l = QPixmap(l_file).scaled(
                    self.w, self.h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.frames[anim]["right"].append(pix_r)
                self.frames[anim]["left"].append(pix_l)
                idx += 1

    def say(self, text: str, duration_ms=2800):
        self.bubble.show_message(text, self.geometry(), duration_ms)

    def squawk(self, quote=None):
        self.sound.play("squawk")
        quotes = [
            "Кра-а-а! Піастри!",
            "Кра-а! Рому капітану!",
            "Кра-а! Всіх нагору!",
            "Кра-а-а! Скарби!",
            "Кра-а! Ледар на палубі!",
        ]
        self.say(quote or random.choice(quotes))

    def update_shoulder_position(self):
        """Calculates parrot's perch position on pirate's left/right shoulder."""
        pw = self.pirate.sprite_w
        ph = self.pirate.sprite_h
        px = self.pirate.x
        py = self.pirate.y

        # Shoulder offset depends on pirate facing direction
        if self.pirate.facing == "right":
            # Left shoulder (behind/above)
            self.x = px + pw * 0.12 - self.w * 0.4
            self.y = py + ph * 0.22 - self.h * 0.5
            self.facing = "right"
        else:
            # Right shoulder
            self.x = px + pw * 0.70 - self.w * 0.4
            self.y = py + ph * 0.22 - self.h * 0.5
            self.facing = "left"

        self.move(int(self.x), int(self.y))

    def take_flight_to_random_icon(self):
        """Starts parrot flight towards a desktop icon or screen vantage point."""
        if self.state in (ParrotState.FLYING, ParrotState.RETURNING, ParrotState.DRAGGED):
            return

        ledges = self.pirate.detector.get_all_ledges()
        if ledges:
            target_icon = random.choice(ledges)
            self.target_x = float(target_icon.center().x() - self.w // 2)
            self.target_y = float(target_icon.top() - self.h + 6)
        else:
            screen = QApplication.primaryScreen().availableGeometry()
            self.target_x = float(random.randint(screen.left() + 50, screen.right() - 100))
            self.target_y = float(random.randint(screen.top() + 80, screen.top() + 350))

        self.state = ParrotState.FLYING
        self.state_time = 0.0
        self.sound.play("squawk")
        self.say("Кра-а! Полетів на розвідку!")

    def return_to_pirate(self):
        """Called when pirate whistles/shouts for the parrot to return."""
        if self.state == ParrotState.PERCHED or self.state == ParrotState.DRAGGED:
            return

        self.state = ParrotState.RETURNING
        self.sound.play("squawk")
        self.say("Кра-а! Лечу, капітане!")

    # =========================================================================
    # FLIGHT & BEHAVIOR TICK
    # =========================================================================

    def _tick(self):
        dt = 0.03
        self.state_time += dt

        if self.state == ParrotState.DRAGGED:
            return

        elif self.state == ParrotState.PERCHED:
            # Follow pirate's shoulder continuously
            self.update_shoulder_position()

            # Autonomously decide to take flight
            if self.state_time >= self.next_flight_cooldown:
                self.take_flight_to_random_icon()

        elif self.state == ParrotState.FLYING:
            # Fly towards target location in an organic arc
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)

            self.facing = "right" if dx >= 0 else "left"

            if dist < 8.0:
                # Landed on icon!
                self.x = self.target_x
                self.y = self.target_y
                self.state = ParrotState.PERCHED_ICON
                self.state_time = 0.0
                self.perch_on_icon_duration = random.uniform(8.0, 16.0)
                self.squawk("Кра-а! Знайшов ярлик!")
            else:
                # Smooth flight steering
                speed = min(self.flight_speed, dist * 0.1 + 2.5)
                # Add small sine wave flap wobble
                wobble = math.sin(self.state_time * 8.0) * 1.5
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed + wobble

            self.move(int(self.x), int(self.y))

        elif self.state == ParrotState.PERCHED_ICON:
            # Sits on the desktop shortcut icon
            if self.state_time >= self.perch_on_icon_duration:
                # Pirate notices parrot is away and calls him back!
                self.pirate.call_parrot_back()

        elif self.state == ParrotState.RETURNING:
            # Target is current pirate shoulder
            pw = self.pirate.sprite_w
            ph = self.pirate.sprite_h
            if self.pirate.facing == "right":
                tx = self.pirate.x + pw * 0.12 - self.w * 0.4
                ty = self.pirate.y + ph * 0.22 - self.h * 0.5
            else:
                tx = self.pirate.x + pw * 0.70 - self.w * 0.4
                ty = self.pirate.y + ph * 0.22 - self.h * 0.5

            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)

            self.facing = "right" if dx >= 0 else "left"

            if dist < 10.0:
                # Successfully landed on shoulder!
                self.state = ParrotState.PERCHED
                self.state_time = 0.0
                self.next_flight_cooldown = random.uniform(30.0, 60.0)
                self.update_shoulder_position()
                self.sound.play("squawk")
                self.say("Кра-а! На містку!")
            else:
                speed = min(self.flight_speed * 1.4, dist * 0.15 + 3.0)
                wobble = math.sin(self.state_time * 9.0) * 1.2
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed + wobble
                self.move(int(self.x), int(self.y))

        # Keep speech bubble tracking
        if self.bubble.isVisible():
            self.bubble.adjust_size_and_position(self.geometry())

    # =========================================================================
    # ANIMATION TICK
    # =========================================================================

    def _anim_tick(self):
        anim_key = "perch"
        if self.state in (ParrotState.FLYING, ParrotState.RETURNING, ParrotState.TAKING_OFF, ParrotState.DRAGGED):
            anim_key = "fly"
        elif self.bubble.isVisible() and self.state == ParrotState.PERCHED_ICON:
            anim_key = "squawk"

        frames_list = self.frames.get(anim_key, {}).get(self.facing, [])
        if not frames_list:
            return

        self.frame_idx = (self.frame_idx + 1) % len(frames_list)
        self.update()

    def paintEvent(self, event):
        anim_key = "perch"
        if self.state in (ParrotState.FLYING, ParrotState.RETURNING, ParrotState.TAKING_OFF, ParrotState.DRAGGED):
            anim_key = "fly"
        elif self.bubble.isVisible() and self.state == ParrotState.PERCHED_ICON:
            anim_key = "squawk"

        frames_list = self.frames.get(anim_key, {}).get(self.facing, [])
        if frames_list and self.frame_idx < len(frames_list):
            painter = QPainter(self)
            painter.drawPixmap(0, 0, frames_list[self.frame_idx])

    # =========================================================================
    # MOUSE EVENTS
    # =========================================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start = event.globalPosition().toPoint()
            self.drag_offset = event.globalPosition().toPoint() - self.pos()
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            cur = event.globalPosition().toPoint()
            dist = (cur - self.drag_start).manhattanLength()
            if dist > 5 and not self.is_dragging:
                self.is_dragging = True
                self.state = ParrotState.DRAGGED
                self.sound.play("squawk")
                self.say("Кра-а! Відпусти крила!")

            if self.is_dragging:
                new_p = cur - self.drag_offset
                self.x = float(new_p.x())
                self.y = float(new_p.y())
                self.move(int(self.x), int(self.y))
                if self.bubble.isVisible():
                    self.bubble.adjust_size_and_position(self.geometry())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_dragging:
                self.is_dragging = False
                # User released parrot in air: fly back or land
                self.return_to_pirate()
            else:
                # Clicked: either make him squawk or take flight
                if self.state == ParrotState.PERCHED:
                    self.take_flight_to_random_icon()
                else:
                    self.return_to_pirate()

