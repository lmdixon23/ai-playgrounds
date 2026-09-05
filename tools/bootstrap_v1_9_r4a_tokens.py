#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "src" / "design" / "ai-playgrounds.tokens.json"
BINDINGS = ROOT / "src" / "design" / "current-bindings.json"

LAB_ACCENTS = {
    "search-pathfinding": "#2563eb",
    "hill-climbing": "#a16207",
    "wumpus-world": "#c2410c",
    "cnf-sat": "#6d28d9",
    "bayes-classifier": "#a21caf",
    "bayes-network": "#0f766e",
    "knn-classifier": "#be123c",
    "overfitting": "#047857",
    "neural-network": "#4338ca",
    "kmeans": "#4d7c0f",
    "convolution": "#0e7490",
    "q-learning-gridworld": "#b91c1c",
    "transformer-language-model": "#6d28d9",
    "agent-tool-context": "#0f766e",
    "minimax-alpha-beta": "#0d9488",
}

ORIGINAL = [
    "search-pathfinding", "hill-climbing", "wumpus-world", "cnf-sat",
    "bayes-classifier", "bayes-network", "knn-classifier", "overfitting",
    "neural-network", "kmeans", "convolution", "q-learning-gridworld",
]


def color_value(value: str, alpha: float | None = None) -> dict:
    raw = value.lstrip("#")
    if len(raw) == 3:
        raw = "".join(char * 2 for char in raw)
    rgb = [round(int(raw[index:index + 2], 16) / 255, 6) for index in (0, 2, 4)]
    result = {"colorSpace": "srgb", "components": rgb, "hex": f"#{raw.lower()}"}
    if alpha is not None:
        result["alpha"] = alpha
    return result


def dim(value: int | float, unit: str = "px") -> dict:
    return {"value": value, "unit": unit}


