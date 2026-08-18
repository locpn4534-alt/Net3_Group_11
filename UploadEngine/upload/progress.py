"""
progress.py
Theo dõi tiến trình upload: phần trăm hoàn thành và tốc độ (MB/s).
Dùng moving average để tốc độ hiển thị mượt, không bị nhảy giật.
"""

import time
from collections import deque


class ProgressTracker:
    """
    Theo dõi tiến trình upload cho MỘT file.
    Gọi update(bytes_sent) mỗi khi có thêm dữ liệu được gửi đi.
    """

    def __init__(self, total_bytes: int, smoothing_window: int = 5):
        self.total_bytes = max(total_bytes, 1)  # tránh chia cho 0
        self.bytes_sent = 0
        self.start_time = time.monotonic()
        self.last_time = self.start_time
        self.last_bytes = 0

        # Lưu (delta_bytes, delta_time) gần nhất để tính tốc độ trung bình trượt
        self._samples = deque(maxlen=smoothing_window)

    def update(self, bytes_sent: int) -> dict:
        """
        Cập nhật số byte đã gửi (lũy kế, không phải delta).
        Trả về dict {percent, speed_mb_s, bytes_sent, total_bytes}.
        """
        now = time.monotonic()
        delta_time = now - self.last_time
        delta_bytes = bytes_sent - self.last_bytes

        if delta_time > 0:
            self._samples.append((delta_bytes, delta_time))

        self.bytes_sent = bytes_sent
        self.last_time = now
        self.last_bytes = bytes_sent

        return {
            "percent": self.percent,
            "speed_mb_s": self.speed_mb_s,
            "bytes_sent": self.bytes_sent,
            "total_bytes": self.total_bytes,
        }

    @property
    def percent(self) -> float:
        return round((self.bytes_sent / self.total_bytes) * 100, 1)

    @property
    def speed_mb_s(self) -> float:
        """Tốc độ trung bình dựa trên các mẫu gần nhất (moving average)."""
        total_bytes = sum(b for b, _ in self._samples)
        total_time = sum(t for _, t in self._samples)
        if total_time <= 0:
            return 0.0
        bytes_per_sec = total_bytes / total_time
        return round(bytes_per_sec / (1024 * 1024), 2)

    @property
    def elapsed_seconds(self) -> float:
        return round(time.monotonic() - self.start_time, 1)

    def is_complete(self) -> bool:
        return self.bytes_sent >= self.total_bytes