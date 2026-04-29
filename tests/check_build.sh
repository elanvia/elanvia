#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"

echo "Building with hugo --minify..."
hugo --source "$REPO" --destination "$REPO/public" --minify 2>&1 | tail -3

HTML="$REPO/public/index.html"
[ -s "$HTML" ] || { echo "FAIL: public/index.html missing or empty"; exit 1; }

# 6 service cards from data loop
COUNT=$(grep -o 'offer__card--' "$HTML" | wc -l | tr -d ' ')
[ "$COUNT" -eq 6 ] || { echo "FAIL: expected 6 service cards, got $COUNT"; exit 1; }

# All accent modifiers present
for ACCENT in sage plum rose saffron; do
    grep -q "offer__card--$ACCENT" "$HTML" \
        || { echo "FAIL: missing accent class offer__card--$ACCENT"; exit 1; }
done

# Fingerprinted CSS file referenced in HTML and exists on disk
grep -q 'css/main.min\.' "$HTML" \
    || { echo "FAIL: no fingerprinted CSS link in HTML"; exit 1; }
find "$REPO/public/css" -name "main.min.*.css" | grep -q . \
    || { echo "FAIL: no fingerprinted CSS file in public/css/"; exit 1; }

# Fingerprinted JS file referenced in HTML and exists on disk
grep -q 'js/main.min\.' "$HTML" \
    || { echo "FAIL: no fingerprinted JS script in HTML"; exit 1; }
find "$REPO/public/js" -name "main.min.*.js" | grep -q . \
    || { echo "FAIL: no fingerprinted JS file in public/js/"; exit 1; }

echo "OK: build succeeded — 6 service cards + fingerprinted assets verified"
