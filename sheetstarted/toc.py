from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class TocEntry:
    title: str
    page: int | None = None


TOC_PATTERN = re.compile(r"^(?P<title>.+?)\s+(?P<page>\d{1,4})$")


def parse_toc(text: str, limit: int = 20) -> List[TocEntry]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    entries: List[TocEntry] = []
    for line in lines:
        match = TOC_PATTERN.match(line)
        if match:
            title = match.group("title")
            page = int(match.group("page"))
            entries.append(TocEntry(title=title, page=page))
            continue
        if "บท" in line or "หน่วย" in line:
            entries.append(TocEntry(title=line))
        if len(entries) >= limit:
            break
    return entries
