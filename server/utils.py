import os

def get_safe_filename(upload_dir: str, filename: str) -> str:
    """
    Tạo tên file mới nếu tên file đã tồn tại.
    """
    base_name, ext = os.path.splitext(filename)
    counter = 1
    safe_filename = filename
    
    # Tìm tên file chưa tồn tại
    while os.path.exists(os.path.join(upload_dir, safe_filename)):
        safe_filename = f"{base_name}_{counter}{ext}"
        counter += 1
        
    return safe_filename