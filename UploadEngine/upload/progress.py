from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor


class FileStatus(str, Enum):
    WAITING = "Waiting"
    UPLOADING = "Uploading"
    COMPLETED = "Completed"
    ERROR = "Error"
    CANCELED = "Canceled"


class WorkerSignals(QObject):
    status_changed = pyqtSignal(str, str)
    progress = pyqtSignal(str, int)
    speed = pyqtSignal(str, float)
    error = pyqtSignal(str, str)
    finished = pyqtSignal(str)


STATUS_COLOR = {
    FileStatus.WAITING.value: QColor("#9e9e9e"),
    FileStatus.UPLOADING.value: QColor("#2196f3"),
    FileStatus.COMPLETED.value: QColor("#4caf50"),
    FileStatus.ERROR.value: QColor("#f44336"),
    FileStatus.CANCELED.value: QColor("#ff9800"),
}