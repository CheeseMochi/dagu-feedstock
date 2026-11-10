#!/usr/bin/env python3
"""Bump recipe/meta.yaml to Dagu's newest release.

Finds the newest vX.Y.Z tag with `git ls-remote`, reads the release's checksums.txt, and
rewrites the version and the four per-platform sha256 values. Prints GitHub Actions outputs
(bumped, old_version, new_version) when GITHUB_OUTPUT is set. Standard library only.
Usage: bump_dagu_version.py [--check]   (--check: report only, change nothing)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = "https://github.com/dagucloud/dagu"
META = Path(__file__).resolve().parents[2] / "recipe" / "meta.yaml"
PLATFORMS = {  # recipe variable -> upstream asset suffix
    "sha_osx_arm64": "darwin_arm64",
    "sha_osx_64": "darwin_amd64",
    "sha_linux_64": "linux_amd64",
    "sha_linux_aarch64": "linux_arm64",
}


def version_key(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split("."))


def latest_version() -> str:
    out = subprocess.run(["git", "ls-remote", "--tags", REPO], check=True, capture_output=True, text=True).stdout
    tags = {m.group(1) for m in re.finditer(r"refs/tags/v(\d+\.\d+\.\d+)$", out, re.M)}
    if not tags:
        sys.exit("no release tags found upstream")
    return max(tags, key=version_key)


def checksums(version: str) -> dict[str, str]:
    url = f"{REPO}/releases/download/v{version}/checksums.txt"
    with urllib.request.urlopen(url, timeout=60) as resp:
        text = resp.read().decode()
    sums = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 2:
            sums[parts[1]] = parts[0]
    return sums


def set_var(text: str, name: str, value: str) -> str:
    new, n = re.subn(rf'({{% set {name} = ")[^"]*(" %}})', rf"\g<1>{value}\g<2>", text)
    if n != 1:
        sys.exit(f"recipe/meta.yaml: expected one `set {name}`, found {n}")
    return new


def main() -> None:
    text = META.read_text()
    current = re.search(r'{% set version = "([^"]+)" %}', text).group(1)
    newest = latest_version()
    bumped = version_key(newest) > version_key(current)
    print(f"recipe: {current}, upstream: {newest}")
    if bumped and "--check" not in sys.argv:
        sums = checksums(newest)
        text = set_var(text, "version", newest)
        for var, suffix in PLATFORMS.items():
            asset = f"dagu_{newest}_{suffix}.tar.gz"
            if asset not in sums:
                sys.exit(f"checksums.txt for v{newest} has no {asset}")
            text = set_var(text, var, sums[asset])
        META.write_text(text)
        print(f"bumped recipe/meta.yaml to {newest}")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as out:
            out.write(f"bumped={'true' if bumped else 'false'}\nold_version={current}\nnew_version={newest}\n")


if __name__ == "__main__":
    main()
