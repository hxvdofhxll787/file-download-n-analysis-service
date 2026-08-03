from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

from app.clients.remote_api import RemoteAPIClient
from app.core.config import settings
from app.services.download_state import download_state
from app.services.file_service import FileService
from app.core.logger import logger

class DownloadService:
    def __init__(self, file_service: FileService):
        self.file_service = file_service
        self.state = download_state()

    async def download_all(self) -> None:
        self.state.start()

        logger.info("Начало загрузки")

        storage = Path(settings.FILES_STORAGE_PATH)
        storage.mkdir(parents=True, exist_ok=True)

        async with RemoteAPIClient() as client:
            while True:
                names = await client.get_file_names()

                if not names:
                    break

                self.state.total_names += len(names)

                logger.info("Получено %s файлов", len(names))

                batches = self._split_batches(names, 3)

                for batch in batches:
                    archive = await client.download_files(batch)

                    paths = self._extract_archive(archive, storage)

                    for path in paths:
                        await self.file_service.save(filename=path, path=str(path))

                    await client.mark_downloaded(batch)

                    self.state.downloaded += len(batch)

                    logger.info(
                        "Скачано %s из %s файлов",
                        self.state.downloaded,
                        self.state.total_names,
                    )

        self.state.finish()

        logger.info("Загрузка завершена")

    def _split_batches(self, items: list[str], size: int):
        for i in range(0, len(items), size):
            yield items[i:i + size]

    def _extract_archive(self, archive: bytes, storage: Path) -> list[Path]:
        result = []

        with ZipFile(BytesIO(archive)) as zip_file:
            for filename in zip_file.namelist():
                target = storage / filename

                zip_file.extract(
                    filename,
                    storage,
                )

                result.append(target)

        return result