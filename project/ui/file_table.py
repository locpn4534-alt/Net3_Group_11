from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QProgressBar, QHeaderView
from PyQt6.QtCore import Qt


class FileTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["File", "Size", "Progress", "Speed", "Status"])

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)

    def add_file_row(self, file_name: str, file_size_text: str = "0 MB"):
        row = self.rowCount()
        self.insertRow(row)

        self.setItem(row, 0, QTableWidgetItem(file_name))
        self.setItem(row, 1, QTableWidgetItem(file_size_text))

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCellWidget(row, 2, progress_bar)

        self.setItem(row, 3, QTableWidgetItem("0 MB/s"))
        self.setItem(row, 4, QTableWidgetItem("Waiting"))

        return row

    def update_progress(self, row: int, percent: int):
        progress_bar = self.cellWidget(row, 2)
        if progress_bar:
            progress_bar.setValue(percent)

    def update_speed(self, row: int, speed_text: str):
        self.setItem(row, 3, QTableWidgetItem(speed_text))

    def update_status(self, row: int, status_text: str):
        self.setItem(row, 4, QTableWidgetItem(status_text))

    def clear_all(self):
        self.setRowCount(0)