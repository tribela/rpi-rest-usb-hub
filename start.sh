#!/usr/bin/env bash
set -eo pipefail

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

source .venv/bin/activate

exec uvicorn --host 0.0.0.0 --port 8000 --reload --log-level info app:app
