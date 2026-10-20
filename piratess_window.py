"""
Pirate Girl (Piratess) Window.
Interactive female pirate desktop mascot who playfully roams the desktop,
climbs, lands on icons, runs away from the pirate, and kisses him when caught!
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
from minion_window import MinionWindow
from utils import get_asset_path


class PiratessState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"          # Fleeing from pirate!
    JUMP = "jump"
    FALL = "fall"
    LAND = "land"
    CLIMB_WALL = "climb_wall"
    KISS = "kiss"        # Kissing the pirate!
    BLUSH = "blush"      # Blushing / blowing kiss
    DRAGGED = "dragged"
    SLEEP = "sleep"


class PiratessWindow(QWidget):
    def __init__(self, pirate=None, sound_mgr=None, scale=2.1):
        super().__init__()
        self.pirate = pirate
        self.sound = sound_mgr or SoundManager()
        self.scale = scale
        self.base_size = 64
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
        self.x = 400.0
        self.y = 500.0
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.70
        self.speed = 2.7
        self.facing = "left"
        self.current_ledge = None

        # State machine
        self.state = PiratessState.IDLE
        self.state_time = 0.0
        self.state_duration = 3.0
        self.climb_wall_side = "right"

        # Romance & Chase logic
        self.is_chased = False
        self.chase_cooldown = random.uniform(25.0, 45.0)
        self.kids = []  # Spawned pirate kids!

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
        self.anim_timer.setInterval(120)
        self.anim_timer.timeout.connect(self._anim_tick)
        self.anim_timer.start()

        self.init_position()

    def set_pirate(self, pirate):
        self.pirate = pirate

    def init_position(self):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        self.current_ledge = None
        # Start some distance away from the pirate
        self.x = float(avail.center().x() + 180)
        self.y = float(avail.bottom() - self.h + 2)
        self.move(int(self.x), int(self.y))

    def set_scale(self, new_scale: float):
        self.scale = new_scale
        self.w = int(self.base_size * self.scale)
        self.h = int(self.base_size * self.scale)
        self.resize(self.w, self.h)
        self.load_sprites()
        self.update()

    def load_sprites(self):
        self.frames.clear()
        sp_dir = get_asset_path("sprites", "piratess")

        for anim in [s.value for s in PiratessState]:
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

    def say(self, text: str, duration_ms=3500):
        self.bubble.show_message(text, self.geometry(), duration_ms)

    def change_state(self, new_state: PiratessState, duration=3.0):
        self.state = new_state
        self.frame_idx = 0
        self.state_time = 0.0
        self.state_duration = duration

        if new_state == PiratessState.KISS:
            self.sound.play("kiss")

    def trigger_kiss(self):
        """Executes the romantic kiss when pirate and girl meet!"""
        if not self.pirate:
            return

        # Face each other
        if self.pirate.x < self.x:
            self.facing = "left"
            self.pirate.facing = "right"
        else:
            self.facing = "right"
            self.pirate.facing = "left"

        self.is_chased = False
        self.chase_cooldown = random.uniform(30.0, 50.0)

        # Girl kisses
        self.change_state(PiratessState.KISS, duration=2.5)
        self.say(get_quote("kiss_girl"))

        # Pirate celebrates/kisses
        from pirate_window import PirateState
        self.pirate.change_state(PirateState.CELEBRATE, duration=2.5)
        self.pirate.say(get_quote("kiss_pirate"))

        # If parrot is present, squawk "Гірко!"
        if self.pirate.parrot:
            QTimer.singleShot(600, lambda: self.pirate.parrot.squawk("Гірко! Кра-а! Любов на палубі!"))

        # SPAWN A MINION AFTER THE KISS!
        QTimer.singleShot(1500, self.spawn_minion)

    def spawn_minion(self):
        """Spawns a cheerful yellow Minion between the parents!"""
        if not self.pirate:
            return

        # Cap at 8 active minions to prevent excessive window count
        if len(self.kids) >= 8:
            oldest = self.kids.pop(0)
            try:
                oldest.close()
            except Exception:
                pass

        mid_x = (self.x + self.pirate.x) / 2
        mid_y = max(self.y, self.pirate.y) + 12
        minion = MinionWindow(pirate=self.pirate, piratess=self, sound_mgr=self.sound)
        minion.set_spawn_pos(mid_x, mid_y)
        minion.show()
        self.kids.append(minion)

        # Parents react with surprise and laughter!
        self.say(get_quote("parent_new_minion"))

    def spawn_kid(self):
        self.spawn_minion()

    def clear_all_kids(self):
        """Dismisses all minions to look for bananas."""
        for k in self.kids:
            try:
                k.close()
            except Exception:
                pass
        self.kids.clear()
        self.say("Міньйони побігли шукати банани! 🍌")

    def start_chase(self):
        """Girl teases pirate and runs away playfully!"""
        if self.is_chased or self.state == PiratessState.KISS or not self.pirate:
            return

        self.is_chased = True
        self.state_time = 0.0

        # Run away in opposite direction of pirate
        if self.pirate.x < self.x:
            self.facing = "right"
        else:
            self.facing = "left"

        self.change_state(PiratessState.RUN, duration=15.0)
        self.say(get_quote("flee_girl"))

        # Signal pirate to start chasing
        self.pirate.start_chasing_girl(self)

    # =========================================================================
    # PHYSICS & CHASE TICK
    # =========================================================================

    def _physics_tick(self):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        floor_y = float(avail.bottom() - self.h + 2)
        left_x = float(avail.left())
        right_x = float(avail.right() - self.w + 1)
        top_y = float(avail.top())

        dt = 0.03
        self.state_time += dt

        if self.state == PiratessState.DRAGGED:
            # Check if user dragged her right on top of pirate -> trigger kiss!
            if self.pirate:
                dist = math.hypot(self.pirate.x - self.x, self.pirate.y - self.y)
                if dist < 65 and self.pirate.state.value != "kiss":
                    pass
            return

        elif self.state == PiratessState.KISS:
            self.vx = 0.0
            self.vy = 0.0
            if self.state_time >= self.state_duration:
                self.change_state(PiratessState.BLUSH, duration=2.0)
            self.move(int(self.x), int(self.y))
            if self.bubble.isVisible():
                self.bubble.adjust_size_and_position(self.geometry())
            return

        elif self.state == PiratessState.BLUSH:
            if self.state_time >= self.state_duration:
                self.change_state(PiratessState.IDLE, duration=2.5)

        # Autonomous chase timer: girl decides to tease pirate!
        if not self.is_chased and self.state != PiratessState.KISS:
            self.chase_cooldown -= dt
            if self.chase_cooldown <= 0:
                self.start_chase()

        # Handle movement states
        if self.state == PiratessState.IDLE:
            if self.state_time >= self.state_duration:
                self._choose_action()

        elif self.state == PiratessState.WALK:
            dir_mult = 1.0 if self.facing == "right" else -1.0
            self.x += dir_mult * self.speed

            if self.current_ledge:
                if self.x <= self.current_ledge.left() - 10 or self.x >= self.current_ledge.right() - self.w + 10:
                    self.current_ledge = None
                    self.change_state(PiratessState.FALL)
            else:
                if self.x <= left_x:
                    self.x = left_x
                    self.facing = "right"
                    if random.random() < 0.4:
                        self.climb_wall_side = "left"
                        self.change_state(PiratessState.CLIMB_WALL, duration=random.uniform(4.0, 7.0))
                elif self.x >= right_x:
                    self.x = right_x
                    self.facing = "left"
                    if random.random() < 0.4:
                        self.climb_wall_side = "right"
                        self.change_state(PiratessState.CLIMB_WALL, duration=random.uniform(4.0, 7.0))

            if self.state_time >= self.state_duration:
                self._choose_action()

        elif self.state == PiratessState.RUN:
            # Playfully fleeing from pirate!
            flee_speed = self.speed * 1.55
            dir_mult = 1.0 if self.facing == "right" else -1.0
            self.x += dir_mult * flee_speed

            # Screen bounds: turn around or leap
            if self.x <= left_x:
                self.x = left_x
                self.facing = "right"
                # Leap over pirate if trapped at edge!
                if self.pirate and abs(self.pirate.x - self.x) < 220:
                    self.vx = 5.5
                    self.vy = -13.0
                    self.change_state(PiratessState.JUMP)
            elif self.x >= right_x:
                self.x = right_x
                self.facing = "left"
                if self.pirate and abs(self.pirate.x - self.x) < 220:
                    self.vx = -5.5
                    self.vy = -13.0
                    self.change_state(PiratessState.JUMP)

            # Check if pirate caught up!
            if self.pirate and self.is_chased:
                dist = math.hypot(self.pirate.x - self.x, self.pirate.y - self.y)
                if dist < 55:
                    # CAUGHT! Kiss event!
                    self.trigger_kiss()

            if self.state_time >= self.state_duration:
                # Chase timeout if escaped
                self.is_chased = False
                self.change_state(PiratessState.BLUSH, duration=2.0)
                self.say("Хі-хі, не наздогнав!")

        elif self.state == PiratessState.JUMP:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            self.x = max(left_x, min(right_x, self.x))
            if self.vy > 0:
                self.state = PiratessState.FALL

            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.w, self.h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                ledges = self.detector.get_all_ledges()
                self.current_ledge = next((r for r in ledges if abs(r.top() - self.h + 2 - ledge_y) < 6), None)
                self.change_state(PiratessState.LAND, duration=0.2)
            elif self.y >= floor_y:
                self.y = floor_y
                self.current_ledge = None
                self.change_state(PiratessState.LAND, duration=0.2)

        elif self.state == PiratessState.FALL:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity
            self.vx *= 0.98

            self.x = max(left_x, min(right_x, self.x))

            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.w, self.h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                ledges = self.detector.get_all_ledges()
                self.current_ledge = next((r for r in ledges if abs(r.top() - self.h + 2 - ledge_y) < 6), None)
                self.change_state(PiratessState.LAND, duration=0.25)
            elif self.y >= floor_y:
                self.y = floor_y
                self.vx = 0.0
                self.vy = 0.0
                self.current_ledge = None
                self.change_state(PiratessState.LAND, duration=0.25)

        elif self.state == PiratessState.LAND:
            if self.state_time >= self.state_duration:
                if self.is_chased:
                    self.change_state(PiratessState.RUN, duration=6.0)
                else:
                    self.change_state(PiratessState.IDLE, duration=random.uniform(1.0, 2.5))

        elif self.state == PiratessState.CLIMB_WALL:
            self.y -= 2.2
            self.x = left_x if self.climb_wall_side == "left" else right_x
            if self.y <= top_y + 20 or self.state_time >= self.state_duration:
                self.facing = "right" if self.climb_wall_side == "left" else "left"
                self.vx = 4.0 if self.climb_wall_side == "left" else -4.0
                self.vy = 1.0
                self.change_state(PiratessState.FALL)

        elif self.state == PiratessState.SLEEP:
            if self.state_time >= self.state_duration:
                self.change_state(PiratessState.IDLE, duration=2.0)

        self.move(int(self.x), int(self.y))
        if self.bubble.isVisible():
            self.bubble.adjust_size_and_position(self.geometry())

    def _choose_action(self):
        r = random.random()
        if r < 0.45:
            self.facing = "left" if random.random() < 0.5 else "right"
            self.change_state(PiratessState.WALK, duration=random.uniform(3.0, 7.0))
        elif r < 0.65:
            self.change_state(PiratessState.IDLE, duration=random.uniform(2.0, 5.0))
        elif r < 0.80:
            # Leap
            self.facing = "left" if random.random() < 0.5 else "right"
            self.vx = 3.5 if self.facing == "right" else -3.5
            self.vy = -12.0
            self.current_ledge = None
            self.change_state(PiratessState.JUMP)
        elif r < 0.92:
            self.change_state(PiratessState.BLUSH, duration=2.0)
        else:
            self.change_state(PiratessState.SLEEP, duration=random.uniform(6.0, 12.0))

    # =========================================================================
    # ANIMATION TICK
    # =========================================================================

    def _anim_tick(self):
        frames_list = self.frames.get(self.state.value, {}).get(self.facing, [])
        if not frames_list:
            return
        self.frame_idx = (self.frame_idx + 1) % len(frames_list)
        self.update()

    def paintEvent(self, event):
        frames_list = self.frames.get(self.state.value, {}).get(self.facing, [])
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
            if dist > 6 and not self.is_dragging:
                self.is_dragging = True
                self.current_ledge = None
                self.change_state(PiratessState.DRAGGED)
                self.say("Ой! Куди це ми летимо?")

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
                        self.vx = max(-20.0, min(20.0, (dx / dt) * 0.035))
                        self.vy = max(-22.0, min(20.0, (dy / dt) * 0.035))
                else:
                    self.vx = 0.0
                    self.vy = 1.0

                # Check if dropped next to pirate -> instant kiss!
                if self.pirate:
                    dist = math.hypot(self.pirate.x - self.x, self.pirate.y - self.y)
                    if dist < 65:
                        self.trigger_kiss()
                        return

                self.change_state(PiratessState.FALL)
            else:
                # Clicked: blow a kiss or start playful chase
                r = random.random()
                if r < 0.5:
                    self.change_state(PiratessState.BLUSH, duration=2.0)
                    self.say("Привіт, корсаре! 💕")
                else:
                    self.start_chase()

        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())

    def _show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b1f24;
                color: #ffe4e9;
                border: 2px solid #a84260;
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
                background-color: #a84260;
                color: #ffffff;
            }
        """)

        act_chase = menu.addAction("💖  Почати романтичну погоню")
        act_kiss = menu.addAction("💋  Поцілувати капітана зараз")
        act_blush = menu.addAction("💕  Послати повітряний поцілунок")
        act_spawn_kid = menu.addAction("🍌  Покликати міньйона (BANANA!)")
        if self.kids:
            act_clear_kids = menu.addAction("🧹  Відправити міньйонів за бананами")
        else:
            act_clear_kids = None

        menu.addSeparator()

        scale_menu = menu.addMenu("📏  Розмір піратки")
        act_scale_15 = scale_menu.addAction("Маленький (1.5x)")
        act_scale_21 = scale_menu.addAction("Звичайний (2.1x)")
        act_scale_28 = scale_menu.addAction("Великий (2.8x)")

        menu.addSeparator()
        act_home = menu.addAction("⚓  Повернути на робочий стіл")

        action = menu.exec(global_pos)

        if action == act_chase:
            self.start_chase()
        elif action == act_kiss:
            self.trigger_kiss()
        elif action == act_blush:
            self.change_state(PiratessState.BLUSH, duration=2.5)
            self.say("Лови мій поцілунок! 💕")
        elif action == act_spawn_kid:
            self.spawn_kid()
        elif act_clear_kids and action == act_clear_kids:
            self.clear_all_kids()
        elif action == act_scale_15:
            self.set_scale(1.5)
        elif action == act_scale_21:
            self.set_scale(2.1)
        elif action == act_scale_28:
            self.set_scale(2.8)
        elif action == act_home:
            self.init_position()

