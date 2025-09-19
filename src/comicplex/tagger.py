from __future__ import annotations
from sqlmodel import select
from .db import session, upsert_tag, link_issue_tag
from .models import Issue

CREATOR_KEYS = ["writer", "artist", "penciler", "inker", "colorist", "letterer"]

def attach_basic_tags():
    with session() as s:
        issues = s.exec(select(Issue)).all()
        for iss in issues:
            # creators
            for key in CREATOR_KEYS:
                val = getattr(iss, key)
                if val:
                    tag = upsert_tag(s, kind="creator", name=val)
                    link_issue_tag(s, iss, tag)
            # publisher
            if iss.publisher:
                tag = upsert_tag(s, kind="publisher", name=iss.publisher)
                link_issue_tag(s, iss, tag)
