"""Smoke and regression tests for GuruAssist helper scripts."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "teacher-administration"
VALIDATOR = SKILL / "scripts" / "validate_lesson_data.py"
GENERATOR = SKILL / "scripts" / "generate_docx.py"
EXAMPLE = SKILL / "examples" / "pai-salat-berjamaah.json"


class ScriptTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_example_json_passes_validation(self):
        result = self.run_script(VALIDATOR, str(EXAMPLE))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("JSON structure is valid", result.stdout)

    def test_invalid_nested_type_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "bad.json"
            source.write_text(json.dumps({
                "subject": "IPA",
                "education_level": "SMP",
                "topic": "Tekanan zat",
                "activities": ["not", "an", "object"],
            }), encoding="utf-8")
            result = self.run_script(VALIDATOR, str(source))
        self.assertEqual(result.returncode, 1)
        self.assertIn("activities", result.stderr)

    def test_invalid_json_reports_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "bad.json"
            source.write_text("{invalid", encoding="utf-8")
            result = self.run_script(VALIDATOR, str(source))
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid JSON", result.stderr)

    def test_generator_creates_openable_docx(self):
        from docx import Document
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "nested" / "modul-ajar.docx"
            result = self.run_script(GENERATOR, str(EXAMPLE), "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())
            generated = Document(output)
            text = "\n".join(p.text for p in generated.paragraphs)
            self.assertIn("Rancangan Pembelajaran", text)
            self.assertIn("Perlu Konfirmasi Guru", text)

    def test_generator_rejects_wrong_nested_type(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "bad.json"
            output = Path(temp_dir) / "bad.docx"
            source.write_text(json.dumps({
                "subject": "IPA",
                "education_level": "SMP",
                "topic": "Tekanan zat",
                "assessment": "must be an object",
            }), encoding="utf-8")
            result = self.run_script(GENERATOR, str(source), "--output", str(output))
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
