from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.summarizer import summarize_text

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/summarize-text")
async def summarize_raw_text(payload: TextInput):
    content = (payload.text or "").strip()
    if not content:
        raise HTTPException(status_code=400, detail="Text is empty.")
    summary = summarize_text(content)
    return {"summary": summary}


