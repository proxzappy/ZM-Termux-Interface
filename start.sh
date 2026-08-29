#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
else
    echo "[-] Python is required."
    exit 1
fi

chmod +x "$SCRIPT_DIR/hacker-zappy.py" 2>/dev/null || true

exec "$PYTHON_BIN" "$SCRIPT_DIR/hacker-zappy.py"
