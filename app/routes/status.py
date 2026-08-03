from fastapi import APIRouter

from app.services import download_state
from app.services.download_state import download_state

router = APIRouter(prefix="/status", tags=["Download"])


@router.get("")
async def status():
    return {
        "running": download_state.running,
        "started_at": download_state.started_at,
        "downloaded": download_state.downloaded,
        "total": download_state.total_names,
    }