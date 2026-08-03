from sqlalchemy.ext.asyncio import AsyncSession

from app.models.downloaded_file import DownloadedFile
from app.repositories.file_repository import FileRepository

class FileService:
    def __init__(self, session: AsyncSession):
        self.repository = FileRepository(session)

    async def save(self, filename: str, path: str) -> DownloadedFile:
        return await self.repository.create(filename, path)

    async def get_files(self) -> list[DownloadedFile]:
        return await self.repository.get_all()