def build_tokens() -> dict:
    payload: dict = OrderedDict()
    payload["$schema"] = "https://www.designtokens.org/schemas/2025.10/format.json"
    payload["$description"] = (
        "AI Playgrounds frozen v1.8.1 design-token contract for v1.9 architecture work. "
        "Values describe current output; they do not authorize visible redesign."
    )
    payload["dimension"] = {
        "space": {
            "$type": "dimension",
            **{
                f"s{value:02d}": {"$value": dim(value)}
                for value in (2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 22, 24, 30, 32, 34, 36, 48, 64)
            },
        },
        "radius": {
            "$type": "dimension",
            "compact": {"$value": dim(6)},
            "control": {"$value": dim(8)},
            "panel": {"$value": dim(10)},
            "prominent": {"$value": dim(12)},
            "large": {"$value": dim(14)},
            "pill": {"$value": dim(999)},
        },
        "control": {
            "$type": "dimension",
            "inline": {"$value": dim(36)},
            "compact": {"$value": dim(38)},
            "standard": {"$value": dim(42)},
            "touch": {"$value": dim(44)},
        },
        "focus": {
            "$type": "dimension",
            "ringWidth": {"$value": dim(3)},
            "offsetCompact": {"$value": dim(2)},
            "offsetStandard": {"$value": dim(3)},
        },
        "layout": {
            "$type": "dimension",
            "reading": {"$value": dim(760)},
            "support": {"$value": dim(820)},
            "learning": {"$value": dim(980)},
            "wide": {"$value": dim(1180)},
            "gutterCompact": {"$value": "{dimension.space.s14}"},
            "gutterStandard": {"$value": "{dimension.space.s20}"},
        },
        "breakpoint": {
            "$type": "dimension",
            "phoneLegacy": {"$value": dim(480)},
            "phoneNewer": {"$value": dim(520)},
            "supportCompact": {"$value": dim(680)},
            "shellCompact": {"$value": dim(720)},
            "learningCompact": {"$value": dim(820)},
            "wideNewer": {"$value": dim(980)},
        },
        "fontSize": {
            "$type": "dimension",
            "micro": {"$value": dim(0.72, "rem")},
            "caption": {"$value": dim(0.78, "rem")},
            "small": {"$value": dim(0.82, "rem")},
            "body": {"$value": dim(1, "rem")},
            "bodyLarge": {"$value": dim(1.03, "rem")},
            "subheading": {"$value": dim(1.05, "rem")},
            "subheadingStrong": {"$value": dim(1.08, "rem")},
            "section": {"$value": dim(1.45, "rem")},
        },
    }
    payload["number"] = {
        "lineHeight": {
            "$type": "number",
            "compact": {"$value": 1.45},
            "body": {"$value": 1.5},
            "reading": {"$value": 1.6},
        },
        "fontWeight": {
            "$type": "number",
            "regular": {"$value": 400},
            "strong": {"$value": 700},
            "action": {"$value": 750},
            "emphasis": {"$value": 800},
        },
    }
    payload["font"] = {
        "family": {
            "ui": {"$type": "fontFamily", "$value": ["system-ui", "-apple-system", "sans-serif"]}
        }
    }

    primitive_colors = {
        "warmPage": "#fefdf8", "neutralPage": "#f8fafc", "minimaxPage": "#f7f8fb",
        "white": "#ffffff", "legacyText": "#1f2937", "newerText": "#172033",
        "legacyMuted": "#6b7280", "newerMuted": "#64748b", "minimaxMuted": "#637083",
        "legacyBorder": "#e5e7eb", "newerBorder": "#cbd5e1", "minimaxBorder": "#d7dde7",
        "legacySoft": "#f9fafb", "newerSoft": "#f1f5f9", "minimaxSoft": "#eef2ff",
        "darkPage": "#0f172a", "darkLegacyCard": "#1e293b", "darkNewerCard": "#172033",
        "darkText": "#e2e8f0", "darkLegacyMuted": "#94a3b8", "darkNewerMuted": "#a9b6c9",
        "darkBorder": "#334155", "success": "#047857", "warning": "#9a3412", "error": "#b91c1c",
        "minimaxSuccess": "#0f766e", "minimaxWarning": "#b45309",
        "darkSuccess": "#6ee7b7", "darkWarning": "#fdba74", "darkError": "#fca5a5",
    }
    payload["color"] = {
        "primitive": {
            "$type": "color",
            **{name: {"$value": color_value(value)} for name, value in primitive_colors.items()},
        },
        "lab": {},
    }
    for slug, value in LAB_ACCENTS.items():
        key = slug.replace("-", "_")
        lab = {
            "$type": "color",
            "catalogue": {"$value": color_value(value)},
        }
        if slug == "minimax-alpha-beta":
            lab["uiLight"] = {
                "$value": color_value("#3157c8"),
                "$description": (
                    "Frozen light-theme page accent differs from catalogue accent; "
                    "tracked as a v1.9 visual-consistency candidate."
                ),
            }
            lab["uiDark"] = {"$value": color_value("#93c5fd")}
            lab["uiDarkStrong"] = {"$value": color_value("#1d4ed8")}
        elif slug == "transformer-language-model":
            lab["uiLight"] = {"$value": f"{{color.lab.{key}.catalogue}}"}
            lab["uiDark"] = {"$value": color_value("#c4b5fd")}
            lab["uiDarkStrong"] = {"$value": f"{{color.lab.{key}.catalogue}}"}
        elif slug == "agent-tool-context":
            lab["uiLight"] = {"$value": f"{{color.lab.{key}.catalogue}}"}
            lab["uiDark"] = {"$value": color_value("#5eead4")}
            lab["uiDarkStrong"] = {"$value": f"{{color.lab.{key}.catalogue}}"}
        else:
            lab["uiLight"] = {"$value": f"{{color.lab.{key}.catalogue}}"}
            lab["uiDark"] = {"$value": f"{{color.lab.{key}.catalogue}}"}
        payload["color"]["lab"][key] = lab

    payload["color"]["theme"] = {
        "legacyLight": {
            "$type": "color",
            "page": {"$value": "{color.primitive.warmPage}"},
            "card": {"$value": "{color.primitive.white}"},
            "text": {"$value": "{color.primitive.legacyText}"},
            "muted": {"$value": "{color.primitive.legacyMuted}"},
            "border": {"$value": "{color.primitive.legacyBorder}"},
            "soft": {"$value": "{color.primitive.legacySoft}"},
        },
        "legacyDark": {
            "$type": "color",
            "page": {"$value": "{color.primitive.darkPage}"},
            "card": {"$value": "{color.primitive.darkLegacyCard}"},
            "text": {"$value": "{color.primitive.darkText}"},
            "muted": {"$value": "{color.primitive.darkLegacyMuted}"},
            "border": {"$value": "{color.primitive.darkBorder}"},
            "soft": {"$value": "{color.primitive.darkLegacyCard}"},
        },
        "newerLight": {
            "$type": "color",
            "page": {"$value": "{color.primitive.neutralPage}"},
            "card": {"$value": "{color.primitive.white}"},
            "text": {"$value": "{color.primitive.newerText}"},
            "muted": {"$value": "{color.primitive.newerMuted}"},
            "border": {"$value": "{color.primitive.newerBorder}"},
            "soft": {"$value": "{color.primitive.newerSoft}"},
        },
        "newerDark": {
            "$type": "color",
            "page": {"$value": "{color.primitive.darkPage}"},
            "card": {"$value": "{color.primitive.darkNewerCard}"},
            "text": {"$value": "{color.primitive.darkText}"},
            "muted": {"$value": "{color.primitive.darkNewerMuted}"},
            "border": {"$value": "{color.primitive.darkBorder}"},
            "soft": {"$value": "{color.primitive.darkLegacyCard}"},
        },
        "minimaxLight": {
            "$type": "color",
            "page": {"$value": "{color.primitive.minimaxPage}"},
            "card": {"$value": "{color.primitive.white}"},
            "text": {"$value": "{color.primitive.newerText}"},
            "muted": {"$value": "{color.primitive.minimaxMuted}"},
            "border": {"$value": "{color.primitive.minimaxBorder}"},
            "soft": {"$value": "{color.primitive.minimaxSoft}"},
        },
        "semantic": {
            "$type": "color",
            "success": {"$value": "{color.primitive.success}"},
            "warning": {"$value": "{color.primitive.warning}"},
            "error": {"$value": "{color.primitive.error}"},
            "darkSuccess": {"$value": "{color.primitive.darkSuccess}"},
            "darkWarning": {"$value": "{color.primitive.darkWarning}"},
            "darkError": {"$value": "{color.primitive.darkError}"},
        },
    }
    payload["shadow"] = {
        "$type": "shadow",
        "popover": {
            "$value": {
                "color": color_value("#0f172a", 0.18), "offsetX": dim(0), "offsetY": dim(16),
                "blur": dim(35), "spread": dim(0),
            }
        },
        "cardSubtle": {
            "$value": {
                "color": color_value("#0f172a", 0.05), "offsetX": dim(0), "offsetY": dim(6),
                "blur": dim(18), "spread": dim(0),
            }
        },
        "card": {
            "$value": {
                "color": color_value("#0f172a", 0.08), "offsetX": dim(0), "offsetY": dim(3),
                "blur": dim(12), "spread": dim(0),
            }
        },
    }
    return payload


