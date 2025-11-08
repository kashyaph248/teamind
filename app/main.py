from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, text_summary

app = FastAPI(title="TeamMind AI - Backend")

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev: allow all origins so extension & any page can call
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(text_summary.router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}

