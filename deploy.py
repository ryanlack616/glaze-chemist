#!/usr/bin/env python3
"""Deploy glaze-chemist dist/ to stullatlas.app/glaze-chemist via GitHub Pages.

Clones (or pulls) the ryanlack616/stull-atlas deployment repo,
copies dist/ into the glaze-chemist/ subdirectory, commits, and pushes.
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/ryanlack616/stull-atlas.git"
DEPLOY_DIR = Path(__file__).resolve().parent / "_deploy"
DIST_DIR = Path(__file__).resolve().parent / "dist"
SUB_PATH = "glaze-chemist"

DRY_RUN = "--dry-run" in sys.argv


def run(cmd, **kwargs):
    """Run a command, print it, and return result."""
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)


def ensure_repo():
    """Clone or pull the deployment repo."""
    if (DEPLOY_DIR / ".git").exists():
        print("Pulling latest...")
        run(["git", "-C", str(DEPLOY_DIR), "pull", "--ff-only"])
    else:
        print("Cloning deployment repo...")
        run(["git", "clone", "--depth", "1", str(REPO_URL), str(DEPLOY_DIR)])


def sync_files():
    """Copy dist/ contents into the sub-path directory."""
    target = DEPLOY_DIR / SUB_PATH
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(DIST_DIR, target)

    files = [f for f in target.rglob("*") if f.is_file()]
    print(f"Synced {len(files)} file(s) to {SUB_PATH}/")
    for f in sorted(files):
        rel = f.relative_to(target)
        print(f"  {SUB_PATH}/{rel.as_posix()} ({f.stat().st_size:,} bytes)")
    return len(files)


def commit_and_push():
    """Stage, commit, and push changes."""
    run(["git", "-C", str(DEPLOY_DIR), "add", SUB_PATH])

    # Check if there are changes
    result = subprocess.run(
        ["git", "-C", str(DEPLOY_DIR), "diff", "--cached", "--quiet"],
        capture_output=True,
    )
    if result.returncode == 0:
        print("No changes to deploy.")
        return False

    run(["git", "-C", str(DEPLOY_DIR), "commit", "-m",
         f"Update {SUB_PATH} sub-site"])
    run(["git", "-C", str(DEPLOY_DIR), "push", "origin", "main"])
    return True


def main():
    if not DIST_DIR.exists():
        print(f"ERROR: {DIST_DIR} not found. Run 'python build.py' first.")
        sys.exit(1)

    files = [f for f in DIST_DIR.rglob("*") if f.is_file()]
    print(f"Deploying {len(files)} file(s) to {SUB_PATH}/")

    if DRY_RUN:
        for f in sorted(files):
            rel = f.relative_to(DIST_DIR)
            print(f"  [dry-run] {SUB_PATH}/{rel.as_posix()}")
        return

    ensure_repo()
    count = sync_files()
    pushed = commit_and_push()

    print(f"\n=== Deploy {'complete' if pushed else 'skipped (no changes)'}! ===")
    print(f"  {count} file(s) in {SUB_PATH}/")
    print(f"  https://stullatlas.app/{SUB_PATH}/")


if __name__ == "__main__":
    main()
