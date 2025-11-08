from fastapi import APIRouter, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
import io
from app.services.summarizer import summarize_text

router = APIRouter()

def extract_text(file: UploadFile) -> str:
    name = file.filename.lower()
    if name.endswith(".txt"):
        return file.file.read().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        pdf = PdfReader(io.BytesIO(file.file.read()))
        return "\n".join([p.extract_text() or "" for p in pdf.pages])
    return file.file.read().decode("utf-8", errors="ignore")

@router.post("/upload")
async def upload_and_summarize(file: UploadFile = File(...)):
    text = extract_text(file)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in file.")
    summary = summarize_text(text)
    return {"filename": file.filename, "summary": summary}


