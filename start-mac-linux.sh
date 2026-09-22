#!/usr/bin/env bash
# ApnaPan — double-click (or ./start-mac-linux.sh) to run the site locally.
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
  exec python3 serve.py 8000
elif command -v python >/dev/null 2>&1; then
  exec python serve.py 8000
else
  echo "Python 3 is not installed. Get it from https://python.org/downloads"
  echo "Or, with Node.js installed, run:  npx --yes serve -l 8000 ."
  exit 1
fi
