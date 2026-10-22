"""
Minion Mascot Window.
A cute, mischievous yellow Minion who spawns after a kiss between the Pirate and Piratess!
Waddles, jumps, shouts "BANANA!", climbs desktop icons, and follows the pirate crew.
"""

import os
import random
import time
from enum import Enum
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QMenu, QApplication

from sound_manager import SoundManager
from speech_bubble import SpeechBubble
from pirate_quotes import get_quote
from desktop_icons import DesktopIconDetector
from utils import get_asset_path


class MinionState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"
    FALL = "fall"
    CHEER = "cheer"
    DRAGGED = "dragged"
    SLEEP = "sleep"


class MinionWindow(QWidget):
    def __init__(self, pirate=None, piratess=None, sound_mgr=None, scale=1.8):
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

        # Physics & Position
        self.x = 300.0
        self.y = 500.0
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.65
        self.speed = 2.5
        self.facing = "right"
        self.current_ledge = None

        # State machine
        self.state = MinionState.CHEER
        self.state_time = 0.0
        self.state_duration = 2.0

        # Target parent to follow
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

        # Minion spawn sound & quote!
        self.sound.play("minion")
        QTimer.singleShot(350, lambda: self.say(get_quote("minion_spawn")))

    def set_spawn_pos(self, sx, sy):
        self.x = float(sx)
        self.y = float(sy)
        self.move(int(self.x), int(self.y))

    def load_sprites(self):
        self.frames.clear()
        sp_dir = get_asset_path("sprites", "minion")

        for anim in [s.value for s in MinionState]:
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

    def change_state(self, new_state: MinionState, duration=3.0):
        self.state = new_state
        self.frame_idx = 0
        self.state_time = 0.0
        self.state_duration = duration

    # =========================================================================
    # PHYSICS & MINION AI
    # =========================================================================

    def _physics_tick(self):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        floor_y = float(avail.bottom() - self.h + 2)
        left_x = float(avail.left())
        right_x = float(avail.right() - self.w + 1)

        dt = 0.03
        self.state_time += dt

        if self.state == MinionState.DRAGGED:
            return

        elif self.state == MinionState.IDLE:
            if self.state_time >= self.state_duration:
                self._choose_action()

        elif self.state in (MinionState.WALK, MinionState.RUN):
            speed_mult = 1.0 if self.state == MinionState.WALK else 1.85
            move_speed = self.speed * speed_mult

            # Follow pirates or roam
            if self.follow_target:
                target_x = self.follow_target.x
                dist_x = target_x - self.x
                if abs(dist_x) > 60:
                    dir_mult = 1.0 if dist_x > 0 else -1.0
                    self.facing = "right" if dir_mult > 0 else "left"
                    self.x += dir_mult * move_speed
                else:
                    if random.random() < 0.22:
                        self.change_state(MinionState.CHEER, duration=1.5)
                        self.sound.play("minion")
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

        elif self.state == MinionState.JUMP:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            self.x = max(left_x, min(right_x, self.x))
            if self.vy > 0:
                self.state = MinionState.FALL

            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.w, self.h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                self.change_state(MinionState.CHEER, duration=1.2)
                self.say("BANANA! 🍌")
            elif self.y >= floor_y:
                self.y = floor_y
                self.current_ledge = None
                self.change_state(MinionState.IDLE, duration=0.8)

        elif self.state == MinionState.FALL:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            self.x = max(left_x, min(right_x, self.x))

            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.w, self.h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                self.change_state(MinionState.CHEER, duration=1.2)
            elif self.y >= floor_y:
                self.y = floor_y
                self.vx = 0.0
                self.vy = 0.0
                self.current_ledge = None
                self.change_state(MinionState.IDLE, duration=0.8)

        elif self.state == MinionState.CHEER:
            if self.state_time >= self.state_duration:
                self.change_state(MinionState.IDLE, duration=random.uniform(1.0, 2.0))

        elif self.state == MinionState.SLEEP:
            if self.state_time >= self.state_duration:
                self.change_state(MinionState.IDLE, duration=1.5)

        self.move(int(self.x), int(self.y))
        if self.bubble.isVisible():
            self.bubble.adjust_size_and_position(self.geometry())

    def _choose_action(self):
        if random.random() < 0.35 and self.pirate and self.piratess:
            self.follow_target = self.piratess if self.follow_target == self.pirate else self.pirate

        r = random.random()
        if r < 0.38:
            self.change_state(MinionState.WALK, duration=random.uniform(2.5, 6.0))
        elif r < 0.65:
            self.change_state(MinionState.RUN, duration=random.uniform(2.0, 4.0))
        elif r < 0.80:
            # Minion jump!
            self.vx = 2.8 if self.facing == "right" else -2.8
            self.vy = -11.0
            self.change_state(MinionState.JUMP)
        elif r < 0.92:
            self.change_state(MinionState.CHEER, duration=1.6)
            self.sound.play("minion")
            self.say(get_quote("minion_spawn"))
        else:
            self.change_state(MinionState.SLEEP, duration=random.uniform(6.0, 10.0))

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
                self.change_state(MinionState.DRAGGED)
                self.sound.play("minion")
                self.say("Tulaliloo ti amo! 🍌")

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

                self.change_state(MinionState.FALL)
            else:
                self.change_state(MinionState.CHEER, duration=1.6)
                self.sound.play("minion")
                quotes = [
                    "BANANA!! 🍌",
                    "Bello! 👋",
                    "Papoi! 🍌",
                    "Poopaye! 💛",
                    "Лака-тука! 🍌",
                ]
                self.say(random.choice(quotes))

        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())

    def _show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #242416;
                color: #fff4a3;
                border: 2px solid #e0c822;
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
                background-color: #e0c822;
                color: #222211;
            }
        """)

        act_banana = menu.addAction("🍌  Дати банан (BANANA!)")
        act_cheer = menu.addAction("🎉  Радісний танець міньйона")
        act_parents = menu.addAction("🦘  Побігти за капітаном")
        act_sleep = menu.addAction("💤  Подрімати")
        menu.addSeparator()
        act_close = menu.addAction("🚪  Відправити за бананами (Прибрати)")

        action = menu.exec(global_pos)

        if action == act_banana:
            self.change_state(MinionState.CHEER, duration=2.2)
            self.sound.play("minion")
            self.say("BANANA!! 🍌🍌🍌")
        elif action == act_cheer:
            self.change_state(MinionState.CHEER, duration=2.0)
            self.sound.play("minion")
            self.say("Bello! Papoi! 🎉")
        elif action == act_parents:
            self.change_state(MinionState.RUN, duration=4.0)
            self.say("Капітан! Банана!")
        elif action == act_sleep:
            self.change_state(MinionState.SLEEP, duration=15.0)
        elif action == act_close:
            self.close()

