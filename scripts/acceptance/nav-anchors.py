#!/usr/bin/env python3
"""
V1 gate — nav-anchor resolution.

Fetches the home page from the preview URL and asserts that every
in-page anchor referenced by <header class="site-header"> <nav> links
resolves to a DOM element with the matching `id=` attribute on the
same page.

External nav links (starting with http or a path without `#`) are
reported but not asserted.

Usage:  python3 nav-anchors.py [BASE_URL]
Default BASE_URL: https://redesign-step1--jikaiwebsite.netlify.app
"""
import re
import sys
import urllib.request
import urllib.error

BASE = (sys.argv[1] if len(sys.argv) > 1 else
        "https://redesign-step1--jikaiwebsite.netlify.app").rstrip("/")

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "cutover-verify/1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", errors="ignore")

def main():
    print(f"V1 nav-anchor resolution @ {BASE}/")
    status, body = fetch(f"{BASE}/")
    assert status == 200, f"home page not 200 (got {status})"

    # Extract the <header class=site-header ...>...</header> block.
    # Hugo minification drops quotes from attribute values, so accept
    # both quoted and unquoted forms.
    m = re.search(r'<header[^>]*\bclass=["\']?site-header\b[^>]*>.*?</header>',
                  body, re.DOTALL)
    assert m, "site-header block not found in home HTML"
    header_block = m.group(0)

    # Collect every anchor href in the header (quoted or unquoted)
    hrefs = re.findall(r'<a[^>]+\bhref=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))',
                       header_block)
    hrefs = [a or b or c for (a, b, c) in hrefs]
    if not hrefs:
        print("  (no nav links found — suspicious)")
        sys.exit(2)

    # Collect every id on the home page (quoted and unquoted)
    ids_on_page = set()
    for m2 in re.finditer(r'\bid=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))', body):
        ids_on_page.add(m2.group(1) or m2.group(2) or m2.group(3))

    internal, external = [], []
    for h in hrefs:
        if h.startswith("#") or h.startswith("/#"):
            internal.append(h)
        else:
            external.append(h)

    resolved, broken = [], []
    for h in internal:
        anchor = h.split("#", 1)[1]
        if anchor in ids_on_page:
            resolved.append(h)
        else:
            broken.append(h)

    for h in resolved:
        print(f"  PASS  {h}")
    for h in broken:
        print(f"  FAIL  {h}  (no DOM id=\"{h.split('#')[1]}\")")
    for h in external:
        print(f"  (external, not checked) {h}")

    print(f"\nV1 result: {'PASS' if not broken else 'FAIL'}  "
          f"({len(resolved)}/{len(internal)} in-page anchors resolved)")
    sys.exit(0 if not broken else 1)

if __name__ == "__main__":
    main()
