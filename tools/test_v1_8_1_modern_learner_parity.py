#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser

from modern_learning_v1_8_1 import LABS, LOCALES


ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EVIDENCE = ROOT / "release-evidence" / "v1.8.1-modern-learner-parity.json"
MODERN = tuple(LABS)


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
        [sys.executable, str(ROOT / "tools" / "build_site_v1_8_1.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=180,
    )


def hashes() -> dict[str, str]:
    return {
        str(path.relative_to(SITE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(SITE.rglob("*"))
        if path.is_file()
    }


def qa_count(source: str) -> int:
    return len(re.findall(r"<[^>]+\bdata-quick-assign-id\s*=", source, flags=re.I))


def write_evidence(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    first = build()
    if first.returncode:
        payload = {"harness": __file__, "stage": "first-build", "pass": False, "stdout": first.stdout[-12000:], "stderr": first.stderr[-12000:]}
        write_evidence(payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return first.returncode
    first_hashes = hashes()
    second = build()
    if second.returncode:
        payload = {"harness": __file__, "stage": "second-build", "pass": False, "stdout": second.stdout[-12000:], "stderr": second.stderr[-12000:]}
        write_evidence(payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return second.returncode

    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), {} if detail is None else detail))

    second_hashes = hashes()
    changed = sorted(
        set(first_hashes) ^ set(second_hashes)
        | {name for name in set(first_hashes) & set(second_hashes) if first_hashes[name] != second_hashes[name]}
    )
    files = [path for path in SITE.rglob("*") if path.is_file()]
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    check("v1.8.1 boundary remains 58 files / 15 applets", len(files) == 58 and len(applets) == 15, {"files": len(files), "applets": len(applets)})
    check("two clean v1.8.1 builds are byte-for-byte repeatable", not changed, changed)

    javascript: list[dict[str, str]] = []
    json_blocks = 0
    for path in sorted(SITE.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(SITE))
        check(f"{relative}: exact v1.8.1 analytics provenance", source.count('data-ai-playgrounds-analytics="v1.8.1"') == 1)
        parser = ScriptCollector()
        parser.feed(source)
        for index, (attrs, script) in enumerate(parser.scripts, 1):
            if attrs.get("src") or not script.strip():
                continue
            name = f"{relative}: inline script {index}"
            if attrs.get("type", "").lower() in {"application/ld+json", "application/json"}:
                json_blocks += 1
                try:
                    json.loads(script)
                except Exception as exc:
                    check(name, False, f"invalid JSON: {exc}")
                else:
                    check(name, True)
            else:
                javascript.append({"name": name, "source": script})

    checker = """
const fs=require('fs'),vm=require('vm');
const rows=JSON.parse(fs.readFileSync(0,'utf8')),errors={};
for(const row of rows){try{new vm.Script(row.source,{filename:row.name})}catch(error){errors[row.name]=String(error&&error.stack||error)}}
process.stdout.write(JSON.stringify(errors));
"""
    compiled = subprocess.run(
        ["node", "-e", checker], input=json.dumps(javascript, ensure_ascii=False), text=True,
        capture_output=True, check=False, timeout=50,
    )
    if compiled.returncode:
        check("all final inline JavaScript compiles", False, compiled.stderr[-2000:])
    else:
        errors = json.loads(compiled.stdout or "{}")
        check("all final inline JavaScript compiles", not errors, errors)
    check("final JSON metadata blocks were validated", json_blocks > 0, json_blocks)

    manifest = {row["slug"]: row for row in json.loads((SITE / "applets.json").read_text(encoding="utf-8"))}
    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        initial = source.split('<script id="v181-modern-learner-parity-runtime">', 1)[0]
        check(f"{slug}: one featured experiment", initial.count('class="signature-challenge ap-modern-featured"') == 1)
        check(f"{slug}: five visible initial scenario cards", initial.count('data-modern-scenario-card=') == 5)
        check(
            f"{slug}: scenario → Quick Assign → explanation reading order",
            0 <= initial.find('id="ap-modern-learning"') < initial.find('data-quick-assign-id=') < initial.find('id="ap-modern-explanation"'),
        )
        check(f"{slug}: full terminology primer", initial.count('<dt>') >= 8 and 'class="essay-primer"' in initial)
        check(f"{slug}: step-by-step explanation", initial.count('<section><h2>') >= 5 and 'id="essay"' in initial)
        check(f"{slug}: teacher prompts", 'class="for-teachers"' in initial and "Pre-exploration prompts" in initial and "Post-exploration prompts" in initial)
        check(f"{slug}: one Quick Assign surface", qa_count(source) == 1, qa_count(source))
        check(f"{slug}: one canonical native text state", source.count(f'id="{LABS[slug]["state_id"]}"') == 1)
        check(f"{slug}: no duplicated accessibility state mirror", 'id="ap-modern-a11y-state"' not in source and 'ap-modern-a11y-parity" open' not in source)
        check(f"{slug}: Quick Assign state waits for learner refresh", "state.dataset.qaStateReady='1'" in source and "if(state?.dataset.qaStateReady==='1')" in source)
        header = source[source.find('<header class="ap-standard-header'):source.find('</header>')]
        check(f"{slug}: mature header control families", all(marker in header for marker in ('class="header-theme"', 'class="header-png"', 'class="header-reset"', 'class="lang-switch modern-lang-switch"')))
        check(f"{slug}: all four actions are visible in the header row", 'id="ap-modern-more"' not in header and all(header.count(f'id="{control}"') == 1 for control in ("ap-modern-share", "ap-modern-embed", "ap-modern-settings-json", "ap-standard-reset")))
        check(f"{slug}: explicit dark-theme surface fixes", all(marker in source for marker in ('body.ap-standard-dark .boundary', 'body.ap-standard-dark .tree-wrap', 'body.ap-standard-dark .node circle', 'body.ap-standard-dark .warning')))
        check(f"{slug}: v1.8.1 composition runtime is at the real document boundary", source.rfind('id="v181-modern-learner-parity-runtime"') > source.rfind('id="v172-modern-packet-label-runtime"'))
        for locale in LOCALES:
            local = LABS[slug]["copy"][locale]
            check(f"{slug}/{locale}: five localized scenarios", len(local["scenarios"]) == 5)
            check(f"{slug}/{locale}: at least five localized explanation sections", len(local["sections"]) >= 5)
            check(f"{slug}/{locale}: localized teacher sequence", len(local["teacher"]["pre"]) >= 3 and len(local["teacher"]["post"]) >= 4)
        row = manifest[slug]
        check(f"{slug}: plain-language English catalogue description", len(row["desc"].split()) <= 18, row["desc"])
        check(f"{slug}: concise English featured prompt", len(row["featured"].split()) <= 14, row["featured"])
        for key in ("desc_zh", "desc_vi", "desc_es", "featured_zh", "featured_vi", "featured_es"):
            check(f"{slug}: catalogue includes {key}", bool(str(row.get(key, "")).strip()), row.get(key))

    for slug, markers in {
        "hill-climbing": ("restartBenchmark", "__hillBenchmarkTest"),
        "knn-classifier": ("taskMode", "__knnModeTest"),
        "cnf-sat": ("cdclTrace", "__cdclModeTest"),
    }.items():
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        check(f"{slug}: v1.8.0 mechanism mode preserved", all(marker in source for marker in markers))

    cff = (SITE / "CITATION.cff").read_text(encoding="utf-8")
    codemeta = json.loads((SITE / "codemeta.json").read_text(encoding="utf-8"))
    home = (SITE / "index.html").read_text(encoding="utf-8")
    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    check("deployed citation identifies v1.8.1", re.search(r"(?m)^version:\s*['\"]?1\.8\.1['\"]?\s*$", cff) is not None)
    check("deployed CodeMeta identifies v1.8.1", codemeta.get("softwareVersion") == "1.8.1" and str(codemeta.get("identifier", "")).endswith("/v1.8.1"), codemeta)
    check("homepage visible version is v1.8.1", '<span class="site-version">v1.8.1</span>' in home)
    check("release history preserves v1.8.1, v1.8.0, and v1.7.2", all(f'id="release-{version}"' in notes for version in ("v1-8-1", "v1-8-0", "v1-7-2")))

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_8_1_modern_learner_parity.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    write_evidence(payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
