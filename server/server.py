from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from server.file_receiver import save_uploaded_files

app = FastAPI(
    title="Multi-File Uploader Server",
    version="1.0.0",
    description="Backend server hỗ trợ tiếp nhận và lưu trữ nhiều file đồng thời từ Client."
)

@app.get("/")
def health_check():
    """Kiểm tra server."""
    return {"status": "online", "message": "Server is running"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(..., description="Chọn nhiều file")):
    if not files:
        raise HTTPException(status_code=400, detail="Không có file nào.")
    saved_files = await save_uploaded_files(files)
    return {"status": "success", "saved_files": saved_files}
