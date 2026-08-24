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

| Chức năng                   | Kết quả |
|-----------------------------|---------|
| Khởi động GUI               | PASS    |
| Chọn file                   | PASS    |
| Hiển thị file               | PASS    |
| Drag & Drop                 | PASS    |
| Nút Upload                  | FAIL    |

### Ghi chú
- GUI khởi động và nhận file bình thường.
- File được hiển thị với trạng thái `Waiting`.
- Nút `UPLOAD` chưa kết nối với Upload Engine nên file không được upload.
- Cần kiểm tra hàm `on_upload_clicked()`.

---

## Upload Engine (Quang)

| Chức năng                    | Kết quả |
|------------------------------|---------|
| Import UploadWorker          | PASS    |
| Tương thích với FileItem     | FAIL    |
| Kết nối Server               | CHƯA TEST |

### Ghi chú

- `UploadWorker` sử dụng `FileItem.id`.
- `FileItem` hiện tại không có thuộc tính `id`.
- Cần kiểm tra và thống nhất interface với `FileItem` của Huy.