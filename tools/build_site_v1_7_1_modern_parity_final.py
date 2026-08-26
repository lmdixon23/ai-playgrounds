#!/usr/bin/env python3
from __future__ import annotations

"""Final validation wrapper for the v1.7.1 modern-lab parity candidate.

The parity layer standardizes only suite-level affordances. It preserves the
verified Transformer, agent-runtime, and Minimax/Alpha-Beta mechanisms while
normalizing the mature product shell, preference namespace, provenance, and
head/discovery metadata used by the original twelve applets.
"""

import html as html_lib
import json
import re

import build_site_v1_7_1_modern_parity as candidate

SITE = candidate.SITE
MODERN = candidate.MODERN
ESTABLISHED_PORTFOLIO = "https://lmdixon23.github.io/"
ESTABLISHED_ORCID = "https://orcid.org/0009-0001-0592-462X"
PUBLIC_ROOT = "https://lmdixon23.github.io/ai-playgrounds/"
OG_IMAGE = PUBLIC_ROOT + "og-image.png"
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230284c7'/%3E%3Cpath d='M13 10l9 6-9 6z' fill='%23ffffff'/%3E%3C/svg%3E"


def quick_assign_surface_count(page: str) -> int:
    return len(re.findall(r'<[^>]+\bdata-quick-assign-id\s*=', page, flags=re.I))


def manifest_by_slug() -> dict[str, dict]:
    rows = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    return {row["slug"]: row for row in rows}


def metadata_block(row: dict) -> str:
    slug = row["slug"]
    title = f'{row["title"]} | AI Playgrounds'
    description = row["desc"]
    canonical = f"{PUBLIC_ROOT}playgrounds/{slug}/"
    alternates = "".join(
        f'<link rel="alternate" hreflang="{lang}" href="{canonical}?lang={query}">\n'
        for lang, query in (("en", "en"), ("zh-Hans", "zh"), ("vi", "vi"), ("es", "es"), ("x-default", "en"))
    )
    jsonld = {
        "@context": "https://schema.org",
        "@type": ["WebApplication", "LearningResource"],
        "name": title,
        "url": canonical,
        "description": description,
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "Any (web browser)",
        "isAccessibleForFree": True,
        "inLanguage": ["en", "zh", "vi", "es"],
        "license": "https://opensource.org/licenses/MIT",
        "learningResourceType": "interactive simulation",
        "educationalLevel": ["high school", "undergraduate"],
        "isPartOf": {"@type": "WebSite", "name": "AI Playgrounds", "url": PUBLIC_ROOT},
        "author": {"@type": "Person", "name": "Logan M. Dixon", "sameAs": ESTABLISHED_ORCID},
    }
    esc = lambda value: html_lib.escape(str(value), quote=True)
    return (
        f'<meta name="description" content="{esc(description)}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:url" content="{esc(canonical)}">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(description)}">\n'
        f'<meta property="og:image" content="{esc(OG_IMAGE)}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{esc(title)}">\n'
        f'<meta name="twitter:description" content="{esc(description)}">\n'
        f'<meta name="twitter:image" content="{esc(OG_IMAGE)}">\n'
        f'<link rel="icon" href="{FAVICON}">\n'
        + alternates
        + '<script type="application/ld+json">'
        + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + '</script>\n'
    )


