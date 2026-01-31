from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .extractors import summarize_text


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


DEFAULT_SECTION_TITLES = [
    "สารบรรณ",
    "เนื้อหาสรุป",
    "คำสำคัญ",
    "แบบฝึกหัด",
    "เฉลย/แนวคิด",
]


def create_draft(
    subject: str,
    lesson_title: str,
    grade_level: str,
    raw_text: str,
) -> WorksheetDraft:
    paragraphs = [p for p in raw_text.splitlines() if p.strip()]
    summary = summarize_text(paragraphs)

    key_points = paragraphs[:5] if paragraphs else ["เติมเนื้อหาจากหนังสือให้ครบถ้วน"]
    exercises = [
        "อธิบายแนวคิดสำคัญจากบทเรียนนี้",
        "ยกตัวอย่างที่สัมพันธ์กับชีวิตประจำวัน",
        "สร้างโจทย์ฝึกทักษะ 3 ข้อ",
    ]
    answer_hints = [
        "แนวคิดหลักควรอิงจากข้อความในหนังสือ",
        "ตอบเป็นข้อ ๆ เพื่อความชัดเจน",
    ]

    sections = [
        WorksheetSection(DEFAULT_SECTION_TITLES[0], [
            f"รายวิชา: {subject}",
            f"เรื่อง: {lesson_title}",
            f"ระดับชั้น: {grade_level}",
        ]),
        WorksheetSection(DEFAULT_SECTION_TITLES[1], [summary or "เพิ่มบทสรุปที่นี่"]),
        WorksheetSection(DEFAULT_SECTION_TITLES[2], key_points),
        WorksheetSection(DEFAULT_SECTION_TITLES[3], exercises),
        WorksheetSection(DEFAULT_SECTION_TITLES[4], answer_hints),
    ]

    return WorksheetDraft(
        subject=subject,
        lesson_title=lesson_title,
        grade_level=grade_level,
        sections=sections,
    )
