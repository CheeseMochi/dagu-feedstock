# Releasing

The recipe always targets one Dagu version, the newest this feedstock has published, as
conda-forge feedstocks do. Older versions stay installable from the channel
(`conda install dagu=2.25.8`), and each published version has a matching git tag here.

## A new upstream release

1. `version-check.yml` runs daily. When Dagu has a newer `vX.Y.Z` tag, it runs
   `.github/scripts/bump_dagu_version.py`, which sets the version and the four checksums from
   the release's `checksums.txt`, and opens (or refreshes) a PR from `bot/bump-dagu`. It starts
   `test.yml` on that branch, since bot pushes don't trigger it.
2. Review and merge the PR once the builds are green. To bump by hand instead:
   `python3 .github/scripts/bump_dagu_version.py`, commit, open a PR.
3. Publish: tag the merge commit with the version and push the tag.

   ```bash
   git checkout main && git pull
   git tag v2.26.0 && git push origin v2.26.0
   ```

   `release.yml` checks the tag matches the recipe, builds each platform on its own runner,
   uploads to the `cheesemochi` channel and creates a GitHub release.

## A packaging fix without a new Dagu version

Raise `build: number` in `recipe/meta.yaml` (reset it to 0 on the next version bump), merge, and
publish with a tag that names the build, for example `v2.26.0-1`. Update the tag check in
`release.yml` if you do this often.

## Setup (once)

- Repository secret `ANACONDA_API_TOKEN`: an anaconda.org token for the `cheesemochi` account
  with upload scope (the same one brew-feedstock uses).
- Settings, Actions, General: allow GitHub Actions to create pull requests (for the bump PR).
