#!/usr/bin/env python3
"""
Trade Hunter Distribution Script
Generates clean source trees for both editions:
  dist/trade-hunter-commercial/  — full source, IS_COMMERCIAL=True, no dev junk
  dist/trade-hunter-public/      — stripped source, IS_COMMERCIAL=False

Usage:
  python scripts/distribute.py          # builds both
  python scripts/distribute.py --public # builds public only
"""

from __future__ import annotations

import fnmatch
import os
import shutil
import sys
from pathlib import Path

# Configuration
ROOT = Path(__file__).parent.parent.resolve()
DIST_ROOT = ROOT / "dist"
COMMERCIAL_DIR = DIST_ROOT / "trade-hunter-commercial"
PUBLIC_DIR = DIST_ROOT / "trade-hunter-public"

# ── HARDENED CASE-INSENSITIVE CONFIGURATIONS ──────────────────────────────
IGNORE_NAMES = {n.lower() for n in {
    # VCS / tool / env hygiene
    ".git",
    ".github",  
    ".home",
    ".pytest_cache",
    ".venv",
    ".vscode",
    "__pycache__",
    ".env",
    # Output / ephemeral / workspace cruft from local runs
    "dist",
    "scratch",
    "tests",  
    "build",
    "tmp",
    ".tmp",
    ".artifacts",
    # Private agent + milestone metadata (commercial repo continuity)
    ".gsd",
    ".gsd-id",
    ".gsd.migrating",
    ".antigravity_session",
    ".holistic",
    ".planning",
    ".cursor",
    ".beads",
    # IDE / toolchain rules wired to authors' setups
    ".cursorrules",
    ".windsurfrules",
    # Repo-local secrets or integration scratch (never distribute)
    ".bg-shell",
    ".kalshi-keys",
    # Ephemeral notebooks / probes (not docs)
    "current_feeds.txt",
    "proposal_feeds.txt",
    "HANDOFF.md",
    # Generated / leaked local artefacts
    "trade_hunter.egg-info",
    "integration_test_results.md",
    "integration_test_results_sqlite.md",
    "output.log",
    "trade-hunter-boot.log",
    "design-proposal.html",
    "trade-hunter_dashboard_mockup.html",
    # Agent protocol copies at repo root
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "HOLISTIC.md",
    # Commercial-only plain-text README
    "README.txt",
}}

IGNORE_NAME_GLOBS = (
    "trade-hunter*.exe",
    "trade_hunter.corrupt*.db",
    "*.pyc",
    # Local SQLite WAL / SHM / backups from dev machines
    "trade_hunter.db-shm",
    "trade_hunter.db-wal",
    "trade_hunter.db.bak-*",
    "trade_hunter.db",
    "trade-hunter*.spec",
    # Aggressive defensive wildcards to catch stray keys or workspace clutter
    "*key*", 
    "*secret*", 
    "*token*", 
    "*.pem", 
    "*.key",
    "*.env*", 
    "*_backup.*", 
    "*.bak", 
    "*.old", 
    "*.tmp",
    "*credentials*", 
    "*access_token*", 
    "*refresh_token*"
)

def _ignore_basename(name: str) -> bool:
    ln = name.lower()
    if ln in IGNORE_NAMES:
        return True
    for pat in IGNORE_NAME_GLOBS:
        if fnmatch.fnmatch(ln, pat.lower()):
            return True
    return False

def ignore_func(directory, contents):
    # directory is a full path; we only need the basenames of entries
    return [c for c in contents if _ignore_basename(c)]


# Commercial-only source files removed after copy (replaced with .py stub)
STRIP_FILES = [
    "app/feeds/kalshi_pykalshi.py",
]


