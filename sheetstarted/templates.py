from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SubjectTemplate:
    subject: str
    summary_prompt: str
    key_point_prefix: str
    exercise_prompts: List[str]
    answer_hint: str


SUBJECT_TEMPLATES = {
    "คณิตศาสตร์": SubjectTemplate(
        subject="คณิตศาสตร์",
        summary_prompt="สรุปแนวคิด/สูตรสำคัญพร้อมตัวอย่างสั้น ๆ",
        key_point_prefix="สูตร/นิยามสำคัญ",
        exercise_prompts=[
            "สร้างโจทย์คำนวณ 3 ข้อ ระดับง่าย-กลาง-ยาก",
            "อธิบายขั้นตอนการแก้โจทย์อย่างละเอียด",
            "ยกตัวอย่างโจทย์ที่เกี่ยวข้องกับชีวิตประจำวัน",
        ],
        answer_hint="เฉลยพร้อมแสดงวิธีทำทุกขั้น",
    ),
    "วิทยาศาสตร์": SubjectTemplate(
        subject="วิทยาศาสตร์",
        summary_prompt="สรุปแนวคิดและกระบวนการที่สำคัญ",
        key_point_prefix="กระบวนการ/คำศัพท์",
        exercise_prompts=[
            "ออกแบบกิจกรรมทดลองง่าย ๆ 1 กิจกรรม",
            "ถาม-ตอบ 5 ข้อเกี่ยวกับความเข้าใจหลักการ",
            "ยกตัวอย่างปรากฏการณ์ที่พบในชีวิตจริง",
        ],
        answer_hint="ชี้แจงหลักการที่ถูกต้องและสั้นกระชับ",
    ),
    "ภาษาอังกฤษ": SubjectTemplate(
        subject="ภาษาอังกฤษ",
        summary_prompt="สรุปโครงสร้างประโยค/คำศัพท์หลัก",
        key_point_prefix="คำศัพท์/โครงสร้าง",
        exercise_prompts=[
            "ให้เติมคำในช่องว่าง 5 ข้อ",
            "แต่งประโยค 3 ประโยคตามหลักไวยากรณ์",
            "ถาม-ตอบเกี่ยวกับบทสนทนา",
        ],
        answer_hint="เฉลยพร้อมคำอธิบายไวยากรณ์สั้น ๆ",
    ),
    "ภาษาไทย": SubjectTemplate(
        subject="ภาษาไทย",
        summary_prompt="สรุปหลักภาษาและวรรณคดีที่เกี่ยวข้อง",
        key_point_prefix="คำสำคัญ",
        exercise_prompts=[
            "ให้สรุปใจความสำคัญจากบทอ่าน",
            "ตั้งคำถามเชิงวิเคราะห์ 3 ข้อ",
            "ฝึกเรียบเรียงประโยคให้ถูกต้อง",
        ],
        answer_hint="เฉลยพร้อมเหตุผลประกอบ",
    ),
    "สังคมศึกษา": SubjectTemplate(
        subject="สังคมศึกษา",
        summary_prompt="สรุปเนื้อหาประเด็นสำคัญตามลำดับเวลา",
        key_point_prefix="เหตุการณ์/แนวคิด",
        exercise_prompts=[
            "สรุปเหตุการณ์สำคัญ 3 เหตุการณ์",
            "ตั้งคำถามเชิงเปรียบเทียบ 3 ข้อ",
            "เชื่อมโยงบทเรียนกับสถานการณ์ปัจจุบัน",
        ],
        answer_hint="เฉลยเน้นเหตุผลและข้อมูลอ้างอิง",
    ),
    "เคมี": SubjectTemplate(
        subject="เคมี",
        summary_prompt="สรุปโครงสร้าง/สมการ/กระบวนการ",
        key_point_prefix="สมการ/คำศัพท์",
        exercise_prompts=[
            "เขียนสมการเคมี 3 สมการ",
            "ถาม-ตอบแนวคิดหลัก 5 ข้อ",
            "โจทย์คำนวณ 2 ข้อ",
        ],
        answer_hint="เฉลยพร้อมหน่วยและสมการที่ถูกต้อง",
    ),
    "ฟิสิกส์": SubjectTemplate(
        subject="ฟิสิกส์",
        summary_prompt="สรุปกฎ/สูตรและตัวอย่างการใช้",
        key_point_prefix="กฎ/สูตร",
        exercise_prompts=[
            "โจทย์คำนวณ 3 ข้อ",
            "อธิบายกฎฟิสิกส์ที่เกี่ยวข้อง",
            "ยกตัวอย่างการประยุกต์ใช้จริง",
        ],
        answer_hint="เฉลยพร้อมขั้นตอนและหน่วย",
    ),
    "ชีววิทยา": SubjectTemplate(
        subject="ชีววิทยา",
        summary_prompt="สรุปโครงสร้างและกระบวนการชีวภาพ",
        key_point_prefix="โครงสร้าง/กระบวนการ",
        exercise_prompts=[
            "ถาม-ตอบเชิงอธิบาย 5 ข้อ",
            "สร้างแผนผังความสัมพันธ์ของกระบวนการ",
            "ยกตัวอย่างระบบชีวภาพใกล้ตัว",
        ],
        answer_hint="เฉลยสั้นกระชับและถูกต้องตามหลักชีววิทยา",
    ),
}


def get_template(subject: str, fallback_subject: Optional[str] = None) -> SubjectTemplate:
    if subject in SUBJECT_TEMPLATES:
        return SUBJECT_TEMPLATES[subject]
    if fallback_subject and fallback_subject in SUBJECT_TEMPLATES:
        return SUBJECT_TEMPLATES[fallback_subject]
    return SubjectTemplate(
        subject=subject,
        summary_prompt="สรุปเนื้อหาสำคัญ",
        key_point_prefix="คำสำคัญ",
        exercise_prompts=[
            "อธิบายแนวคิดสำคัญจากบทเรียนนี้",
            "ยกตัวอย่างที่สัมพันธ์กับชีวิตประจำวัน",
            "สร้างโจทย์ฝึกทักษะ 3 ข้อ",
        ],
        answer_hint="แนวคิดหลักควรอิงจากข้อความในหนังสือ",
    )
