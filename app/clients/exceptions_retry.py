import asyncio
import httpx

class RemoteAPIError(Exception):
    """Базовые исключения"""

class RateLimitError(RemoteAPIError):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Повторить попытку можно через {retry_after} секунд")

class BlockError(RemoteAPIError):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Блокировка на {retry_after} секунд")

class RetryPolicy:
    MAX_RETRIES = 5

    async def execute(self, request):
        for attempt in range(self.MAX_RETRIES):
            response = await request()

            if response.status_code < 400:
                return response

            if response.status_code == 429:
                retry = int(response.headers.get("Retry-After"))

                await asyncio.sleep(retry)
                continue

            if response.status_code == 403:
                retry = int(response.headers.get("Retry-After"))

                raise BlockError(retry)

            response.raise_for_status()

        raise RateLimitError(retry)