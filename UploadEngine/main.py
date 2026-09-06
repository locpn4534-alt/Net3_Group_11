import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QLabel
)
from PyQt6.QtGui import QColor

from upload.progress import FileStatus, STATUS_COLOR
from upload.uploader import UploadManager

SERVER_URL = "http://127.0.0.1:8000"
MAX_CONCURRENT = 3


class UploaderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-file Uploader — Demo")
        self.resize(520, 420)

        self.manager = UploadManager(SERVER_URL, max_concurrent=MAX_CONCURRENT)
        self.manager.file_status_changed.connect(self.on_status_changed)
        self.manager.file_error.connect(self.on_error)

        self.row_by_file_id = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.btn_choose = QPushButton("Chọn file...")
        self.btn_choose.clicked.connect(self.choose_files)
        top.addWidget(self.btn_choose)
        top.addWidget(QLabel(f"Tối đa {MAX_CONCURRENT} file upload đồng thời"))
        top.addStretch()
        layout.addLayout(top)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Tên file", "Trạng thái"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

    def choose_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Chọn file để upload")
        if not paths:
            return
        for file_id, filename in self.manager.add_files(paths):
            self._add_row(file_id, filename)

    def _add_row(self, file_id, filename):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(filename))
        item = QTableWidgetItem(FileStatus.WAITING.value)
        self.table.setItem(row, 1, item)
        self.row_by_file_id[file_id] = row

    def on_status_changed(self, file_id, filename, status):
        row = self.row_by_file_id.get(file_id)
        if row is None:
            return
        item = self.table.item(row, 1)
        item.setText(status)
        item.setForeground(STATUS_COLOR.get(status, QColor("#000000")))

    def on_error(self, file_id, filename, message):
        print(f"[LỖI] {filename}: {message}")


def main():
    app = QApplication(sys.argv)
    win = UploaderWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()