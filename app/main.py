from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.db.database import AsyncSessionLocal
from app.services.download_service import DownloadService

app = FastAPI(
    title=settings.APP_NAME,
    version="0.2.8",
)

app.state.download_service = DownloadService(session_factory=AsyncSessionLocal)

@app.get("/")
async def root():
    return {"message": settings.APP_NAME}

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))

    return {
        "status": "ok",
    }