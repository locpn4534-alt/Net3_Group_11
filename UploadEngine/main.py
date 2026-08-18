# main.py
import sys
from PyQt6.QtWidgets import QApplication
from upload import UploadManager

app = QApplication(sys.argv)

manager = UploadManager(server_url="http://127.0.0.1:8000/upload")
manager.status_changed.connect(lambda fid, status: print(fid, status))
manager.progress_updated.connect(lambda fid, pct, speed: print(fid, pct, speed))

print("UploadManager khởi tạo thành công:", manager)