#!/usr/bin/env bash
# One-time setup for Py's Python Adventure (macOS / Linux).
#
# A grown-up runs this ONCE on a new computer. It:
#   1. Checks whether Python is installed (and helps install it if not).
#   2. Makes sure `make` is available.
#   3. Builds the .venv virtual environment and installs the lesson tools.
#   4. Offers to open the lessons right away.
#
# Usage:  ./setup.sh
set -e

say()  { printf "\n\033[1m%s\033[0m\n" "$1"; }
ok()   { printf "  \033[32m✅ %s\033[0m\n" "$1"; }
warn() { printf "  \033[33m⚠️  %s\033[0m\n" "$1"; }

say "🐢 Py's Python Adventure — setup"

OS="$(uname -s)"

# --------------------------------------------------------------- 1. Python
if command -v python3 >/dev/null 2>&1; then
  ok "Python is already installed ($(python3 --version))"
else
  warn "Python is not installed on this computer."
  if [ "$OS" = "Darwin" ]; then
    # macOS: install via Homebrew.
    if ! command -v brew >/dev/null 2>&1; then
      if [ -t 0 ]; then
        printf "  Install Homebrew (the tool that installs Mac software)? [Y/n] "
        read -r reply
        case "$reply" in
          [Nn]*)
            echo "  No problem — install Python yourself from https://www.python.org/downloads/"
            echo "  then run ./setup.sh again."
            exit 1 ;;
        esac
        say "Installing Homebrew…"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      else
        echo "  Please install Python from https://www.python.org/downloads/ then re-run ./setup.sh"
        exit 1
      fi
    fi
    say "Installing Python with Homebrew…"
    brew install python
  else
    # Linux
    warn "Please install Python 3 with your package manager, for example:"
    echo "    sudo apt update && sudo apt install -y python3 python3-venv python3-pip"
    echo "  Then run ./setup.sh again."
    exit 1
  fi
  ok "Python installed ($(python3 --version))"
fi

# ----------------------------------------------------------------- 2. make
if command -v make >/dev/null 2>&1; then
  ok "make is already installed"
else
  warn "make is not installed."
  if [ "$OS" = "Darwin" ]; then
    say "Installing Apple Command Line Tools (this includes make)…"
    xcode-select --install || true
    echo "  A little window may pop up — finish that install, then run ./setup.sh again."
    exit 1
  else
    echo "    sudo apt install -y make"
    echo "  Then run ./setup.sh again."
    exit 1
  fi
fi

# -------------------------------------------------------- 3. venv + tools
say "Building the virtual environment (.venv) and installing the lesson tools…"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
ok "All the lesson tools are installed!"

# ------------------------------------------------------------- 4. all done
say "🎉 All done!"
echo "  To start the lessons at any time, run:   make notebook"
echo "  (or activate the venv yourself with:     source .venv/bin/activate )"

if [ -t 0 ]; then
  printf "\n  Open the lessons now? [Y/n] "
  read -r reply
  case "$reply" in
    [Nn]*) echo "  Okay! Run 'make notebook' whenever you're ready." ;;
    *)     exec .venv/bin/jupyter notebook ;;
  esac
fi
