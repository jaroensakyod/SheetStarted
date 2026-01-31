from __future__ import annotations

from pathlib import Path

from docx import Document

from .organizer import WorksheetDraft


def write_docx(draft: WorksheetDraft, output_path: Path) -> Path:
    document = Document()
    document.add_heading("ใบงาน", level=0)
    document.add_paragraph(f"รายวิชา: {draft.subject}")
    document.add_paragraph(f"เรื่อง: {draft.lesson_title}")
    document.add_paragraph(f"ระดับชั้น: {draft.grade_level}")

    for section in draft.sections:
        document.add_heading(section.title, level=1)
        for item in section.content:
            document.add_paragraph(item)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
    return output_path
