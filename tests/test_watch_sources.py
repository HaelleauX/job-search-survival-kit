import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'automation'))
from watch_sources import discover, normalized_url


class TestLinkDiscovery(unittest.TestCase):
    def setUp(self):
        self.source = {
            'id': 'example', 'url': 'https://reports.example.com/research/',
            'domains': ['reports.example.com'],
            'terms': ['hiring', 'report', 'benchmark']
        }

    def test_tracking_removed_and_offsite_skipped(self):
        page = '''<a href="/2026/hiring-report?utm_source=email">Fall 2026 hiring report</a>
                  <a href="https://evil.example.net/capture">Recruiting report</a>
                  <a href="/about">About</a>'''
        self.assertEqual(discover(page, self.source), {'https://reports.example.com/2026/hiring-report': 'Fall 2026 hiring report'})

    def test_external_and_non_http_urls_not_used(self):
        self.assertIsNone(normalized_url('mailto:hello@sample.com', self.source['url']))
        self.assertEqual(normalized_url('/a?trk=abc&year=2026#top', self.source['url']), 'https://reports.example.com/a?year=2026')

    def test_nested_anchor_text(self):
        page = '<a href="/2026/new-report"><strong>New</strong> hiring <span>report</span></a>'
        self.assertIn('https://reports.example.com/2026/new-report', discover(page, self.source))


if __name__ == '__main__':
    unittest.main()
