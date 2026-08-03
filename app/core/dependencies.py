from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.file_service import FileService

def get_file_service(session: AsyncSession = Depends(get_db)) -> FileService:
    return FileService(session)