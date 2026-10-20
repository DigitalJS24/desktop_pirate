"""
Speech bubble widget for Desktop Pirate.
Displays pirate quotes in a parchment-style bubble floating above the mascot.
"""

from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QPainterPath
from PyQt6.QtWidgets import QWidget

class SpeechBubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Frameless, transparent, stays on top, tool tip mode (no focus stealing)
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.text = ""
        self.opacity = 1.0
        self.font = QFont("Segoe UI", 10, QFont.Weight.Bold)

        # Timers
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.start_fade)

        self.fade_timer = QTimer(self)
        self.fade_timer.setInterval(40)
        self.fade_timer.timeout.connect(self._step_fade)

    def show_message(self, text: str, pirate_rect, duration_ms=3800):
        self.text = text
        self.opacity = 1.0
        self.setWindowOpacity(1.0)
        self.fade_timer.stop()

        # Calculate required size based on font
        self.adjust_size_and_position(pirate_rect)
        self.show()
        self.raise_()
        self.hide_timer.start(duration_ms)

    def adjust_size_and_position(self, pirate_rect):
        # Measure text size
        from PyQt6.QtGui import QFontMetrics
        fm = QFontMetrics(self.font)
        padding_h = 24
        padding_v = 16
        tail_h = 10

        # Word wrap or max width
        max_w = 260
        bounding = fm.boundingRect(0, 0, max_w - padding_h, 1000, Qt.TextFlag.TextWordWrap, self.text)
        bubble_w = max(110, bounding.width() + padding_h)
        bubble_h = bounding.height() + padding_v + tail_h

        self.resize(bubble_w, bubble_h)

        # Position bubble horizontally centered above pirate
        bx = int(pirate_rect.center().x() - bubble_w // 2)
        by = int(pirate_rect.top() - bubble_h - 4)

        # Keep on screen if possible
        if pirate_rect.top() < bubble_h + 10:
            # If pirate is near ceiling, show bubble below him!
            by = int(pirate_rect.bottom() + 6)
            self.tail_at_bottom = False
        else:
            self.tail_at_bottom = True

        self.move(bx, by)
        self.update()

    def start_fade(self):
        self.fade_timer.start()

    def _step_fade(self):
        self.opacity -= 0.08
        if self.opacity <= 0.05:
            self.fade_timer.stop()
            self.hide()
        else:
            self.setWindowOpacity(self.opacity)

    def paintEvent(self, event):
        if not self.text:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        tail_h = 10

        # Background parchment colors
        c_parchment = QColor(255, 248, 225, 245)      # Light antique parchment
        c_border = QColor(90, 50, 20, 255)            # Pirate leather brown border
        c_text = QColor(35, 20, 10, 255)              # Dark ink

        path = QPainterPath()
        if getattr(self, "tail_at_bottom", True):
            box_rect = QRectF(2, 2, w - 4, h - tail_h - 4)
            path.addRoundedRect(box_rect, 10, 10)
            # Add tail pointing down to pirate
            tail_x = w / 2
            path.moveTo(tail_x - 8, h - tail_h - 2)
            path.lineTo(tail_x, h - 2)
            path.lineTo(tail_x + 8, h - tail_h - 2)
        else:
            # Tail at top
            box_rect = QRectF(2, tail_h + 2, w - 4, h - tail_h - 4)
            path.addRoundedRect(box_rect, 10, 10)
            tail_x = w / 2
            path.moveTo(tail_x - 8, tail_h + 2)
            path.lineTo(tail_x, 2)
            path.lineTo(tail_x + 8, tail_h + 2)

        # Shadow
        painter.save()
        painter.translate(2, 2)
        painter.fillPath(path, QColor(0, 0, 0, 45))
        painter.restore()

        # Draw bubble background & border
        painter.fillPath(path, c_parchment)
        pen = QPen(c_border, 2)
        painter.strokePath(path, pen)

        # Inner decorative border line
        inner_path = QPainterPath()
        if getattr(self, "tail_at_bottom", True):
            inner_rect = QRectF(5, 5, w - 10, h - tail_h - 10)
        else:
            inner_rect = QRectF(5, tail_h + 5, w - 10, h - tail_h - 10)
        inner_path.addRoundedRect(inner_rect, 7, 7)
        painter.strokePath(inner_path, QPen(QColor(180, 130, 80, 120), 1, Qt.PenStyle.DashLine))

        # Text
        painter.setFont(self.font)
        painter.setPen(c_text)
        text_rect = QRectF(8, 6 if getattr(self, "tail_at_bottom", True) else tail_h + 6, w - 16, h - tail_h - 12)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.text)

