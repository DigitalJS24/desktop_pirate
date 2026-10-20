"""
Main entry point for Desktop Pirate.
Initializes application, system tray icon, and launches:
- The Pirate Captain
- The Pirate Girl (Piratess)
- The Parrot Companion
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from pirate_window import PirateWindow
from parrot_window import ParrotWindow
from piratess_window import PiratessWindow
from minion_window import MinionWindow
from sprite_generator import generate_all_sprites
from parrot_sprite_generator import generate_parrot_sprites
from piratess_sprite_generator import generate_all_piratess_sprites
from minion_sprite_generator import generate_all_minion_sprites
from utils import get_asset_path


def create_tray_icon(app: QApplication, pirate: PirateWindow, piratess: PiratessWindow, parrot: ParrotWindow):
    icon_path = get_asset_path("sprites", "idle_right_0.png")
    if os.path.exists(icon_path):
        tray_icon = QSystemTrayIcon(QIcon(icon_path), app)
    else:
        tray_icon = QSystemTrayIcon(app)

    tray_menu = QMenu()
    tray_menu.setStyleSheet("""
        QMenu {
            background-color: #2b221b;
            color: #f7e7ce;
            border: 2px solid #8d6238;
            font-family: 'Segoe UI';
            font-size: 12px;
            font-weight: bold;
        }
        QMenu::item:selected {
            background-color: #8d6238;
            color: #ffffff;
        }
    """)

    act_say = tray_menu.addAction("🏴‍☠️  Покликати капітана")
    act_say.triggered.connect(lambda: pirate.say("Я тут, салаги! Робота кипить!"))

    act_chase = tray_menu.addAction("💖  Почати романтичну погоню")
    act_chase.triggered.connect(lambda: piratess.start_chase())

    act_kiss = tray_menu.addAction("💋  Поцілуватися зараз")
    act_kiss.triggered.connect(lambda: piratess.trigger_kiss())

    act_kid = tray_menu.addAction("🍌  Покликати міньйона (BANANA!)")
    act_kid.triggered.connect(lambda: piratess.spawn_minion())

    act_clear_kids = tray_menu.addAction("🧹  Прибрати міньйонів")
    act_clear_kids.triggered.connect(lambda: piratess.clear_all_kids())

    tray_menu.addSeparator()

    act_call_parrot = tray_menu.addAction("🦜  Покликати папугу")
    act_call_parrot.triggered.connect(lambda: pirate.call_parrot_back())

    act_fly_parrot = tray_menu.addAction("🪶  Відпустити папугу політати")
    act_fly_parrot.triggered.connect(lambda: parrot.take_flight_to_random_icon())

    tray_menu.addSeparator()

    act_home = tray_menu.addAction("⚓  Повернути всіх на робочий стіл")
    def return_all():
        pirate.init_position()
        piratess.init_position()
    act_home.triggered.connect(return_all)

    tray_menu.addSeparator()

    act_exit = tray_menu.addAction("🚪  Вийти")
    act_exit.triggered.connect(app.quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.setToolTip("Десктопний Пірат, Піратка та Папуга")
    tray_icon.show()
    return tray_icon


def main():
    # High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Pirate")
    app.setQuitOnLastWindowClosed(False)

    # Ensure pirate sprites exist
    sprites_dir = get_asset_path("sprites")
    if not os.path.exists(sprites_dir) or not os.listdir(sprites_dir):
        print("Generating pirate sprite assets...")
        generate_all_sprites(sprites_dir)

    # Ensure parrot sprites exist
    parrot_sprites_dir = os.path.join(sprites_dir, "parrot")
    if not os.path.exists(parrot_sprites_dir) or not os.listdir(parrot_sprites_dir):
        print("Generating parrot sprite assets...")
        generate_parrot_sprites(parrot_sprites_dir)

    # Ensure piratess sprites exist
    piratess_sprites_dir = os.path.join(sprites_dir, "piratess")
    if not os.path.exists(piratess_sprites_dir) or not os.listdir(piratess_sprites_dir):
        print("Generating piratess sprite assets...")
        generate_all_piratess_sprites(piratess_sprites_dir)

    # Ensure minion sprites exist
    minion_sprites_dir = os.path.join(sprites_dir, "minion")
    if not os.path.exists(minion_sprites_dir) or not os.listdir(minion_sprites_dir):
        print("Generating minion sprite assets...")
        generate_all_minion_sprites(minion_sprites_dir)

    # 1. Create Pirate mascot (scale 2.2)
    pirate = PirateWindow(sprites_dir=sprites_dir, scale=2.2)
    pirate.show()

    # 2. Create Pirate Girl (scale 2.1)
    piratess = PiratessWindow(pirate=pirate, sound_mgr=pirate.sound, scale=2.1)
    pirate.set_piratess(piratess)
    piratess.show()

    # 3. Create Parrot companion (scale 2.0)
    parrot = ParrotWindow(pirate=pirate, sound_mgr=pirate.sound, scale=2.0)
    pirate.set_parrot(parrot)
    parrot.show()

    tray = create_tray_icon(app, pirate, piratess, parrot)

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        log_path = os.path.join(os.path.dirname(sys.executable), "crash.log")
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        with open("crash.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
