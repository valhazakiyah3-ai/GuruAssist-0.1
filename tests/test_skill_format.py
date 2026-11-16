"""Conformance checks for the bundled Agent Skill manifest."""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "teacher-administration"
SKILL_FILE = SKILL_DIR / "SKILL.md"


class SkillFormatTests(unittest.TestCase):
    def test_frontmatter_matches_agent_skills_core_rules(self):
        content = SKILL_FILE.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
        parts = content.split("---", 2)
        self.assertEqual(len(parts), 3, "SKILL.md must have a closing frontmatter delimiter")
        metadata = yaml.safe_load(parts[1])
        self.assertIsInstance(metadata, dict)
        self.assertEqual(metadata.get("name"), SKILL_DIR.name)
        self.assertRegex(metadata.get("name", ""), r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(metadata["name"]), 64)
        description = metadata.get("description")
        self.assertIsInstance(description, str)
        self.assertTrue(description.strip())
        self.assertLessEqual(len(description), 1024)
        self.assertNotRegex(description, r"[<>]")
        self.assertEqual(metadata.get("license"), "MIT")
        self.assertLessEqual(len(metadata.get("compatibility", "")), 500)
        self.assertIsInstance(metadata.get("metadata"), dict)
        self.assertTrue(all(isinstance(k, str) and isinstance(v, str) for k, v in metadata["metadata"].items()))
        self.assertLessEqual(len(content.splitlines()), 500)

    def test_skill_resource_paths_exist(self):
        content = SKILL_FILE.read_text(encoding="utf-8")
        paths = re.findall(r"(?:references|templates|scripts|examples)/[A-Za-z0-9_.-]+(?:\.[A-Za-z0-9_.-]+)*", content)
        self.assertTrue(paths)
        for relative in set(paths):
            with self.subTest(resource=relative):
                self.assertTrue((SKILL_DIR / relative).is_file(), f"Missing referenced resource: {relative}")


if __name__ == "__main__":
    unittest.main()
