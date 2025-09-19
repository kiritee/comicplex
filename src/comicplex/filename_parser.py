from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Handles examples like:
# "Batman v2 012 (2012) (Digital).cbz"
# "The Amazing Spider-Man (1963) #050.cbz"
# "Daredevil 10.1 (2012).cbr"
# "Action Comics 1000 (2018).cbz"
# "X-Men - Messiah Complex 01 (of 13) (2007).pdf"

VOL = r"v(?P<volume>\d{1,2})"
YEAR = r"\(?(?P<year>19\d{2}|20\d{2})\)?"
ISSUE = r"(?P<issue>(?:\d+\.?\d*|Annual ?\d*|One[- ]Shot|FCBD|0\.1|0))"
OF = r"(?:\(of (?P<of>\d{1,3})\))?"

CORE = rf"^(?P<title>.+?)\s+(?:{VOL}\s+)?(?:#?\s*)?{ISSUE}\s*(?:{YEAR})?\b"
ALT = rf"^(?P<title>.+?)\s+{YEAR}\s*[# ]\s*{ISSUE}"
MINI = rf"^(?P<title>.+?)\s+{ISSUE}\s*{OF}\s*{YEAR}?"

PATTERNS = [re.compile(p, re.IGNORECASE) for p in [CORE, ALT, MINI]]

@dataclass
class ParsedName:
    title: str
    issue: str
    volume: Optional[int]
    year: Optional[int]
    ext: str

def parse_filename(path: Path) -> ParsedName | None:
    name = path.stem
    for pat in PATTERNS:
        m = pat.search(name)
        if m:
            gd = m.groupdict()
            title = re.sub(r"[._]+", " ", gd.get("title", "").strip(" -_"))
            vol = gd.get("volume")
            year = gd.get("year")
            issue = gd.get("issue")
            return ParsedName(
                title=title,
                issue=issue.strip() if issue else "",
                volume=int(vol) if vol else None,
                year=int(year) if year else None,
                ext=path.suffix.lower().lstrip("."),
            )
    # Fallback: "Title - 123 (2014)"
    m = re.search(r"^(?P<title>.+?)[-_ ]+(?P<issue>\d{1,4})\s*\((?P<year>\d{4})\)", name)
    if m:
        gd = m.groupdict()
        return ParsedName(
            title=gd["title"].strip(),
            issue=gd["issue"],
            volume=None,
            year=int(gd["year"]),
            ext=path.suffix.lower().lstrip("."),
        )
    return None
