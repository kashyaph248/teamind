from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.summarizer import summarize_text
from app.services.summarizer import client  # reuse OpenAI client

router = APIRouter()

class AskRequest(BaseModel):
    text: str
    question: str

@router.post("/ask-about-text")
async def ask_about_text(payload: AskRequest):
    base_text = (payload.text or "").strip()
    question = (payload.question or "").strip()

    if not base_text:
        raise HTTPException(status_code=400, detail="Text is empty.")
    if not question:
        raise HTTPException(status_code=400, detail="Question is empty.")

    # Use a chat completion focused on the user's question about the given text
    prompt = f"""
You are TeamMind AI, an assistant helping teams understand content.

Context text:
\"\"\"{base_text[:8000]}\"\"\"

User question about this text:
\"\"\"{question}\"\"\"

Answer clearly, referencing only the given context. If something is not supported
by the text, say so briefly.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You answer questions about the provided context text only."},
            {"role": "user", "content": prompt},
        ],
    )

    answer = response.choices[0].message.content.strip()
    return {"answer": answer}


