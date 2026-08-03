from fastapi import FastAPI
from app.core.config import settings
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": settings.APP_NAME}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok"
    }