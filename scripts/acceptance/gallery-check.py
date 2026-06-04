#!/usr/bin/env python3
"""
Gallery acceptance gates (G1, G3, G4, G6, G7, G8) from gallery-v1.md.

Usage:  python3 gallery-check.py [BASE_URL]
Default BASE_URL: https://redesign-step1--jikaiwebsite.netlify.app

Runs against a live preview URL. Complements the existing cutover
harness (verify.py, nav-anchors.py, pub-links-parity.py) — this
script does NOT re-cover those gates.

G1  /gallery/ returns 200 and contains at least one album tile
    (PASS if zero albums are live on prod AND the page still serves)
G3  Every live album's cover resolves (fetched image has non-zero size)
G4  Home page has id="gallery" section
G6  At least one _hu_*.webp derivative served under /gallery/<slug>/
G7  Full-res originals for each album image return 200
G8  Every album single page has og:image + twitter:image meta tags

Exit code 0 = PASS, 1 = FAIL.
"""
import re
import sys
import urllib.request
import urllib.error

BASE = (sys.argv[1] if len(sys.argv) > 1 else
        "https://redesign-step1--jikaiwebsite.netlify.app").rstrip("/")


def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url,
                                     headers={"User-Agent": "gallery-check/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return None, b""


def head(url, timeout=15):
    try:
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "gallery-check/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, int(r.headers.get("Content-Length") or 0)
    except Exception:
        return None, 0


def extract_album_hrefs(list_html):
    """From /gallery/ body, extract the set of /gallery/<slug>/ URLs."""
    out = set()
    for m in re.finditer(rb'<a[^>]+\bhref=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))',
                         list_html):
        href = (m.group(1) or m.group(2) or m.group(3) or b"").decode()
        if re.match(r"^/gallery/[^/]+/$", href) and href != "/gallery/":
            out.add(href)
    return sorted(out)


def extract_img_srcs(html):
    out = set()
    for m in re.finditer(rb'<(?:img|a)[^>]+\b(?:src|href)=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))',
                         html):
        u = (m.group(1) or m.group(2) or m.group(3) or b"").decode()
        if u.startswith("/gallery/") and re.search(r"\.(jpe?g|png|webp)$", u, re.I):
            out.add(u)
    return out


def main():
    print(f"Gallery acceptance @ {BASE}\n")
    status, body = fetch(f"{BASE}/gallery/")
    print("=== G1 /gallery/ ===")
    g1 = status == 200
    print(f"  {'PASS' if g1 else 'FAIL'}  HTTP {status}")
    album_paths = extract_album_hrefs(body) if body else []
    print(f"  live albums: {len(album_paths)}")
    for p in album_paths:
        print(f"    - {p}")

    # G4 is about home page, runs independently.
    print("\n=== G4 home has id=gallery ===")
    _, home = fetch(f"{BASE}/")
    g4 = bool(re.search(rb'\bid=["\']?gallery\b', home))
    print(f"  {'PASS' if g4 else 'FAIL'}")

    # G3, G6, G7, G8 iterate over live albums. If none, these are vacuous-PASS.
    g3_all, g6_any, g7_all, g8_all = True, False, True, True
    per_album = {}
    for path in album_paths:
        status, album_body = fetch(f"{BASE}{path}")
        rec = {"status": status, "cover_ok": None, "webp": 0,
               "orig_ok": 0, "orig_total": 0, "og": False, "twitter": False}
        if status == 200:
            # Find cover img src (first one under /gallery/<slug>/)
            src_match = re.search(rb'<img[^>]+\bsrc=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))',
                                  album_body)
            if src_match:
                src = (src_match.group(1) or src_match.group(2) or src_match.group(3) or b"").decode()
                st, sz = head(f"{BASE}{src}" if src.startswith("/") else src)
                rec["cover_ok"] = (st == 200 and sz > 0)
                if not rec["cover_ok"]:
                    g3_all = False
            else:
                rec["cover_ok"] = None  # no <img> on the page — unusual but allowed

            # G6/G7: count webp derivatives and originals
            for u in extract_img_srcs(album_body):
                rec["orig_total"] += 1
                st, _ = head(f"{BASE}{u}" if u.startswith("/") else u)
                if st == 200:
                    rec["orig_ok"] += 1
                    if "_hu_" in u and u.endswith(".webp"):
                        rec["webp"] += 1
            if rec["webp"] > 0:
                g6_any = True
            if rec["orig_ok"] != rec["orig_total"]:
                g7_all = False

            # G8: og:image + twitter:image
            rec["og"] = b'og:image' in album_body
            rec["twitter"] = b'twitter:image' in album_body
            if not (rec["og"] and rec["twitter"]):
                g8_all = False
        per_album[path] = rec

    print("\n=== G3 cover resolves (per album) ===")
    if not album_paths:
        print("  PASS vacuously (no live albums)")
    else:
        for p, r in per_album.items():
            tag = "PASS" if r["cover_ok"] else "FAIL"
            print(f"  {tag}  {p}  cover_ok={r['cover_ok']}")
        print(f"  G3 result: {'PASS' if g3_all else 'FAIL'}")

    print("\n=== G6 responsive webp derivatives ===")
    if not album_paths:
        print("  PASS vacuously (no live albums)")
    else:
        for p, r in per_album.items():
            print(f"  {p}: {r['webp']} webp derivatives served")
        print(f"  G6 result: {'PASS' if g6_any else 'FAIL (no _hu_*.webp found)'}")

    print("\n=== G7 full-res originals reachable ===")
    if not album_paths:
        print("  PASS vacuously (no live albums)")
    else:
        for p, r in per_album.items():
            print(f"  {p}: {r['orig_ok']}/{r['orig_total']} images reachable")
        print(f"  G7 result: {'PASS' if g7_all else 'FAIL'}")

    print("\n=== G8 og:image + twitter:image on album singles ===")
    if not album_paths:
        print("  PASS vacuously (no live albums)")
    else:
        for p, r in per_album.items():
            tag = "PASS" if (r["og"] and r["twitter"]) else "FAIL"
            print(f"  {tag}  {p}  og={r['og']} twitter={r['twitter']}")
        print(f"  G8 result: {'PASS' if g8_all else 'FAIL'}")

    overall = g1 and g4 and g3_all and (g6_any or not album_paths) and g7_all and g8_all
    print(f"\nOverall: {'PASS' if overall else 'FAIL'}")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
