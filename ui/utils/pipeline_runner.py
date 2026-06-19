from __future__ import annotations
import subprocess
import sys
import os
from typing import Generator


def run_pipeline(project_dir: str | None = None) -> Generator[str, None, None]:
    if project_dir is None:
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    script = os.path.join(project_dir, "run_pipeline.py")
    cmd = [sys.executable, script]

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
        cwd=project_dir,
    )

    for line in process.stdout:
        yield line.strip()

    process.wait()
    if process.returncode != 0:
        yield f"ERROR: Pipeline exited with code {process.returncode}"
