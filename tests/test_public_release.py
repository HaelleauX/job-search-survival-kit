"""Static release-safety checks. This is not a substitute for human source audit."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MDS = list(ROOT.rglob('*.md'))

class PublicReleaseTests(unittest.TestCase):
    def test_required_files_exist(self):
        for filename in ('README.md','START_HERE.md','PUBLISHING.md','SOURCE_POLICY.md',
                         'CONTENT-LICENSE.md','LICENSE','CONTRIBUTING.md',
                         'examples/FICTIONAL-EXAMPLE.md'):
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / filename).is_file())

    def test_markdown_local_links_resolve(self):
        failures = []
        pattern = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
        for p in MDS:
            content = p.read_text(encoding='utf-8')
            for target in pattern.findall(content):
                if (target.startswith(('https://','http://','mailto:','#')) or
                    target.startswith('${{')):
                    continue
                path = unquote(target.split('#',1)[0].split('?',1)[0])
                if not (p.parent / path).exists():
                    failures.append(f'{p.relative_to(ROOT)} -> {target}')
        self.assertEqual([], failures, 'Broken local links')

    def test_no_private_drive_links_in_public_guides(self):
        prohibited = re.compile(r'https?://(?:docs|drive)\.google\.com/', re.IGNORECASE)
        violations = []
        for p in MDS:
            if prohibited.search(p.read_text(encoding='utf-8')):
                violations.append(str(p.relative_to(ROOT)))
        self.assertEqual([], violations, 'Private Google Drive links need review')

    def test_no_public_bundle_with_resumes_or_raw_user_files(self):
        disallowed = {'.docx', '.xlsx', '.pdf', '.zip', '.jpeg', '.jpg', '.png'}
        violations = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
                      if p.is_file() and p.suffix.lower() in disallowed]
        self.assertEqual([], violations)

    def test_quickstart_has_real_world_stop_conditions(self):
        t = (ROOT/'START_HERE.md').read_text(encoding='utf-8').lower()
        for phrase in ('skip', 'verify', 'job description', 'not established',
                       'no', 'confidential'):
            self.assertIn(phrase,t)

if __name__ == '__main__':
    unittest.main()
