from pathlib import Path
from io import BytesIO
from zipfile import ZipFile

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.clients.remote_api import RemoteAPIClient
from app.core.config import settings
from app.core.logger import logger
from app.services.download_state import DownloadState
from app.services.file_service import FileService


class DownloadService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self.session_factory = session_factory
        self.state = DownloadState()

    async def download_all(self) -> None:
        self.state.start()

        logger.info("Начало загрузки файлов")

        storage = Path(settings.FILES_STORAGE_PATH)
        storage.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            async with self.session_factory() as session:
                file_service = FileService(session)

                async with RemoteAPIClient() as client:
                    while True:
                        names = await client.get_file_names()

                        if not names:
                            break

                        self.state.total_names += len(names)

                        logger.info(
                            "Получено %s имен файлов",
                            len(names),
                        )

                        for batch in self._split_batches(names, 3):
                            logger.info(
                                "Скачивание группы файлов: %s",
                                batch,
                            )

                            archive = await client.download_files(
                                batch
                            )

                            paths = self._extract_archive(
                                archive,
                                storage,
                            )

                            for path in paths:
                                await file_service.save(
                                    filename=path.name,
                                    path=str(path),
                                )

                            await client.mark_downloaded(batch)

                            self.state.downloaded += len(batch)

                            logger.info(
                                "Скачано %s файлов",
                                self.state.downloaded,
                            )

        except Exception as exc:
            self.state.set_error(str(exc))

            logger.exception(
                "Ошибка во время загрузки файлов"
            )

            raise

        finally:
            self.state.finish()

        logger.info(
            "Загрузка завершена. Скачано %s файлов",
            self.state.downloaded,
        )

    def get_state(self) -> DownloadState:
        return self.state

    @staticmethod
    def _split_batches(
        items: list[str],
        size: int,
    ):
        for i in range(0, len(items), size):
            yield items[i:i + size]

    @staticmethod
    def _extract_archive(
        archive: bytes,
        storage: Path,
    ) -> list[Path]:
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