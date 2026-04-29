#!/usr/bin/env python3
"""Structural assertions on the Hugo-built public/index.html."""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
html_path = ROOT / "public" / "index.html"

if not html_path.exists():
    print("FAIL: public/index.html not found — run hugo --minify first")
    sys.exit(1)

HTML = html_path.read_text()
failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def has_attr(attr, value):
    """Match both quoted (attr="value") and unquoted (attr=value) HTML attributes."""
    quoted = f'{attr}="{value}"'
    # unquoted value ends at whitespace or >
    unquoted = re.search(rf"{re.escape(attr)}={re.escape(value)}[\s>]", HTML)
    return quoted in HTML or bool(unquoted)


# Language and meta basics
check(has_attr("lang", "fr"), 'missing lang=fr on <html>')
check(has_attr("charset", "utf-8"), "missing charset=utf-8")
check(has_attr("name", "viewport"), "missing viewport meta")
check(has_attr("name", "description"), "missing description meta")
check('property="og:title"' in HTML, "missing og:title meta")
check(has_attr("rel", "icon"), "missing favicon <link>")

# Skip link
check(has_attr("class", "skip-link"), "missing skip-link element")
check("href=#contenu" in HTML or 'href="#contenu"' in HTML, "skip-link must point to #contenu")

# Section IDs (all internal nav links must resolve)
for section_id in ["accueil", "qui", "offre", "rdv", "contact", "contenu", "nav-links"]:
    check(has_attr("id", section_id), f'missing id={section_id}')

# JS DOM hooks — sticky nav
check("data-nav" in HTML, "[data-nav] missing on header — sticky nav JS will silently break")

# JS DOM hooks — mobile menu
check(has_attr("aria-expanded", "false"), 'aria-expanded=false missing on nav toggle')
check(has_attr("aria-controls", "nav-links"), 'aria-controls=nav-links missing on nav toggle')

# Scroll reveal elements — guard against mass deletion (19 in current build)
reveal_count = HTML.count("reveal")
check(reveal_count >= 10, f"too few reveal references: {reveal_count} (expected ≥10)")

# Heading hierarchy
h1_count = len(re.findall(r"<h1[\s>]", HTML))
check(h1_count == 1, f"expected exactly 1 <h1>, found {h1_count}")

# Asset loading — JS must be deferred
check("defer" in HTML, "JS <script> missing defer attribute — blocks render")

if failures:
    print(f"FAIL: {len(failures)} assertion(s) failed:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("OK: all HTML structural assertions passed")
