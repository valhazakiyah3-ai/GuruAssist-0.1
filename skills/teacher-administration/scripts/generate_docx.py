#!/usr/bin/env python3
"""Create an editable DOCX draft from a GuruAssist lesson JSON record.

This script formats supplied data only. It does not generate content with AI,
verify curriculum, or submit documents to any education platform.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from docx import Document
    from docx.shared import Inches, Pt
except ImportError:
    print("ERROR: python-docx is required. Run: python -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

try:
    from validate_lesson_data import validate
except ImportError:  # Allows importing this file as a module in tests or other scripts.
    validate = None


def add_bullets(doc: Any, items: list[str] | None) -> None:
    for item in items or []:
        doc.add_paragraph(item, style="List Bullet")


def load_input(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    except OSError as exc:
        raise ValueError(f"cannot read input: {exc}") from exc

    if validate is not None:
        errors, _warnings = validate(data)
    else:
        errors = []
        if not isinstance(data, dict):
            errors.append("top-level JSON value must be an object")
        else:
            for key in ("subject", "education_level", "topic"):
                if not isinstance(data.get(key), str) or not data[key].strip():
                    errors.append(f"'{key}' must be a non-empty string")
    if errors:
        raise ValueError("invalid lesson data: " + "; ".join(errors))
    return data


def build_document(data: dict[str, Any]) -> Any:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10)

    doc.add_heading("Rancangan Pembelajaran — DRAF", 0)
    doc.add_paragraph(
        "Dokumen ini dibuat dari data yang diberikan. Guru wajib memeriksa dan "
        "menyesuaikannya sebelum digunakan."
    )
    doc.add_heading("A. Identitas", level=1)
    identity = [
        ("Satuan pendidikan", data.get("school_name", "Belum diisi")),
        ("Mata pelajaran", data.get("subject", "Belum diisi")),
        ("Jenjang", data.get("education_level", "Belum diisi")),
        ("Kelas", data.get("grade", "Belum diisi")),
        ("Fase", data.get("phase", "Belum diisi")),
        ("Semester", data.get("semester", "Belum diisi")),
        ("Kurikulum", data.get("curriculum", "Belum diisi")),
        ("Topik", data.get("topic", "Belum diisi")),
        ("Alokasi waktu", data.get("duration", "Belum diisi")),
    ]
    table = doc.add_table(rows=0, cols=2)
    table.style = "Light Shading Accent 1"
    for label, value in identity:
        cells = table.add_row().cells
        cells[0].text = str(label)
        cells[1].text = str(value) if value not in (None, "") else "Belum diisi"

    doc.add_heading("B. Capaian dan Tujuan Pembelajaran", level=1)
    doc.add_heading("Capaian/standar pembelajaran", level=2)
    add_bullets(doc, data.get("learning_outcomes", []))
    doc.add_heading("Tujuan pembelajaran", level=2)
    add_bullets(doc, data.get("learning_objectives", []))

    doc.add_heading("C. Karakteristik Peserta Didik", level=1)
    doc.add_paragraph(data.get("student_context") or "Belum diisi")
    doc.add_heading("D. Materi, Metode, dan Sumber", level=1)
    add_bullets(doc, data.get("materials", []))
    add_bullets(doc, data.get("learning_method", []))
    if data.get("references"):
        doc.add_heading("Sumber/referensi", level=2)
        add_bullets(doc, data.get("references", []))

    activities = data.get("activities", {})
    doc.add_heading("E. Langkah Pembelajaran", level=1)
    for key, heading in (("opening", "Pendahuluan"), ("core", "Kegiatan Inti"), ("closing", "Penutup")):
        doc.add_heading(heading, level=2)
        add_bullets(doc, activities.get(key, []))

    assessment = data.get("assessment", {})
    doc.add_heading("F. Asesmen", level=1)
    for key, heading in (("formative", "Formatif"), ("summative", "Sumatif"), ("criteria", "Kriteria")):
        doc.add_heading(heading, level=2)
        add_bullets(doc, assessment.get(key, []))

    doc.add_heading("G. Perlu Konfirmasi Guru", level=1)
    add_bullets(doc, data.get("needs_confirmation", []))
    doc.add_paragraph(
        "Catatan: dokumen ini merupakan draf format, bukan pengesahan kurikulum. "
        "Periksa kesesuaian kurikulum, fakta, sumber, aksesibilitas, dan kebijakan sekolah."
    )
    return doc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input lesson JSON")
    parser.add_argument("--output", type=Path, default=Path("guruassist-draft.docx"), help="Output DOCX path")
    args = parser.parse_args()

    try:
        data = load_input(args.input)
        doc = build_document(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        doc.save(args.output)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Created editable draft: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
