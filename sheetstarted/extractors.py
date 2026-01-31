from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

import pdfplumber
import pytesseract
from PIL import Image


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


class ExtractionError(RuntimeError):
    pass


def extract_text_from_pdf(path: Path) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            pages_text = [page.extract_text() or "" for page in pdf.pages]
    except Exception as exc:
        raise ExtractionError(f"อ่าน PDF ไม่สำเร็จ: {path}") from exc

    combined = "\n".join(text.strip() for text in pages_text if text.strip())
    if not combined:
        raise ExtractionError(
            "ไม่พบข้อความใน PDF หากเป็นไฟล์สแกนควรแปลงเป็นภาพและใช้ OCR"
        )
    return combined


def extract_text_from_image(path: Path, language: str = "tha+eng") -> str:
    try:
        image = Image.open(path)
        text = pytesseract.image_to_string(image, lang=language)
    except Exception as exc:
        raise ExtractionError(f"อ่านรูปภาพไม่สำเร็จ: {path}") from exc

    cleaned = text.strip()
    if not cleaned:
        raise ExtractionError("ไม่พบข้อความในรูปภาพ")
    return cleaned


def infer_extractor(path: Path) -> Tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return "pdf", suffix
    if suffix in SUPPORTED_IMAGE_EXTENSIONS:
        return "image", suffix
    raise ExtractionError(f"ไม่รองรับไฟล์นามสกุล {suffix}")


def extract_text(path: Path, ocr_language: str) -> str:
    kind, _ = infer_extractor(path)
    if kind == "pdf":
        return extract_text_from_pdf(path)
    return extract_text_from_image(path, language=ocr_language)


def summarize_text(text_blocks: Iterable[str], limit: int = 3) -> str:
    paragraphs = [block.strip() for block in text_blocks if block.strip()]
    summary = paragraphs[:limit]
    return "\n".join(summary)
