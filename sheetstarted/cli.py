from __future__ import annotations

import argparse
import zipfile
from pathlib import Path
from typing import List, Optional

from .docx_writer import write_docx
from .downloader import resolve_input
from .extractors import extract_text
from .llm import LlmError, summarize_with_llm
from .organizer import WorksheetMetadata, create_draft
from .toc import parse_toc


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
    parser.add_argument(
        "--difficulty",
        default="ปานกลาง",
        help="ระดับความยากของแบบฝึกหัด",
    )
    parser.add_argument(
        "--exercise-count",
        type=int,
        default=3,
        help="จำนวนข้อแบบฝึกหัด",
    )
    parser.add_argument(
        "--standard",
        help="มาตรฐาน/สาระการเรียนรู้",
    )
    parser.add_argument(
        "--indicator",
        help="ตัวชี้วัด",
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        help="แท็กเพิ่มเติม",
    )
    parser.add_argument(
        "--template-subject",
        help="ใช้เทมเพลตของรายวิชาอื่น",
    )
    parser.add_argument(
        "--llm-summary",
        action="store_true",
        help="ใช้ LLM เพื่อสรุปเนื้อหา (ต้องตั้งค่า LLM_ENDPOINT)",
    )
    parser.add_argument(
        "--split-by-toc",
        action="store_true",
        help="แยกสร้างใบงานตามสารบัญที่ตรวจพบ",
    )
    parser.add_argument(
        "--bundle-zip",
        action="store_true",
        help="สร้างไฟล์ zip รวมชุดใบงาน",
    )
    return parser


def gather_texts(inputs: List[str], cache_dir: Path, ocr_language: str) -> List[str]:
    texts = []
    for item in inputs:
        path = resolve_input(item, cache_dir)
        texts.append(extract_text(path, ocr_language))
    return texts


def build_metadata(args: argparse.Namespace) -> WorksheetMetadata:
    return WorksheetMetadata(
        standard=args.standard,
        indicator=args.indicator,
        tags=args.tags,
    )


def _resolve_summary(text: str, subject: str, use_llm: bool) -> Optional[str]:
    if not use_llm:
        return None
    try:
        return summarize_with_llm(text, subject)
    except LlmError as exc:
        print(f"ไม่สามารถใช้ LLM ได้: {exc}")
        return None


def _write_bundle(outputs: List[Path], zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for output in outputs:
            archive.write(output, arcname=output.name)


def _sanitize_filename(name: str) -> str:
    return "".join(ch for ch in name if ch.isalnum() or ch in {" ", "-", "_"}).strip()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    texts = gather_texts(args.inputs, cache_dir, args.ocr_language)
    combined_text = "\n".join(texts)
    metadata = build_metadata(args)
    summary_override = _resolve_summary(combined_text, args.subject, args.llm_summary)

    output_path = Path(args.output)
    outputs: List[Path] = []

    if args.split_by_toc:
        toc_entries = parse_toc(combined_text)
        if not toc_entries:
            print("ไม่พบสารบัญ ใช้โหมดสร้างใบงานปกติแทน")
        else:
            output_dir = output_path if output_path.suffix == "" else output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            for entry in toc_entries:
                filename = _sanitize_filename(entry.title) or "worksheet"
                draft = create_draft(
                    subject=args.subject,
                    lesson_title=entry.title,
                    grade_level=args.grade,
                    raw_text=combined_text,
                    metadata=metadata,
                    difficulty=args.difficulty,
                    exercise_count=args.exercise_count,
                    template_subject=args.template_subject,
                    summary_override=summary_override,
                )
                file_path = output_dir / f"{filename}.docx"
                outputs.append(write_docx(draft, file_path))
    if not outputs:
        draft = create_draft(
            subject=args.subject,
            lesson_title=args.lesson_title,
            grade_level=args.grade,
            raw_text=combined_text,
            metadata=metadata,
            difficulty=args.difficulty,
            exercise_count=args.exercise_count,
            template_subject=args.template_subject,
            summary_override=summary_override,
        )
        outputs.append(write_docx(draft, output_path))

    if args.bundle_zip and len(outputs) > 1:
        zip_path = output_path.with_suffix(".zip")
        _write_bundle(outputs, zip_path)
        print(f"สร้างไฟล์ zip รวมใบงานเรียบร้อย: {zip_path}")

    for output in outputs:
        print(f"สร้างไฟล์ใบงานเรียบร้อย: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
