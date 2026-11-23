#!/usr/bin/env python3
"""Review-first link discovery for official hiring research index pages.

Uses only Python's standard library and public pages. It *does not* extract
statistics, scrape private data, or auto-publish new benchmark claims.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "automation" / "sources.json"
SEEN = ROOT / "automation" / "seen-links.json"
INBOX = ROOT / "evidence" / "inbox"
TIMEOUT = 18
MAX_BYTES = 1_800_000
MAX_RESULTS_PER_SOURCE = 120
UNWANTED_SUFFIXES = (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".css", ".js", ".ico", ".xml")
TRACKING = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "trk", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"}


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items: list[tuple[str, str]] = []
        self.stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        if tag == "a":
            href = dict(attrs).get("href")
            self.stack.append({"href": href or "", "text": []})

    def handle_data(self, data: str):
        if self.stack:
            self.stack[-1]["text"].append(data)

    def handle_endtag(self, tag: str):
        if tag == "a" and self.stack:
            item = self.stack.pop()
            label = re.sub(r"\s+", " ", " ".join(item["text"])).strip()
            if item["href"]:
                self.items.append((item["href"], label))


def normalized_url(href: str, base: str) -> str | None:
    url = urljoin(base, href)
    p = urlsplit(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return None
    params = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
              if k.lower() not in TRACKING and not k.lower().startswith("utm_")]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/") or "/", urlencode(params), ""))


def discover(html: str, source: dict) -> dict[str, str]:
    parser = Anchors()
    parser.feed(html)
    results: dict[str, str] = {}
    for href, title in parser.items:
        url = normalized_url(href, source["url"])
        if not url:
            continue
        p = urlsplit(url)
        if not any(p.hostname == d or p.hostname.endswith("." + d) for d in source["domains"]):
            continue
        if p.path.lower().endswith(UNWANTED_SUFFIXES) or url == normalized_url(source["url"], source["url"]):
            continue
        # Strong relevance requires report/topic terms in the link, not only site navigation.
        haystack = f"{title} {p.path.replace('-', ' ').replace('_', ' ')}".lower()
        if not any(term.lower() in haystack for term in source["terms"]):
            continue
        if len(title.strip()) < 7 or title.strip().lower() in {"report", "reports", "read more", "learn more", "download"}:
            continue
        results[url] = title[:180]
        if len(results) >= MAX_RESULTS_PER_SOURCE:
            break
    return results


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "CareerOS-ReportWatcher/0.1 (weekly research-link check)", "Accept": "text/html,application/xhtml+xml"})
    with urlopen(req, timeout=TIMEOUT) as res:
        content_type = res.headers.get("content-type", "")
        if "text/html" not in content_type:
            raise ValueError(f"Unexpected content type: {content_type}")
        raw = res.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Page too large; skipping")
        charset = res.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def run() -> int:
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    known = json.loads(SEEN.read_text(encoding="utf-8")) if SEEN.exists() else {}
    updated = dict(known)
    new_items: list[tuple[str, str, str]] = []
    successes = 0
    failures = 0
    for source in sources:
        try:
            found = discover(fetch(source["url"]), source)
            if not found:
                raise ValueError("No relevant links found (possible JavaScript-rendered index); retaining baseline")
            successes += 1
            previous = known.get(source["id"])
            if previous is None:
                # Baseline on the very first run, otherwise every historical link would be "news".
                updated[source["id"]] = found
                print(f"BASELINE {source['id']}: {len(found)} links")
                continue
            for url, title in found.items():
                if url not in previous:
                    new_items.append((source["name"], title, url))
            updated[source["id"]] = {**previous, **found}
            print(f"CHECK {source['id']}: {len(found)} visible; {len(found.keys() - previous.keys())} new")
        except (HTTPError, URLError, TimeoutError, ValueError, OSError, UnicodeError) as error:
            failures += 1
            print(f"WARNING {source['id']}: {type(error).__name__}: {error}; preserving existing links", file=sys.stderr)

    if updated != known:
        SEEN.write_text(json.dumps(updated, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if new_items:
        INBOX.mkdir(parents=True, exist_ok=True)
        today = dt.datetime.now(dt.timezone.utc).date().isoformat()
        path = INBOX / f"{today}.md"
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# Research links detected on {today} (UTC)\n\n**Unverified.** Do not publish numerical claims from these links without reading source methodology.\n\n"
        lines = []
        for source, title, url in new_items:
            if url not in existing:
                lines.append(f"- **{source}:** [{title}]({url}) — [ ] Verify date, sample, exact claims and methodology")
        if lines:
            path.write_text(existing + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"Summary: {successes} source(s) checked; {failures} error(s); {len(new_items)} new report-style link(s)")
    return 1 if successes == 0 else 0


if __name__ == "__main__":
    sys.exit(run())
