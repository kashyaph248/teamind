from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI

from app.services.storage import save_summary

router = APIRouter()

# Initialize OpenAI client once
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TextRequest(BaseModel):
    text: str

@router.post("/summarize-text")
async def summarize_text(payload: TextRequest):
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text field is empty.")

    try:
        # Call OpenAI to generate structured summary
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are TeamMind AI, an assistant that summarizes content for teams. "
                        "Return a concise, structured summary with clear bullets: "
                        "Key points, decisions, action items, and risks if present."
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )

        summary = (response.choices[0].message.content or "").strip()
        if not summary:
            raise HTTPException(status_code=500, detail="No summary generated.")

        # Save to Supabase (non-blocking from user POV; errors are logged only)
        save_summary(
            source="text",
            input_text=text,
            summary=summary,
            user_id=None,  # later we’ll plug real auth here
            meta={"route": "summarize-text"},
        )

        return {"summary": summary}

    except HTTPException:
        raise
    except Exception as e:
        # Log server-side, return safe error
        print("summarize_text error:", e)
        raise HTTPException(
            status_code=500,
            detail="Error while generating summary. Please try again.",
        )

