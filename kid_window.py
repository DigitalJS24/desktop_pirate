"""
Pirate Kid (Mini Pirate / Юнга) Window.
A cute, toddler pirate child who is born after a kiss between the Pirate and Piratess!
Follows parents, jumps, climbs icons, and waves a wooden toy cutlass.
"""

import os
import random
import time
import math
from enum import Enum
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QMenu, QApplication

from sound_manager import SoundManager
from speech_bubble import SpeechBubble
from pirate_quotes import get_quote
from desktop_icons import DesktopIconDetector


class KidState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"
    FALL = "fall"
    CHEER = "cheer"
    DRAGGED = "dragged"
    SLEEP = "sleep"


class KidWindow(QWidget):
    def __init__(self, pirate=None, piratess=None, sound_mgr=None, scale=1.7):
        super().__init__()
        self.pirate = pirate
        self.piratess = piratess
        self.sound = sound_mgr or SoundManager()
        self.scale = scale
        self.base_size = 40
        self.w = int(self.base_size * self.scale)
        self.h = int(self.base_size * self.scale)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(self.w, self.h)

        self.bubble = SpeechBubble()
        self.detector = DesktopIconDetector()

        # Physics
        self.x = 300.0
        self.y = 500.0
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.65
        self.speed = 2.4
        self.facing = "right"
        self.current_ledge = None

        # State machine
        self.state = KidState.CHEER
        self.state_time = 0.0
        self.state_duration = 2.0

        # Follow parent behavior
        self.follow_target = random.choice([self.pirate, self.piratess]) if (self.pirate and self.piratess) else self.pirate

        # Dragging
        self.is_dragging = False
        self.drag_mouse_offset = QPoint(0, 0)
        self.drag_click_start = QPoint(0, 0)
        self.drag_history = []

        # Frames
        self.frames = {}
        self.frame_idx = 0
        self.load_sprites()

        # Timers
        self.physics_timer = QTimer(self)
        self.physics_timer.setInterval(30)
        self.physics_timer.timeout.connect(self._physics_tick)
        self.physics_timer.start()

        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(110)
        self.anim_timer.timeout.connect(self._anim_tick)
        self.anim_timer.start()

        # Spawn pop sound & quote!
        self.sound.play("baby")
        QTimer.singleShot(400, lambda: self.say(get_quote("kid_spawn")))

    def set_spawn_pos(self, sx, sy):
        self.x = float(sx)
        self.y = float(sy)
        self.move(int(self.x), int(self.y))

    def load_sprites(self):
        self.frames.clear()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sp_dir = os.path.join(base_dir, "assets", "sprites", "kid")

        for anim in [s.value for s in KidState]:
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
                    Qt.TransformationMode.FastTransformation
                )
                pix_l = QPixmap(l_file).scaled(
                    self.w, self.h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.FastTransformation
                )
                self.frames[anim]["right"].append(pix_r)
                self.frames[anim]["left"].append(pix_l)
                idx += 1

    def say(self, text: str, duration_ms=2800):
        self.bubble.show_message(text, self.geometry(), duration_ms)

    def change_state(self, new_state: KidState, duration=3.0):
        self.state = new_state
        self.frame_idx = 0
        self.state_time = 0.0
        self.state_duration = duration

    # =========================================================================
    # PHYSICS & TODDLER AI
    # =========================================================================

    def _physics_tick(self):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        floor_y = float(avail.bottom() - self.h + 2)
        left_x = float(avail.left())
        right_x = float(avail.right() - self.w + 1)

        dt = 0.03
        self.state_time += dt

        if self.state == KidState.DRAGGED:
            return

        elif self.state == KidState.IDLE:
            if self.state_time >= self.state_duration:
                self._choose_action()

        elif self.state in (KidState.WALK, KidState.RUN):
            # Move towards followed parent or roam
            speed_mult = 1.0 if self.state == KidState.WALK else 1.8
            move_speed = self.speed * speed_mult

            # If following a parent, orient towards them
            if self.follow_target:
                target_x = self.follow_target.x
                # Keep comfortable toddler distance (35 - 70px)
                dist_x = target_x - self.x
                if abs(dist_x) > 60:
                    dir_mult = 1.0 if dist_x > 0 else -1.0
                    self.facing = "right" if dir_mult > 0 else "left"
                    self.x += dir_mult * move_speed
                else:
                    # Near parent: cheer or jump!
                    if random.random() < 0.2:
                        self.change_state(KidState.CHEER, duration=1.5)
            else:
                dir_mult = 1.0 if self.facing == "right" else -1.0
                self.x += dir_mult * move_speed

            # Screen bounds
            if self.x <= left_x:
                self.x = left_x
                self.facing = "right"
            elif self.x >= right_x:
                self.x = right_x
                self.facing = "left"

            if self.state_time >= self.state_duration:
                self._choose_action()

        elif self.state == KidState.JUMP:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            self.x = max(left_x, min(right_x, self.x))
            if self.vy > 0:
                self.state = KidState.FALL

            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.w, self.h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                self.change_state(KidState.IDLE, duration=1.0)
            elif self.y >= floor_y:
                self.y = floor_y
                self.current_ledge = None
                self.change_state(KidState.IDLE, duration=0.8)

        elif self.state == KidState.FALL:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            self.x = max(left_x, min(right_x, self.x))

            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.w, self.h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                self.change_state(KidState.IDLE, duration=0.8)
            elif self.y >= floor_y:
                self.y = floor_y
                self.vx = 0.0
                self.vy = 0.0
                self.current_ledge = None
                self.change_state(KidState.IDLE, duration=0.8)

        elif self.state == KidState.CHEER:
            if self.state_time >= self.state_duration:
                self.change_state(KidState.IDLE, duration=random.uniform(1.0, 2.0))

        elif self.state == KidState.SLEEP:
            if self.state_time >= self.state_duration:
                self.change_state(KidState.IDLE, duration=1.5)

        self.move(int(self.x), int(self.y))
        if self.bubble.isVisible():
            self.bubble.adjust_size_and_position(self.geometry())

    def _choose_action(self):
        # Periodically switch parent to follow
        if random.random() < 0.35 and self.pirate and self.piratess:
            self.follow_target = self.piratess if self.follow_target == self.pirate else self.pirate

        r = random.random()
        if r < 0.40:
            self.change_state(KidState.WALK, duration=random.uniform(2.5, 6.0))
        elif r < 0.65:
            self.change_state(KidState.RUN, duration=random.uniform(2.0, 4.0))
        elif r < 0.80:
            # Toddler hop!
            self.vx = 2.5 if self.facing == "right" else -2.5
            self.vy = -10.5
            self.change_state(KidState.JUMP)
        elif r < 0.92:
            self.change_state(KidState.CHEER, duration=1.6)
            if random.random() < 0.35:
                self.say("Йо-хо-хо! ⚔️")
        else:
            self.change_state(KidState.SLEEP, duration=random.uniform(6.0, 10.0))

    # =========================================================================
    # ANIMATION TICK
    # =========================================================================

    def _anim_tick(self):
        anim_key = self.state.value
        frames_list = self.frames.get(anim_key, {}).get(self.facing, [])
        if not frames_list:
            return
        self.frame_idx = (self.frame_idx + 1) % len(frames_list)
        self.update()

    def paintEvent(self, event):
        anim_key = self.state.value
        frames_list = self.frames.get(anim_key, {}).get(self.facing, [])
        if frames_list and self.frame_idx < len(frames_list):
            painter = QPainter(self)
            painter.drawPixmap(0, 0, frames_list[self.frame_idx])

    # =========================================================================
    # MOUSE EVENTS
    # =========================================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_click_start = event.globalPosition().toPoint()
            self.drag_mouse_offset = event.globalPosition().toPoint() - self.pos()
            self.is_dragging = False
            self.drag_history = [(time.time(), event.globalPosition().toPoint())]

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            cur = event.globalPosition().toPoint()
            dist = (cur - self.drag_click_start).manhattanLength()
            if dist > 5 and not self.is_dragging:
                self.is_dragging = True
                self.change_state(KidState.DRAGGED)
                self.say("Я лечу, як папуга! Хі-хі!")

            if self.is_dragging:
                new_pos = cur - self.drag_mouse_offset
                self.x = float(new_pos.x())
                self.y = float(new_pos.y())
                self.move(int(self.x), int(self.y))

                now = time.time()
                self.drag_history.append((now, cur))
                self.drag_history = [(t, p) for t, p in self.drag_history if now - t <= 0.18]

                if self.bubble.isVisible():
                    self.bubble.adjust_size_and_position(self.geometry())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_dragging:
                self.is_dragging = False
                now = time.time()
                recent = [(t, p) for t, p in self.drag_history if now - t <= 0.15]
                if len(recent) >= 2:
                    dt = recent[-1][0] - recent[0][0]
                    if dt > 0.02:
                        dx = recent[-1][1].x() - recent[0][1].x()
                        dy = recent[-1][1].y() - recent[0][1].y()
                        self.vx = max(-18.0, min(18.0, (dx / dt) * 0.035))
                        self.vy = max(-18.0, min(18.0, (dy / dt) * 0.035))
                else:
                    self.vx = 0.0
                    self.vy = 1.0

                self.change_state(KidState.FALL)
            else:
                self.change_state(KidState.CHEER, duration=1.5)
                quotes = [
                    "Я новий грізний корсар! ⚔️",
                    "Дайте мені штурвал!",
                    "Ура-а-а! Скарби!",
                    "Папуго, лови сухарик!",
                ]
                self.say(random.choice(quotes))

        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())

    def _show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e2638;
                color: #e0edff;
                border: 2px solid #3c70b4;
                border-radius: 8px;
                padding: 6px;
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: bold;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3c70b4;
                color: #ffffff;
            }
        """)

        act_cheer = menu.addAction("⚔️  Помахати шаблею")
        act_parents = menu.addAction("🦘  Побігти до батьків")
        act_sleep = menu.addAction("💤  Подрімати")
        menu.addSeparator()
        act_close = menu.addAction("🚪  Спати в каюту (Прибрати малюка)")

        action = menu.exec(global_pos)

        if action == act_cheer:
            self.change_state(KidState.CHEER, duration=2.0)
            self.say("На абордаж! ⚔️")
        elif action == act_parents:
            self.change_state(KidState.RUN, duration=4.0)
            self.say("Мамо! Тату! Я тут!")
        elif action == act_sleep:
            self.change_state(KidState.SLEEP, duration=15.0)
        elif action == act_close:
            self.close()

