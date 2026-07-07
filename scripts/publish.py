#!/usr/bin/env python3
"""
Trade Hunter Publisher
Commits and pushes both repos in the correct order.

Usage:
    python scripts/publish.py
    python scripts/publish.py --message "your commit message"

Repos:
    origin       → https://github.com/lweiss01/trade-hunter-commercial  (private)
    public-dist  → https://github.com/lweiss01/trade-hunter             (public)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
DIST = ROOT / "dist"
PUBLIC_SRC  = DIST / "trade-hunter-public"

# Single source of truth for the version lives in app/edition.py.
sys.path.insert(0, str(ROOT))
from app.edition import VERSION


def run(label: str, *cmd: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd, cwd=cwd or ROOT,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"\n[FAIL] {label}")
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", "-m", default=f"{VERSION} — self-improving tuning ruleset")
    args = parser.parse_args()
    msg = args.message

    # ── Step 1: Commercial repo (origin / main) ───────────────────────────
    print(f"\n{'='*60}")
    print("  Step 1/2 — Commercial repo (private)")
    print(f"{'='*60}")

    # Check for anything to commit
    status = run("git status", "git", "status", "--porcelain")
    if status:
        run("git add", "git", "add", "-A")
        run("git commit", "git", "commit", "-m", msg)
        print(f"[OK] Committed: {msg}")
    else:
        print("[OK] Nothing to commit — working tree clean.")

    run("git push", "git", "push", "origin", "main")
    print("[OK] Pushed to github.com/lweiss01/trade-hunter-commercial")

    # ── Step 2: Public repo (public-dist / main) ──────────────────────────
    print(f"\n{'='*60}")
    print("  Step 2/2 — Public repo")
    print(f"{'='*60}")

    # Always regenerate the public source tree from the current master so
    # changes like docs/index.html are included without needing a full exe rebuild.
    run("distribute", sys.executable, "scripts/distribute.py", "--public")

    if not PUBLIC_SRC.exists():
        print(f"[FAIL] {PUBLIC_SRC} not found — run build_release.py first.")
        sys.exit(1)

    # Build a fresh orphan commit in a temp dir and force-push to public repo.
    # This keeps the public repo's history clean and avoids branch-switching
    # in the main worktree.
    with tempfile.TemporaryDirectory() as tmp:
        pub = Path(tmp) / "public"
        shutil.copytree(PUBLIC_SRC, pub)

        run("git init",      "git", "init",                    cwd=pub)
        run("git add",       "git", "add", "-A",               cwd=pub)
        run("git commit",    "git", "commit", "-m", msg,       cwd=pub)
        run("git branch",    "git", "branch", "-M", "main",    cwd=pub)
        run("git remote add","git", "remote", "add", "origin",
            "https://github.com/lweiss01/trade-hunter.git",    cwd=pub)
        run("git push",      "git", "push", "-f", "origin", "main", cwd=pub)

    print("[OK] Pushed to github.com/lweiss01/trade-hunter")

    print(f"\n{'='*60}")
    print("  PUBLISH COMPLETE")
    print(f"{'='*60}")
    print(f"  Commercial : github.com/lweiss01/trade-hunter-commercial")
    print(f"  Public     : github.com/lweiss01/trade-hunter")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
