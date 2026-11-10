#!/bin/bash
# tests/run.sh: build the package for this machine's platform and run its tests
# (recipe/meta.yaml `test:`: `dagu version` matches the recipe). Needs conda-build.
# Usage: tests/run.sh [extra conda-build args]
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
python3 "$here/.github/scripts/bump_dagu_version.py" --check
conda build "$here/recipe" -c conda-forge --override-channels "$@"
