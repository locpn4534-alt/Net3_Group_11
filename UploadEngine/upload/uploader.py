"""
uploader.py
Bộ điều phối (Manager) toàn bộ quá trình upload nhiều file.
Giới hạn tối đa 3 file upload đồng thời bằng QThreadPool.

Người 1 (GUI) và Người 2 (Queue) chỉ cần import UploadManager,
gọi start_upload(file_list) và lắng nghe các signal để cập nhật UI.
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThreadPool

from .upload_worker import UploadWorker

MAX_CONCURRENT_UPLOADS = 3


class UploadManager(QObject):
    """
    Quản lý hàng đợi upload với giới hạn số file chạy đồng thời.
    Không tự lấy file từ UploadQueue của Người 2 — nhận danh sách file_item
    trực tiếp qua start_upload(), để giữ 2 module độc lập, dễ test riêng.
    """

    # Signal tổng hợp bắn ra ngoài (GUI / Queue sẽ connect vào đây)
    progress_updated = pyqtSignal(str, float, float)    # file_id, percent, speed
    status_changed = pyqtSignal(str, str)               # file_id, status
    file_completed = pyqtSignal(str)                    # file_id
    file_failed = pyqtSignal(str, str)                  # file_id, error_message
    all_finished = pyqtSignal()                         # khi hàng đợi rỗng

    def __init__(self, server_url: str, max_concurrent: int = MAX_CONCURRENT_UPLOADS):
        super().__init__()
        self.server_url = server_url
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(max_concurrent)

        self._pending = []      # file_item đang chờ (WAITING)
        self._active_workers = {}   # file_id -> UploadWorker đang chạy
        self._total_count = 0
        self._done_count = 0

    def start_upload(self, file_items: list):
        """
        Nhận danh sách file_item (từ FileManager của Người 2) và bắt đầu upload.
        QThreadPool tự động giới hạn số worker chạy song song (max_concurrent),
        các worker còn lại sẽ tự chờ đến khi có slot trống.
        """
        self._pending.extend(file_items)
        self._total_count += len(file_items)

        for item in file_items:
            self._submit_worker(item)

    def _submit_worker(self, file_item):
        worker = UploadWorker(file_item, self.server_url)

        worker.signals.progress.connect(self.progress_updated)
        worker.signals.status_changed.connect(self.status_changed)
        worker.signals.finished.connect(self._on_worker_finished)
        worker.signals.error.connect(self._on_worker_error)

        self._active_workers[file_item.id] = worker
        self.thread_pool.start(worker)  # QThreadPool tự xếp hàng nếu đủ 3 luồng

    def cancel_file(self, file_id: str):
        worker = self._active_workers.get(file_id)
        if worker:
            worker.cancel()

    def cancel_all(self):
        for worker in self._active_workers.values():
            worker.cancel()
        self.thread_pool.clear()  # hủy các worker chưa kịp chạy

    def retry_file(self, file_item):
        """Đưa lại 1 file lỗi vào hàng đợi để upload lại."""
        self._submit_worker(file_item)

    def _on_worker_finished(self, file_id: str):
        self.file_completed.emit(file_id)
        self._mark_done(file_id)

    def _on_worker_error(self, file_id: str, message: str):
        self.file_failed.emit(file_id, message)
        self._mark_done(file_id)

    def _mark_done(self, file_id: str):
        self._active_workers.pop(file_id, None)
        self._done_count += 1
        if self._done_count >= self._total_count:
            self.all_finished.emit()

    def active_count(self) -> int:
        return len(self._active_workers)