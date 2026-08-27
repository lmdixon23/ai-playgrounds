#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"


class ScriptCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.scripts: list[tuple[dict[str, str], str]] = []
        self._attrs: dict[str, str] | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "script":
            self._attrs = {key.lower(): value or "" for key, value in attrs}
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._attrs is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._attrs is not None:
            self.scripts.append((self._attrs, "".join(self._parts)))
            self._attrs = None
            self._parts = []


def build() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_7_2.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=90,
    )


def artifact_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(SITE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(SITE.rglob("*"))
        if path.is_file()
    }


def actual_quick_assign_count(source: str) -> int:
    return len(re.findall(r"<[^>]+\bdata-quick-assign-id\s*=", source, flags=re.I))


def main() -> int:
    first = build()
    if first.returncode:
        print(first.stdout)
        print(first.stderr, file=sys.stderr)
        return first.returncode
    first_hashes = artifact_hashes()

    second = build()
    if second.returncode:
        print(second.stdout)
        print(second.stderr, file=sys.stderr)
        return second.returncode
    second_hashes = artifact_hashes()

    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), {} if detail is None else detail))

    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    rows = json.loads(REGISTRY.read_text(encoding="utf-8"))["activities"]
    check(
        "v1.7.2 public boundary remains 58 files / 15 applets",
        len(files) == 58 and len(applets) == 15,
        {"files": len(files), "applets": len(applets)},
    )
    changed = sorted(
        set(first_hashes) ^ set(second_hashes)
        | {name for name in set(first_hashes) & set(second_hashes) if first_hashes[name] != second_hashes[name]}
    )
    check("two clean v1.7.2 builds are byte-for-byte repeatable", not changed, changed)
    check(
        "v1.7.2 preserves 15 active Quick Assigns",
        len(rows) == 15
        and len({row["id"] for row in rows}) == 15
        and all(row.get("status") == "active" for row in rows),
    )
    deployed_codemeta = json.loads((SITE / "codemeta.json").read_text(encoding="utf-8"))
    deployed_cff = (SITE / "CITATION.cff").read_text(encoding="utf-8")
    check(
        "deployed CodeMeta identifies v1.7.2",
        deployed_codemeta.get("softwareVersion") == "1.7.2"
        and str(deployed_codemeta.get("identifier", "")).endswith("/releases/tag/v1.7.2"),
        deployed_codemeta,
    )
    check(
        "deployed citation metadata identifies v1.7.2",
        re.search(r"(?m)^version:\s*['\"]?1\.7\.2['\"]?\s*$", deployed_cff) is not None,
    )

    for path in applets:
        source = path.read_text(encoding="utf-8")
        slug = path.parent.name
        check(
            f"{slug}: version metadata v1.7.2",
            source.count('<meta name="ai-playgrounds-version" content="1.7.2">') == 1,
        )
        check(
            f"{slug}: analytics provenance v1.7.2",
            source.count('data-ai-playgrounds-analytics="v1.7.2"') == 1,
        )
        count = actual_quick_assign_count(source)
        check(f"{slug}: exactly one real Quick Assign element", count == 1, count)
        check(
            f"{slug}: no literal undefined output",
            "undefinedundefined" not in source and re.search(r">\s*undefined\s*<", source) is None,
        )

    agent_source = (SITE / "playgrounds" / "agent-tool-context" / "index.html").read_text(encoding="utf-8")
    check(
        "agent startup has no unbounded zero-delay initializer polling",
        "setTimeout(init,0)" not in agent_source
        and "setTimeout(wait,20)" not in agent_source
        and agent_source.count("document.addEventListener('DOMContentLoaded',init,{once:true})") == 2
        and agent_source.count("document.addEventListener('DOMContentLoaded',wait,{once:true})") == 1
        and "if(mutating||active==='en')return" in agent_source,
    )

    script_count = 0
    javascript: list[dict[str, str]] = []
    for path in sorted(SITE.rglob("*.html")):
        parser = ScriptCollector()
        parser.feed(path.read_text(encoding="utf-8"))
        for index, (attrs, source) in enumerate(parser.scripts, 1):
            if attrs.get("src") or not source.strip():
                continue
            script_count += 1
            script_type = attrs.get("type", "").lower()
            name = f"{path.relative_to(SITE)}: inline script {index}"
            if script_type in {"application/ld+json", "application/json"}:
                try:
                    json.loads(source)
                except Exception as exc:
                    check(name, False, f"invalid JSON: {exc}")
                else:
                    check(name, True)
                continue
            javascript.append({"name": name, "source": source})
    checker = r"""
const fs=require('fs'),vm=require('vm');
const rows=JSON.parse(fs.readFileSync(0,'utf8')),errors={};
for(const row of rows){try{new vm.Script(row.source,{filename:row.name})}catch(error){errors[row.name]=String(error&&error.stack||error)}}
process.stdout.write(JSON.stringify(errors));
"""
    compiled = subprocess.run(
        ["node", "-e", checker],
        input=json.dumps(javascript, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if compiled.returncode:
        check("final inline JavaScript compilation batch", False, compiled.stderr.strip()[-1200:])
    else:
        syntax_errors = json.loads(compiled.stdout or "{}")
        for row in javascript:
            check(row["name"], row["name"] not in syntax_errors, syntax_errors.get(row["name"], ""))
    check("final artifact contains inline scripts to validate", script_count > 0, script_count)

    home = (SITE / "index.html").read_text(encoding="utf-8")
    check("homepage visible release is v1.7.2", '<span class="site-version">v1.7.2</span>' in home)
    check(
        "homepage retains 15-card/four-locale composition",
        "v161-home-four-locale-runtime" in home and 'hreflang="vi"' in home and 'hreflang="es"' in home,
    )

    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    for row in rows:
        canonical = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
        check(f"{row['id']}: Teacher Pack canonical link preserved", row["id"] in teacher and canonical in teacher)
        check(f"{row['id']}: Curriculum canonical link preserved", row["id"] in curriculum and canonical in curriculum)

    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        for marker in (
            'class="ap-standard-header page-header"',
            'id="ap-modern-share"',
            'id="ap-modern-more"',
            'id="ap-modern-embed"',
            'id="ap-modern-settings-json"',
            'class="ap-modern-tldr"',
            'id="ap-modern-key-terms"',
            'id="ap-modern-a11y"',
            'id="ap-modern-a11y-state"',
            'id="ap-modern-fidelity"',
            'class="ap-standard-footer ap-modern-rich-footer"',
            'id="v172-modern-toolbar-runtime"',
            'id="v172-modern-packet-runtime"',
            'id="v172-modern-packet-label-runtime"',
            '<script type="application/ld+json">',
            'hreflang="en"',
            'hreflang="zh-Hans"',
            'hreflang="vi"',
            'hreflang="es"',
            'hreflang="x-default"',
        ):
            check(f"{slug}: {marker}", marker in source)
        panel = re.search(r'<details\s+id="ap-modern-a11y"([^>]*)>', source, flags=re.I)
        check(f"{slug}: structured accessibility panel is open", bool(panel and "open" in panel.group(1).lower()))
        head_start = source.lower().find("<head")
        head_open = source.find(">", head_start)
        head_end = source.lower().find("</head>", head_open + 1)
        style_pos = source.find('id="v172-modern-a11y-parity-style"')
        check(
            f"{slug}: accessibility stylesheet is structurally inside head",
            0 <= head_start < head_open < style_pos < head_end,
            {"head": [head_start, head_open, head_end], "style": style_pos},
        )
        check(
            f"{slug}: canonical theme preference with one-time legacy migration",
            "localStorage.setItem('theme'" in source
            and "localStorage.getItem('theme')||localStorage.getItem('ai-playgrounds-theme')" in source
            and "localStorage.removeItem('ai-playgrounds-theme')" in source
            and "localStorage.setItem('ai-playgrounds-theme'" not in source,
        )

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for release in ("release-v1-7-2", "release-v1-7-1", "release-v1-7-0", "release-v1-6-2"):
        check(f"release notes preserve {release}", f'id="{release}"' in notes)

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_2_public_release.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
