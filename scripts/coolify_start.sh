#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

# App modules import `config` as a top-level module from repo_root/app.
export PYTHONPATH="${ROOT_DIR}/app:${PYTHONPATH:-}"

PY_BIN="python"
if ! command -v python >/dev/null 2>&1; then
  PY_BIN="python3"
fi

# Keep startup simple for production: init local data files, then parse.
"${PY_BIN}" - <<'PY'
from main import make_dirs_and_files
from parse import parse

make_dirs_and_files()
parse()
PY

if "${PY_BIN}" -c "import gunicorn" >/dev/null 2>&1; then
  exec "${PY_BIN}" -m gunicorn \
    --chdir app \
    --bind "0.0.0.0:${PORT:-5000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --threads "${GUNICORN_THREADS:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    web:app
fi

echo "gunicorn not found; falling back to Flask dev server"
exec "${PY_BIN}" app/web.py
