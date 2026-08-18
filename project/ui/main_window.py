from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar
)
from PyQt6.QtCore import Qt
import os

from ui.drop_area import DropArea
from ui.file_table import FileTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi File Uploader")
        self.setGeometry(100, 100, 700, 500)

        self.file_row_map = {}

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title = QLabel("MULTI FILE UPLOADER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title)

        self.drop_area = DropArea()
        self.drop_area.files_dropped.connect(self.on_files_added)
        main_layout.addWidget(self.drop_area)

        self.file_table = FileTable()
        main_layout.addWidget(self.file_table)

        self.overall_progress = QProgressBar()
        self.overall_progress.setValue(0)
        main_layout.addWidget(self.overall_progress)

        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("UPLOAD")
        self.upload_button.clicked.connect(self.on_upload_clicked)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.on_clear_clicked)

        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

    def on_files_added(self, file_paths: list):
        for path in file_paths:
            if path in self.file_row_map:
                continue

            file_name = os.path.basename(path)
            file_size = self.get_file_size_text(path)

            row = self.file_table.add_file_row(file_name, file_size)
            self.file_row_map[path] = row

    def get_file_size_text(self, path: str) -> str:
        try:
            size_bytes = os.path.getsize(path)
            size_mb = size_bytes / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        except OSError:
            return "N/A"

    def on_upload_clicked(self):
        print("Upload button clicked. Files:", list(self.file_row_map.keys()))
        # TODO: gọi sang Upload Engine (Người 3) ở đây

    def on_clear_clicked(self):
        self.file_table.clear_all()
        self.file_row_map.clear()
        self.overall_progress.setValue(0)