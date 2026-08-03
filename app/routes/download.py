from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.dependencies import get_file_service
from app.services.download_service import DownloadService

router = APIRouter(prefix="/download", tags=["Download"])


@router.post("")
async def start_download(
        background_tasks: BackgroundTasks,
        file_service = Depends(get_file_service),
):
    service = DownloadService(file_service)

    background_tasks.add_task(service.download_all())

    return {"message": "Начало загрузки"}