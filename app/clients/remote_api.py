from typing import Any

import httpx

from app.core.config import settings

class RemoteAPIError(Exception):
    pass

class RemoteAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.REMOTE_API_URL,
            timeout=60.0,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def get_file_names(self, filenames: list[str]) -> list[str]:
        response = await self.client.post(
            "/api/files/download",
            json={
                "names": filenames,
            }
        )

        await self._handle_errors(response)

        return response.content

    async def mark_downloaded(self, filenames: list[str]) -> None:
        response = await self.client.post(
            "/api/files/downloaded",
            json={
                "names": filenames,
            },
        )

        await self._handle_errors(response)

    async def _handle_errors(self, response: httpx.Response) -> None:
        if response.status_code == 200:
            return

        raise RemoteAPIError(
            f"API error: {response.status_code}"
        )