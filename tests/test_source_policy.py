"""Guard against accidentally shipping known paid-program workbook files.

This is a filename/content smoke test, not a legal or conceptual provenance audit.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"SOURCE_POLICY.md", "test_source_policy.py"}
PAID_WORKBOOK_NAMES = re.compile(
    r"(?:exp(?:erienced)?[ _-]*csm[ _-]*resume[ _-]*workbook|"
    r"(?:healthcare|education|all[ _-]*industries)[ _-]*(?:focus[ _-]*)?resume[ _-]*workbook)",
    re.IGNORECASE,
)


class SourcePolicyTest(unittest.TestCase):
    def test_known_workbook_names_not_shipped(self):
        violations = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.name in SKIP:
                continue
            if PAID_WORKBOOK_NAMES.search(path.name):
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual([], violations, f"Paid-program workbook file(s) found: {violations}")

    def test_restricted_workbook_titles_not_in_public_guides(self):
        violations = []
        for folder in ("prompts", "guides", "templates", "promos", "evidence"):
            for path in (ROOT / folder).rglob("*.md"):
                if PAID_WORKBOOK_NAMES.search(path.read_text(encoding="utf-8")):
                    violations.append(str(path.relative_to(ROOT)))
        self.assertEqual([], violations, f"Potentially restricted source names: {violations}")

    def test_public_career_educator_sources_not_banned(self):
        policy = (ROOT / "SOURCE_POLICY.md").read_text(encoding="utf-8").lower()
        self.assertIn("public linkedin posts", policy)
        self.assertIn("public podcasts", policy)
        self.assertIn("paid-program", policy)

    def test_no_private_exclusion_register_in_public_tree(self):
        self.assertFalse((ROOT / "Career_OS_PRIVATE_SOURCE_EXCLUSIONS.md").exists())


if __name__ == "__main__":
    unittest.main()
