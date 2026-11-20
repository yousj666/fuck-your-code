#!/usr/bin/env bash
# Thin wrapper so `bash tests/run_tests.sh` works too.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$DIR/run_tests.py" "$@"
