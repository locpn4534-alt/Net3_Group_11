## File Manager & Upload Queue (Huy)

| Chức năng                    | Kết quả |
|------------------------------|---------|
| Khởi tạo FileManager         | PASS    |
| Thêm file                    | PASS    |
| Thêm nhiều file              | PASS    |
| Trạng thái WAITING           | PASS    |
| Queue rỗng                   | PASS    |
| Thêm file vào Queue          | PASS    |
| FIFO                         | PASS    |
| Giới hạn 3 upload            | PASS    |
| Hoàn thành upload            | PASS    |

---

## Server & File Receiver (Phúc)

| Chức năng                    | Kết quả |
|------------------------------|---------|
| Khởi động Server             | PASS    |
| Health Check                 | PASS    |
| Swagger API                  | PASS    |
| Upload 1 file                | PASS    |
| Lưu file vào uploads         | PASS    |
| Upload nhiều file            | PASS    |
| Xử lý file trùng tên         | PASS    |



---

## GUI & Drag/Drop (Đạt)

| Chức năng         | Kết quả |
|-------------------|---------|
| Khởi động GUI     | PASS    |
| Chọn file         | PASS    |
| Hiển thị file     | PASS    |
| Drag & Drop       | PASS    |
| Xử lý file trùng  | PASS    |
| Nút Upload        | PASS    |
| Clear             | PASS    |
| Overall Progress  | PASS    |

---

## Upload Engine (Quang)

| Chức năng                 | Kết quả |
|---------------------------|---------|
| Import UploadWorker       | PASS    |
| Import UploadManager      | PASS    |
| Tương thích với FileItem  | PASS    |
| Upload file               | PASS    |
| Upload nhiều file         | PASS    |
| Kết nối Server            | PASS    |
| Xử lý lỗi kết nối         | PASS    |
| Speed                     | PASS    |

---

## Integration & Testing (Lộc)

| Chức năng                    | Kết quả |
|------------------------------|---------|
| Tích hợp GUI → Upload Engine | PASS    |
| Upload Engine → Server       | PASS    |
| Upload nhiều file từ GUI     | PASS    |
| Progress từng file           | PASS    |
| Xử lý lỗi kết nối            | PASS    |
| Kiểm thử toàn hệ thống       | PASS    |

