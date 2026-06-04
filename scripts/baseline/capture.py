#!/usr/bin/env python3
"""
Baseline capture for cutover Step 2.
Reads live production (jkjin.com) and writes a reproducible snapshot
to .omc/research/cutover-baseline/ — ground truth for A3/A4/A5/A7b/A9 gates.

Safe to re-run; overwrites artifacts.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

PROD = "https://jkjin.com"
ROOT = Path("/Users/jkJin/Documents/Research Projects/LLM and Labor Economics/.omc/scratch/jikaiwebsite")
BASELINE = Path("/Users/jkJin/Documents/Research Projects/LLM and Labor Economics/.omc/research/cutover-baseline")

for sub in ("refs", "pubs", "pdfs", "imgs"):
    (BASELINE / sub).mkdir(parents=True, exist_ok=True)


def fetch(url, timeout=15):
    """Return (status, bytes) for url; None on error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cutover-baseline/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b""
    except Exception as e:
        print(f"  !! {url}: {e}", file=sys.stderr)
        return None, b""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ============================================================
# A — URL universe
# ============================================================
print("=== A — sitemap + URL universe ===")
status, body = fetch(f"{PROD}/sitemap.xml")
(BASELINE / "sitemap.xml").write_bytes(body)
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
root = ET.fromstring(body)
urls = sorted({loc.text for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if loc.text})
(BASELINE / "urls.txt").write_text("\n".join(urls) + "\n")
print(f"  sitemap URL count: {len(urls)}")

# ============================================================
# B — basic site files
# ============================================================
print("\n=== B — robots.txt + rss + 404 ===")
for asset in ("robots.txt", "index.xml", "404.html"):
    st, bd = fetch(f"{PROD}/{asset}")
    if bd:
        (BASELINE / asset).write_bytes(bd)
    print(f"  {st}  {asset}")

# ============================================================
# C — reference HTML snapshots (for A7b, A9)
# ============================================================
print("\n=== C — reference HTML snapshots ===")
ref_pages = {
    "home-ref.html": "/",
    "getting-started-ref.html": "/post/getting-started/",
    "prescriptive-scaling-ref.html": "/post/prescriptive-scaling/",
    "publications-ref.html": "/publication/",
}
ref_bodies = {}
for fname, path in ref_pages.items():
    st, bd = fetch(f"{PROD}{path}")
    if bd:
        (BASELINE / "refs" / fname).write_bytes(bd)
    ref_bodies[fname] = bd
    print(f"  {st}  {path}  -> refs/{fname} ({len(bd)} bytes)")

# ============================================================
# D — cite.bib sha256 per publication (slugs from sitemap, not dir names)
# ============================================================
print("\n=== D — cite.bib sha256 per publication ===")
pub_slug_urls = [u for u in urls if "/publication/" in u and u != f"{PROD}/publication/"]
bibs = []
for pub_url in pub_slug_urls:
    # derive slug from URL
    slug = pub_url.rstrip("/").rsplit("/", 1)[-1]
    url = f"{pub_url.rstrip('/')}/cite.bib"
    st, bd = fetch(url)
    if st == 200 and bd:
        h = sha256(bd)
        rel = url.replace(PROD, "")
        bibs.append((h, rel, len(bd)))
        (BASELINE / "pubs" / f"{slug}.bib").write_bytes(bd)
with open(BASELINE / "cite-bib.sha256", "w") as f:
    for h, u, n in bibs:
        f.write(f"{h}  {u}  ({n} bytes)\n")
print(f"  captured {len(bibs)} cite.bib files out of {len(pub_slug_urls)} pub URLs")

# ============================================================
# E — PDF sha256
# ============================================================
print("\n=== E — PDF sha256 ===")
pdfs = []
# Probe each publication page's HTML for pdf links
for pub_url in pub_slug_urls:
    st, bd = fetch(pub_url)
    if not bd:
        continue
    # Find .pdf links on the publication page
    for m in re.finditer(rb'href="([^"]+\.pdf)"', bd, re.IGNORECASE):
        pdf_url = m.group(1).decode()
        if pdf_url.startswith("/"):
            pdf_url = PROD + pdf_url
        elif not pdf_url.startswith("http"):
            # relative to the pub URL
            pdf_url = pub_url.rstrip("/") + "/" + pdf_url
        st2, bd2 = fetch(pdf_url)
        if st2 == 200 and bd2 and len(bd2) > 1000:  # sanity check — not a 404 page
            h = sha256(bd2)
            rel = pdf_url.replace(PROD, "")
            pdfs.append((h, rel, len(bd2)))

# Known static PDFs
for static_path in ("/uploads/resume.pdf",):
    st, bd = fetch(f"{PROD}{static_path}")
    if st == 200 and bd:
        h = sha256(bd)
        pdfs.append((h, static_path, len(bd)))

# Dedupe
seen = set()
unique_pdfs = []
for h, u, n in pdfs:
    if u not in seen:
        seen.add(u)
        unique_pdfs.append((h, u, n))
pdfs = unique_pdfs

with open(BASELINE / "pdf.sha256", "w") as f:
    for h, u, n in pdfs:
        f.write(f"{h}  {u}  ({n} bytes)\n")
print(f"  captured {len(pdfs)} PDFs")

