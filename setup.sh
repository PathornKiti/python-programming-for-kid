#!/usr/bin/env bash
# Optional grown-up helper for macOS / Linux.
# It never installs Python or system tools. It only checks what is present,
# then delegates the project setup to `make setup`.
set -e

say()  { printf "\n\033[1m%s\033[0m\n" "$1"; }
ok()   { printf "  \033[32m✅ %s\033[0m\n" "$1"; }
warn() { printf "  \033[33m⚠️  %s\033[0m\n" "$1"; }

say "🐢 Py's Python Adventure — setup checker"

if command -v python3 >/dev/null 2>&1; then
  ok "Python is ready ($(python3 --version))"
else
  warn "Python 3 was not found."
  echo "  Please install Python 3.10+ from https://www.python.org/downloads/"
  echo "  Then open a new terminal in this folder and run: make setup"
  exit 1
fi

if command -v make >/dev/null 2>&1; then
  ok "make is ready"
else
  warn "make was not found."
  echo "  On macOS, install Apple's Command Line Tools if Terminal asks for them."
  echo "  Then run these commands from this folder:"
  echo "    python3 -m venv .venv"
  echo "    .venv/bin/python -m pip install --upgrade pip"
  echo "    .venv/bin/pip install -r requirements.txt"
  echo "    .venv/bin/jupyter notebook lessons"
  exit 1
fi

say "Building the lesson toolbox with make setup…"
make setup

say "🎉 All done!"
echo "  Student start command: make start"