def normalize_head_metadata(page: str, row: dict) -> str:
    head_start = page.find("<head")
    head_open_end = page.find(">", head_start)
    head_end = page.find("</head>", head_open_end)
    if min(head_start, head_open_end, head_end) < 0:
        raise RuntimeError(f'No complete <head> for {row["slug"]}')
    head = page[head_open_end + 1:head_end]

    # Replace crawler-visible page title with the same product naming used by the
    # original twelve. Runtime locale synchronization below keeps it reversible.
    public_title = f'{row["title"]} | AI Playgrounds'
    head, title_count = re.subn(r'<title>.*?</title>', f'<title>{html_lib.escape(public_title)}</title>', head, count=1, flags=re.S | re.I)
    if title_count != 1:
        raise RuntimeError(f'Missing title element for {row["slug"]}')

    # Remove only the metadata families governed by this parity layer; preserve
    # viewport, version markers, canonical, and any mechanism-specific head data.
    governed_meta = (
        "description", "og:type", "og:url", "og:title", "og:description", "og:image",
        "twitter:card", "twitter:title", "twitter:description", "twitter:image",
    )
    for key in governed_meta:
        head = re.sub(
            rf'<meta\b(?=[^>]*(?:name|property)=["\']{re.escape(key)}["\'])[^>]*>\s*',
            "",
            head,
            flags=re.I,
        )
    head = re.sub(r'<link\b(?=[^>]*\brel=["\']icon["\'])[^>]*>\s*', "", head, flags=re.I)
    head = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])[^>]*>\s*', "", head, flags=re.I)
    head = re.sub(r'<script\b(?=[^>]*\btype=["\']application/ld\+json["\'])[^>]*>.*?</script>\s*', "", head, flags=re.S | re.I)

    head = head.rstrip() + "\n" + metadata_block(row)
    return page[:head_open_end + 1] + head + page[head_end:]


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'class="ap-modern-skip"',
            'class="ap-standard-header page-header"',
            'id="ap-modern-share"',
            'id="ap-modern-embed"',
            'class="ap-modern-tldr"',
            'id="ap-modern-key-terms"',
            'id="ap-modern-a11y"',
            'id="ap-modern-fidelity"',
            'class="ap-standard-footer ap-modern-rich-footer"',
            'id="v171-modern-parity-runtime"',
            '<meta name="twitter:image"',
            '<script type="application/ld+json">',
            'rel="icon"',
        )
        missing = [marker for marker in required if marker not in page]
        if missing:
            raise RuntimeError(f"Modern parity contract incomplete for {slug}: {missing}")
        count = quick_assign_surface_count(page)
        if count != 1:
            raise RuntimeError(f"Expected one Quick Assign element for {slug}, found {count}")
        if "ai-playgrounds-theme" in page:
            raise RuntimeError(f"Modern lab still uses a separate theme preference key: {slug}")
        prefs_start = page.find('<div class="header-prefs">')
        prefs_end = page.find('</div>', prefs_start)
        theme_pos = page.find('id="ap-standard-theme"')
        if not (prefs_start >= 0 and prefs_start < theme_pos < prefs_end):
            raise RuntimeError(f"Theme control is not in the shared header preference row: {slug}")
        for hreflang in ("en", "zh-Hans", "vi", "es", "x-default"):
            if f'hreflang="{hreflang}"' not in page:
                raise RuntimeError(f"Missing {hreflang} alternate for {slug}")
    candidate.predecessor.quick.base.base.impl.base.validate_local_references()


def normalize_shell_provenance_and_metadata() -> None:
    rows = manifest_by_slug()
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")

        # Preserve the exact identity/provenance already used by the original 12.
        page = page.replace("https://logandixon.me", ESTABLISHED_PORTFOLIO)
        page = page.replace("https://orcid.org/0009-0008-1712-6630", ESTABLISHED_ORCID)

        # The original twelve share `theme`; the v1.6.x modern shell accidentally
        # introduced a second preference namespace. Rejoin the existing contract.
        page = page.replace("ai-playgrounds-theme", "theme")

        # Match the established hierarchy: Theme + language are preferences in the
        # utility row; Share / Embed / Reset are actions beside the title.
        theme_match = re.search(r'<button\b[^>]*\bid="ap-standard-theme"[^>]*>.*?</button>', page, flags=re.S | re.I)
        if not theme_match:
            raise RuntimeError(f"Modern theme control missing before hierarchy normalization: {slug}")
        theme_button = theme_match.group(0)
        page = page[:theme_match.start()] + page[theme_match.end():]
        prefs_marker = '<div class="header-prefs">'
        if prefs_marker not in page:
            raise RuntimeError(f"Modern header preference row missing: {slug}")
        page = page.replace(prefs_marker, prefs_marker + theme_button, 1)

        # Keep browser title synchronized with the localized standard-shell H1.
        marker = "$('#ap-standard-title').textContent=f('title',l);"
        replacement = marker + "document.title=f('title',l)+' | AI Playgrounds';"
        if marker not in page:
            raise RuntimeError(f"Standard-shell title synchronization marker missing: {slug}")
        page = page.replace(marker, replacement, 1)

        page = normalize_head_metadata(page, rows[slug])

        if ESTABLISHED_PORTFOLIO not in page or ESTABLISHED_ORCID not in page:
            raise RuntimeError(f"Established modern-lab provenance missing after normalization: {slug}")
        if "https://logandixon.me" in page or "0009-0008-1712-6630" in page:
            raise RuntimeError(f"Unapproved alternate provenance survived normalization: {slug}")
        path.write_text(page, encoding="utf-8")


def build_site() -> None:
    # Let the base parity layer compose the feature shell, but suppress its original
    # textual Quick Assign validator until the DOM-aware final validation below.
    candidate.validate = lambda: candidate.predecessor.quick.base.base.impl.base.validate_local_references()
    candidate.build_site()
    normalize_shell_provenance_and_metadata()
    validate()
    print("Finalized v1.7.1 modern-lab parity composition with shared theme/header hierarchy, established provenance, and original-suite discovery metadata")


if __name__ == "__main__":
    build_site()
