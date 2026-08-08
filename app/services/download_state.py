from dataclasses import dataclass, field
from datetime import datetime, UTC

@dataclass
class DownloadState:
    started_at: datetime | None = None
    finished_at: datetime | None = None
    total_names: int = 0
    downloaded: int = 0
    running: bool = False
    error: str | None = None

    def start(self) -> None:
        self.started_at = datetime.now(UTC)
        self.finished_at = None
        self.total_names = 0
        self.downloaded = 0
        self.running = True
        self.error = None

    def finish(self) -> None:
        self.finished_at = datetime.now(UTC)
        self.running = False

    def set_error(self, message: str) -> None:
        self.error = message