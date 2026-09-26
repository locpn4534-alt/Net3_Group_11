import os
from core.file_item import FileItem, FileStatus
from core.file_manager import FileManager
from core.upload_queue import UploadQueue


def test_person_2_work():
    print("=== DEMO PHẦN VIỆC NGƯỜI 2: FILE MANAGER & QUEUE ===\n")

    manager = FileManager()
    queue = UploadQueue(max_concurrent=2)

    files = manager.add_files(["video.mp4", "report.pdf", "image.png"])
    print("1. Thêm danh sách file vào Manager:")
    for f in manager.get_all_files():
        print(f"   - {f.name} | Trạng thái: {f.status.value}")

    queue.add_many(files)
    print(f"\n2. Số file trong hàng đợi UploadQueue: {queue.size()}")
    print(f"   Giới hạn upload đồng thời: {queue.max_concurrent}")

    print("\n3. Lấy file ra xử lý theo giới hạn (max=2):")
    f1 = queue.get_next()
    if f1 and queue.start_upload():
        f1.status = FileStatus.UPLOADING
        print(f"   [+] Đang chạy: {f1.name} | Tác vụ active: {queue.active_count}")

    f2 = queue.get_next()
    if f2 and queue.start_upload():
        f2.status = FileStatus.UPLOADING
        print(f"   [+] Đang chạy: {f2.name} | Tác vụ active: {queue.active_count}")

    print(f"   [?] Có thể upload thêm không? {queue.can_upload()}")

    print("\n4. Hoàn thành 1 tác vụ để mở slot:")
    queue.finish_upload()
    f1.status = FileStatus.COMPLETED
    print(f"   [-] {f1.name} đã {f1.status.value} | Tác vụ active còn: {queue.active_count}")

    f3 = queue.get_next()
    if f3 and queue.start_upload():
        f3.status = FileStatus.UPLOADING
        print(f"   [+] Đang chạy: {f3.name} | Tác vụ active: {queue.active_count}")

    print("\n5. Thử nghiệm quy tắc giải quyết trùng tên trên Server:")
    os.makedirs("./test_server", exist_ok=True)
    with open("./test_server/report.pdf", "w") as f:
        f.write("test")

    resolved_name = FileManager.resolve_filename_conflict("./test_server", "report.pdf")
    print(f"   Tên gốc: report.pdf -> Tên sau xử lý trùng: {resolved_name}")

    if os.path.exists("./test_server/report.pdf"):
        os.remove("./test_server/report.pdf")
        os.rmdir("./test_server")


if __name__ == "__main__":
    test_person_2_work()
