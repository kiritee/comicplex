from __future__ import annotations
from pathlib import Path
from sqlmodel import select
from .db import session
from .models import Issue, Tag
import os

def safe_name(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in " .-_").strip()

def build_symlink_views(views_root: Path):
    views_root.mkdir(parents=True, exist_ok=True)
    with session() as s:
        tags = s.exec(select(Tag)).all()
        for t in tags:
            base = views_root / f"{t.kind}s" / safe_name(t.name)
            base.mkdir(parents=True, exist_ok=True)
            # Tag.issues relationship is available; iterate directly
            for iss in t.issues:
                src = Path(iss.path)
                if not src.exists():
                    continue
                link_name = base / f"{safe_name(iss.series.name)} #{iss.number}{src.suffix}"
                try:
                    if not link_name.exists():
                        os.symlink(src, link_name)
                except FileExistsError:
                    pass
                except OSError:
                    # Fallback (Windows without symlink privilege): try hardlink
                    try:
                        os.link(src, link_name)
                    except Exception:
                        pass
