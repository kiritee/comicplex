from __future__ import annotations
from pathlib import Path
from typing import Iterable
from .filename_parser import parse_filename
from .db import upsert_series, upsert_issue, session

SUPPORTED = {".cbz", ".cbr", ".pdf", ".zip", ".rar"}

def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED:
            yield p

def scan_into_db(library_root: Path):
    for p in iter_files(library_root):
        parsed = parse_filename(p)
        if not parsed:
            continue
        with session() as s:
            series = upsert_series(s, parsed.title, parsed.volume, parsed.year)
            upsert_issue(
                s,
                series,
                number=parsed.issue,
                path=str(p.resolve()),
                file_ext=parsed.ext,
            )
