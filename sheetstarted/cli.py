from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from .docx_writer import write_docx
from .downloader import resolve_input
from .extractors import extract_text
from .organizer import create_draft


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="สร้างใบงานจากไฟล์ PDF/รูปภาพ แล้วส่งออกเป็น Word (.docx)",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="พาธไฟล์ PDF/รูปภาพ หรือ URL ที่ต้องการอ่าน",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="ชื่อรายวิชา เช่น คณิตศาสตร์",
    )
    parser.add_argument(
        "--lesson-title",
        required=True,
        help="ชื่อบทเรียน เช่น สมการเชิงเส้น",
    )
    parser.add_argument(
        "--grade",
        default="มัธยมศึกษา",
        help="ระดับชั้นที่ต้องการ",
    )
    parser.add_argument(
        "--output",
        default="output/worksheet.docx",
        help="ที่อยู่ไฟล์ Word ที่ต้องการสร้าง",
    )
    parser.add_argument(
        "--ocr-language",
        default="tha+eng",
        help="ภาษาสำหรับ OCR ของภาพ (ค่าเริ่มต้น: tha+eng)",
    )
    parser.add_argument(
        "--cache-dir",
        default=".cache",
        help="โฟลเดอร์เก็บไฟล์ที่ดาวน์โหลด",
    )
    return parser


def gather_texts(inputs: List[str], cache_dir: Path, ocr_language: str) -> List[str]:
    texts = []
    for item in inputs:
        path = resolve_input(item, cache_dir)
        texts.append(extract_text(path, ocr_language))
    return texts


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    texts = gather_texts(args.inputs, cache_dir, args.ocr_language)
    combined_text = "\n".join(texts)

    draft = create_draft(
        subject=args.subject,
        lesson_title=args.lesson_title,
        grade_level=args.grade,
        raw_text=combined_text,
    )

    output_path = Path(args.output)
    write_docx(draft, output_path)
    print(f"สร้างไฟล์ใบงานเรียบร้อย: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
