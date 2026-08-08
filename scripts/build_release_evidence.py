#!/usr/bin/env python3
"""Build a complete, durable release-evidence bundle for an exact AI Playgrounds tree."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, pathlib, platform, subprocess, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

def run(cmd, timeout=900):
    p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return {"command": cmd, "exit_code": p.returncode, "output": p.stdout}

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda: f.read(1024 * 1024), b""):
            h.update(c)
    return h.hexdigest()

def save_run(out, name, result, runs):
    (out / f"{name}.log").write_text(result.pop("output"), encoding="utf-8")
    result["name"] = name
    runs.append(result)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="working-tree")
    ap.add_argument("--screenshots", action="store_true", help="retain browser screenshots in generated evidence")
    args = ap.parse_args()

    out = ROOT / "release-evidence" / args.tag
    out.mkdir(parents=True, exist_ok=True)
    runs = []

    save_run(out, "release-check", run([sys.executable, "tools/release_check.py", "--json", str(out / "release-check.json")]), runs)
    save_run(out, "release-metadata", run([sys.executable, "tools/check_release_metadata.py"]), runs)
    save_run(out, "build-site", run([sys.executable, "tools/build_site.py"]), runs)
    save_run(out, "algorithm-tests", run([sys.executable, "tools/run_algorithm_tests.py", "--expected-total", "45", "--json", str(out / "algorithm-tests.json")]), runs)
    browser_cmd = [sys.executable, "tools/browser_qa.py"]
    if not args.screenshots:
        browser_cmd.append("--no-screenshots")
    save_run(out, "browser-qa", run(browser_cmd, timeout=1200), runs)
    browser_dir = ROOT / "release-evidence" / "browser-qa"
    for name in ("browser-qa-results.json", "BROWSER_QA_REPORT.md"):
        src = browser_dir / name
        if src.exists():
            (out / name).write_bytes(src.read_bytes())
    save_run(out, "git-diff-check", run(["git", "diff", "--check"]), runs)
    status = run(["git", "status", "--porcelain", "--untracked-files=no"])
    tracked_clean = status["exit_code"] == 0 and not status["output"].strip()
    (out / "git-status.log").write_text(status["output"], encoding="utf-8")
    runs.append({"command": status["command"], "exit_code": 0 if tracked_clean else 1, "name": "tracked-worktree-clean"})

    commit = run(["git", "rev-parse", "HEAD"])
    commit_value = commit["output"].strip() if commit["exit_code"] == 0 else "unavailable"
    manifest = {
        "tag": args.tag,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "commit": commit_value,
        "python": sys.version,
        "platform": platform.platform(),
        "runs": runs,
        "all_pass": all(r["exit_code"] == 0 for r in runs),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    files = [x for x in out.rglob("*") if x.is_file() and x.name != "SHA256SUMS"]
    (out / "SHA256SUMS").write_text("".join(f"{digest(x)}  {x.relative_to(out)}\n" for x in sorted(files)), encoding="utf-8")
    z = ROOT / "release-evidence" / (args.tag + ".zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zz:
        for x in out.rglob("*"):
            if x.is_file():
                zz.write(x, x.relative_to(out.parent))
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["all_pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
