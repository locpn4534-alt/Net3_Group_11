# Net3_Group_11

## Môn học

Lập trình mạng

## Đề tài

UDM_10 - Upload nhiều file sử dụng TCP Socket bằng Python

## Thành viên

- Ngô Phúc Gia Huy (Trưởng nhóm)
- Phạm Ngọc Lộc
- Nguyễn Đình Phúc
- Mông Ngọc Quang
- Lý Tấn Đạt

# Phân công nhiệm vụ

| Thành viên                         | Nhiệm vụ                                                                     |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| **Ngô Phúc Gia Huy (Nhóm trưởng)** | File Manager & Queue - Quản lý danh sách file, trạng thái, hàng đợi          |
| **Lý Tấn Đạt**                     | GUI & Drag/Drop - Thiết kế giao diện PyQt6, kéo thả file                     |
| **Mông Ngọc Quang**                | Upload Engine - Code chức năng upload, progress, tốc độ                      |
| **Nguyễn Đình Phúc**               | Server - Xây dựng Server nhận và lưu file                                    |
| **Phạm Ngọc Lộc**                  | GitHub, Integration & Testing - Ghép hệ thống, xử lý lỗi, kiểm thử, tài liệu |

## Công nghệ sử dụng

- Python 3
- TCP Socket Programming
- Git & GitHub
- Visual Studio Code

## Cấu trúc dự án

```text
Net3_Group_11
│
├── client/
│   ├── client.py
│   ├── file_sender.py
│   ├── utils.py
│   └── client/
│       └── core/
│           ├── file_item.py
│           ├── file_manager.py
│           ├── test_file_manager.py
│           └── upload_queue.py
│
├── UploadEngine/
│   ├── main.py
│   └── upload/
│       ├── progress.py
│       ├── upload_worker.py
│       └── uploader.py
│
├── project/
│   ├── main.py
│   └── ui/
│       ├── drop_area.py
│       ├── file_table.py
│       └── main_window.py
│
├── server/
│   ├── server.py
│   ├── file_receiver.py
│   └── utils.py
│
├── docs/
│   └── protocol.md
│
├── test_files/
├── uploads/
├── README.md
├── requirements.txt
└── .gitignore
```

## Tiến độ dự án

- [x] Khởi tạo Repository
- [x] Xây dựng cấu trúc dự án
- [x] Phát triển File Manager & Upload Queue
- [x] Phát triển Server & File Receiver
- [x] Phát triển File Sender
- [x] Phát triển GUI & Drag/Drop cơ bản
- [x] Phát triển Upload Engine cơ bản
- [x] Tích hợp hoàn bộ hệ thống
- [x] Kiểm thử từng module
- [x] Kiểm thử toàn hệ thống
- [x] Xử lý lỗi tích hợp
- [ ] Hoàn thiện báo cáo

---

## Trạng thái kiểm thử

| Module                      | Trạng thái         | Ghi chú                                      |
|-----------------------------|--------------------|----------------------------------------------|
| File Manager & Upload Queue | PASS               | Queue, FIFO, giới hạn upload                 |
| Server & File Receiver      | PASS               | Health Check, upload, file trùng             |
| GUI & Drag/Drop             | PASS               | GUI, Drag/Drop, Upload                       |
| Upload Engine               | PASS               | Upload file và nhiều file                    |
| Integration toàn hệ thống   | PASS               | Còn Overall Progress và Speed                |

---

## Tài liệu

| Tài liệu            | Mô tả                                  |
| ------------------- | -------------------------------------- |
| `docs/test_plan.md` | Kế hoạch và kết quả kiểm thử           |
| `docs/protocol.md`  | Đặc tả giao tiếp giữa Client và Server |
| `requirements.txt`  | Danh sách thư viện của dự án           |
| `README.md`         | Tổng quan và tiến độ dự án             |

---
