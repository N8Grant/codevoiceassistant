from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import itertools
from config import END_PHRASE


class ListeningOverlayWidget(QDialog):
    done_signal = pyqtSignal()  # ✅ External signal emitted when user clicks done

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(800, 300)
        self.move(300, 200)

        self.spinner = itertools.cycle(
            ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        )

        # UI Elements
        self.label = QLabel("🎤 Listening...", self)
        self.label.setStyleSheet("color: white; font-size: 24px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.done_button = QPushButton("✅ Done", self)
        self.done_button.setStyleSheet(
            "background-color: green; color: white; font-size: 16px; padding: 10px;"
        )
        self.done_button.clicked.connect(self._handle_done)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.done_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 220);")

        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self._update_spinner)
        self.spinner_timer.start(150)

    def _update_spinner(self):
        next_spin = next(self.spinner)
        self.label.setText(
            f"🎤 Listening {next_spin}\nSay '{END_PHRASE}' or click ✅ to finish."
        )

    def _handle_done(self):
        self.spinner_timer.stop()
        self.done_signal.emit()
        self.close()
