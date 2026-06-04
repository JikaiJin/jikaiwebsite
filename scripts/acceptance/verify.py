#!/usr/bin/env python3
"""
Acceptance harness — diff a preview URL against the baseline captured in
.omc/research/cutover-baseline/.

Covers: A3 URL parity, A4 cite.bib sha256, A5 PDF sha256, third-party
scripts present, RSS guids stable, theme-swap lishu assets present.

Usage:  python3 verify.py [BASE_URL]
Default BASE_URL: https://redesign-step1--jikaiwebsite.netlify.app
"""
import hashlib
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

BASE = (sys.argv[1] if len(sys.argv) > 1 else
        "https://redesign-step1--jikaiwebsite.netlify.app").rstrip("/")
BASELINE = Path("/Users/jkJin/Documents/Research Projects/LLM and Labor Economics/.omc/research/cutover-baseline")

def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cutover-verify/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return None, b""

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

# Parse "<sha>  <path>  (N bytes)" lines into [(sha, path, size)]
def parse_sha_manifest(p: Path):
    if not p.exists(): return []
    out = []
    for line in p.read_text().splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(\S+)", line)
        if m: out.append((m.group(1), m.group(2)))
    return out

print(f"Verifying against: {BASE}\n")

# ============================================================
# A0 — home page 200
# ============================================================
print("=== A0: home page 200 ===")
st, _ = fetch(f"{BASE}/")
print(f"  {st}  /")
assert st == 200, "home page not 200 — aborting"

# ============================================================
# A3 — URL parity (full sitemap set)
# ============================================================
print("\n=== A3: URL parity ===")
baseline_urls = (BASELINE / "urls.txt").read_text().splitlines()
missing, present = [], []
for u in baseline_urls:
    if not u.startswith("http"): continue
    # map jkjin.com -> preview base
    path = u.replace("https://jkjin.com", "")
    st, _ = fetch(f"{BASE}{path}")
    if st == 200:
        present.append(path)
    else:
        missing.append(f"{st}  {path}")
pct = len(present) / max(1, len(baseline_urls)) * 100
print(f"  {len(present)}/{len(baseline_urls)} URLs serve 200  ({pct:.1f}%)")
if missing:
    print("  MISSING:")
    for m in missing[:10]:
        print(f"    {m}")
    if len(missing) > 10: print(f"    ... and {len(missing)-10} more")
print(f"  A3 result: {'PASS' if pct >= 99.0 else 'FAIL (gate: >=99%)'}")

# ============================================================
# A4 — cite.bib sha256
# ============================================================
print("\n=== A4: cite.bib byte-stability ===")
bibs = parse_sha_manifest(BASELINE / "cite-bib.sha256")
ok, bad = 0, []
for expected_sha, path in bibs:
    st, body = fetch(f"{BASE}{path}")
    actual = sha256(body) if body else ""
    if actual == expected_sha:
        ok += 1
    else:
        bad.append(f"  {path}: got {actual[:12]}.. expected {expected_sha[:12]}.. (status {st})")
print(f"  {ok}/{len(bibs)} bib files byte-stable")
for b in bad[:5]: print(b)
print(f"  A4 result: {'PASS' if ok == len(bibs) else 'FAIL'}")

# ============================================================
# A5 — PDF sha256
# ============================================================
print("\n=== A5: PDF byte-stability ===")
pdfs = parse_sha_manifest(BASELINE / "pdf.sha256")
ok, bad = 0, []
for expected_sha, path in pdfs:
    st, body = fetch(f"{BASE}{path}")
    actual = sha256(body) if body else ""
    if actual == expected_sha:
        ok += 1
    else:
        bad.append(f"  {path}: got {actual[:12]}.. expected {expected_sha[:12]}.. (status {st})")
print(f"  {ok}/{len(pdfs)} PDFs byte-stable")
for b in bad: print(b)
print(f"  A5 result: {'PASS' if ok == len(pdfs) else 'FAIL'}")

# ============================================================
# A10 — third-party scripts (clustrmaps, netlify-identity)
# ============================================================
print("\n=== A10: third-party scripts on home page ===")
st, body = fetch(f"{BASE}/")
scripts_required = [b"cdn.clustrmaps.com"]
scripts_check = {}
for s in scripts_required:
    present = s in body
    scripts_check[s.decode()] = present
    print(f"  {'PASS' if present else 'FAIL'}  {s.decode()}")

# Also check /admin/ still serves CMS
st_admin, body_admin = fetch(f"{BASE}/admin/")
cms_live = st_admin == 200 and b"netlify-cms" in body_admin
print(f"  {'PASS' if cms_live else 'FAIL'}  /admin/ CMS live (status {st_admin})")

# ============================================================
# NEW — lishu PNG theme assets
# ============================================================
print("\n=== lishu PNG theme assets ===")
for p in ("/jin-jikai-lishu.png", "/jin-jikai-lishu-dark.png"):
    st, body = fetch(f"{BASE}{p}")
    ok = st == 200 and len(body) > 1000
    print(f"  {'PASS' if ok else 'FAIL'}  {p}  ({st}, {len(body)} bytes)")

# ============================================================
# RSS guid stability
# ============================================================
print("\n=== RSS guid stability (path-only comparison) ===")
# Compare by PATH not full URL; preview emits *.netlify.app URLs, baseline
# has jkjin.com URLs. On cutover the URLs will re-match; path equality is
# what actually matters.
baseline_guids_raw = [g for g in (BASELINE / "rss-guids.txt").read_text().splitlines() if g]
def path_of(u):
    for prefix in ("https://jkjin.com", "http://jkjin.com",
                   "https://redesign-step1--jikaiwebsite.netlify.app",
                   "https://jikaiwebsite.netlify.app"):
        if u.startswith(prefix):
            return u[len(prefix):] or "/"
    return u
baseline_paths = {path_of(g) for g in baseline_guids_raw}
st, body = fetch(f"{BASE}/index.xml")
current = re.findall(rb"<guid[^>]*>([^<]+)</guid>", body)
current_paths = {path_of(g.decode()) for g in current}
missing = baseline_paths - current_paths
extra = current_paths - baseline_paths
print(f"  baseline paths: {len(baseline_paths)}, current paths: {len(current_paths)}")
print(f"  missing in preview RSS: {len(missing)}")
for m in sorted(missing)[:3]: print(f"    - {m}")
if extra:
    print(f"  NEW in preview (post additions): {len(extra)}")
    for e in sorted(extra)[:3]: print(f"    + {e}")
rss_ok = not missing
print(f"  RSS result: {'PASS' if rss_ok else 'FAIL'}")

# ============================================================
# Summary
# ============================================================
print("\n=== summary ===")
print(f"  URLs present: {len(present)}/{len(baseline_urls)} ({pct:.1f}%)")
print(f"  cite.bib byte-stable: {len(bibs) - len(bad)}/{len(bibs)} — see A4 above")
print(f"  PDF byte-stable: see A5 above")
print(f"  Scripts + CMS: see A10 above")
print(f"  RSS path-parity: {'PASS' if rss_ok else 'FAIL'}")
