#!/usr/bin/env bash
set -euo pipefail

# Patch frappe esbuild scripts to be resilient when app public paths are missing.
# Usage: FRAPPE_BENCH_ROOT=/home/frappe/frappe-bench ./patch_fr_esbuild.sh

FRAPPE_BENCH_ROOT=${FRAPPE_BENCH_ROOT:-"$HOME/frappe-bench"}

UTILS_PATH="$FRAPPE_BENCH_ROOT/apps/frappe/frappe/esbuild/utils.js"
ESBUILD_PATH="$FRAPPE_BENCH_ROOT/apps/frappe/frappe/esbuild/esbuild.js"

if [ ! -f "$UTILS_PATH" ]; then
  echo "Cannot find $UTILS_PATH"
  exit 1
fi
if [ ! -f "$ESBUILD_PATH" ]; then
  echo "Cannot find $ESBUILD_PATH"
  exit 1
fi

TIMESTAMP=$(date +%s)
cp "$UTILS_PATH" "$UTILS_PATH.bak.$TIMESTAMP"
cp "$ESBUILD_PATH" "$ESBUILD_PATH.bak.$TIMESTAMP"

echo "Backed up original files to *.bak.$TIMESTAMP"

python3 - <<'PY'
from pathlib import Path
import sys

utils = Path(r"$UTILS_PATH")
esbuild = Path(r"$ESBUILD_PATH")

u_text = utils.read_text()

# Replace existing simple get_public_path with safe variant
old_get = "const get_public_path = (app) => public_paths[app];"
if old_get in u_text:
    new_block = '''const get_public_path_safe = (app) => {
    // Prefer mapped public path if available
    if (public_paths[app]) return public_paths[app];
    // Fallback to conventional location: apps/<app>/<app>/public
    return path.resolve(apps_path, app, app, "public");
};

const get_public_path = (app) => public_paths[app];'''
    u_text = u_text.replace(old_get, new_block)

# Ensure get_public_path_safe is exported in module.exports
if "get_public_path_safe" not in u_text:
    u_text = u_text.replace("get_public_path,", "get_public_path_safe,\n\tget_public_path,")

utils.write_text(u_text)
print('Patched utils.js')

# Patch esbuild.js to use get_public_path_safe and skip missing public paths
e_text = esbuild.read_text()
# Replace destructured import
if "get_public_path," in e_text:
    e_text = e_text.replace("get_public_path,", "get_public_path_safe,")

# Insert fs.existsSync check in get_all_files_to_build (look for include_patterns.push line)
import re
pattern = r"for \(let app of apps\) \{\n\s*let public_path = get_public_path_safe\(app\);"
if re.search(pattern, e_text):
    e_text = re.sub(pattern, "for (let app of apps) {\n\t\tlet public_path = get_public_path_safe(app);\n\t\tif (!fs.existsSync(public_path)) {\n\t\t\tlog_warn(`Public path not found for app ${app} (${public_path}), skipping asset build for this app.`);\n\t\t\tcontinue;\n\t\t}", e_text)
else:
    # fallback: patch the first occurrence of get_public_path_safe in the function
    e_text = e_text.replace('let public_path = get_public_path_safe(app);', 'let public_path = get_public_path_safe(app);\n\t\tif (!fs.existsSync(public_path)) {\n\t\t\tlog_warn(`Public path not found for app ${app} (${public_path}), skipping asset build for this app.`);\n\t\t\tcontinue;\n\t\t}')

# Patch get_files_to_build similarly
pattern2 = r"for \(let file of files\) \{\n\s*let \[app, bundle\] = file.split\("/"\);\n\s*let public_path = get_public_path_safe\(app\);"
if re.search(pattern2, e_text):
    e_text = re.sub(pattern2, "for (let file of files) {\n\t\tlet [app, bundle] = file.split(\"/\");\n\t\tlet public_path = get_public_path_safe(app);\n\t\tif (!fs.existsSync(public_path)) {\n\t\t\tlog_warn(`Public path not found for app ${app} (${public_path}), skipping asset build for this file.`);\n\t\t\tcontinue;\n\t\t}", e_text)
else:
    e_text = e_text.replace('let public_path = get_public_path_safe(app);', 'let public_path = get_public_path_safe(app);\n\t\tif (!fs.existsSync(public_path)) {\n\t\t\tlog_warn(`Public path not found for app ${app} (${public_path}), skipping asset build for this file.`);\n\t\t\tcontinue;\n\t\t}')

esbuild.write_text(e_text)
print('Patched esbuild.js')
PY

echo "Patch applied. Please run 'bench build' again. If anything goes wrong, restore backups:"
echo "  mv $UTILS_PATH.bak.$TIMESTAMP $UTILS_PATH"
echo "  mv $ESBUILD_PATH.bak.$TIMESTAMP $ESBUILD_PATH"

exit 0
