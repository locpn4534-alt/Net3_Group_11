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

### Ghi chú
- Upload file trùng tên được xử lý đúng.
- Cần kiểm tra lại `saved_files` trong response có trả đúng tên file thực tế sau khi đổi tên hay không.

---

## GUI & Drag/Drop (Đạt)

| Chức năng         | Kết quả |
|-------------------|---------|
| Khởi động GUI     | PASS    |
| Chọn file         | PASS    |
| Hiển thị file     | PASS    |
| Drag & Drop       | PASS    |
| Xử lý file trùng  | PASS    |
| Nút Upload        | FAIL    |
| Clear             | PASS    |

### Ghi chú

- Nút `UPLOAD` chưa tích hợp với `UploadManager` nên file vẫn ở trạng thái `Waiting`.

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

### Ghi chú

- Chưa kiểm thử chức năng `Cancel` và hiển thị `Progress` trên giao diện.

