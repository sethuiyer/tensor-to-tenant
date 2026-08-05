"""T1.4.f: Astro/Pagefind site build smoke test."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_npm_build_succeeds() -> None:
    npm = shutil.which("npm")
    assert npm, "npm is required for the site build smoke test"
    result = subprocess.run(
        [npm, "run", "build"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert (ROOT / "dist" / "index.html").exists()
