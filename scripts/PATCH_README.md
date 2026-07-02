# Patch description

This script patches frappe's esbuild scripts to avoid crashing the asset build when an app's public path cannot be resolved during `bench build` or `yarn build`.

It:
- Adds a safe get_public_path_safe fallback in `frappe/esbuild/utils.js`.
- Exports the safe getter.
- Replaces usage in `frappe/esbuild/esbuild.js` to use get_public_path_safe.
- Skips apps whose public paths do not exist (logs a warning instead of crashing).

Usage:

1. Copy this repository to the bench/apps directory (or run from within your repository).
2. On the bench machine, run:

   FRAPPE_BENCH_ROOT=/path/to/frappe-bench bash scripts/patch_fr_esbuild.sh

3. Re-run `bench build` or `bench install-app` as needed.

Note: the script creates backups of the patched files with a timestamp suffix. You can restore them if needed.
