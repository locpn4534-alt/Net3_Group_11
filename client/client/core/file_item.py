from dataclasses import dataclass
from enum import Enum
import os


class FileStatus(Enum):
    WAITING = "Chờ"
    UPLOADING = "Đang tải"
    COMPLETED = "Hoàn tất"
    ERROR = "Lỗi"


@dataclass
class FileItem:
    path: str
    status: FileStatus = FileStatus.WAITING
    progress: float = 0.0
    speed: float = 0.0
    error_message: str = ""

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def size(self):
        if os.path.exists(self.path):
            return os.path.getsize(self.path)
        return 0
