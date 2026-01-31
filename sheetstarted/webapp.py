from __future__ import annotations

import os
from pathlib import Path
from typing import List

from flask import Flask, flash, redirect, render_template, request, send_file, url_for

from .cli import _sanitize_filename
from .docx_writer import write_docx
from .extractors import extract_text
from .organizer import WorksheetMetadata, create_draft


def _save_uploads(files, upload_dir: Path) -> List[Path]:
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for file_storage in files:
        filename = _sanitize_filename(Path(file_storage.filename or "upload").stem) or "upload"
        suffix = Path(file_storage.filename or "").suffix or ".bin"
        path = upload_dir / f"{filename}{suffix}"
        file_storage.save(path)
        saved.append(path)
    return saved


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("SHEETSTARTED_SECRET", "sheetstarted")

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            subject = request.form.get("subject", "")
            lesson_title = request.form.get("lesson_title", "")
            grade = request.form.get("grade", "มัธยมศึกษา")
            difficulty = request.form.get("difficulty", "ปานกลาง")
            exercise_count = int(request.form.get("exercise_count", 3))
            standard = request.form.get("standard")
            indicator = request.form.get("indicator")
            tags = request.form.get("tags", "")
            tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

            uploads = request.files.getlist("files")
            if not uploads:
                flash("กรุณาเลือกไฟล์ PDF หรือรูปภาพ")
                return redirect(url_for("index"))

            upload_dir = Path("uploads")
            paths = _save_uploads(uploads, upload_dir)
            texts = [extract_text(path, "tha+eng") for path in paths]
            combined_text = "\n".join(texts)

            metadata = WorksheetMetadata(
                standard=standard,
                indicator=indicator,
                tags=tags_list,
            )
            draft = create_draft(
                subject=subject,
                lesson_title=lesson_title,
                grade_level=grade,
                raw_text=combined_text,
                metadata=metadata,
                difficulty=difficulty,
                exercise_count=exercise_count,
            )
            output_dir = Path("output")
            filename = _sanitize_filename(lesson_title) or "worksheet"
            output_path = output_dir / f"{filename}.docx"
            write_docx(draft, output_path)
            return send_file(output_path, as_attachment=True)

        return render_template("index.html")

    return app


def main() -> int:
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
