"""
Pirate Desktop Mascot Window.
Interactive desktop pet with climbing, jumping, running, dragging, physics, speech,
desktop icon clinging, and companion parrot integration.
"""

import os
import random
import time
from enum import Enum
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QPointF
from PyQt6.QtGui import QPainter, QPixmap, QCursor, QAction, QIcon
from PyQt6.QtWidgets import QWidget, QMenu, QSystemTrayIcon, QApplication

from sound_manager import SoundManager
from speech_bubble import SpeechBubble
from pirate_quotes import get_quote
from desktop_icons import DesktopIconDetector
from utils import get_asset_path


class PirateState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"
    FALL = "fall"
    LAND = "land"
    CLIMB_WALL = "climb_wall"
    CLIMB_CEILING = "climb_ceiling"
    DRAGGED = "dragged"
    HANG_ICON = "dragged"      # Clinging to a desktop shortcut icon
    ATTACK = "attack"
    CELEBRATE = "celebrate"
    SLEEP = "sleep"


class PirateWindow(QWidget):
    def __init__(self, sprites_dir=None, scale=2.2):
        super().__init__()
        if sprites_dir is None:
            sprites_dir = get_asset_path("sprites")
        self.sprites_dir = sprites_dir
        self.scale = scale
        self.base_size = 64
        self.sprite_w = int(self.base_size * self.scale)
        self.sprite_h = int(self.base_size * self.scale)

        # Window properties
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(self.sprite_w, self.sprite_h)

        # Audio, speech, and icon detector
        self.sound = SoundManager()
        self.bubble = SpeechBubble()
        self.detector = DesktopIconDetector()
        self.parrot = None    # Assigned by main.py
        self.piratess = None  # Assigned by main.py
        self.is_chasing_girl = False

        # Physics & Position
        self.x = 200.0
        self.y = 500.0
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.70
        self.facing = "right"  # "left" or "right"
        self.speed = 2.6       # Horizontal walk speed

        # Current ledge (e.g. desktop icon shortcut)
        self.current_ledge = None

        # Dragging state
        self.is_dragging = False
        self.drag_mouse_offset = QPoint(0, 0)
        self.drag_click_start = QPoint(0, 0)
        self.drag_history = []  # list of (timestamp, pos) for throw velocity

        # State machine
        self.state = PirateState.IDLE
        self.state_time = 0.0
        self.state_duration = 3.0
        self.climb_wall_side = "left"  # "left" or "right"

        # Animation frames
        self.frames = {}
        self.frame_idx = 0
        self.load_all_sprites()

        # Timers
        # Physics / AI tick: 30 FPS (~33ms)
        self.physics_timer = QTimer(self)
        self.physics_timer.setInterval(30)
        self.physics_timer.timeout.connect(self._physics_tick)
        self.physics_timer.start()

        # Animation frame tick: ~130ms per frame
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(130)
        self.anim_timer.timeout.connect(self._anim_tick)
        self.anim_timer.start()

        # Place initially on desktop
        self.init_position()

        # Initial pirate greeting
        QTimer.singleShot(1000, lambda: self.say(get_quote("click")))

    def set_parrot(self, parrot):
        self.parrot = parrot

    def set_piratess(self, piratess):
        self.piratess = piratess

    def start_chasing_girl(self, girl=None):
        if not self.piratess and girl:
            self.piratess = girl
        if not self.piratess:
            return
        self.is_chasing_girl = True
        self.facing = "right" if self.piratess.x > self.x else "left"
        self.change_state(PirateState.RUN, duration=15.0)
        self.say(get_quote("chase_pirate"))

    def init_position(self):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        self.current_ledge = None
        self.x = float(avail.center().x() - self.sprite_w // 2)
        self.y = float(avail.bottom() - self.sprite_h + 2)
        self.move(int(self.x), int(self.y))
        if self.parrot:
            self.parrot.update_shoulder_position()

    def set_scale(self, new_scale: float):
        self.scale = new_scale
        self.sprite_w = int(self.base_size * self.scale)
        self.sprite_h = int(self.base_size * self.scale)
        self.resize(self.sprite_w, self.sprite_h)
        self.load_all_sprites()
        if self.parrot:
            self.parrot.set_scale(new_scale * 0.9)
        self.update()

    def load_all_sprites(self):
        """Pre-load and scale all sprite frames for fast rendering."""
        self.frames.clear()
        anim_names = ["idle", "walk", "run", "jump", "fall", "land", "climb_wall", "climb_ceiling", "dragged", "attack", "celebrate", "sleep"]

        for anim in anim_names:
            self.frames[anim] = {"left": [], "right": []}
            idx = 0
            while True:
                r_file = os.path.join(self.sprites_dir, f"{anim}_right_{idx}.png")
                l_file = os.path.join(self.sprites_dir, f"{anim}_left_{idx}.png")
                if not os.path.exists(r_file):
                    break
                pix_r = QPixmap(r_file).scaled(
                    self.sprite_w, self.sprite_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                pix_l = QPixmap(l_file).scaled(
                    self.sprite_w, self.sprite_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.frames[anim]["right"].append(pix_r)
                self.frames[anim]["left"].append(pix_l)
                idx += 1

    def say(self, text: str, duration_ms=3800):
        pirate_rect = self.geometry()
        self.bubble.show_message(text, pirate_rect, duration_ms)

    def call_parrot_back(self):
        """Pirate whistles and commands the parrot to return to his shoulder."""
        if not self.parrot:
            return
        self.sound.play("whistle")
        self.say(get_quote("call_parrot"))
        self.parrot.return_to_pirate()

    def change_state(self, new_state: PirateState, duration=3.0):
        self.state = new_state
        self.frame_idx = 0
        self.state_time = 0.0
        self.state_duration = duration

        if new_state == PirateState.ATTACK:
            self.sound.play("sword")
        elif new_state == PirateState.CELEBRATE:
            self.sound.play("coin")
        elif new_state == PirateState.JUMP:
            self.sound.play("jump")
        elif new_state == PirateState.LAND:
            self.sound.play("land")
        elif new_state == PirateState.DRAGGED:
            self.sound.play("grab")
        elif new_state == PirateState.HANG_ICON:
            self.sound.play("grab")
            self.say(get_quote("icon"))

    # =========================================================================
    # PHYSICS & AI LOGIC
    # =========================================================================

    def _physics_tick(self):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        floor_y = float(avail.bottom() - self.sprite_h + 2)
        left_x = float(avail.left())
        right_x = float(avail.right() - self.sprite_w + 1)
        top_y = float(avail.top())

        dt = 0.03
        self.state_time += dt

        if self.state == PirateState.DRAGGED:
            return

        elif self.state == PirateState.HANG_ICON:
            # Hanging by hands from a desktop shortcut icon
            self.vx = 0.0
            self.vy = 0.0
            if self.state_time >= self.state_duration:
                # 50% pull up onto the icon, 50% drop down
                if random.random() < 0.55 and self.current_ledge:
                    self.y = float(self.current_ledge.top() - self.sprite_h + 2)
                    self.change_state(PirateState.IDLE, duration=2.0)
                    self.say("Виліз на ярлик!")
                else:
                    self.current_ledge = None
                    self.vx = 1.0 if self.facing == "right" else -1.0
                    self.vy = 1.0
                    self.change_state(PirateState.FALL)

        elif self.state == PirateState.IDLE:
            if self.state_time >= self.state_duration:
                self._choose_next_action()

        elif self.state == PirateState.WALK:
            dir_mult = 1.0 if self.facing == "right" else -1.0
            self.x += dir_mult * self.speed

            # Check if walking on a desktop icon ledge
            if self.current_ledge:
                ledge_l = float(self.current_ledge.left() - 10)
                ledge_r = float(self.current_ledge.right() - self.sprite_w + 10)
                if self.x <= ledge_l or self.x >= ledge_r:
                    # Stepped off icon ledge!
                    if random.random() < 0.45:
                        # Grab edge and hang!
                        self.change_state(PirateState.HANG_ICON, duration=random.uniform(2.5, 5.0))
                    else:
                        # Fall off icon
                        self.current_ledge = None
                        self.vy = 1.0
                        self.change_state(PirateState.FALL)
            else:
                # Walking on desktop taskbar/floor
                if self.x <= left_x:
                    self.x = left_x
                    if random.random() < 0.45:
                        self.climb_wall_side = "left"
                        self.facing = "right"
                        self.change_state(PirateState.CLIMB_WALL, duration=random.uniform(4.0, 9.0))
                    else:
                        self.facing = "right"
                elif self.x >= right_x:
                    self.x = right_x
                    if random.random() < 0.45:
                        self.climb_wall_side = "right"
                        self.facing = "left"
                        self.change_state(PirateState.CLIMB_WALL, duration=random.uniform(4.0, 9.0))
                    else:
                        self.facing = "left"

            if self.state_time >= self.state_duration:
                self._choose_next_action()

        elif self.state == PirateState.RUN:
            if self.is_chasing_girl and self.piratess:
                # Actively chasing pirate girl!
                dir_mult = 1.0 if self.piratess.x > self.x else -1.0
                self.facing = "right" if dir_mult > 0 else "left"
                chase_speed = self.speed * 1.65
                self.x += dir_mult * chase_speed

                # If girl is on an icon ledge higher up, leap towards her!
                if self.piratess.y < self.y - 30 and abs(self.piratess.x - self.x) < 130 and self.state != PirateState.JUMP:
                    self.vx = dir_mult * 3.8
                    self.vy = -13.5
                    self.change_state(PirateState.JUMP)

                # Catch check!
                import math
                dist = math.hypot(self.piratess.x - self.x, self.piratess.y - self.y)
                if dist < 55:
                    self.is_chasing_girl = False
                    self.piratess.trigger_kiss()
            else:
                dir_mult = 1.0 if self.facing == "right" else -1.0
                self.x += dir_mult * (self.speed * 2.1)

            if self.current_ledge:
                ledge_l = float(self.current_ledge.left() - 10)
                ledge_r = float(self.current_ledge.right() - self.sprite_w + 10)
                if self.x <= ledge_l or self.x >= ledge_r:
                    self.current_ledge = None
                    self.change_state(PirateState.FALL)
            else:
                if self.x <= left_x:
                    self.x = left_x
                    self.facing = "right"
                    if not self.is_chasing_girl:
                        self.change_state(PirateState.IDLE, duration=1.5)
                elif self.x >= right_x:
                    self.x = right_x
                    self.facing = "left"
                    if not self.is_chasing_girl:
                        self.change_state(PirateState.IDLE, duration=1.5)

            if self.state_time >= self.state_duration:
                self.is_chasing_girl = False
                self.change_state(PirateState.IDLE, duration=random.uniform(1.5, 3.0))

        elif self.state == PirateState.JUMP:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            self.x = max(left_x, min(right_x, self.x))

            if self.vy > 0:
                self.state = PirateState.FALL

            # Check landing on icon ledges
            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.sprite_w, self.sprite_h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                ledges = self.detector.get_all_ledges()
                self.current_ledge = next((r for r in ledges if abs(r.top() - self.sprite_h + 2 - ledge_y) < 6), None)
                self.change_state(PirateState.LAND, duration=0.25)
                if random.random() < 0.5:
                    self.say(get_quote("icon"))

            # Check ground hit
            elif self.y >= floor_y:
                self.y = floor_y
                self.current_ledge = None
                self.change_state(PirateState.LAND, duration=0.25)

        elif self.state == PirateState.FALL:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity
            self.vx *= 0.98

            self.x = max(left_x, min(right_x, self.x))

            # 1. Check if can cling/grab onto desktop icon with hands while falling!
            grab_ledge = self.detector.find_ledge_to_grab(self.x, self.y, self.sprite_w, self.sprite_h)
            if grab_ledge and random.random() < 0.40 and self.vy > 1.5:
                self.current_ledge = grab_ledge
                self.y = float(grab_ledge.bottom() - 15)
                self.change_state(PirateState.HANG_ICON, duration=random.uniform(3.0, 5.5))
                return

            # 2. Check landing on icon ledges
            ledge_y = self.detector.find_ledge_under(self.x, self.y, self.sprite_w, self.sprite_h, self.vy)
            if ledge_y is not None and self.vy > 0:
                self.y = ledge_y
                self.vx = 0.0
                self.vy = 0.0
                ledges = self.detector.get_all_ledges()
                self.current_ledge = next((r for r in ledges if abs(r.top() - self.sprite_h + 2 - ledge_y) < 6), None)
                self.change_state(PirateState.LAND, duration=0.3)
                if random.random() < 0.5:
                    self.say(get_quote("icon"))

            # 3. Ground hit
            elif self.y >= floor_y:
                self.y = floor_y
                self.vx = 0.0
                self.vy = 0.0
                self.current_ledge = None
                self.change_state(PirateState.LAND, duration=0.3)
                if random.random() < 0.4:
                    self.say(get_quote("land"))

        elif self.state == PirateState.LAND:
            if self.state_time >= self.state_duration:
                self.change_state(PirateState.IDLE, duration=random.uniform(1.0, 2.5))

        elif self.state == PirateState.CLIMB_WALL:
            climb_speed = 2.2
            self.y -= climb_speed
            self.current_ledge = None

            if self.climb_wall_side == "left":
                self.x = left_x
            else:
                self.x = right_x

            if self.y <= top_y + 10:
                self.y = top_y + 10
                if random.random() < 0.6:
                    self.change_state(PirateState.CLIMB_CEILING, duration=random.uniform(3.0, 7.0))
                else:
                    self.facing = "right" if self.climb_wall_side == "left" else "left"
                    self.vx = 4.5 if self.climb_wall_side == "left" else -4.5
                    self.vy = 2.0
                    self.change_state(PirateState.FALL)
                    self.say("Земля на горизонті!")

            elif self.state_time >= self.state_duration:
                self.facing = "right" if self.climb_wall_side == "left" else "left"
                self.vx = 3.0 if self.climb_wall_side == "left" else -3.0
                self.vy = 1.0
                self.change_state(PirateState.FALL)

        elif self.state == PirateState.CLIMB_CEILING:
            crawl_speed = 1.8
            dir_mult = 1.0 if self.facing == "right" else -1.0
            self.x += dir_mult * crawl_speed
            self.y = top_y + 5
            self.current_ledge = None

            if self.x <= left_x:
                self.facing = "right"
            elif self.x >= right_x:
                self.facing = "left"

            if self.state_time >= self.state_duration:
                self.vx = 0.0
                self.vy = 2.0
                self.change_state(PirateState.FALL)
                self.say("Людина за бортом!")

        elif self.state in (PirateState.ATTACK, PirateState.CELEBRATE):
            if self.state_time >= self.state_duration:
                self.change_state(PirateState.IDLE, duration=random.uniform(2.0, 4.0))

        elif self.state == PirateState.SLEEP:
            if self.state_time >= self.state_duration:
                self.change_state(PirateState.IDLE, duration=2.0)

        # Apply position to Qt widget
        self.move(int(self.x), int(self.y))

        # Update parrot shoulder position if perched
        if self.parrot and self.parrot.state.value == "perched":
            self.parrot.update_shoulder_position()

        if self.bubble.isVisible():
            self.bubble.adjust_size_and_position(self.geometry())

    def _choose_next_action(self):
        """Pirate AI: chooses next action with desktop icon awareness."""
        # Check if parrot is away on an icon, 30% chance to call him back!
        if self.parrot and self.parrot.state.value == "icon" and random.random() < 0.35:
            self.call_parrot_back()
            return

        r = random.random()
        if r < 0.40:
            self.facing = "left" if random.random() < 0.5 else "right"
            self.change_state(PirateState.WALK, duration=random.uniform(3.0, 7.0))
        elif r < 0.60:
            self.change_state(PirateState.IDLE, duration=random.uniform(2.0, 5.0))
        elif r < 0.78:
            # Jump! (Can jump towards desktop icons)
            self.facing = "left" if random.random() < 0.5 else "right"
            self.vx = 3.8 if self.facing == "right" else -3.8
            self.vy = -12.5  # Higher leap to reach icon shortcuts!
            self.current_ledge = None
            self.change_state(PirateState.JUMP)
        elif r < 0.88:
            self.facing = "left" if random.random() < 0.5 else "right"
            self.change_state(PirateState.RUN, duration=random.uniform(2.0, 4.0))
        elif r < 0.94:
            self.change_state(PirateState.ATTACK, duration=0.8)
        else:
            self.change_state(PirateState.SLEEP, duration=random.uniform(6.0, 14.0))

    # =========================================================================
    # ANIMATION TICK
    # =========================================================================

    def _anim_tick(self):
        anim_key = self.state.value
        # HANG_ICON uses dragged animation frames
        if self.state == PirateState.HANG_ICON:
            anim_key = "dragged"

        frames_list = self.frames.get(anim_key, {}).get(self.facing, [])
        if not frames_list:
            return

        self.frame_idx = (self.frame_idx + 1) % len(frames_list)
        self.update()

    def paintEvent(self, event):
        anim_key = self.state.value
        if self.state == PirateState.HANG_ICON:
            anim_key = "dragged"

        frames_list = self.frames.get(anim_key, {}).get(self.facing, [])
        if frames_list and self.frame_idx < len(frames_list):
            painter = QPainter(self)
            painter.drawPixmap(0, 0, frames_list[self.frame_idx])

    # =========================================================================
    # MOUSE INTERACTION & DRAG-AND-DROP
    # =========================================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_click_start = event.globalPosition().toPoint()
            self.drag_mouse_offset = event.globalPosition().toPoint() - self.pos()
            self.is_dragging = False
            self.drag_history = [(time.time(), event.globalPosition().toPoint())]

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            cur_pos = event.globalPosition().toPoint()
            dist = (cur_pos - self.drag_click_start).manhattanLength()

            if dist > 6 and not self.is_dragging:
                self.is_dragging = True
                self.current_ledge = None
                self.change_state(PirateState.DRAGGED)
                if random.random() < 0.6:
                    self.say(get_quote("dragged"))

            if self.is_dragging:
                new_pos = cur_pos - self.drag_mouse_offset
                self.x = float(new_pos.x())
                self.y = float(new_pos.y())
                self.move(int(self.x), int(self.y))

                if self.parrot and self.parrot.state.value == "perched":
                    self.parrot.update_shoulder_position()

                now = time.time()
                self.drag_history.append((now, cur_pos))
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
                else:
                    self.vx = 0.0
                    self.vy = 1.0

                if self.vx < -1:
                    self.facing = "left"
                elif self.vx > 1:
                    self.facing = "right"

                # Check if dropped next to piratess -> instant kiss!
                if self.piratess:
                    import math
                    dist = math.hypot(self.piratess.x - self.x, self.piratess.y - self.y)
                    if dist < 65:
                        self.piratess.trigger_kiss()
                        return

                self.change_state(PirateState.FALL)

            else:
                self._handle_click_reaction()

        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.change_state(PirateState.CELEBRATE, duration=1.6)
            self.say(get_quote("treasure"))

    def _handle_click_reaction(self):
        if self.state == PirateState.SLEEP:
            self.change_state(PirateState.IDLE, duration=2.0)
            self.say("Excuse me?! Хто будить президента?!")
            return

        actions = [PirateState.ATTACK, PirateState.JUMP, PirateState.CELEBRATE]
        chosen = random.choice(actions)

        if chosen == PirateState.JUMP:
            self.vy = -13.0
            self.vx = random.uniform(-4.0, 4.0)
            self.current_ledge = None
            self.change_state(PirateState.JUMP)
        elif chosen == PirateState.ATTACK:
            self.change_state(PirateState.ATTACK, duration=0.8)
        else:
            self.change_state(PirateState.CELEBRATE, duration=1.2)

        self.say(get_quote("click"))

    # =========================================================================
    # CONTEXT MENU
    # =========================================================================

    def _show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b221b;
                color: #f7e7ce;
                border: 2px solid #8d6238;
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
                background-color: #8d6238;
                color: #ffffff;
            }
            QMenu::separator {
                height: 1px;
                background-color: #553b26;
                margin: 4px 0px;
            }
        """)

        # Actions
        act_attack = menu.addAction("🫵  Ви звільнені! (You're fired!)")
        act_jump_icon = menu.addAction("🎯  Стрибнути на ярлик")
        act_romance = menu.addAction("💖  Почати романтичну погоню")
        act_kiss_now = menu.addAction("💋  Поцілуватися зараз")
        act_spawn_kid = menu.addAction("🍌  Покликати міньйона (BANANA!)")

        # Parrot menu actions
        if self.parrot and self.parrot.state.value != "perched":
            act_parrot_call = menu.addAction("📢  Покликати папугу назад")
        else:
            act_parrot_call = menu.addAction("🦜  Відпустити папугу політати")

        act_treasure = menu.addAction("💰  Пошукати капітал")
        sleep_text = "⏰  Розбудити" if self.state == PirateState.SLEEP else "💤  Подрімати (Сон)"
        act_sleep = menu.addAction(sleep_text)

        menu.addSeparator()

        # Scale submenu
        scale_menu = menu.addMenu("📏  Розмір персонажа")
        act_scale_15 = scale_menu.addAction("Маленький (1.5x)")
        act_scale_22 = scale_menu.addAction("Звичайний (2.2x - Рекомендовано)")
        act_scale_28 = scale_menu.addAction("Великий (2.8x)")
        act_scale_34 = scale_menu.addAction("Гігантський (3.4x)")

        # Sound toggle
        sound_text = "🔊  Звук: Увімкнено" if self.sound.enabled else "🔇  Звук: Вимкнено"
        act_sound = menu.addAction(sound_text)

        menu.addSeparator()

        act_home = menu.addAction("🇺🇸  Повернути на панель завдань")
        act_exit = menu.addAction("🚪  Вийти")

        action = menu.exec(global_pos)

        if action == act_attack:
            self.change_state(PirateState.ATTACK, duration=1.0)
            self.say("You're fired! 🫵")
        elif action == act_romance:
            if self.piratess:
                self.piratess.start_chase()
        elif action == act_kiss_now:
            if self.piratess:
                self.piratess.trigger_kiss()
        elif action == act_spawn_kid:
            if self.piratess:
                self.piratess.spawn_kid()
        elif action == act_jump_icon:
            ledges = self.detector.get_all_ledges()
            if ledges:
                target = random.choice(ledges)
                # Leap towards target icon
                dx = target.center().x() - (self.x + self.sprite_w / 2)
                self.vx = max(-10.0, min(10.0, dx * 0.05))
                self.vy = -14.0
                self.facing = "right" if self.vx >= 0 else "left"
                self.current_ledge = None
                self.change_state(PirateState.JUMP)
                self.say("Стрибаю на ярлик!")
        elif action == act_parrot_call:
            if self.parrot and self.parrot.state.value != "perched":
                self.call_parrot_back()
            elif self.parrot:
                self.parrot.take_flight_to_random_icon()
        elif action == act_treasure:
            self.change_state(PirateState.CELEBRATE, duration=1.5)
            self.say(get_quote("treasure"))
        elif action == act_sleep:
            if self.state == PirateState.SLEEP:
                self.change_state(PirateState.IDLE, duration=2.0)
                self.say("Я прокинувся! Курс на море!")
            else:
                self.change_state(PirateState.SLEEP, duration=20.0)
                self.say("Хр-рр... час поспати... Zzz...")
        elif action == act_scale_15:
            self.set_scale(1.5)
        elif action == act_scale_22:
            self.set_scale(2.2)
        elif action == act_scale_28:
            self.set_scale(2.8)
        elif action == act_scale_34:
            self.set_scale(3.4)
        elif action == act_sound:
            self.sound.set_enabled(not self.sound.enabled)
        elif action == act_home:
            self.init_position()
            self.change_state(PirateState.IDLE)
            self.say("Make Desktop Great Again! 🇺🇸")
        elif action == act_exit:
            self.close()
            if self.parrot:
                self.parrot.close()
            QApplication.quit()
