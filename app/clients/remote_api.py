from typing import Any

import httpx

from app.clients.exceptions_retry import RetryPolicy
from app.core.config import settings

class RemoteAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.REMOTE_API_URL,
            timeout=60.0,
        )

        self.retry = RetryPolicy()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def get_file_names(self) -> list[str]:
        response = await self.retry.execute(
            lambda: self.client.get("/api/files/names")
        )

        return response.json()

    async def download_files(self, filenames: list[str]) -> bytes:
        response = await self.retry.execute(
            lambda: self.client.post(
                "/api/files/download",
                json={"names": filenames},
            )
        )

        return response.content

    async def mark_downloaded(self, filenames: list[str]) -> None:
        await self.retry.execute(
            lambda: self.client.post(
                "/api/files/downloaded",
                json={"names": filenames},
            )
        )