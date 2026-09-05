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
- GUI khởi động và nhận file bình thường.
- Có thể chọn nhiều file và hiển thị tên, kích thước file.
- Chức năng Drag & Drop hoạt động bình thường.
- File trùng không được thêm lại vào danh sách.
- Chức năng `Clear` xóa danh sách file và reset progress.
- Nút `UPLOAD` chưa kết nối với Upload Engine nên file không được upload.
- Cần kiểm tra lại hàm `on_upload_clicked()` để tích hợp với Upload Engine.

## Upload Engine (Quang)
| Chức năng                         | Kết quả    |
|-----------------------------------|------------|
| Import UploadWorker               | PASS       |
| Import UploadManager              | PASS       |
| Tương thích với FileItem          | PASS       |
| Xử lý file không tồn tại          | PASS       |
| Xử lý file hợp lệ                 | PASS       |
| Cập nhật trạng thái               | PASS       |
| Cập nhật Progress                 | PASS       |
| Kết nối Server                    | FAIL       |
| Upload nhiều file                 | CHƯA TEST  |
| Upload đồng thời (3 file)         | CHƯA TEST  |
| Xử lý lỗi từ Server               | PASS       |
| Hủy Upload                        | CHƯA TEST  |

### Ghi chú
- `UploadWorker` import và khởi tạo thành công.
- Xử lý file không tồn tại đúng, trả về trạng thái `Error`.
- File hợp lệ chuyển sang trạng thái `Uploading` và phát tín hiệu progress.
- Khi upload tới Server, Server trả lỗi HTTP 422 do thiếu field `files`.
- Upload Engine đang gửi field `file`, trong khi Server yêu cầu `files`.
- Test đối chứng bằng `curl` với field `files` trả về HTTP 200 và upload thành công.

