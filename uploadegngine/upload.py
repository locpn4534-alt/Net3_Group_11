import sys
import os
import uuid
import requests
from enum import Enum
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QLabel
)
from PyQt6.QtGui import QColor

try:
    from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
    HAS_TOOLBELT = True
except ImportError:
    HAS_TOOLBELT = False

SERVER_URL = "http://127.0.0.1:8000"
MAX_CONCURRENT = 3


#progress 
class FileStatus(str, Enum):
    WAITING = "Waiting"
    UPLOADING = "Uploading"
    COMPLETED = "Completed"
    ERROR = "Error"
    CANCELED = "Canceled"


class WorkerSignals(QObject):
    status_changed = pyqtSignal(str, str)
    progress = pyqtSignal(str, int)
    error = pyqtSignal(str, str)
    finished = pyqtSignal(str)


#  upload_worker 
class UploadWorker(QRunnable):
    def __init__(self, file_id, filepath, server_url, timeout=60):
        super().__init__()
        self.file_id = file_id
        self.filepath = filepath
        self.server_url = server_url.rstrip("/")
        self.timeout = timeout
        self.signals = WorkerSignals()
        self._is_canceled = False

    def cancel(self):
        self._is_canceled = True

    @pyqtSlot()
    def run(self):
        filename = os.path.basename(self.filepath)
        try:
            if not os.path.isfile(self.filepath):
                raise FileNotFoundError(f"File không tồn tại: {self.filepath}")

            self.signals.status_changed.emit(self.file_id, FileStatus.UPLOADING.value)

            if HAS_TOOLBELT:
                self._upload_with_progress(filename)
            else:
                self._upload_simple(filename)

            if self._is_canceled:
                self.signals.status_changed.emit(self.file_id, FileStatus.CANCELED.value)
                return

            self.signals.progress.emit(self.file_id, 100)
            self.signals.status_changed.emit(self.file_id, FileStatus.COMPLETED.value)

        except Exception as e:
            self.signals.status_changed.emit(self.file_id, FileStatus.ERROR.value)
            self.signals.error.emit(self.file_id, str(e))
        finally:
            self.signals.finished.emit(self.file_id)

    def _upload_simple(self, filename):
        with open(self.filepath, "rb") as f:
            response = requests.post(
                f"{self.server_url}/upload",
                files={"file": (filename, f)},
                timeout=self.timeout,
            )
        self._check_response(response)

    def _upload_with_progress(self, filename):
        with open(self.filepath, "rb") as f:
            encoder = MultipartEncoder(fields={"file": (filename, f, "application/octet-stream")})

            def _callback(monitor):
                if self._is_canceled:
                    raise Exception("Upload đã bị hủy bởi người dùng")
                if monitor.len:
                    percent = int(monitor.bytes_read * 100 / monitor.len)
                    self.signals.progress.emit(self.file_id, percent)

            monitor = MultipartEncoderMonitor(encoder, _callback)
            response = requests.post(
                f"{self.server_url}/upload",
                data=monitor,
                headers={"Content-Type": monitor.content_type},
                timeout=self.timeout,
            )
        self._check_response(response)

    def _check_response(self, response):
        if response.status_code != 200:
            raise Exception(f"Server trả về lỗi {response.status_code}: {response.text[:200]}")


#  uploader 
class UploadManager(QObject):
    file_status_changed = pyqtSignal(str, str, str)
    file_progress = pyqtSignal(str, int)
    file_error = pyqtSignal(str, str, str)
    all_finished = pyqtSignal()

    def __init__(self, server_url, max_concurrent=3, parent=None):
        super().__init__(parent)
        self.server_url = server_url
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(max_concurrent)

        self._filenames = {}
        self._statuses = {}
        self._workers = {}
        self._pending = 0

    def add_files(self, filepaths):
        added = []
        for path in filepaths:
            file_id = str(uuid.uuid4())
            filename = os.path.basename(path)

            self._filenames[file_id] = filename
            self._statuses[file_id] = FileStatus.WAITING.value
            self._pending += 1

            worker = UploadWorker(file_id, path, self.server_url)
            worker.signals.status_changed.connect(self._on_status_changed)
            worker.signals.progress.connect(self.file_progress.emit)
            worker.signals.error.connect(self._on_error)
            worker.signals.finished.connect(self._on_worker_finished)
            self._workers[file_id] = worker

            self.file_status_changed.emit(file_id, filename, FileStatus.WAITING.value)
            self.pool.start(worker)
            added.append((file_id, filename))

        return added

    def cancel_file(self, file_id):
        worker = self._workers.get(file_id)
        if worker:
            worker.cancel()

    def set_max_concurrent(self, n):
        self.pool.setMaxThreadCount(n)

    def get_status(self, file_id):
        return self._statuses.get(file_id)

    def wait_for_all(self, timeout_ms=-1):
        self.pool.waitForDone(timeout_ms)

    def _on_status_changed(self, file_id, status):
        self._statuses[file_id] = status
        filename = self._filenames.get(file_id, "")
        self.file_status_changed.emit(file_id, filename, status)

    def _on_error(self, file_id, message):
        filename = self._filenames.get(file_id, "")
        self.file_error.emit(file_id, filename, message)

    def _on_worker_finished(self, file_id):
        self._pending -= 1
        if self._pending <= 0:
            self.all_finished.emit()


#  ui 
STATUS_COLOR = {
    FileStatus.WAITING.value: QColor("#9e9e9e"),
    FileStatus.UPLOADING.value: QColor("#2196f3"),
    FileStatus.COMPLETED.value: QColor("#4caf50"),
    FileStatus.ERROR.value: QColor("#f44336"),
    FileStatus.CANCELED.value: QColor("#ff9800"),
}


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


# main 
def main():
    app = QApplication(sys.argv)
    win = UploaderWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()