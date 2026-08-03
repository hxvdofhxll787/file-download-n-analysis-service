from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.downloaded_file import DownloadedFile
from app.repositories.base import BaseRepository

class FileRepository(BaseRepository[DownloadedFile]):
    async def create(self, filename: str, path: str) -> DownloadedFile:
        file = DownloadedFile(filename=filename, path=path)

        self.session.add(file)

        await self.session.commit()

        await self.session.refresh(file)

        return file

    async def get_all(self) -> list[DownloadedFile]:
        result = await self.session.execute(
            select(DownloadedFile)
            .order_by(DownloadedFile.downloaded_at.desc())
        )

        return list(result.scalars().all())