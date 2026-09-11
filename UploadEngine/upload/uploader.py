import os
import uuid
from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal

from .progress import FileStatus
from .upload_worker import UploadWorker


class UploadManager(QObject):
    file_status_changed = pyqtSignal(str, str, str)
    file_progress = pyqtSignal(str, int)
    speed = pyqtSignal(str, float)
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
            worker.signals.speed.connect(self.speed.emit)
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