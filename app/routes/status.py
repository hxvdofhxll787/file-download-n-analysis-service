from fastapi import APIRouter

from app.services import download_state
from app.services.download_state import download_state

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