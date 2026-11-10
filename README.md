About dagu-feedstock
====================

Feedstock license: [BSD-3-Clause](LICENSE)

Home: https://github.com/dagucloud/dagu

Package license: GPL-3.0 (upstream's [LICENSE](https://github.com/dagucloud/dagu/blob/main/LICENSE))

Summary: Local-first workflow engine and scheduler with a web UI

**Dagu as a conda package**, on the `cheesemochi` channel, so other conda packages can depend
on it. [agent-org](https://github.com/CheeseMochi/agent-org) uses it as its scheduler and
dashboard. Dagu isn't on conda-forge, and this is not an official Dagu package: report packaging
problems here, and Dagu bugs [upstream](https://github.com/dagucloud/dagu/issues).

```bash
conda install -c conda-forge -c cheesemochi dagu
dagu version
```

## How it is built

Upstream ships a single, statically linked Go binary with the web UI embedded; building the UI
takes a separate Node toolchain. This recipe downloads upstream's official release archive for
the platform being built, checks it against the sha256 from the release's `checksums.txt`, and
installs the `dagu` binary into `$PREFIX/bin`. Nothing is patched or rebuilt.

Platforms: osx-arm64, osx-64, linux-64, linux-aarch64. Windows is skipped.

## Layout

| Path | What it is |
|---|---|
| `recipe/meta.yaml` | The recipe: version and the four per-platform checksums. |
| `tests/run.sh` | Builds the package for this machine and runs its test (`dagu version` matches). |
| `.github/scripts/bump_dagu_version.py` | Finds the newest upstream release and updates the recipe. |
| `.github/workflows/test.yml` | Builds on macOS and Linux for every PR. |
| `.github/workflows/version-check.yml` | Daily: opens a bump PR when upstream releases. |
| `.github/workflows/release.yml` | On a `v*` tag: builds every platform and uploads to the channel. |

See [RELEASING.md](RELEASING.md) for publishing a version.
