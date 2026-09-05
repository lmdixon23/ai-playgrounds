#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
LAB_ROOT = ROOT / "src" / "labs"
COMPONENT_ROOT = ROOT / "src" / "ui" / "components"
MANIFEST = ROOT / "src" / "product" / "page-components.json"
ORACLE_PATH = ROOT / "src" / "product" / "public-artifact-sha256.json"

ORIGINAL = [
    "search-pathfinding",
    "hill-climbing",
    "wumpus-world",
    "cnf-sat",
    "bayes-classifier",
    "bayes-network",
    "knn-classifier",
    "overfitting",
    "neural-network",
    "kmeans",
    "convolution",
    "q-learning-gridworld",
]
NEWER = ["transformer-language-model", "agent-tool-context", "minimax-alpha-beta"]

EXPECTED = {
    "original/essay-language-script": ("b0dc4b4dd2a2cab3de9538577802580e31c4b44315cc5b327e09594c710e0c2d", 438),
    "original/learner-interface-style": ("c52b08bd150e94a4bacf448f60d182a918da330ab0c9a90a269bbc5cfce14d4a", 2559),
    "original/learning-modes-script": ("6f440c1a512641f25db3e190e928a17683710937b1f50fca79c4a01e1e6bd31e", 12168),
    "original/learning-modes-style-common": ("6e3acd3d71aeff5d002e4eb0a984ccc121208b8ac371704bafc06472482661a0", 3884),
    "original/learning-modes-style-hill-climbing": ("d6b04accf5f22a789174a28e75c1c2023dd24e52b71c5d705d52988ac8888a42", 5194),
    "original/learning-modes-style-knn-classifier": ("8c967d00798115cc03a43786e8079a27e043cc4b641cc5de79be62258167cedb", 4733),
    "original/v14-version-provenance-style": ("1fd9926c019b564849aa138d00f297dbff9064eba7fb31ddc86d77a954696100", 413),
    "newer/v17-modern-quick-assign": ("55cf9c3cd1cf35e7745a4ebcd6883193618a118225a1813e83c4d2d743df2b85", 286),
    "newer/v17-modern-quick-assign-containment": ("b1cbc35c2274b0f45ba427d374ad00858be1c531aed6d3cd50da648b47ea988c", 1386),
    "newer/v172-modern-a11y-parity-style": ("c09fc73758b30d03ce0b5818f23b4359a9492a1347b9915ece41eb02ad507c80", 1423),
    "newer/v172-modern-parity-style": ("7d8e25228c1668178fa42c74f58fa8be3c4e2c07433e7ab72391ae307356b7cb", 2763),
    "newer/v172-modern-quick-assign-parity-style": ("312c3992ad88dd104e918a3ec130f1f540b51497b1825474a9f6c3b4c2320b83", 2138),
    "newer/v172-modern-toolbar-parity-style": ("73417e66b4941e9bbaac3f113d1db0b109824f7b1a20e018a5c02dc504b86e18", 1642),
    "newer/v172-modern-toolbar-runtime": ("7c5e28072d8ff74c3dc36352aa204defc2918539f7badc06315e804c71b411eb", 2060),
    "newer/v181-modern-learner-parity-style": ("8817e557b2093861d6dd4794296a95b2badc00ca276caa2094c7fca276d0ea61", 7789),
    "newer/transformer-agent/v172-modern-packet-runtime": ("af96ebc1a9442cb30930993a63b4f2ff8dfd942c9b45153954fa00d1fc5d5f96", 4557),
    "newer/transformer-agent/v172-modern-packet-label-runtime": ("779769513d54326b1adcf1fb6dd7499cc2199ec79c50cbd62414e258b7881c8a", 3496),
}

