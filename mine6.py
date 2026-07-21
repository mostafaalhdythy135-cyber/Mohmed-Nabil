import sys
import random
import math

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QFrame,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPointF,
    QRectF,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QLinearGradient,
    QRadialGradient,
    QFont,
    QPixmap,
)


# =========================================================
# FULL PROSTHETIC ARM
# =========================================================

class ProstheticArmWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(200, 300)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.arm_label = QLabel(self)
        self.arm_label.setAlignment(Qt.AlignCenter)
        self.arm_label.setStyleSheet("background: transparent; border: none;")

        # تحميل arm.png من نفس مجلد ملف main.py
        self.original_pixmap = QPixmap()

        if self.original_pixmap.isNull():
            self.arm_label.setText("arm.png not found")
            self.arm_label.setStyleSheet("color: #1A237E; background: transparent; border: none;")

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.arm_label.setGeometry(self.rect())

        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.arm_label.setPixmap(scaled_pixmap)

    def start_arm(self):
        pass

    def stop_arm(self):
        pass


# =========================================================
# NEURAL PROCESSING FLOW
# =========================================================

class NeuralFlowWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(105)
        self.setMaximumHeight(115)

        self.progress = 0.0
        self.flow_active = True

        self.stage_names = [
            "HUMAN INTENT",
            "EMG SENSORS",
            "AI CORTEX",
            "MOTOR CONTROL",
            "FEEDBACK",
        ]

        self.stage_subtitles = [
            "INTENTION",
            "SIGNAL",
            "DECISION",
            "COMMAND",
            "RESPONSE",
        ]

        self.stage_colors = [
            QColor("#64F5A2"),
            QColor("#58E8FF"),
            QColor("#FFB75D"),
            QColor("#58E8FF"),
            QColor("#C77DFF"),
        ]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_flow)
        self.timer.start(25)

    def animate_flow(self):
        if not self.flow_active:
            return

        self.progress += 0.007

        if self.progress >= 1.0:
            self.progress = 0.0

        self.update()

    def start_flow(self):
        self.flow_active = True
        if not self.timer.isActive():
            self.timer.start(25)

    def stop_flow(self):
        self.flow_active = False

    def reset_flow(self):
        self.progress = 0.0
        self.update()

    def draw_stage_icon(self, painter, index, center, color):
        painter.save()
        painter.translate(center)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(
            QPen(
                color,
                2,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )

        if index == 0:
            painter.drawEllipse(QPointF(0, -7), 6, 7)
            painter.drawArc(QRectF(-11, 1, 22, 18), 0, 180 * 16)

        elif index == 1:
            signal_path = QPainterPath()
            signal_path.moveTo(-14, 1)
            signal_path.lineTo(-9, 1)
            signal_path.lineTo(-5, -7)
            signal_path.lineTo(0, 10)
            signal_path.lineTo(5, -5)
            signal_path.lineTo(9, 1)
            signal_path.lineTo(14, 1)
            painter.drawPath(signal_path)

        elif index == 2:
            painter.drawEllipse(QRectF(-12, -10, 24, 20))
            painter.drawLine(-2, -9, -2, 9)
            painter.drawLine(-9, -4, -2, 0)
            painter.drawLine(8, -4, -2, 0)
            painter.drawLine(-2, 0, 7, 6)

            painter.setBrush(color)
            painter.drawEllipse(QPointF(-9, -4), 2, 2)
            painter.drawEllipse(QPointF(8, -4), 2, 2)
            painter.drawEllipse(QPointF(7, 6), 2, 2)

        elif index == 3:
            painter.drawEllipse(QPointF(0, 0), 10, 10)
            painter.drawEllipse(QPointF(0, 0), 4, 4)

            for angle in range(0, 360, 45):
                radians = math.radians(angle)
                start_point = QPointF(
                    math.cos(radians) * 11,
                    math.sin(radians) * 11,
                )
                end_point = QPointF(
                    math.cos(radians) * 16,
                    math.sin(radians) * 16,
                )
                painter.drawLine(start_point, end_point)

        else:
            painter.drawArc(QRectF(-13, -13, 26, 26), 35 * 16, 285 * 16)
            painter.drawLine(QPointF(-12, -6), QPointF(-16, -1))
            painter.drawLine(QPointF(-12, -6), QPointF(-7, -5))

        painter.restore()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        painter.fillRect(self.rect(), QColor("#081724"))

        painter.setPen(QPen(QColor(35, 105, 135, 35), 1))
        for x in range(0, width, 28):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, 22):
            painter.drawLine(0, y, width, y)

        margin = 55
        line_y = 41
        available_width = max(1, width - margin * 2)
        stage_spacing = available_width / 4

        stage_points = [
            QPointF(margin + index * stage_spacing, line_y)
            for index in range(5)
        ]

        painter.setPen(
            QPen(
                QColor("#17465B"),
                6,
                Qt.SolidLine,
                Qt.RoundCap,
            )
        )
        painter.drawLine(stage_points[0], stage_points[-1])

        packet_x = (
            stage_points[0].x()
            + (stage_points[-1].x() - stage_points[0].x()) * self.progress
        )

        packet_position = self.progress * 4
        current_stage = min(4, int(packet_position + 0.25))
        current_color = self.stage_colors[current_stage]

        painter.setPen(
            QPen(
                QColor(
                    current_color.red(),
                    current_color.green(),
                    current_color.blue(),
                    70,
                ),
                11,
                Qt.SolidLine,
                Qt.RoundCap,
            )
        )
        painter.drawLine(stage_points[0], QPointF(packet_x, line_y))

        painter.setPen(
            QPen(
                current_color,
                2,
                Qt.SolidLine,
                Qt.RoundCap,
            )
        )
        painter.drawLine(stage_points[0], QPointF(packet_x, line_y))

        for index, point in enumerate(stage_points):
            color = self.stage_colors[index]
            distance = abs(packet_position - index)
            glow_strength = max(0.0, 1.0 - distance * 1.7)

            glow = QRadialGradient(point, 34)
            glow.setColorAt(
                0,
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    int(130 * glow_strength),
                ),
            )
            glow.setColorAt(
                1,
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    0,
                ),
            )

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(point, 34, 34)

            circle_radius = 22 + glow_strength * 3
            painter.setBrush(QColor("#0A202D"))
            painter.setPen(QPen(color, 2 + glow_strength))
            painter.drawEllipse(point, circle_radius, circle_radius)

            self.draw_stage_icon(painter, index, point, color)

            painter.setFont(QFont("Segoe UI", 7, QFont.Bold))
            painter.setPen(
                QColor("#FFFFFF")
                if glow_strength > 0.25
                else QColor("#8AA8B8")
            )
            painter.drawText(
                QRectF(point.x() - 62, 68, 124, 16),
                Qt.AlignCenter,
                self.stage_names[index],
            )

            painter.setFont(QFont("Segoe UI", 6))
            if glow_strength > 0.30:
                status_text = "PROCESSING"
                painter.setPen(color)
            else:
                status_text = self.stage_subtitles[index]
                painter.setPen(QColor("#536D7C"))

            painter.drawText(
                QRectF(point.x() - 55, 86, 110, 14),
                Qt.AlignCenter,
                status_text,
            )

        packet_point = QPointF(packet_x, line_y)
        packet_glow = QRadialGradient(packet_point, 22)
        packet_glow.setColorAt(0, QColor(255, 255, 255, 255))
        packet_glow.setColorAt(
            0.25,
            QColor(
                current_color.red(),
                current_color.green(),
                current_color.blue(),
                220,
            ),
        )
        packet_glow.setColorAt(
            1,
            QColor(
                current_color.red(),
                current_color.green(),
                current_color.blue(),
                0,
            ),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(packet_glow))
        painter.drawEllipse(packet_point, 22, 22)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(packet_point, 4.5, 4.5)


