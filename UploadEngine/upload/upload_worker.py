import os
import requests
import time
from PyQt6.QtCore import QRunnable, pyqtSlot


try:
    from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
    HAS_TOOLBELT = True
except ImportError:
    HAS_TOOLBELT = False

from .progress import FileStatus, WorkerSignals


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
                files={"files": (filename, f)},
                timeout=self.timeout,
            )
        self._check_response(response)

    def _upload_with_progress(self, filename):
        with open(self.filepath, "rb") as f:
            encoder = MultipartEncoder(fields={"files": (filename, f, "application/octet-stream")})

            start_time = time.monotonic()


            def _callback(monitor):
                if self._is_canceled:
                    raise Exception("Upload đã bị hủy bởi người dùng")
                if monitor.len:
                    percent = int(monitor.bytes_read * 100 / monitor.len)
                    self.signals.progress.emit(self.file_id, percent)

                    elapsed = time.monotonic() - start_time

                    if elapsed > 0:
                        speed = monitor.bytes_read / elapsed / (1024 * 1024)
                        self.signals.speed.emit(self.file_id, speed)


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