from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.parse import urlparse

import requests


class DownloadError(RuntimeError):
    pass


def is_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def download_to_cache(url: str, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    file_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    extension = Path(urlparse(url).path).suffix or ".bin"
    target_path = cache_dir / f"{file_hash}{extension}"
    if target_path.exists():
        return target_path

    response = requests.get(url, timeout=30)
    if not response.ok:
        raise DownloadError(f"ดาวน์โหลดไม่สำเร็จ: {url} ({response.status_code})")

    with open(target_path, "wb") as file_handle:
        file_handle.write(response.content)

    return target_path


def resolve_input(input_value: str, cache_dir: Path) -> Path:
    if is_url(input_value):
        return download_to_cache(input_value, cache_dir)

    path = Path(os.path.expanduser(input_value)).resolve()
    if not path.exists():
        raise FileNotFoundError(f"ไม่พบไฟล์: {path}")
    return path