# =========================================================
# EMG SIGNAL GRAPH
# =========================================================

class EMGGraph(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(110)

        self.values = [0.5] * 190
        self.signal_active = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_signal)
        self.timer.start(35)

    def update_signal(self):
        if not self.signal_active:
            return

        new_value = 0.5 + random.uniform(-0.025, 0.025)

        if random.random() < 0.09:
            pulse = random.uniform(0.18, 0.39)

            if random.random() < 0.5:
                pulse *= -1

            new_value += pulse

        new_value = max(0.06, min(0.94, new_value))

        self.values.append(new_value)
        self.values.pop(0)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        painter.fillRect(self.rect(), QColor("#071520"))

        painter.setPen(QPen(QColor("#163C50"), 1))

        for x in range(0, width, 35):
            painter.drawLine(x, 0, x, height)

        for y in range(0, height, 25):
            painter.drawLine(0, y, width, y)

        painter.setPen(QPen(QColor("#28617A"), 1))
        painter.drawLine(0, height // 2, width, height // 2)

        path = QPainterPath()

        step = width / (len(self.values) - 1)

        first_y = height - self.values[0] * height
        path.moveTo(0, first_y)

        for index, value in enumerate(self.values):
            x = index * step
            y = height - value * height
            path.lineTo(x, y)

        painter.setPen(QPen(QColor(78, 235, 224, 65), 8))
        painter.drawPath(path)

        painter.setPen(QPen(QColor("#58F0DF"), 2))
        painter.drawPath(path)

    def start_signal(self):
        self.signal_active = True

    def stop_signal(self):
        self.signal_active = False


# =========================================================
# SMALL INFORMATION CARD
# =========================================================

class InfoCard(QFrame):

    def __init__(self, title, value, status):
        super().__init__()

        self.setObjectName("smallCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 7, 12, 7)
        layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #85A6B9;
            font-size: 11px;
        """)

        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("""
            color: #54E7FF;
            font-size: 18px;
            font-weight: 700;
        """)

        status_label = QLabel(status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("""
            color: #74F0A3;
            font-size: 10px;
            font-weight: 600;
        """)

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(status_label)


# =========================================================
# CIRCULAR GAUGE
# =========================================================

class CircularGauge(QWidget):

    def __init__(self, title, value=0, max_value=100, color="#56E5F5", suffix="%"):
        super().__init__()
        self.title = title
        self.value = value
        self.max_value = max_value
        self.color = QColor(color)
        self.suffix = suffix
        self.setMinimumSize(150, 150)

    def setValue(self, value):
        self.value = max(0, min(self.max_value, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        side = min(self.width(), self.height())
        rect = QRectF(18, 30, side - 36, side - 36)

        painter.setPen(QPen(QColor("#17384B"), 13, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 90 * 16, -300 * 16)

        span = int(-300 * 16 * (self.value / self.max_value))
        painter.setPen(QPen(self.color, 13, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 90 * 16, span)

        painter.setPen(QColor("#B7D6E6"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(QRectF(0, 0, self.width(), 28), Qt.AlignCenter, self.title)

        painter.setPen(self.color)
        painter.setFont(QFont("Segoe UI", 19, QFont.Bold))
        value_text = f"{self.value:.1f}{self.suffix}" if isinstance(self.value, float) else f"{self.value}{self.suffix}"
        painter.drawText(rect, Qt.AlignCenter, value_text)


# =========================================================
# MAIN DASHBOARD
# =========================================================

class Dashboard(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NeuroGenesis Dashboard")
        self.resize(1450, 900)
        self.setMinimumSize(1150, 720)

        self.system_running = True
        self.force_number = 12.5
        self.accuracy_number = 98.7

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        self.setStyleSheet("""
            QWidget#central {
                background-color: #06111C;
                color: white;
                font-family: "Segoe UI";
            }

            QFrame#header,
            QFrame#card,
            QFrame#armCard,
            QFrame#emgCard,
            QFrame#smallCard,
            QFrame#controlsCard {
                background-color: #0D1D2C;
                border: 1px solid #285A73;
                border-radius: 16px;
            }

            QFrame#armCard {
                background-color: #081724;
                border: 1px solid #43ADD8;
                border-radius: 20px;
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QLabel#sectionTitle {
                color: #EDF9FF;
                font-size: 16px;
                font-weight: 700;
            }

            QLabel#mainValue {
                color: #55E8FF;
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#orangeValue {
                color: #FFB75D;
                font-size: 24px;
                font-weight: 700;
            }

            QLabel#greenStatus {
                color: #76F0A2;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#normalText {
                color: #A7C2D1;
                font-size: 12px;
            }

            QLabel#fingerOpen {
                color: #7CFFAA;
                background-color: #0E3025;
                border: 1px solid #397C5B;
                border-radius: 8px;
                padding: 7px;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#fingerClosed {
                color: #FFC176;
                background-color: #312318;
                border: 1px solid #8A6031;
                border-radius: 8px;
                padding: 7px;
                font-size: 12px;
                font-weight: 600;
            }

            QProgressBar {
                background-color: #07141F;
                border: 1px solid #2A5971;
                border-radius: 7px;
                height: 14px;
                color: white;
                text-align: center;
                font-size: 10px;
                font-weight: 600;
            }

            QProgressBar::chunk {
                background-color: #56E5F5;
                border-radius: 6px;
            }

            QPushButton {
                background-color: #173A52;
                color: white;
                border: 1px solid #357A9D;
                border-radius: 9px;
                padding: 9px 15px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #215675;
                border: 1px solid #5BE6FF;
            }

            QPushButton#startButton {
                background-color: #1C823D;
                border: 1px solid #59D881;
            }

            QPushButton#stopButton {
                background-color: #C17B13;
                border: 1px solid #F2B44B;
            }

            QPushButton#emergencyButton {
                background-color: #C83246;
                border: 1px solid #FF6577;
            }
        """)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        # Header
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(78)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(22, 8, 22, 8)

        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(0)

        logo = QLabel("NeuroGenesis")
        logo.setStyleSheet("""
            color: #59E5FF;
            font-size: 25px;
            font-weight: 700;
        """)

        logo_description = QLabel("AI Prosthetic Control")
        logo_description.setStyleSheet("""
            color: #7F9EAF;
            font-size: 10px;
        """)

        logo_layout.addWidget(logo)
        logo_layout.addWidget(logo_description)

        title = QLabel("INTELLIGENT PROSTHETIC CONTROL SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1px;
        """)

        status_layout = QVBoxLayout()
        status_layout.setSpacing(1)

        self.connection_status = QLabel("● SYSTEM ONLINE")
        self.connection_status.setAlignment(Qt.AlignRight)
        self.connection_status.setStyleSheet("""
            color: #76F0A2;
            font-size: 12px;
            font-weight: 700;
        """)

        device_label = QLabel("ESP32  •  EMG SENSOR")
        device_label.setAlignment(Qt.AlignRight)
        device_label.setStyleSheet("""
            color: #7F9EAF;
            font-size: 9px;
        """)

        status_layout.addWidget(self.connection_status)
        status_layout.addWidget(device_label)

        header_layout.addLayout(logo_layout)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)

        main_layout.addWidget(header)

        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        # Left card: static arm2.png image
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        arm2_card = QFrame()
        arm2_card.setObjectName("card")
        arm2_layout = QVBoxLayout(arm2_card)
        arm2_layout.setContentsMargins(10, 10, 10, 10)

        arm2_title = QLabel("PROSTHETIC ARM")
        arm2_title.setObjectName("sectionTitle")
        arm2_title.setAlignment(Qt.AlignCenter)

        self.arm2_label = QLabel()
        self.arm2_label.setAlignment(Qt.AlignCenter)
        self.arm2_label.setStyleSheet("background: transparent; border: none;")

        self.arm2_label.setText("Image removed")

        arm2_layout.addWidget(arm2_title)
        arm2_layout.addWidget(self.arm2_label, 1)
        left_layout.addWidget(arm2_card)

        # Center arm
        arm_card = QFrame()
        arm_card.setObjectName("armCard")

        arm_layout = QVBoxLayout(arm_card)
        arm_layout.setContentsMargins(10, 10, 10, 10)

        arm_header = QHBoxLayout()

        arm_title = QLabel("DIGITAL PROSTHETIC MODEL")
        arm_title.setObjectName("sectionTitle")

        live_label = QLabel("● LIVE")
        live_label.setStyleSheet("""
            color: #7CFFAA;
            background-color: #113526;
            border: 1px solid #397C5B;
            border-radius: 8px;
            padding: 4px 9px;
            font-size: 10px;
            font-weight: 700;
        """)

        arm_header.addWidget(arm_title)
        arm_header.addStretch()
        arm_header.addWidget(live_label)

        self.arm_widget = ProstheticArmWidget()
        self.neural_flow = NeuralFlowWidget()

        arm_layout.addLayout(arm_header)
        arm_layout.addWidget(self.arm_widget, 1)
        arm_layout.addWidget(self.neural_flow)

        # Right card: grip force + AI accuracy circular gauges
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        metrics_card = QFrame()
        metrics_card.setObjectName("card")
        metrics_layout = QVBoxLayout(metrics_card)
        metrics_layout.setContentsMargins(10, 12, 10, 12)
        metrics_layout.setSpacing(8)

        metrics_title = QLabel("LIVE AI METRICS")
        metrics_title.setObjectName("sectionTitle")
        metrics_title.setAlignment(Qt.AlignCenter)

        gauges_layout = QHBoxLayout()
        gauges_layout.setSpacing(4)

        self.force_gauge = CircularGauge("GRIP FORCE", 42, 100, "#FFD21F", "%")
        self.ai_gauge = CircularGauge("AI ACCURACY", 98.7, 100, "#56E5F5", "%")

        gauges_layout.addWidget(self.force_gauge)
        gauges_layout.addWidget(self.ai_gauge)

        metrics_status = QLabel("● REAL-TIME ANALYSIS ACTIVE")
        metrics_status.setObjectName("greenStatus")
        metrics_status.setAlignment(Qt.AlignCenter)

        metrics_layout.addWidget(metrics_title)
        metrics_layout.addLayout(gauges_layout)
        metrics_layout.addWidget(metrics_status)

        # Movement control table (placed in the empty area under the gauges)
        movement_frame = QFrame()
        movement_frame.setStyleSheet("""
            QFrame {
                background-color: #091925;
                border: 1px solid #24546C;
                border-radius: 12px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        movement_layout = QVBoxLayout(movement_frame)
        movement_layout.setContentsMargins(10, 8, 10, 9)
        movement_layout.setSpacing(5)

        movement_title = QLabel("MOVEMENT CONTROL")
        movement_title.setAlignment(Qt.AlignCenter)
        movement_title.setStyleSheet("""
            color: #59E5FF;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        movement_layout.addWidget(movement_title)

        movement_grid = QGridLayout()
        movement_grid.setContentsMargins(2, 2, 2, 2)
        movement_grid.setHorizontalSpacing(8)
        movement_grid.setVerticalSpacing(4)

        movement_items = [
            ("HAND GRIP", "READY"),
            ("HAND OPEN", "READY"),
            ("WRIST RIGHT", "READY"),
            ("WRIST LEFT", "READY"),
            ("WRIST UP", "READY"),
            ("WRIST DOWN", "READY"),
            ("ELBOW FLEXION", "READY"),
            ("ELBOW EXTENSION", "READY"),
        ]

        self.movement_status_labels = {}

        for row, (movement_name, movement_state) in enumerate(movement_items):
            name_label = QLabel(movement_name)
            name_label.setStyleSheet("""
                color: #B7D6E6;
                font-size: 10px;
                font-weight: 600;
                padding: 3px 2px;
            """)

            state_label = QLabel(f"● {movement_state}")
            state_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            state_label.setStyleSheet("""
                color: #76F0A2;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 2px;
            """)

            movement_grid.addWidget(name_label, row, 0)
            movement_grid.addWidget(state_label, row, 1)
            self.movement_status_labels[movement_name] = state_label

        movement_grid.setColumnStretch(0, 1)
        movement_layout.addLayout(movement_grid)
        metrics_layout.addWidget(movement_frame, 1)

        right_layout.addWidget(metrics_card)

        content_layout.addLayout(left_layout, 2)
        content_layout.addWidget(arm_card, 5)
        content_layout.addLayout(right_layout, 2)

        main_layout.addLayout(content_layout, 1)

        # EMG graph
        emg_card = QFrame()
        emg_card.setObjectName("emgCard")
        emg_card.setFixedHeight(150)

        emg_layout = QVBoxLayout(emg_card)
        emg_layout.setContentsMargins(14, 7, 14, 9)
        emg_layout.setSpacing(3)

        emg_header = QHBoxLayout()

        emg_title = QLabel("REAL-TIME EMG MUSCLE SIGNAL")
        emg_title.setObjectName("sectionTitle")

        self.emg_status = QLabel("● SIGNAL ACTIVE")
        self.emg_status.setObjectName("greenStatus")

        emg_header.addWidget(emg_title)
        emg_header.addStretch()
        emg_header.addWidget(self.emg_status)

        self.emg_graph = EMGGraph()

        emg_layout.addLayout(emg_header)
        emg_layout.addWidget(self.emg_graph)

        main_layout.addWidget(emg_card)

        # Bottom information
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(8)

        self.battery_card = InfoCard(
            "BATTERY",
            "87%",
            "NORMAL"
        )

        self.temperature_card = InfoCard(
            "TEMPERATURE",
            "34°C",
            "SAFE"
        )

        self.signal_card = InfoCard(
            "EMG SIGNAL",
            "ACTIVE",
            "GOOD"
        )

        self.esp_card = InfoCard(
            "ESP32",
            "CONNECTED",
            "ONLINE"
        )

        controls_card = QFrame()
        controls_card.setObjectName("controlsCard")

        controls_layout = QHBoxLayout(controls_card)
        controls_layout.setContentsMargins(9, 7, 9, 7)
        controls_layout.setSpacing(7)

        start_button = QPushButton("▶ START")
        start_button.setObjectName("startButton")

        stop_button = QPushButton("■ STOP")
        stop_button.setObjectName("stopButton")

        calibration_button = QPushButton("⚙ CALIBRATE")

        emergency_button = QPushButton("EMERGENCY")
        emergency_button.setObjectName("emergencyButton")

        start_button.clicked.connect(self.start_system)
        stop_button.clicked.connect(self.stop_system)
        calibration_button.clicked.connect(self.calibrate_system)
        emergency_button.clicked.connect(self.emergency_stop)

        controls_layout.addWidget(start_button)
        controls_layout.addWidget(stop_button)
        controls_layout.addWidget(calibration_button)
        controls_layout.addWidget(emergency_button)

        bottom_layout.addWidget(self.battery_card)
        bottom_layout.addWidget(self.temperature_card)
        bottom_layout.addWidget(self.signal_card)
        bottom_layout.addWidget(self.esp_card)
        bottom_layout.addWidget(controls_card, 2)

        main_layout.addLayout(bottom_layout)

        # Automatic demo data
        self.data_timer = QTimer(self)
        self.data_timer.timeout.connect(self.update_dashboard)
        self.data_timer.start(900)

    def set_finger_state(self, label, name, is_open):
        if is_open:
            label.setText(f"{name}      OPEN")
            label.setObjectName("fingerOpen")
        else:
            label.setText(f"{name}      CLOSED")
            label.setObjectName("fingerClosed")

        label.style().unpolish(label)
        label.style().polish(label)

    def update_dashboard(self):
        if not self.system_running:
            return

        self.force_number += random.uniform(-1.5, 1.5)
        self.force_number = max(2, min(29, self.force_number))

        force_percent = int(self.force_number / 30 * 100)
        self.force_gauge.setValue(force_percent)

        self.accuracy_number += random.uniform(-0.2, 0.2)
        self.accuracy_number = max(
            95.0,
            min(99.9, self.accuracy_number)
        )

        self.ai_gauge.setValue(self.accuracy_number)

        battery = random.randint(84, 88)

        self.battery_card.value_label.setText(
            f"{battery}%"
        )

        temperature = random.uniform(33, 35.5)

        self.temperature_card.value_label.setText(
            f"{temperature:.1f}°C"
        )

    def start_system(self):
        self.system_running = True
        self.emg_graph.start_signal()
        self.neural_flow.start_flow()

        self.connection_status.setText(
            "● SYSTEM ONLINE"
        )

        self.connection_status.setStyleSheet("""
            color: #76F0A2;
            font-size: 12px;
            font-weight: 700;
        """)

        self.emg_status.setText("● SIGNAL ACTIVE")
        self.signal_card.value_label.setText("ACTIVE")
        self.esp_card.value_label.setText("CONNECTED")

    def stop_system(self):
        self.system_running = False
        self.emg_graph.stop_signal()
        self.neural_flow.stop_flow()

        self.connection_status.setText(
            "● SYSTEM PAUSED"
        )

        self.connection_status.setStyleSheet("""
            color: #FFB75D;
            font-size: 12px;
            font-weight: 700;
        """)

        self.emg_status.setText("● SIGNAL PAUSED")
        self.signal_card.value_label.setText("PAUSED")

    def calibrate_system(self):
        self.ai_status.setText(
            "● CALIBRATION IN PROGRESS..."
        )

        self.neural_flow.reset_flow()
        self.motion_value.setText("CALIBRATING")

        QTimer.singleShot(
            2000,
            self.finish_calibration
        )

    def finish_calibration(self):
        self.ai_status.setText(
            "● CALIBRATION COMPLETED"
        )

        self.motion_value.setText("POWER GRIP")

    def emergency_stop(self):
        self.system_running = False
        self.emg_graph.stop_signal()
        self.neural_flow.stop_flow()

        self.connection_status.setText(
            "● EMERGENCY STOP"
        )

        self.connection_status.setStyleSheet("""
            color: #FF5F73;
            font-size: 12px;
            font-weight: 700;
        """)

        self.emg_status.setText(
            "● SIGNAL DISABLED"
        )

        self.ai_status.setText(
            "● MOTORS DISABLED"
        )

        self.signal_card.value_label.setText("STOPPED")
        self.esp_card.value_label.setText("LOCKED")


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setFont(
        QFont("Segoe UI", 10)
    )

    window = Dashboard()
    window.show()

    sys.exit(app.exec())