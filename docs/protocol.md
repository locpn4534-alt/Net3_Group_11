# Communication Protocol

## Overview

| Thành phần  | Công nghệ             |
|-------------|-----------------------|
| Client      | Python                |
| Server      | FastAPI + Uvicorn     |
| Protocol    | HTTP                  |
| Upload      | multipart/form-data   |

## API Endpoints

| Method | Endpoint  | Chức năng                     |
|--------|-----------|-------------------------------|
| GET    | `/`       | Kiểm tra trạng thái Server    |
| POST   | `/upload` | Upload một hoặc nhiều file    |
| GET    | `/docs`   | Swagger API Documentation     |

## File Upload

| Thành phần   | Giá trị                 |
|--------------|-------------------------|
| Method       | POST                    |
| Endpoint     | `/upload`               |
| Content-Type | `multipart/form-data`   |
| Field        | `files`                 |
| Storage      | `uploads/`              |

### Response

```json
{
  "status": "success",
  "saved_files": [
    "test1.txt",
    "test2.txt"
  ]
}