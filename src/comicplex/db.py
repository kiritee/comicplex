from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, select
from .models import Series, Issue, Tag, IssueTagLink

_engine = None

def init(db_path: Path):
    global _engine
    db_path.parent.mkdir(parents=True, exist_ok=True)
    _engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(_engine)
    return _engine

@contextmanager
def session():
    assert _engine is not None, "DB not initialized. Call db.init() first."
    with Session(_engine) as s:
        yield s

def upsert_series(s: Session, name: str, volume: int | None, start_year: int | None) -> Series:
    stmt = select(Series).where(Series.name == name, Series.volume == volume, Series.start_year == start_year)
    existing = s.exec(stmt).first()
    if existing:
        return existing
    obj = Series(name=name, volume=volume, start_year=start_year)
    s.add(obj); s.commit(); s.refresh(obj)
    return obj

def upsert_issue(s: Session, series: Series, number: str, path: str, **kwargs) -> Issue:
    stmt = select(Issue).where(Issue.series_id == series.id, Issue.number == number)
    existing = s.exec(stmt).first()
    if existing:
        for k, v in kwargs.items():
            if v is not None:
                setattr(existing, k, v)
        existing.path = path
        s.add(existing); s.commit(); s.refresh(existing)
        return existing
    obj = Issue(series_id=series.id, number=str(number), path=path, **kwargs)
    s.add(obj); s.commit(); s.refresh(obj)
    return obj

def upsert_tag(s: Session, kind: str, name: str) -> Tag:
    stmt = select(Tag).where(Tag.kind == kind, Tag.name == name)
    existing = s.exec(stmt).first()
    if existing:
        return existing
    obj = Tag(kind=kind, name=name)
    s.add(obj); s.commit(); s.refresh(obj)
    return obj

def link_issue_tag(s: Session, issue: Issue, tag: Tag):
    # Insert if not exists (composite PK enforces uniqueness)
    link = IssueTagLink(issue_id=issue.id, tag_id=tag.id)
    s.add(link)
    try:
        s.commit()
    except Exception:
        s.rollback()
