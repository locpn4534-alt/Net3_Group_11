import os
import shutil
from typing import List
from fastapi import UploadFile, HTTPException
from server.utils import get_safe_filename

# Thư mục lưu file
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

# Tạo thư mục nếu chưa có
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """
    Lưu các file upload và xử lý tên file trùng.
    """
    saved_files = []
    
    for file in files:
        if not file.filename:
            continue
            
        # Lấy tên file
        clean_filename = os.path.basename(file.filename)
        
        # Xử lý tên file trùng
        safe_name = get_safe_filename(UPLOAD_DIR, clean_filename)
        file_path = os.path.join(UPLOAD_DIR, safe_name)
        
        try:
            # Lưu file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_files.append(safe_name)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Lỗi hệ thống: Không thể lưu file '{clean_filename}'. Chi tiết: {str(e)}"
            )
            
    return saved_files