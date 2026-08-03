from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DownloadedFile(Base):
    __tablename__ = "downloaded_files"

    id: Mapped[int] = mapped_column(primary_key=True)

    filename: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    downloaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )