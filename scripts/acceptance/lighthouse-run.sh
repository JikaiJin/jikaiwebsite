#!/bin/bash
# Lighthouse median-of-N runs against preview URL.
# Mobile profile default + Slow 4G + 4x CPU (Lighthouse defaults for mobile).

set -e
export PATH="/opt/homebrew/bin:$PATH"
BASE="${BASE:-https://redesign-step1--jikaiwebsite.netlify.app}"
RUNS="${RUNS:-5}"
OUT="${OUT:-/Users/jkJin/Documents/Research Projects/LLM and Labor Economics/.omc/research/cutover-baseline/lighthouse}"
mkdir -p "$OUT"

urls=(
  "/"
  "/publication/dro/"
  "/post/getting-started/"
)

for route in "${urls[@]}"; do
  safe=$(echo "$route" | tr '/' '_' | sed 's/^_//; s/_$//' || echo "home")
  [ -z "$safe" ] && safe="home"
  echo "=== $route ($RUNS runs) ==="
  for n in $(seq 1 $RUNS); do
    out_file="$OUT/${safe}_run${n}.json"
    lighthouse "$BASE$route" \
      --only-categories=performance,accessibility \
      --output=json --output-path="$out_file" \
      --chrome-flags="--headless --disable-gpu --no-sandbox" \
      --quiet 2>/dev/null || true
    # extract key metrics
    python3 -c "
import json, sys
try:
    d = json.load(open('$out_file'))
    cats = d['categories']
    audits = d['audits']
    perf = cats['performance']['score']
    a11y = cats['accessibility']['score']
    lcp = audits['largest-contentful-paint']['numericValue'] / 1000
    cls = audits['cumulative-layout-shift']['numericValue']
    tbt = audits['total-blocking-time']['numericValue']
    fcp = audits['first-contentful-paint']['numericValue'] / 1000
    size = audits.get('total-byte-weight', {}).get('numericValue', 0) / 1024
    print(f'  run {$n}: perf={perf:.2f} a11y={a11y:.2f} LCP={lcp:.2f}s CLS={cls:.3f} TBT={tbt:.0f}ms FCP={fcp:.2f}s payload={size:.0f}KB')
except Exception as e:
    print(f'  run {$n}: FAILED - {e}')
"
  done
done
echo ""
echo "All raw JSON saved to $OUT/"
