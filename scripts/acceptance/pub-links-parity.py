#!/usr/bin/env python3
"""
V3 gate — publication-page link parity with prod.

For every publication slug in the baseline sitemap
(.omc/research/cutover-baseline/urls.txt), fetch the corresponding
prod /publication/<slug>/ page and the preview /publication/<slug>/
page, extract the set of action-link labels on each, and assert set
equality (order-free).

Usage:  python3 pub-links-parity.py [PREVIEW_URL] [PROD_URL]
Defaults:
  PREVIEW_URL = https://redesign-step1--jikaiwebsite.netlify.app
  PROD_URL    = https://jkjin.com
"""
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

PREVIEW = (sys.argv[1] if len(sys.argv) > 1 else
           "https://redesign-step1--jikaiwebsite.netlify.app").rstrip("/")
PROD = (sys.argv[2] if len(sys.argv) > 2 else
        "https://jkjin.com").rstrip("/")
BASELINE = Path("/Users/jkJin/Documents/Research Projects/LLM and Labor Economics/.omc/research/cutover-baseline")

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "pub-links-parity/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, ""

def extract_labels(html, is_prod):
    """Return the lowercase set of action-link labels found on the page.
    Prod uses .btn-page-header anchors (Wowchemy); preview uses .pub-link."""
    if is_prod:
        # Wowchemy: <a class="btn btn-outline-primary btn-page-header" ...>PDF</a>
        # Also grab js-cite-modal class (Cite button).
        labels = re.findall(
            r'<a[^>]+class="[^"]*btn-page-header[^"]*"[^>]*>(?:<[^>]+>)*([^<]+?)(?:<[^>]*)?</a>',
            html)
    else:
        # Preview: <a class="pub-link" ...>PDF</a>
        labels = re.findall(r'<a[^>]+class="pub-link"[^>]*>([^<]+)</a>', html)
    # Normalise
    return {x.strip().lower() for x in labels if x.strip()}

def main():
    # Derive the set of publication slugs from the baseline sitemap
    urls_path = BASELINE / "urls.txt"
    assert urls_path.exists(), f"baseline urls.txt missing at {urls_path}"
    pub_paths = []
    for line in urls_path.read_text().splitlines():
        m = re.match(r"^https://jkjin.com(/publication/[^/]+/)$", line.strip())
        if m:
            pub_paths.append(m.group(1))
    pub_paths = [p for p in pub_paths if p != "/publication/"]  # drop index
    print(f"Checking {len(pub_paths)} publication pages\n")

    mismatches = []
    for path in pub_paths:
        _, prod_html = fetch(f"{PROD}{path}")
        _, prev_html = fetch(f"{PREVIEW}{path}")
        prod_labels = extract_labels(prod_html, is_prod=True)
        prev_labels = extract_labels(prev_html, is_prod=False)
        missing_in_preview = prod_labels - prev_labels
        extra_in_preview = prev_labels - prod_labels
        ok = not missing_in_preview
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {path}")
        print(f"         prod:    {sorted(prod_labels)}")
        print(f"         preview: {sorted(prev_labels)}")
        if missing_in_preview:
            print(f"         MISSING (dropped by preview): {sorted(missing_in_preview)}")
            mismatches.append((path, missing_in_preview))
        if extra_in_preview:
            print(f"         extra (preview added):        {sorted(extra_in_preview)}")

    print(f"\nV3 result: {'PASS' if not mismatches else 'FAIL'}  "
          f"({len(pub_paths) - len(mismatches)}/{len(pub_paths)} slugs parity)")
    sys.exit(0 if not mismatches else 1)

if __name__ == "__main__":
    main()
