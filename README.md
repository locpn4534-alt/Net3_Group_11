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
- [ ] Phát triển File Sender
- [x] Phát triển GUI & Drag/Drop cơ bản
- [x] Phát triển Upload Engine cơ bản
- [ ] Hoàn thiện tài liệu giao thức
- [ ] Tích hợp toàn bộ hệ thống
- [x] Kiểm thử từng module
- [ ] Kiểm thử toàn hệ thống
- [ ] Xử lý lỗi tích hợp
- [ ] Hoàn thiện báo cáo

---

## Trạng thái kiểm thử

| Module                      | Trạng thái | Ghi chú                                              |
| --------------------------- | ---------- | ---------------------------------------------------- |
| File Manager & Upload Queue | PASS       | Queue, FIFO và giới hạn upload đã kiểm thử           |
| Server & File Receiver      | PASS       | Health Check, upload và file trùng đã kiểm thử       |
| GUI & Drag/Drop             | PARTIAL    | GUI hoạt động, nút Upload chưa tích hợp              |
| Upload Engine               | FAIL       | Upload gửi sai field `file`, Server yêu cầu `files`  |
| Integration toàn hệ thống   | CHƯA TEST  | Chưa hoàn thiện kết nối GUI, Upload Engine và Server |

> **Trạng thái hiện tại:** Các module chính đã được kiểm thử riêng lẻ. GUI và Server hoạt động, nhưng phần tích hợp Upload Engine chưa hoàn thiện nên kiểm thử toàn hệ thống chưa thể thực hiện.

---

## Tài liệu

| Tài liệu            | Mô tả                                  |
| ------------------- | -------------------------------------- |
| `docs/test_plan.md` | Kế hoạch và kết quả kiểm thử           |
| `docs/protocol.md`  | Đặc tả giao tiếp giữa Client và Server |
| `requirements.txt`  | Danh sách thư viện của dự án           |
| `README.md`         | Tổng quan và tiến độ dự án             |

---
