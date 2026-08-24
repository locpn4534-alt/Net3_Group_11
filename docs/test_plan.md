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