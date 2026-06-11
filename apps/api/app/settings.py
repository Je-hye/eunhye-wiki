from dataclasses import dataclass
from typing import Literal, cast


AppMode = Literal["public", "private"]


@dataclass(frozen=True)
class Settings:
    app_mode: AppMode
    database_url: str
    notes_path: str | None = None

    def __post_init__(self) -> None:
        if self.app_mode not in {"public", "private"}:
            raise ValueError(f"Unsupported APP_MODE: {self.app_mode}")
        if not self.database_url:
            raise ValueError("DATABASE_URL is required")
        if self.app_mode == "public" and self.notes_path is not None:
            raise ValueError("Public mode cannot mount a notes path")

    @classmethod
    def from_values(
        cls,
        *,
        app_mode: str,
        database_url: str,
        notes_path: str | None = None,
    ) -> "Settings":
        return cls(
            app_mode=cast(AppMode, app_mode),
            database_url=database_url,
            notes_path=notes_path,
        )
