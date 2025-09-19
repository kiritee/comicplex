from __future__ import annotations
from typing import Optional
import httpx
import requests_cache
from sqlmodel import select
from .db import session
from .models import Issue, Series

API = "https://comicvine.gamespot.com/api"

class ComicVineClient:
    def __init__(self, api_key: str, user_agent: str = "comicplex/0.1", cache_path: str = ".http_cache"):
        self.api_key = api_key
        self.headers = {"User-Agent": user_agent}
        self.client = httpx.Client(headers=self.headers, timeout=30.0)
        requests_cache.install_cache(cache_path, expire_after=60 * 60 * 24)

    def _get(self, endpoint: str, **params):
        params |= {"api_key": self.api_key, "format": "json"}
        r = self.client.get(f"{API}/{endpoint}", params=params)
        r.raise_for_status()
        return r.json()

    def search_issue(self, series_name: str, issue_number: str, volume_year: Optional[int] = None):
        # Search issues by series name + issue number, then filter
        q = f"{series_name} #{issue_number}"
        data = self._get("search/", query=q, resources="issue", limit=20)
        results = data.get("results", []) or []
        if volume_year:
            filtered = []
            for r in results:
                vol = r.get("volume") or {}
                sy = vol.get("start_year")
                # ComicVine returns start_year as string sometimes
                if str(sy) == str(volume_year):
                    filtered.append(r)
            results = filtered or results
        return results

    def enrich_issue(self, issue: Issue, series: Series):
        results = self.search_issue(series.name, issue.number, series.start_year)
        if not results:
            return False
        r0 = results[0]
        issue.title = r0.get("name") or issue.title
        issue.description = r0.get("description") or issue.description
        vol = r0.get("volume") or {}
        pub = (vol.get("publisher") or {}).get("name")
        if pub:
            issue.publisher = pub
        cover_date = r0.get("cover_date")
        if cover_date:
            issue.cover_date = cover_date  # SQLModel will coerce if string YYYY-MM-DD
        # Credits
        people = r0.get("person_credits") or []
        role_map = {
            "writer": "writer",
            "art": "artist",
            "penciler": "penciler",
            "inker": "inker",
            "colorist": "colorist",
            "letterer": "letterer",
        }
        for p in people:
            role = (p.get("role") or "").lower()
            name = p.get("name")
            if not name:
                continue
            for key, field_name in role_map.items():
                if key in role and (getattr(issue, field_name) in (None, "")):
                    setattr(issue, field_name, name)
        return True

def enrich_missing(api_key: str, user_agent: str = "comicplex/0.1"):
    cv = ComicVineClient(api_key, user_agent)
    with session() as s:
        issues = s.exec(select(Issue)).all()
        for iss in issues:
            if iss.title and iss.publisher and iss.writer:
                continue
            series = s.get(Series, iss.series_id)
            try:
                if cv.enrich_issue(iss, series):
                    s.add(iss); s.commit()
            except Exception:
                s.rollback()