# ── DEEP POST-COPY SAFETY WIPE ────────────────────────────────────────────
def _cleanup_secrets(root: Path):
    secret_patterns = [
        "*key*", "*secret*", "*token*", "*.pem", "*.key",
        "*.env*", "*_backup.*", "*.bak", "*.old", "*.tmp",
        "*credentials*", "*access_token*", "*refresh_token*"
    ]
    for path in list(root.rglob("*")):
        if path.is_file():
            ln = path.name.lower()
            if any(fnmatch.fnmatch(ln, pat.lower()) for pat in secret_patterns):
                try:
                    path.unlink()
                    print(f"[SECURITY] Removed leaked file from distribution tree: {path.relative_to(root)}")
                except Exception as e:
                    print(f"[WARN] Failed to remove dangerous file {path}: {e}")


def build_commercial_source() -> None:
    """Copy master repo → dist/trade-hunter-commercial/ using the same ignore
    patterns as the public build, but WITHOUT stripping any files or changing
    edition.py.  Gives commercial customers a clean source tree with no dev
    junk (no .holistic, .gsd, .env, scratch, .kalshi-keys, etc.).
    """
    print(f"--- Trade Hunter Commercial Source Build ---")

    if os.path.exists(COMMERCIAL_DIR):
        print(f"Cleaning existing folder: {COMMERCIAL_DIR}")
        shutil.rmtree(COMMERCIAL_DIR)

    os.makedirs(DIST_ROOT, exist_ok=True)

    print(f"Syncing master -> {COMMERCIAL_DIR}...")

    shutil.copytree(ROOT, COMMERCIAL_DIR, ignore=ignore_func)
    _cleanup_secrets(COMMERCIAL_DIR)

    print("SUCCESS!")
    print(f"Commercial source ready at: {COMMERCIAL_DIR}")
    print()


def main():
    print("--- Trade Hunter Distribution Tool ---")
    public_only = "--public" in sys.argv

    if not public_only:
        build_commercial_source()

    if os.path.exists(PUBLIC_DIR):
        print(f"Cleaning existing dist folder: {PUBLIC_DIR}")
        shutil.rmtree(PUBLIC_DIR)

    os.makedirs(DIST_ROOT, exist_ok=True)

    print(f"Syncing master -> {PUBLIC_DIR}...")

    shutil.copytree(ROOT, PUBLIC_DIR, ignore=ignore_func)
    _cleanup_secrets(PUBLIC_DIR)

    print("Patching Edition Configuration...")
    edition_path = PUBLIC_DIR / "app" / "edition.py"
    if edition_path.exists():
        with open(edition_path, "w", encoding="utf-8") as f:
            f.write("# Trade Hunter Public Edition\n")
            f.write("# AUTO-GENERATED BY DISTRIBUTE.PY\n")
            f.write("IS_COMMERCIAL = False\n")
        print("[OK] IS_COMMERCIAL set to False.")
    else:
        print("[WARN] WARNING: app/edition.py not found in public copy!")

    print("Stripping Commercial-Only Source Files...")
    for rel_path in STRIP_FILES:
        target = PUBLIC_DIR / rel_path
        if target.exists():
            target.unlink()
            print(f"[OK] Stripped: {rel_path}")
            # Replace with a proper .py stub that raises ImportError.
            target.write_text(
                "# Trade Hunter Public / Simulation Edition\n"
                "# This module is exclusive to the Commercial Edition.\n"
                "# Visit https://tradehunter.ai to upgrade.\n"
                "\n"
                "raise ImportError(\n"
                "    'KalshiPykalshiFeed is only available in the Commercial Edition. '\n"
                "    'Visit https://tradehunter.ai to upgrade.'\n"
                ")\n"
            )
            print(f"[OK] Stub written: {rel_path}")
        else:
            print(f"[WARN] WARNING: Sensitive file not found: {rel_path}")

    print("\nSUCCESS!")
    print(f"Your Public Edition is ready at: {PUBLIC_DIR}")
    print("You can now push the contents of this folder to your public GitHub repository.")


if __name__ == "__main__":
    main()