#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

echo "--- [1/3] YAML data validation"
python3 tests/check_data.py

echo "--- [2/3] Hugo build + service cards"
bash tests/check_build.sh

echo "--- [3/3] HTML structure assertions"
python3 tests/check_html.py

echo ""
echo "All tests passed."
