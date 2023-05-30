from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame, QPushButton, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QSettings, QByteArray
from PyQt6.QtGui import QFont


class CroesusGUI(QMainWindow):
    def __init__(self, queue, croesus_helper, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Croesus Helper")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        # Header
        self.title_label = QLabel("Croesus Boss Encounter", self)
        self.title_label.setFont(QFont('Arial', 20))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Divider Line
        self.divider_line = QFrame(self)
        self.divider_line.setFrameShape(QFrame.Shape.HLine)
        self.divider_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.divider_line)

        # Labels
        self.ability_label = QLabel("Next ability: ", self)
        self.ability_label.setFont(QFont('Arial', 16))
        self.countdown_label = QLabel("Incoming attack in: ", self)
        self.countdown_label.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.ability_label)
        self.layout.addWidget(self.countdown_label)

        # Flash Indicator
        self.color_box = QLabel(self)
        self.color_box.setFixedHeight(100)
        self.color_box.setStyleSheet("background-color: green;")
        self.color_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.color_box)
        self.color_box.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        # Pause/resume button
        self.croesus_helper = croesus_helper

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setFont(QFont('Arial', 16))
        self.pause_button.clicked.connect(self.toggle_pause)
        self.layout.addWidget(self.pause_button)
        self.is_paused = False

        # Reset Button
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFont(QFont('Arial', 16))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                padding: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
            QPushButton:pressed {
                background-color: #b30000;
            }
        """)
        self.reset_button.clicked.connect(self.croesus_helper.reset)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.reset_button)
        self.layout.addLayout(self.button_layout)

        self.queue = queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)

        self.flash_counter = 0
        self.is_red = False

        # Remember window position
        self.settings = QSettings("SilentDevCoPro", "rs3helper")

        self.restoreGeometry(QByteArray.fromHex(self.settings.value("windowGeometry", "", type=QByteArray)))
        self.restoreState(QByteArray.fromHex(self.settings.value("windowState", "", type=QByteArray)))

    def check_queue(self):
        while not self.queue.empty():
            message = self.queue.get()
            if message[0] == "ability":
                self.update_ability(message[1])
            elif message[0] == "countdown":
                self.update_countdown(message[1])
            elif message[0] == "flash":
                self.flash_color_box()

    def toggle_pause(self):
        if self.croesus_helper.paused:
            self.croesus_helper.resume()
            self.pause_button.setText("Pause")
        else:
            self.croesus_helper.pause()
            self.pause_button.setText("Resume")

    def update_ability(self, ability):
        self.ability_label.setText(f"Next ability: {ability}")

    def update_countdown(self, countdown):
        self.countdown_label.setText(f"Incoming attack in: {countdown}")

    def flash_color_box(self):
        self.flash_counter = 6  # flash 3 times (back and forth between two colors)

        if hasattr(self, 'flash_timer'):
            self.flash_timer.stop()
            del self.flash_timer

        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.change_color)
        self.flash_timer.start(250)

    def change_color(self):
        self.is_red = not self.is_red
        self.color_box.setStyleSheet("background-color: red" if self.is_red else "background-color: green")

        self.flash_counter -= 1
        if self.flash_counter == 0:
            self.flash_timer.stop()
            del self.flash_timer

    def closeEvent(self, event):
        # Save window state and geometry
        self.settings.setValue("windowGeometry", self.saveGeometry().toHex())
        self.settings.setValue("windowState", self.saveState().toHex())

        super().closeEvent(event)
