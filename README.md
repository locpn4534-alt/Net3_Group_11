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

```
Net3_Group11_Project

├── client/                         (Đạt + Quang)
│   ├── client.py                   # Chương trình Client
│   ├── gui.py                      # Giao diện PyQt6
│   ├── upload_engine.py            # Upload Engine
│   ├── drag_drop.py                # Kéo thả file
│   ├── progress.py                 # Thanh tiến trình
│   └── utils.py
│
├── server/                         (Phúc)
│   ├── server.py                   # Server chính
│   ├── receiver.py                 # Nhận dữ liệu
│   ├── file_handler.py             # Lưu file
│   └── utils.py
│
├── core/                           (Huy)
│   ├── file_manager.py             # Quản lý danh sách file
│   ├── queue_manager.py            # Quản lý hàng đợi
│   ├── status.py                   # Trạng thái upload
│   └── config.py                   # Cấu hình chung
│
├── uploads/                        # File sau khi upload
│   └── .gitkeep
│
├── test_files/                     # File dùng để test
│   └── .gitkeep
│
├── docs/
│   ├── protocol.md                 # Giao thức truyền file
│   ├── report.pdf                  # Báo cáo
│   └── images/                     # Ảnh minh họa
│
├── README.md
├── requirements.txt
└── .gitignore
```
## Trạng thái dự án

- Đã tạo repository.
- Đã phân chia nhiệm vụ cho các thành viên.
- Đang phát triển các module.