ORIGINAL_SHARED = {
    "learner-interface-style": "original/learner-interface-style",
    "essay-language-script": "original/essay-language-script",
    "learning-modes-script": "original/learning-modes-script",
    "v14-version-provenance-style": "original/v14-version-provenance-style",
}
NEWER_SHARED = {
    "v17-modern-quick-assign": "newer/v17-modern-quick-assign",
    "v17-modern-quick-assign-containment": "newer/v17-modern-quick-assign-containment",
    "v172-modern-parity-style": "newer/v172-modern-parity-style",
    "v172-modern-toolbar-parity-style": "newer/v172-modern-toolbar-parity-style",
    "v172-modern-quick-assign-parity-style": "newer/v172-modern-quick-assign-parity-style",
    "v172-modern-a11y-parity-style": "newer/v172-modern-a11y-parity-style",
    "v181-modern-learner-parity-style": "newer/v181-modern-learner-parity-style",
    "v172-modern-toolbar-runtime": "newer/v172-modern-toolbar-runtime",
}
TRANSFORMER_AGENT_SHARED = {
    "v172-modern-packet-runtime": "newer/transformer-agent/v172-modern-packet-runtime",
    "v172-modern-packet-label-runtime": "newer/transformer-agent/v172-modern-packet-label-runtime",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def marker(key: str) -> bytes:
    return f"<!-- AI_PLAYGROUNDS_COMPONENT:{key} -->".encode("ascii")


def _has_exact_id(open_tag: bytes, element_id: bytes) -> bool:
    return b'id="' + element_id + b'"' in open_tag or b"id='" + element_id + b"'" in open_tag


def extract_block(page: bytes, element_id: str) -> bytes:
    """Return exactly one style/script element with the requested id.

    This deliberately avoids a regex over HTML. R3 needs byte identity, not an
    HTML rewrite, so the safest extraction is bounded byte scanning that returns
    the original element bytes unchanged.
    """
    eid = element_id.encode("ascii")
    matches: list[bytes] = []
    for tag in (b"style", b"script"):
        prefix = b"<" + tag
        suffix = b"</" + tag + b">"
        cursor = 0
        while True:
            start = page.find(prefix, cursor)
            if start < 0:
                break
            after_name = start + len(prefix)
            if after_name < len(page) and page[after_name : after_name + 1] not in b" \t\r\n>":
                cursor = after_name
                continue
            open_end = page.find(b">", after_name)
            if open_end < 0:
                raise RuntimeError(f"unterminated <{tag.decode()}> while locating {element_id}")
            open_tag = page[start : open_end + 1]
            if _has_exact_id(open_tag, eid):
                close_start = page.find(suffix, open_end + 1)
                if close_start < 0:
                    raise RuntimeError(f"unterminated {element_id} element")
                matches.append(page[start : close_start + len(suffix)])
            cursor = open_end + 1
    if len(matches) != 1:
        raise RuntimeError(f"{element_id}: expected one style/script block, found {len(matches)}")
    return matches[0]


def main() -> int:
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    component_bytes: dict[str, bytes] = {}
    users: dict[str, list[str]] = {}

    def use_component(page: bytes, slug: str, element_id: str, key: str) -> bytes:
        block = extract_block(page, element_id)
        expected_sha, expected_bytes = EXPECTED[key]
        actual_sha = sha256(block)
        if len(block) != expected_bytes or actual_sha != expected_sha:
            raise RuntimeError(
                f"component drift {key}: bytes={len(block)} sha256={actual_sha}; "
                f"expected bytes={expected_bytes} sha256={expected_sha}"
            )
        if key in component_bytes and component_bytes[key] != block:
            raise RuntimeError(f"component content mismatch across users: {key}")
        component_bytes[key] = block
        users.setdefault(key, []).append(slug)
        token = marker(key)
        if token in page:
            raise RuntimeError(f"component marker already present before extraction: {slug} {key}")
        return page.replace(block, token, 1)

    pages: list[dict[str, object]] = []
    for slug in ORIGINAL + NEWER:
        public_path = f"playgrounds/{slug}/index.html"
        source = SITE / public_path
        original = source.read_bytes()
        expected_page_sha = oracle.get(public_path)
        actual_page_sha = sha256(original)
        if actual_page_sha != expected_page_sha:
            raise RuntimeError(
                f"pre-extraction public page oracle mismatch for {slug}: "
                f"{actual_page_sha} != {expected_page_sha}"
            )

        template = original
        components: list[str] = []
        if slug in ORIGINAL:
            for element_id, key in ORIGINAL_SHARED.items():
                template = use_component(template, slug, element_id, key)
                components.append(key)
            variant = (
                "hill-climbing"
                if slug == "hill-climbing"
                else "knn-classifier"
                if slug == "knn-classifier"
                else "common"
            )
            key = f"original/learning-modes-style-{variant}"
            template = use_component(template, slug, "learning-modes-style", key)
            components.append(key)
        else:
            for element_id, key in NEWER_SHARED.items():
                template = use_component(template, slug, element_id, key)
                components.append(key)
            if slug in {"transformer-language-model", "agent-tool-context"}:
                for element_id, key in TRANSFORMER_AGENT_SHARED.items():
                    template = use_component(template, slug, element_id, key)
                    components.append(key)

        lab_dir = LAB_ROOT / slug
        lab_dir.mkdir(parents=True, exist_ok=True)
        template_path = lab_dir / "index.template.html"
        template_path.write_bytes(template)

        reconstructed = template
        for key in components:
            token = marker(key)
            if reconstructed.count(token) != 1:
                raise RuntimeError(f"component marker count drift: {slug} {key}")
            reconstructed = reconstructed.replace(token, component_bytes[key], 1)
        if b"<!-- AI_PLAYGROUNDS_COMPONENT:" in reconstructed:
            raise RuntimeError(f"unresolved component marker after reconstruction: {slug}")
        if reconstructed != original:
            raise RuntimeError(f"byte-exact template reconstruction failed: {slug}")

        pages.append(
            {
                "slug": slug,
                "template": template_path.relative_to(ROOT).as_posix(),
                "public_path": public_path,
                "sha256": actual_page_sha,
                "bytes": len(original),
                "components": components,
            }
        )

    components_manifest: dict[str, dict[str, object]] = {}
    for key, data in sorted(component_bytes.items()):
        component_path = COMPONENT_ROOT / f"{key}.html"
        component_path.parent.mkdir(parents=True, exist_ok=True)
        component_path.write_bytes(data)
        components_manifest[key] = {
            "path": component_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(data),
            "bytes": len(data),
            "users": users[key],
        }

    if set(components_manifest) != set(EXPECTED):
        raise RuntimeError(
            "component registry mismatch: "
            f"missing={sorted(set(EXPECTED) - set(components_manifest))}, "
            f"extra={sorted(set(components_manifest) - set(EXPECTED))}"
        )

    full_bytes = sum(int(row["bytes"]) for row in pages)
    template_bytes = sum((ROOT / str(row["template"])).stat().st_size for row in pages)
    component_total = sum(int(row["bytes"]) for row in components_manifest.values())
    net_reduction = full_bytes - (template_bytes + component_total)
    if net_reduction < 200_000:
        raise RuntimeError(f"unexpectedly small canonical source deduplication: {net_reduction} bytes")

    manifest = {
        "schema_version": 1,
        "phase": "v1.9-r3-shared-page-components",
        "marker_format": "<!-- AI_PLAYGROUNDS_COMPONENT:<key> -->",
        "page_count": len(pages),
        "component_count": len(components_manifest),
        "full_page_bytes": full_bytes,
        "template_bytes": template_bytes,
        "component_bytes": component_total,
        "deduplicated_bytes": net_reduction,
        "pages": pages,
        "components": components_manifest,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"R3 materialization PASS: {len(pages)} pages, {len(components_manifest)} components, "
        f"{net_reduction} duplicate canonical-source bytes removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