def component_binding(resource: str, token: str, needle: str, count: int) -> dict:
    return {"resource": resource, "token": token, "needle": needle, "count": count}


def build_bindings() -> dict:
    original_profile = {
        "slugs": ORIGINAL,
        "lightSelector": ":root",
        "light": {
            "--bg": "color.theme.legacyLight.page", "--card": "color.theme.legacyLight.card",
            "--fg": "color.theme.legacyLight.text", "--muted": "color.theme.legacyLight.muted",
            "--border": "color.theme.legacyLight.border", "--soft": "color.theme.legacyLight.soft",
        },
        "darkSelector": "body.dark-mode",
        "dark": {
            "--bg": "color.theme.legacyDark.page", "--card": "color.theme.legacyDark.card",
            "--fg": "color.theme.legacyDark.text", "--muted": "color.theme.legacyDark.muted",
            "--border": "color.theme.legacyDark.border", "--soft": "color.theme.legacyDark.soft",
        },
    }
    transformer_agent_profile = {
        "slugs": ["transformer-language-model", "agent-tool-context"],
        "lightSelector": ":root",
        "light": {
            "--bg": "color.theme.newerLight.page", "--card": "color.theme.newerLight.card",
            "--fg": "color.theme.newerLight.text", "--muted": "color.theme.newerLight.muted",
            "--border": "color.theme.newerLight.border", "--soft": "color.theme.newerLight.soft",
        },
        "darkSelector": "body.ap-standard-dark",
        "dark": {
            "--bg": "color.theme.newerDark.page", "--card": "color.theme.newerDark.card",
            "--fg": "color.theme.newerDark.text", "--muted": "color.theme.newerDark.muted",
            "--border": "color.theme.newerDark.border", "--soft": "color.theme.newerDark.soft",
        },
    }
    minimax_profile = {
        "slugs": ["minimax-alpha-beta"],
        "lightSelector": ":root",
        "light": {
            "--bg": "color.theme.minimaxLight.page", "--card": "color.theme.minimaxLight.card",
            "--fg": "color.theme.minimaxLight.text", "--muted": "color.theme.minimaxLight.muted",
            "--border": "color.theme.minimaxLight.border", "--soft": "color.theme.minimaxLight.soft",
        },
        "darkSelector": "body.ap-standard-dark",
        "dark": {
            "--bg": "color.theme.newerDark.page", "--card": "color.theme.newerDark.card",
            "--fg": "color.theme.newerDark.text", "--muted": "color.theme.newerDark.muted",
            "--border": "color.theme.newerDark.border", "--soft": "color.theme.newerDark.soft",
        },
    }
    accents = {}
    for slug in LAB_ACCENTS:
        key = slug.replace("-", "_")
        accents[slug] = {
            "catalogue": f"color.lab.{key}.catalogue",
            "uiLight": f"color.lab.{key}.uiLight",
            "uiDark": f"color.lab.{key}.uiDark",
        }
        if slug in {"transformer-language-model", "agent-tool-context", "minimax-alpha-beta"}:
            accents[slug]["uiDarkStrong"] = f"color.lab.{key}.uiDarkStrong"

    literals = [
        component_binding("src/ui/components/original/learner-interface-style.html", "dimension.control.compact", "min-height:38px", 1),
        component_binding("src/ui/components/original/learner-interface-style.html", "dimension.radius.control", "border-radius:8px", 2),
        component_binding("src/ui/components/original/learner-interface-style.html", "dimension.space.s08", "gap:8px", 1),
        component_binding("src/ui/components/original/learner-interface-style.html", "dimension.breakpoint.shellCompact", "max-width:720px", 1),
        component_binding("src/ui/components/original/learning-modes-style-common.html", "dimension.control.standard", "min-height:42px", 1),
        component_binding("src/ui/components/original/learning-modes-style-common.html", "dimension.breakpoint.learningCompact", "max-width:820px", 1),
        component_binding("src/ui/components/original/learning-modes-style-common.html", "dimension.breakpoint.wideNewer", "min-width:980px", 1),
        component_binding("src/ui/components/original/v14-version-provenance-style.html", "dimension.layout.wide", "max-width:1180px", 1),
        component_binding("src/ui/components/newer/v172-modern-parity-style.html", "dimension.control.compact", "min-height:38px", 1),
        component_binding("src/ui/components/newer/v172-modern-parity-style.html", "dimension.control.touch", "min-height:44px", 1),
        component_binding("src/ui/components/newer/v172-modern-parity-style.html", "dimension.breakpoint.shellCompact", "max-width:720px", 1),
        component_binding("src/ui/components/newer/v172-modern-toolbar-parity-style.html", "dimension.control.compact", "min-height:38px", 1),
        component_binding("src/ui/components/newer/v172-modern-toolbar-parity-style.html", "dimension.control.touch", "min-height:44px", 2),
        component_binding("src/ui/components/newer/v172-modern-toolbar-parity-style.html", "dimension.breakpoint.shellCompact", "max-width:720px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.control.compact", "min-height:38px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.control.touch", "min-height:44px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.layout.reading", "max-width:760px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.layout.learning", "max-width:980px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.breakpoint.shellCompact", "max-width:720px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.breakpoint.phoneNewer", "max-width:520px", 1),
        component_binding("src/ui/components/newer/v181-modern-learner-parity-style.html", "dimension.breakpoint.wideNewer", "min-width:980px", 1),
    ]
    return {
        "schema_version": 1,
        "phase": "v1.9-r4a-design-token-contract",
        "token_file": "src/design/ai-playgrounds.tokens.json",
        "format": "DTCG 2025.10",
        "public_release_boundary": "v1.8.1",
        "themeProfiles": {
            "legacy": original_profile,
            "transformerAgent": transformer_agent_profile,
            "minimax": minimax_profile,
        },
        "accentBindings": accents,
        "componentLiteralBindings": literals,
        "notes": {
            "lineageNotTaxonomy": (
                "Theme/source profiles describe frozen implementation lineages, not curriculum tracks. "
                "Minimax remains Foundations."
            ),
            "noVisualAuthority": (
                "R4a describes current output and does not authorize visible consolidation. "
                "Candidate normalizations remain owned by v1.9 visual evidence work."
            ),
        },
    }


def main() -> int:
    TOKENS.parent.mkdir(parents=True, exist_ok=True)
    TOKENS.write_text(json.dumps(build_tokens(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BINDINGS.write_text(json.dumps(build_bindings(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Materialized R4a token contract: {TOKENS.relative_to(ROOT)}, {BINDINGS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
