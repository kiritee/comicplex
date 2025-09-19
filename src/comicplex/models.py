from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class IssueTagLink(SQLModel, table=True):
    issue_id: Optional[int] = Field(default=None, foreign_key="issue.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class Series(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    volume: Optional[int] = None      # Relaunch volume (e.g., v2)
    start_year: Optional[int] = None

    issues: List["Issue"] = Relationship(back_populates="series")

class Issue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")
    number: str                        # Keep as string: 0.1, Annual, FCBD, etc.
    title: Optional[str] = None
    cover_date: Optional[date] = None
    path: str                          # Original file path
    file_ext: Optional[str] = None

    writer: Optional[str] = None
    artist: Optional[str] = None
    colorist: Optional[str] = None
    penciler: Optional[str] = None
    inker: Optional[str] = None
    letterer: Optional[str] = None
    publisher: Optional[str] = None
    description: Optional[str] = None

    series: Optional[Series] = Relationship(back_populates="issues")
    tags: List["Tag"] = Relationship(back_populates="issues", link_model=IssueTagLink)

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kind: str  # character | team | event | arc | era | creator | publisher
    name: str

    issues: List[Issue] = Relationship(back_populates="tags", link_model=IssueTagLink)
