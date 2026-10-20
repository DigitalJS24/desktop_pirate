"""
Desktop icon locator and ledge detector.
Finds desktop shortcut coordinates on Windows and macOS so the pirate, parrot, and minions
can hang, stand, and jump on them!
"""

import os
import sys
import ctypes
from ctypes import wintypes
from PyQt6.QtCore import QRect, QPoint
from PyQt6.QtWidgets import QApplication

# Conditional imports for Windows
if sys.platform == "win32":
    try:
        import win32gui
        import win32process
        import win32con
        HAS_WIN32 = True
    except ImportError:
        HAS_WIN32 = False
else:
    HAS_WIN32 = False

# Win32 ListView messages
LVM_FIRST = 0x1000
LVM_GETITEMCOUNT = LVM_FIRST + 4
LVM_GETITEMRECT = LVM_FIRST + 14
LVIR_BOUNDS = 0

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG)
    ]

class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG)
    ]


class DesktopIconDetector:
    def __init__(self):
        self.cached_rects = []
        self.last_update = 0

    def get_desktop_listview(self):
        """Finds the desktop SysListView32 handle on Windows."""
        if not HAS_WIN32:
            return None
        progman = win32gui.FindWindow("Progman", None)
        shelldll = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
        if not shelldll:
            def enum_proc(hwnd, extra):
                if win32gui.GetClassName(hwnd) == "WorkerW":
                    child = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
                    if child:
                        extra.append(child)
                return True
            extra = []
            win32gui.EnumWindows(enum_proc, extra)
            if extra:
                shelldll = extra[0]
        if shelldll:
            return win32gui.FindWindowEx(shelldll, 0, "SysListView32", None)
        return None

    def get_icon_rects_win32(self):
        """Extracts exact icon rectangles using Win32 API memory mapping."""
        if not HAS_WIN32:
            return []
        hwnd = self.get_desktop_listview()
        if not hwnd:
            return []

        count = win32gui.SendMessage(hwnd, LVM_GETITEMCOUNT, 0, 0)
        if count <= 0:
            return []

        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        PROCESS_ALL_ACCESS = 0x1F0FFF
        kernel32 = ctypes.windll.kernel32
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not h_process:
            return []

        rects = []
        try:
            # Allocate memory inside Explorer process for RECT
            MEM_COMMIT = 0x1000
            MEM_RELEASE = 0x8000
            PAGE_READWRITE = 0x04
            remote_mem = kernel32.VirtualAllocEx(h_process, None, ctypes.sizeof(RECT), MEM_COMMIT, PAGE_READWRITE)
            if not remote_mem:
                return []

            local_rect = RECT()
            local_rect.left = LVIR_BOUNDS

            # Cap at first 60 icons for high performance
            max_check = min(count, 60)
            for i in range(max_check):
                # Write initial request to remote memory
                kernel32.WriteProcessMemory(h_process, remote_mem, ctypes.byref(local_rect), ctypes.sizeof(RECT), None)
                # Send LVM_GETITEMRECT message
                res = win32gui.SendMessage(hwnd, LVM_GETITEMRECT, i, remote_mem)
                if res:
                    read_bytes = ctypes.c_size_t(0)
                    kernel32.ReadProcessMemory(h_process, remote_mem, ctypes.byref(local_rect), ctypes.sizeof(RECT), ctypes.byref(read_bytes))
                    w = local_rect.right - local_rect.left
                    h = local_rect.bottom - local_rect.top
                    if 10 < w < 400 and 10 < h < 400:
                        rects.append(QRect(local_rect.left, local_rect.top, w, h))

            kernel32.VirtualFreeEx(h_process, remote_mem, 0, MEM_RELEASE)
        finally:
            kernel32.CloseHandle(h_process)

        return rects

    def get_icon_rects_grid_fallback(self):
        """
        Calculates desktop icon positions using standard Windows desktop grid
        if remote memory access is restricted.
        """
        screen = QApplication.primaryScreen()
        if not screen:
            return []
        avail = screen.availableGeometry()

        # Count actual shortcuts in Desktop folders
        user_desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
        public_desktop = os.path.join(os.environ.get("PUBLIC", "C:\\Users\\Public"), "Desktop")
        count = 0
        if os.path.exists(user_desktop):
            count += len([f for f in os.listdir(user_desktop) if not f.startswith(".")])
        if os.path.exists(public_desktop):
            count += len([f for f in os.listdir(public_desktop) if not f.startswith(".")])

        count = max(8, min(count, 60))

        # Standard Windows 10/11 icon grid layout
        icon_w, icon_h = 75, 75
        step_x, step_y = 78, 86
        margin_x, margin_y = avail.left() + 10, avail.top() + 10

        max_rows = max(1, (avail.height() - 40) // step_y)
        rects = []
        for i in range(count):
            col = i // max_rows
            row = i % max_rows
            x = margin_x + col * step_x
            y = margin_y + row * step_y
            rects.append(QRect(x, y, icon_w, icon_h))
        return rects

    def get_mac_icon_rects(self):
        """
        Calculates desktop icon positions on macOS Finder.
        By default, macOS Finder aligns icons in columns starting from the top-right corner.
        """
        screen = QApplication.primaryScreen()
        if not screen:
            return []
        avail = screen.availableGeometry()

        dt_path = os.path.expanduser("~/Desktop")
        count = 0
        if os.path.exists(dt_path):
            count = len([f for f in os.listdir(dt_path) if not f.startswith(".")])
        count = max(4, min(count, 40))

        # Standard macOS desktop icon size & spacing
        icon_w, icon_h = 70, 75
        step_x, step_y = 80, 85
        margin_right = avail.right() - 85
        margin_top = avail.top() + 30  # Below macOS top menu bar

        max_rows = max(1, (avail.height() - 70) // step_y)
        rects = []
        for i in range(count):
            col = i // max_rows
            row = i % max_rows
            x = margin_right - col * step_x
            y = margin_top + row * step_y
            rects.append(QRect(x, y, icon_w, icon_h))
        return rects

    def get_all_ledges(self):
        """Returns all desktop icon bounding boxes as ledges for the pirate."""
        import time
        now = time.time()
        if now - self.last_update < 4.0 and self.cached_rects:
            return self.cached_rects

        if sys.platform == "darwin":
            rects = self.get_mac_icon_rects()
        elif sys.platform == "win32":
            rects = self.get_icon_rects_win32() or self.get_icon_rects_grid_fallback()
        else:
            rects = self.get_icon_rects_grid_fallback()

        self.cached_rects = rects
        self.last_update = now
        return rects

    def find_ledge_under(self, px, py, pw, ph, vy):
        """
        Checks if the pirate's feet (px, py + ph) are landing on top of any icon ledge.
        Returns the top Y coordinate of the ledge if landed, or None.
        """
        ledges = self.get_all_ledges()
        feet_y = py + ph
        pirate_center_x = px + pw / 2

        for r in ledges:
            # Check horizontal overlap
            if (r.left() - pw * 0.4) <= pirate_center_x <= (r.right() + pw * 0.4):
                # Check if falling onto the top of the icon (within landing threshold)
                top = r.top()
                if (top - 12) <= feet_y <= (top + 16) and vy >= 0:
                    return top - ph + 2
        return None

    def find_ledge_to_grab(self, px, py, pw, ph):
        """
        Checks if the pirate is close to an icon to hang/cling onto it with hands.
        """
        ledges = self.get_all_ledges()
        for r in ledges:
            # Hands at py + 15
            if r.contains(int(px + pw / 2), int(py + 15)):
                return r
        return None

