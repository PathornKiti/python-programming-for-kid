VENV := .venv
PYTHON := python3

.PHONY: setup check-python activate notebook lab clean

# `make` itself can't be installed by make, and neither can Python — so the
# very first cold-start step lives in ./setup.sh (macOS/Linux) or setup.bat
# (Windows). This just checks Python is present and points there if not.
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "❌ Python not found."; \
		echo "   Run ./setup.sh  (macOS/Linux)  or  setup.bat  (Windows) first —"; \
		echo "   it installs Python for you, then finishes this setup."; \
		exit 1; \
	}

setup: check-python
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	@echo ""
	@echo "✅ Setup done!"
	@echo "   Start the lessons with:   make notebook"
	@echo "   Or activate the venv with: source $(VENV)/bin/activate"

# `make` runs each recipe in its own subshell, so it cannot activate the venv
# in your shell for you. This just prints the exact command to copy.
activate:
	@echo "Run this in your terminal (make can't do it for you):"
	@echo "    source $(VENV)/bin/activate"

# Launch Jupyter straight from the venv -- no manual activation needed.
notebook:
	$(VENV)/bin/jupyter notebook

lab:
	$(VENV)/bin/jupyter lab

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
