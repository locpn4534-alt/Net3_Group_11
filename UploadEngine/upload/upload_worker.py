"""
upload_worker.py
Worker chịu trách nhiệm upload MỘT file lên Server qua HTTP.
Chạy trong QThreadPool (QRunnable) để không block giao diện.

Yêu cầu cài đặt:
    pip install requests requests-toolbelt PyQt6
"""

import os
import traceback

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from requests_toolbelt.multipart.encoder import (
    MultipartEncoder,
    MultipartEncoderMonitor,
)
import requests

from .progress import ProgressTracker


class WorkerSignals(QObject):
    """
    QRunnable không tự có signal, nên phải tách riêng ra QObject.
    Người 1 (GUI) và Người 2 (Queue) sẽ lắng nghe các signal này.
    """
    progress = pyqtSignal(str, float, float)   # file_id, percent, speed_mb_s
    status_changed = pyqtSignal(str, str)      # file_id, status ("UPLOADING"/"COMPLETED"/"ERROR")
    finished = pyqtSignal(str)                 # file_id
    error = pyqtSignal(str, str)               # file_id, error_message


class UploadWorker(QRunnable):
    """
    Upload 1 file lên server.
    file_item: object từ Người 2, cần có ít nhất .id, .path, .name, .size
    """

    def __init__(self, file_item, server_url: str, timeout: int = 30):
        super().__init__()
        self.file_item = file_item
        self.server_url = server_url
        self.timeout = timeout
        self.signals = WorkerSignals()
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        """Được QThreadPool gọi tự động khi có slot trống (tối đa 3 song song)."""
        file_id = self.file_item.id
        file_path = self.file_item.path
        file_name = self.file_item.name

        # --- Kiểm tra file tồn tại trước khi upload ---
        if not os.path.exists(file_path):
            msg = f"File không tồn tại: {file_path}"
            self.signals.status_changed.emit(file_id, "ERROR")
            self.signals.error.emit(file_id, msg)
            return

        try:
            total_size = os.path.getsize(file_path)
            tracker = ProgressTracker(total_size)

            self.signals.status_changed.emit(file_id, "UPLOADING")

            with open(file_path, "rb") as f:
                encoder = MultipartEncoder(
                    fields={"file": (file_name, f, "application/octet-stream")}
                )

                def _callback(monitor: MultipartEncoderMonitor):
                    if self._is_cancelled:
                        raise UploadCancelled(f"Upload bị hủy: {file_name}")
                    result = tracker.update(monitor.bytes_read)
                    self.signals.progress.emit(
                        file_id, result["percent"], result["speed_mb_s"]
                    )

                monitor = MultipartEncoderMonitor(encoder, _callback)

                response = requests.post(
                    self.server_url,
                    data=monitor,
                    headers={"Content-Type": monitor.content_type},
                    timeout=self.timeout,
                )

            if response.status_code == 200:
                self.signals.status_changed.emit(file_id, "COMPLETED")
                self.signals.finished.emit(file_id)
            else:
                msg = f"Server trả lỗi {response.status_code}: {response.text[:200]}"
                self.signals.status_changed.emit(file_id, "ERROR")
                self.signals.error.emit(file_id, msg)

        except UploadCancelled as e:
            self.signals.status_changed.emit(file_id, "ERROR")
            self.signals.error.emit(file_id, str(e))

        except requests.exceptions.Timeout:
            self.signals.status_changed.emit(file_id, "ERROR")
            self.signals.error.emit(file_id, "Hết thời gian chờ (timeout)")

        except requests.exceptions.ConnectionError:
            self.signals.status_changed.emit(file_id, "ERROR")
            self.signals.error.emit(file_id, "Không kết nối được đến Server")

        except Exception as e:
            # Bắt mọi lỗi không lường trước, không để làm crash cả pool
            self.signals.status_changed.emit(file_id, "ERROR")
            self.signals.error.emit(file_id, f"Lỗi không xác định: {e}")
            traceback.print_exc()


class UploadCancelled(Exception):
    """Raise để dừng upload giữa chừng khi người dùng hủy."""
    pass 