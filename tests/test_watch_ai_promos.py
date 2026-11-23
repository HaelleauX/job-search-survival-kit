import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'automation'))
from watch_ai_promos import extract_snapshot, promo_snippets, review_file

SOURCE = {"id": "site", "name": "Official provider", "url": "https://offers.example.org/", "domains": ["offers.example.org"], "terms": ["offer", "promo", "discount", "trial"]}


class PromoWatchTests(unittest.TestCase):
    def test_ignores_script_and_catches_text(self):
        html = '<script>Secret free trial offer</script><p>Discount for eligible students.</p>'
        self.assertEqual(promo_snippets(html, SOURCE), ['Discount for eligible students.'])

    def test_official_link_discovery(self):
        page = '<a href="/promo/college-trial">College trial offer</a><a href="https://evil.com/offer">Cheap offer</a>'
        snapshot = extract_snapshot(page, SOURCE)
        self.assertIn('https://offers.example.org/promo/college-trial', snapshot['links'])
        self.assertEqual(len(snapshot['links']), 1)

    def test_changed_offer_prompts_review_without_claiming_active(self):
        old = extract_snapshot('<p>Free trial offer for new users.</p>', SOURCE)
        new = extract_snapshot('<p>Discount offer for new users only.</p>', SOURCE)
        body = review_file(SOURCE, old, new, '2026-11-23 12:00 UTC')
        self.assertIn('UNVERIFIED DISCOVERY', body)
        self.assertIn('text changed', body)
        self.assertIn('cashback', body)

    def test_unchanged_signature(self):
        page = '<p>50% discount for eligible new users.</p>'
        self.assertEqual(extract_snapshot(page, SOURCE)['text_signature'], extract_snapshot(page, SOURCE)['text_signature'])


if __name__ == '__main__':
    unittest.main()
