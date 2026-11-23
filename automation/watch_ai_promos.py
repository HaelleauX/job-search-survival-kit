#!/usr/bin/env python3
"""Public AI subscription promotion watcher (discovery only, never auto-verify).

Checks a list of official/public pages for changed promotion-related text and
newly linked promotion pages. Every detection is queued for human review.
Private account dashboards, paywalled pages, and JS-only offers cannot be seen.
No cookies, credentials, API keys, or applicant records are collected.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

from watch_sources import discover, fetch

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'automation' / 'ai_promo_sources.json'
SEEN = ROOT / 'automation' / 'ai-promo-state.json'
INBOX = ROOT / 'promos' / 'inbox'
MAX_SNIPPETS = 30


class VisibleText(HTMLParser):
    """Extract human-visible text; skip scripts and styles."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'svg', 'noscript'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg', 'noscript') and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            line = re.sub(r'\s+', ' ', data).strip()
            if len(line) > 5:
                self.parts.append(line)


def promo_snippets(html: str, source: dict) -> list[str]:
    """Return bounded promotion-related strings, not alleged valid offers."""
    parser = VisibleText()
    parser.feed(html)
    terms = [s.lower() for s in source['terms']]
    results = []
    for part in parser.parts:
        if any(term in part.lower() for term in terms):
            part = part[:260]
            if part not in results:
                results.append(part)
        if len(results) >= MAX_SNIPPETS:
            break
    return results


def extract_snapshot(html: str, source: dict) -> dict:
    links = discover(html, source)
    snippets = promo_snippets(html, source)
    # Official site copy changes can be noteworthy even if no new link appears.
    signature = hashlib.sha256(json.dumps(snippets, ensure_ascii=False).encode('utf-8')).hexdigest()
    return {'links': links, 'text_signature': signature, 'snippets': snippets}


def review_file(source: dict, previous: dict, current: dict, timestamp: str) -> str:
    new_links = {u: t for u, t in current['links'].items() if u not in previous.get('links', {})}
    text_changed = bool(previous.get('text_signature')) and previous['text_signature'] != current['text_signature']
    out = [f'## {source["name"]}', f'- Source: {source["url"]}', f'- Checked: {timestamp}',
           '- Status: **UNVERIFIED DISCOVERY.** No discount should be described as active until independently confirmed.']
    if new_links:
        out.append('- Newly linked candidate pages:')
        out.extend(f'  - [ ] [{title}]({url})' for url, title in new_links.items())
    if text_changed:
        out.append('- [ ] Promotion-related text changed. Compare the official page with the previous checked source.')
        for snippet in current['snippets'][:8]:
            out.append(f'  - Excerpt for review: {snippet.replace(chr(10), " ")}')
    out.append('- [ ] Verify promotion eligibility, offer expiry/caps, location, payment rail, new/existing subscriber restrictions, *upfront price versus cashback*, full renewal price, cancellation timing, and an official redemption path.')
    out.append('- [ ] If a promotion cannot be independently verified on the official publisher/partner page, label **community-reported / account-specific**, never **verified**.')
    return '\n'.join(out) + '\n\n'


def run() -> int:
    sources = json.loads(SOURCES.read_text(encoding='utf-8'))
    old = json.loads(SEEN.read_text(encoding='utf-8')) if SEEN.exists() else {}
    updated = dict(old)
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    pending = []
    successes = 0
    for source in sources:
        sid = source['id']
        try:
            if urlsplit(source['url']).scheme != 'https':
                raise ValueError('Only HTTPS sources are permitted')
            snapshot = extract_snapshot(fetch(source['url']), source)
            if not snapshot['snippets'] and not snapshot['links']:
                raise ValueError('No readable text/links found; page may require JavaScript or login')
            successes += 1
            prev = old.get(sid)
            if prev is None:
                print(f'BASELINE {sid}: {len(snapshot["links"])} links; no review item')
            else:
                has_new = bool(set(snapshot['links']) - set(prev.get('links', {})))
                has_change = prev.get('text_signature') != snapshot['text_signature']
                if has_new or has_change:
                    pending.append(review_file(source, prev, snapshot, timestamp))
                    print(f'REVIEW {sid}: new links={has_new}; text changed={has_change}')
                else:
                    print(f'UNCHANGED {sid}')
            # Keep historical links so disappearing offers don't look newly added next week.
            if prev:
                snapshot['links'] = {**prev.get('links', {}), **snapshot['links']}
            updated[sid] = snapshot
        except Exception as error:
            # Network/platform interruptions should not erase last known state.
            print(f'WARNING {sid}: {type(error).__name__}: {error}', file=sys.stderr)
    if old != updated:
        SEEN.write_text(json.dumps(updated, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if pending:
        INBOX.mkdir(parents=True, exist_ok=True)
        day = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        path = INBOX / f'{day}.md'
        existing = path.read_text(encoding='utf-8') if path.exists() else f'# AI promotions needing review ({day})\n\nThese detections are **not confirmed offers**. No automatic publication or redemption.\n\n'
        # Avoid duplicate source blocks on retries within the same day.
        additions = [block for block in pending if block.split('\n')[0] not in existing]
        if additions:
            path.write_text(existing + ''.join(additions), encoding='utf-8')
    print(f'Summary: {successes}/{len(sources)} official pages checked; {len(pending)} need review')
    return 0 if successes else 1


if __name__ == '__main__':
    sys.exit(run())
