from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from openai import OpenAI
import os

from app.services.storage import save_summary

from PyPDF2 import PdfReader

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        reader = PdfReader(file.file)
        pages_text = []
        for page in reader.pages:
            try:
                pages_text.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(pages_text).strip()
    finally:
        file.file.seek(0)


async def extract_text_from_upload(file: UploadFile) -> str:
    # Handle by content type or extension
    content_type = (file.content_type or "").lower()
    filename = (file.filename or "").lower()

    if content_type == "application/pdf" or filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    # Plain text
    if content_type.startswith("text/") or filename.endswith(".txt"):
        data = await file.read()
        try:
            return data.decode("utf-8", errors="ignore").strip()
        finally:
            file.file.seek(0)

    # Fallback: try decode as text anyway
    data = await file.read()
    try:
        return data.decode("utf-8", errors="ignore").strip()
    finally:
        file.file.seek(0)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    try:
        extracted_text = await extract_text_from_upload(file)
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract any readable text from the file.",
            )

        # OpenAI summary
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are TeamMind AI. Summarize this document for a busy team. "
                        "Highlight key points, decisions, action items, and risks in a clear format."
                    ),
                },
                {
                    "role": "user",
                    "content": extracted_text,
                },
            ],
        )

        summary = (response.choices[0].message.content or "").strip()
        if not summary:
            raise HTTPException(status_code=500, detail="No summary generated.")

        # Log into Supabase
        save_summary(
            source="file",
            input_text=extracted_text[:8000],  # avoid huge payloads
            summary=summary,
            user_id=None,
            meta={
                "route": "upload",
                "filename": file.filename,
                "content_type": file.content_type,
            },
        )

        return JSONResponse({"summary": summary})

    except HTTPException:
        raise
    except Exception as e:
        print("upload_file error:", e)
        raise HTTPException(
            status_code=500,
            detail="Error while processing file. Please try again.",
        )

