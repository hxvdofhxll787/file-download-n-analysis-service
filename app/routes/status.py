from fastapi import APIRouter, Depends

from app.core.dependencies import get_download_service
from app.services.download_service import DownloadService

router = APIRouter(
    prefix="/status",
    tags=["Download"],
)


@router.get("")
async def get_status(
        service: DownloadService = Depends(get_download_service),
):
    state = service.get_status()

    return {
        "running": state.running,
        "started_at": state.started_at,
        "finished_at": state.finished_at,
        "total": state.total_names,
        "downloaded": state.downloaded,
        "error": state.error,
    }