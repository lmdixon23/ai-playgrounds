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
EVIDENCE = ROOT / "release-evidence" / "v1.8.0-public-release.json"
REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"
FEATURES = {
    "hill-climbing": ("restartBenchmark", "benchmarkRuns", "computeRestartBenchmark", "__hillBenchmarkTest"),
    "knn-classifier": ("taskMode", "targetValue", "aggregateRegressionTargets", "__knnModeTest"),
    "cnf-sat": ("solverMode", "exCdcl", "cdclTrace", "__cdclModeTest", "traceDepth(item)", "cdclTitle"),
}
QUICK_ASSIGN_SEMANTICS = {
    "hill-climbing": {
        "en": "success frequency and mean cost rank algorithms differently",
        "zh": "成功频率和平均成本可能给算法不同的排序",
        "vi": "tần suất thành công cùng chi phí trung bình",
        "es": "frecuencia de éxito y el coste medio",
    },
    "knn-classifier": {
        "en": "classification vote over labels while regression averages continuous targets",
        "zh": "分类对标签投票，而回归对连续目标值取平均",
        "vi": "phân loại bỏ phiếu trên nhãn còn hồi quy lấy trung bình mục tiêu liên tục",
        "es": "clasificación vota sobre etiquetas mientras la regresión promedia objetivos continuos",
    },
    "cnf-sat": {
        "en": "why is the learned clause valid and the backjump level safe",
        "zh": "为什么学习子句有效且回跳层级安全",
        "vi": "vì sao mệnh đề học được hợp lệ và mức nhảy lùi an toàn",
        "es": "por qué es válida la cláusula aprendida y seguro el nivel de salto",
    },
}


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
        [sys.executable, str(ROOT / "tools" / "build_site_v1_8.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=150,
    )


def artifact_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(SITE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(SITE.rglob("*"))
        if path.is_file()
    }


def quick_assign_count(source: str) -> int:
    return len(re.findall(r"<[^>]+\bdata-quick-assign-id\s*=", source, flags=re.I))


def write_evidence(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    for label in ("first", "second"):
        result = build()
        if result.returncode:
            payload = {
                "harness": "tools/test_v1_8_public_release.py",
                "stage": f"{label}-build",
                "pass": False,
                "stdout": result.stdout[-12000:],
                "stderr": result.stderr[-12000:],
            }
            write_evidence(payload)
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return result.returncode
        if label == "first":
            first_hashes = artifact_hashes()

    second_hashes = artifact_hashes()
    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), {} if detail is None else detail))

    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    rows = json.loads(REGISTRY.read_text(encoding="utf-8"))["activities"]
    check(
        "v1.8.0 public boundary is 58 files / 15 applets",
        len(files) == 58 and len(applets) == 15,
        {"files": len(files), "applets": len(applets)},
    )
    changed = sorted(
        set(first_hashes) ^ set(second_hashes)
        | {name for name in set(first_hashes) & set(second_hashes) if first_hashes[name] != second_hashes[name]}
    )
    check("two clean v1.8.0 builds are byte-for-byte repeatable", not changed, changed)
    check(
        "15 unique active four-locale Quick Assigns are preserved",
        len(rows) == 15
        and len({row["id"] for row in rows}) == 15
        and all(row.get("status") == "active" for row in rows)
        and all(row.get("locales") == ["en", "zh", "vi", "es"] for row in rows),
    )
    quick_by_id = {row["id"]: json.dumps(row, ensure_ascii=False).lower() for row in rows}
    check("QA-LOCAL-01 registry covers reliability and cost", all(term in quick_by_id.get("QA-LOCAL-01", "") for term in ("seeded restarts", "success frequency", "mean cost")))
    check("QA-KNN-01 registry covers classification and regression", all(term in quick_by_id.get("QA-KNN-01", "") for term in ("classification", "regression", "weighted mean")))
    check("QA-SAT-01 registry covers CDCL learning and backjumping", all(term in quick_by_id.get("QA-SAT-01", "") for term in ("cdcl", "learned clause", "backjump")))

    deployed_codemeta = json.loads((SITE / "codemeta.json").read_text(encoding="utf-8"))
    deployed_cff = (SITE / "CITATION.cff").read_text(encoding="utf-8")
    deployed_manifest = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    check(
        "deployed CodeMeta identifies v1.8.0",
        deployed_codemeta.get("softwareVersion") == "1.8.0"
        and str(deployed_codemeta.get("identifier", "")).endswith("/releases/tag/v1.8.0"),
        deployed_codemeta,
    )
    check(
        "deployed citation metadata identifies v1.8.0",
        re.search(r"(?m)^version:\s*['\"]?1\.8\.0['\"]?\s*$", deployed_cff) is not None,
    )
    manifest_by_slug = {row["slug"]: row for row in deployed_manifest}
    for slug, terms in {
        "hill-climbing": ("benchmark", "success rate", "seeded comparison"),
        "knn-classifier": ("regression", "continuous target", "weighted mean"),
        "cnf-sat": ("cdcl", "first uip", "backjump"),
    }.items():
        searchable = json.dumps(manifest_by_slug.get(slug, {}), ensure_ascii=False).lower()
        check(f"{slug}: catalogue/search metadata describes the v1.8.0 mode", all(term in searchable for term in terms), searchable)

    javascript: list[dict[str, str]] = []
    script_count = 0
    for path in sorted(SITE.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(SITE))
        check(f"{relative}: analytics provenance appears exactly once at v1.8.0", source.count('data-ai-playgrounds-analytics="v1.8.0"') == 1)
        if 'data-v14-support-version="true"' in source:
            check(f"{relative}: visible support-page version is v1.8.0", 'AI Playgrounds · v1.8.0</p>' in source)
        parser = ScriptCollector()
        parser.feed(source)
        for index, (attrs, script) in enumerate(parser.scripts, 1):
            if attrs.get("src") or not script.strip():
                continue
            script_count += 1
            name = f"{path.relative_to(SITE)}: inline script {index}"
            script_type = attrs.get("type", "").lower()
            if script_type in {"application/ld+json", "application/json"}:
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
        ["node", "-e", checker],
        input=json.dumps(javascript, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
        timeout=40,
    )
    if compiled.returncode:
        check("final inline JavaScript compilation batch", False, compiled.stderr.strip()[-1200:])
    else:
        syntax_errors = json.loads(compiled.stdout or "{}")
        for row in javascript:
            check(row["name"], row["name"] not in syntax_errors, syntax_errors.get(row["name"], ""))
    check("final artifact contains inline scripts to validate", script_count > 0, script_count)

    for path in applets:
        slug = path.parent.name
        source = path.read_text(encoding="utf-8")
        check(f"{slug}: exact v1.8.0 version metadata", source.count('<meta name="ai-playgrounds-version" content="1.8.0">') == 1)
        check(f"{slug}: exact v1.8.0 analytics provenance", source.count('data-ai-playgrounds-analytics="v1.8.0"') == 1)
        check(f"{slug}: exactly one real Quick Assign element", quick_assign_count(source) == 1, quick_assign_count(source))
        check(f"{slug}: no literal undefined output", "undefinedundefined" not in source and re.search(r">\s*undefined\s*<", source) is None)

    for slug, markers in FEATURES.items():
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        for marker in markers:
            check(f"{slug}: final feature marker {marker}", marker in source)
        for locale in ("en", "zh", "vi", "es"):
            check(f"{slug}: {locale} remains declared", f'lang="{locale}"' in source or f'value="{locale}"' in source)
        overlays = re.findall(r'<script data-quick-assign-locales="1">([\s\S]*?)</script>', source)
        check(f"{slug}: exactly one VI/ES Quick Assign locale overlay", len(overlays) == 1, len(overlays))
        overlay = overlays[0] if overlays else ""
        for locale, marker in QUICK_ASSIGN_SEMANTICS[slug].items():
            haystack = overlay if locale in {"vi", "es"} else source
            check(f"{slug}: {locale} Quick Assign reflects the v1.8.0 mode", marker in haystack, marker)

    home = (SITE / "index.html").read_text(encoding="utf-8")
    check("homepage visible release is v1.8.0", '<span class="site-version">v1.8.0</span>' in home)
    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for release in ("release-v1-8-0", "release-v1-7-2", "release-v1-7-1", "release-v1-7-0", "release-v1-6-2"):
        check(f"release notes preserve {release}", f'id="{release}"' in notes)

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_8_public_release.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    write_evidence(payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
