import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(content: str) -> str:
    if not content.strip():
        return "No readable text found."

    prompt = """Summarize the following into:
    1. Key updates
    2. Decisions
    3. Action items
    4. Risks"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

