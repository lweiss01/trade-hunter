#!/usr/bin/env python3
"""
Trade Hunter Release Builder
Builds both the Commercial and Simulation editions in the correct order.

Usage:
    python scripts/build_release.py

Outputs (VERSION is read from app/edition.py — the single edit point):
    dist/trade-hunter-<VERSION>-commercial.zip  — Gumroad upload (exe + source + README.txt)
    dist/trade-hunter-<VERSION>-sim.exe         — Simulation exe (free / public)
    dist/trade-hunter-commercial/               — Clean commercial source tree
    dist/trade-hunter-public/                   — Stripped public source tree
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
DIST = ROOT / "dist"

# Single source of truth for the version lives in app/edition.py. Everything
# below — artifact names, zip name, display strings — derives from it, so
# bumping edition.py is the ONLY edit needed to release a new version.
sys.path.insert(0, str(ROOT))
from app.edition import VERSION  # e.g. "v0.3.0"  # noqa: E402

# The PyInstaller spec filenames are version-independent (they read the version
# from edition.py themselves and name their output exe accordingly), so they
# never need renaming on a version bump.
COMMERCIAL_SPEC = "trade-hunter.spec"
SIM_SPEC = "trade-hunter-sim.spec"


def _require_spec_files() -> None:
    """Fail loudly if the (static-named) spec files are missing rather than
    letting PyInstaller error out mid-build."""
    required = [ROOT / COMMERCIAL_SPEC, ROOT / SIM_SPEC]
    missing = [str(p.name) for p in required if not p.exists()]
    if missing:
        print(f"[FAIL] Expected PyInstaller spec files are missing: {', '.join(missing)}.")
        sys.exit(1)


def run(label: str, *cmd: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\n[FAIL] '{' '.join(cmd)}' exited with code {result.returncode}")
        sys.exit(result.returncode)
    print(f"[OK] {label} complete.")


def main() -> None:
    print(f"Trade Hunter Release Builder — {VERSION}")
    _require_spec_files()

    # Step 1: Commercial exe (built from master repo with IS_COMMERCIAL = True)
    run(
        f"Step 1/3 — Commercial exe (trade-hunter-{VERSION}.exe)",
        sys.executable, "-m", "PyInstaller",
        COMMERCIAL_SPEC, "--distpath", "dist", "--noconfirm",
    )

    # Step 2: Build both source trees:
    #   dist/trade-hunter-commercial/  (clean, IS_COMMERCIAL=True, no dev junk)
    #   dist/trade-hunter-public/      (stripped, IS_COMMERCIAL=False)
    run(
        "Step 2/3 — Source trees (commercial + public)",
        sys.executable, "scripts/distribute.py",
    )

    # Step 3: Simulation exe (built from public tree — must run after step 2)
    run(
        f"Step 3/3 — Simulation exe (trade-hunter-{VERSION}-sim.exe)",
        sys.executable, "-m", "PyInstaller",
        SIM_SPEC, "--distpath", "dist", "--noconfirm",
    )

    # Step 4: Zip the commercial package for Gumroad upload
    print(f"\n{'='*60}")
    print(f"  Step 4/4 — Gumroad zip (trade-hunter-{VERSION}-commercial.zip)")
    print(f"{'='*60}")

    zip_stage = DIST / f"trade-hunter-{VERSION}"
    if zip_stage.exists():
        shutil.rmtree(zip_stage)
    zip_stage.mkdir(parents=True)

    # exe
    shutil.copy2(DIST / f"trade-hunter-{VERSION}.exe", zip_stage)

    # README.txt
    readme = ROOT / "README.txt"
    if readme.exists():
        shutil.copy2(readme, zip_stage)
    else:
        print("[WARN] README.txt not found — zip will not include it")

    # full commercial source tree
    shutil.copytree(DIST / "trade-hunter-commercial", zip_stage / "source")

    zip_path = DIST / f"trade-hunter-{VERSION}-commercial"
    shutil.make_archive(str(zip_path), "zip", DIST, f"trade-hunter-{VERSION}")
    shutil.rmtree(zip_stage)  # clean up staging folder
    print(f"[OK] Zip created: {zip_path}.zip")

    print("\n" + "="*60)
    print("  BUILD COMPLETE")
    print("="*60)
    print(f"  Gumroad zip    : dist/trade-hunter-{VERSION}-commercial.zip")
    print(f"  Simulation exe : dist/trade-hunter-{VERSION}-sim.exe")
    print(f"  Commercial src : dist/trade-hunter-commercial/")
    print(f"  Public src     : dist/trade-hunter-public/")
    print()
    print(f"  Gumroad (paid) -> upload trade-hunter-{VERSION}-commercial.zip")
    print(f"  Public  (free) -> trade-hunter-{VERSION}-sim.exe + dist/trade-hunter-public/")
    print("="*60)


if __name__ == "__main__":
    main()