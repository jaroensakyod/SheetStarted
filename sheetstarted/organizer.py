from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .extractors import summarize_text
from .templates import SubjectTemplate, get_template


@dataclass
class WorksheetMetadata:
    standard: Optional[str] = None
    indicator: Optional[str] = None
    tags: Optional[List[str]] = None


@dataclass
class WorksheetSection:
    title: str
    content: List[str]


@dataclass
class WorksheetDraft:
    subject: str
    lesson_title: str
    grade_level: str
    sections: List[WorksheetSection]
    metadata: WorksheetMetadata


DEFAULT_SECTION_TITLES = [
    "สารบรรณ",
    "สาระ/ตัวชี้วัด",
    "เนื้อหาสรุป",
    "คำสำคัญ",
    "แบบฝึกหัด",
    "เฉลย/แนวคิด",
]


def _build_exercises(template: SubjectTemplate, difficulty: str, count: int) -> List[str]:
    prompts = [
        f"ระดับความยาก: {difficulty}",
    ]
    base = template.exercise_prompts or []
    for index in range(count):
        prompt = base[index % len(base)] if base else "สร้างโจทย์ฝึกทักษะ"
        prompts.append(f"{index + 1}. {prompt}")
    return prompts


def create_draft(
    subject: str,
    lesson_title: str,
    grade_level: str,
    raw_text: str,
    metadata: WorksheetMetadata,
    difficulty: str = "ปานกลาง",
    exercise_count: int = 3,
    template_subject: Optional[str] = None,
    summary_override: Optional[str] = None,
) -> WorksheetDraft:
    paragraphs = [p for p in raw_text.splitlines() if p.strip()]
    summary = summary_override or summarize_text(paragraphs)

    template = get_template(subject, fallback_subject=template_subject)
    key_points = paragraphs[:5] if paragraphs else ["เติมเนื้อหาจากหนังสือให้ครบถ้วน"]
    exercises = _build_exercises(template, difficulty, exercise_count)
    answer_hints = [template.answer_hint]

    sections = [
        WorksheetSection(
            DEFAULT_SECTION_TITLES[0],
            [
                f"รายวิชา: {subject}",
                f"เรื่อง: {lesson_title}",
                f"ระดับชั้น: {grade_level}",
                template.summary_prompt,
            ],
        ),
    ]

    if metadata.standard or metadata.indicator or metadata.tags:
        metadata_lines = []
        if metadata.standard:
            metadata_lines.append(f"มาตรฐาน/สาระ: {metadata.standard}")
        if metadata.indicator:
            metadata_lines.append(f"ตัวชี้วัด: {metadata.indicator}")
        if metadata.tags:
            metadata_lines.append(f"แท็ก: {', '.join(metadata.tags)}")
        sections.append(WorksheetSection(DEFAULT_SECTION_TITLES[1], metadata_lines))

    sections.extend(
        [
            WorksheetSection(DEFAULT_SECTION_TITLES[2], [summary or "เพิ่มบทสรุปที่นี่"]),
            WorksheetSection(DEFAULT_SECTION_TITLES[3], key_points),
            WorksheetSection(DEFAULT_SECTION_TITLES[4], exercises),
            WorksheetSection(DEFAULT_SECTION_TITLES[5], answer_hints),
        ]
    )

    return WorksheetDraft(
        subject=subject,
        lesson_title=lesson_title,
        grade_level=grade_level,
        sections=sections,
        metadata=metadata,
    )
