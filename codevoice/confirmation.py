from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
import pyperclip
from codevoice.llm_refiner import refine_prompt
from PyQt5.QtWidgets import QApplication


class ConfirmationDialog(QDialog):
    def __init__(self, original: str, refined: str = None):
        super().__init__()
        self.original = original
        self.refined = refined
        self.setWindowTitle("Prompt Captured")
        self.setFixedSize(800, 400)
        self.setStyleSheet("background-color: white;")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 🔧 FIX: always define a prompt to display
        display_text = (
            self.refined
            if (self.refined and self.refined.strip() != self.original.strip())
            else self.original
        )

        label = QLabel(
            "✨ LLM-refined prompt" if self.refined else "✅ Prompt captured"
        )
        label.setStyleSheet("font-size: 16px; color: green; font-weight: bold;")
        layout.addWidget(label)

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setText(display_text)
        layout.addWidget(self.text_box)

        # 🔧 Add separator + original only if refined and different
        if self.refined and self.refined.strip() != self.original.strip():
            separator = QLabel("🔁 Original spoken input")
            separator.setStyleSheet("font-size: 13px; color: gray; font-style: italic;")
            layout.addWidget(separator)

            original_box = QTextEdit()
            original_box.setReadOnly(True)
            original_box.setText(self.original)
            layout.addWidget(original_box)

        # Buttons
        button_row = QHBoxLayout()

        quit_btn = QPushButton("Quit")
        quit_btn.setStyleSheet("background-color:#d9534f;color:white;padding:10px;")
        quit_btn.clicked.connect(lambda: QApplication.instance().quit())
        button_row.addWidget(quit_btn)

        self.enhance_btn = QPushButton("✨ Enhance using LLM")
        self.enhance_btn.setStyleSheet(
            "background-color: orange; color: white; padding: 10px;"
        )
        self.enhance_btn.clicked.connect(self.enhance_with_llm)
        button_row.addWidget(self.enhance_btn)

        continue_btn = QPushButton("Continue")
        continue_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px;"
        )
        continue_btn.clicked.connect(self.accept)
        button_row.addWidget(continue_btn)

        layout.addLayout(button_row)
        self.setLayout(layout)

    def enhance_with_llm(self):
        print("[confirmation] Enhancing via LLM...")
        original, refined = refine_prompt(self.original)
        self.text_box.setText(refined)
        pyperclip.copy(refined)
        self.enhance_btn.setDisabled(True)
        self.enhance_btn.setText("✅ Enhanced and copied")
        self.refined = refined


def show_confirmation(original: str, refined: str = None):
    dialog = ConfirmationDialog(original, refined)
    dialog.exec_()
