from __future__ import annotations

import os
from typing import Optional

import requests


class LlmError(RuntimeError):
    pass


def summarize_with_llm(text: str, subject: str) -> str:
    endpoint = os.getenv("LLM_ENDPOINT")
    api_key = os.getenv("LLM_API_KEY")
    if not endpoint:
        raise LlmError("ต้องกำหนด LLM_ENDPOINT เพื่อใช้งาน LLM")

    payload = {
        "prompt": f"สรุปบทเรียนวิชา{subject}แบบสั้นและเป็นหัวข้อ:\n{text}",
        "max_tokens": 512,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(endpoint, json=payload, headers=headers, timeout=60)
    if not response.ok:
        raise LlmError(f"LLM ตอบกลับไม่สำเร็จ: {response.status_code}")
    data = response.json()
    summary: Optional[str] = data.get("summary") or data.get("text")
    if not summary:
        raise LlmError("ไม่พบผลสรุปจาก LLM")
    return summary.strip()
