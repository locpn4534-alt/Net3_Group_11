from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal


class DropArea(QWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Kéo thả file vào đây")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: gray; padding: 30px;")

        self.select_button = QPushButton("Chọn File")
        self.select_button.clicked.connect(self.open_file_dialog)

        layout.addWidget(self.label)
        layout.addWidget(self.select_button)
        self.setLayout(layout)

        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #aaa;
                border-radius: 8px;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.files_dropped.emit(file_paths)

    def open_file_dialog(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Chọn file để upload")
        if file_paths:
            self.files_dropped.emit(file_paths)