from enum import Enum
from dataclasses import dataclass
import os


class FileStatus(Enum):
    WAITING = "Waiting"
    UPLOADING = "Uploading"
    COMPLETED = "Completed"
    ERROR = "Error"


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
        return os.path.getsize(self.path)
