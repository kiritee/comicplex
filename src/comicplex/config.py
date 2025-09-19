from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    library_root: Path = Field(default_factory=lambda: Path.cwd())
    db_path: Path = Field(default_factory=lambda: Path("./data/catalog.db"))
    comicvine_api_key: str | None = Field(default_factory=lambda: os.getenv("COMICVINE_API_KEY"))
    user_agent: str = "comicplex/0.1 (+https://github.com/kiritee/comicplex)"
    cache_path: Path = Path(".http_cache")

    class Config:
        arbitrary_types_allowed = True

def load_settings(**overrides) -> "Settings":
    base = Settings()
    return base.model_copy(update=overrides)
