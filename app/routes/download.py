from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.dependencies import get_download_service
from app.services.download_service import DownloadService

router = APIRouter(
    prefix="/download",
    tags=["Download"],
)


@router.post("")
async def start_download(
        background_tasks: BackgroundTasks,
        service: DownloadService = Depends(get_download_service),
):
    if service.state.running:
        return {
            "message": "Загрузка началась"
        }

    background_tasks.add_task(
        service.download_all,
    )

    return {
        "message": "Download started",
    }