# ============================================================
# F — image URLs (img src extraction from ref HTML) + sha256
# ============================================================
print("\n=== F — img src sha256 ===")
img_urls = set()
# Handle both quoted src="..." AND unquoted src=/path/... (Hugo --minify strips quotes).
img_pattern = re.compile(
    rb'src=(?:"([^"]+\.(?:png|jpg|jpeg|svg|gif|webp)[^"]*)"|([^\s>]+\.(?:png|jpg|jpeg|svg|gif|webp)[^\s>]*))',
    re.IGNORECASE,
)
for bd in ref_bodies.values():
    for m in img_pattern.finditer(bd):
        u = (m.group(1) or m.group(2)).decode()
        # strip query strings / fragments
        u = u.split("?")[0].split("#")[0]
        if u.startswith("//"):
            u = "https:" + u
        elif u.startswith("/"):
            u = PROD + u
        elif u.startswith("http"):
            pass
        else:
            continue  # relative URLs — skip
        img_urls.add(u)

imgs = []
for url in sorted(img_urls):
    st, bd = fetch(url)
    if st == 200 and bd:
        h = sha256(bd)
        imgs.append((h, url, len(bd)))
with open(BASELINE / "img.sha256", "w") as f:
    for h, u, n in imgs:
        f.write(f"{h}  {u}  ({n} bytes)\n")
print(f"  captured {len(imgs)} images")

# ============================================================
# G — third-party script origins
# ============================================================
print("\n=== G — third-party script origins ===")
scripts = set()
script_pattern = re.compile(
    rb'<script\b[^>]*?src=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))',
    re.IGNORECASE,
)
for bd in ref_bodies.values():
    for m in script_pattern.finditer(bd):
        u = (m.group(1) or m.group(2) or m.group(3)).decode()
        scripts.add(u)
(BASELINE / "third-party-scripts.txt").write_text("\n".join(sorted(scripts)) + "\n")
for s in sorted(scripts):
    print(f"  {s}")

# ============================================================
# H — citation_* meta count per publication (per v5, baseline=0)
# ============================================================
print("\n=== H — citation_* meta count on sample pubs ===")
meta_counts = {}
for pub_url in pub_slug_urls[:3]:
    st, bd = fetch(pub_url)
    slug = pub_url.rstrip("/").rsplit("/", 1)[-1]
    # Match both quoted and unquoted name=citation_* (Hugo minified could drop quotes).
    count = len(re.findall(rb'<meta\s+name=(?:"citation_|citation_)', bd, re.IGNORECASE))
    meta_counts[slug] = count
    print(f"  {pub_url}  citation_* count: {count}")
(BASELINE / "citation-meta.json").write_text(json.dumps(meta_counts, indent=2))

# ============================================================
# I — RSS guid list
# ============================================================
print("\n=== I — RSS guid list ===")
rss_body = (BASELINE / "index.xml").read_bytes() if (BASELINE / "index.xml").exists() else b""
guids = re.findall(rb'<guid[^>]*>([^<]+)</guid>', rss_body)
(BASELINE / "rss-guids.txt").write_text("\n".join(g.decode() for g in guids) + "\n")
print(f"  RSS guid count: {len(guids)}")

# ============================================================
# J — CSS payload size
# ============================================================
print("\n=== J — CSS payload size ===")
css_urls = set()
home_body = ref_bodies.get("home-ref.html", b"")
# Two patterns: <link rel=stylesheet href=...> AND <link href=... rel=stylesheet> (both orderings),
# each with quoted or unquoted attribute values (Hugo --minify strips quotes).
# Strategy: find every <link ...> tag that contains rel=stylesheet, then extract href from it.
for tag_match in re.finditer(rb'<link\b[^>]{0,800}>', home_body, re.IGNORECASE):
    tag = tag_match.group(0)
    if not re.search(rb'\brel=(?:"stylesheet"|\'stylesheet\'|stylesheet\b)', tag, re.IGNORECASE):
        continue
    href_m = re.search(
        rb'\bhref=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))',
        tag,
        re.IGNORECASE,
    )
    if not href_m:
        continue
    u = (href_m.group(1) or href_m.group(2) or href_m.group(3)).decode()
    if u.startswith("/"):
        u = PROD + u
    elif u.startswith("//"):
        u = "https:" + u
    elif not u.startswith("http"):
        continue
    css_urls.add(u)

total_bytes = 0
css_report = []
for url in sorted(css_urls):
    st, bd = fetch(url)
    if bd:
        total_bytes += len(bd)
        css_report.append((url, len(bd)))
(BASELINE / "css-size.txt").write_text(
    f"Total CSS bytes (home, not gzipped): {total_bytes}\n\nBreakdown:\n" +
    "\n".join(f"  {n:>8} bytes  {u}" for u, n in css_report)
)
print(f"  total CSS: {total_bytes} bytes across {len(css_report)} files")

# ============================================================
# K — summary
# ============================================================
print("\n=== baseline summary ===")
print(f"  URLs in sitemap: {len(urls)}")
print(f"  cite.bib files:  {len(bibs)}")
print(f"  PDFs:            {len(pdfs)}")
print(f"  Images:          {len(imgs)}")
print(f"  3rd-party scripts: {len(scripts)}")
print(f"  RSS guids:       {len(guids)}")
print(f"  CSS bytes:       {total_bytes}")
print(f"  citation_* meta on 3 pubs: {meta_counts}")
print(f"\nAll artifacts under: {BASELINE}")
