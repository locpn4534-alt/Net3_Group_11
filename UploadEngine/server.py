import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "ok"}


def get_unique_path(directory: Path, filename: str) -> Path:
    dest = directory / filename
    if not dest.exists():
        return dest

    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while True:
        new_dest = directory / f"{stem} ({counter}){suffix}"
        if not new_dest.exists():
            return new_dest
        counter += 1


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            dest_path = get_unique_path(UPLOAD_DIR, file.filename)
            with open(dest_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            results.append({
                "filename": file.filename,
                "saved_as": dest_path.name,
                "status": "success",
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "detail": str(e),
            })
        finally:
            await file.close()

    return JSONResponse(content={"results": results})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)