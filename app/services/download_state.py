from dataclasses import dataclass, field
from datetime import datetime, UTC

@dataclass
class DownloadState:
    started_at: datetime | None = None
    total_names: int = 0
    downloaded: int = 0
    running: bool = False

    def start(self) -> None:
        self.started_at = datetime.now(UTC)
        self.total_names = 0
        self.downloaded = 0
        self.running = True

    def finish(self) -> None:
        self.running = False

download_state = DownloadState()