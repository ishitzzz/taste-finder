from __future__ import annotations

import subprocess
import sys
from pathlib import Path

print(f"Repo: {Path.cwd()}")
ok = True

if not Path("app").exists():
    print("❌ app/ folder not found. Are you in repo root?")
    ok = False

if not Path("app/web.py").exists():
    print("❌ app/web.py missing. You may be on an older commit/branch.")
    ok = False

if ok:
    probe = subprocess.run(
        [sys.executable, "-c", "import app"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        print('❌ Python cannot import package "app" from this directory.')
        ok = False

if ok:
    print("✅ environment looks good: run `make run-web`")
