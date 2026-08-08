from fastapi import Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.file_service import FileService
from app.services.download_service import DownloadService

def get_file_service(session: AsyncSession = Depends(get_db)) -> FileService:
    return FileService(session)

def get_download_service(request: Request) -> DownloadService:
    return request.app.state.download_service