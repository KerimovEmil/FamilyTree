#!/usr/bin/env python3
"""
Crawl the generated family tree site and report broken internal links.

Starts at a page, follows every internal .html link under that page's
directory, and reports any page that does not return HTTP 200.
Exits with code 1 if any broken links are found (CI-friendly).

Usage:
    # Live site
    python tools/check_links.py https://kerimovemil.github.io/FamilyTree/individuals.html

    # Local copy (from repo root): python -m http.server 8000
    python tools/check_links.py http://localhost:8000/individuals.html
"""
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HREF_RE = re.compile(r'href="([^"#]*)"')


def fetch(url):
    """Return (url, status, body) for a URL; status is an int or error string."""
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return url, resp.status, resp.read().decode('utf-8', 'replace')
    except Exception as exc:  # noqa: BLE001 - report any failure as broken
        return url, getattr(exc, 'code', str(exc)), ''


def crawl(start):
    """Crawl all internal pages reachable from start. Returns (seen, broken)."""
    scope = start.rsplit('/', 1)[0] + '/'
    seen, broken, queue = set(), [], [start]
    with ThreadPoolExecutor(16) as pool:
        while queue:
            batch = [u for u in dict.fromkeys(queue) if u not in seen]
            seen.update(batch)
            queue = []
            for url, status, body in pool.map(fetch, batch):
                if status != 200:
                    broken.append((url, status))
                    continue
                for href in HREF_RE.findall(body):
                    if not href or href.startswith(('javascript:', 'mailto:')):
                        continue
                    target = urllib.parse.urljoin(url, href)
                    if target.startswith(scope) and target.endswith('.html') and target not in seen:
                        queue.append(target)
    return seen, broken


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    seen, broken = crawl(sys.argv[1])
    print(f"pages crawled: {len(seen)}  broken: {len(broken)}")
    for url, status in broken:
        print(f"  BROKEN {status} {url}")
    sys.exit(1 if broken else 0)


if __name__ == '__main__':
    main()
