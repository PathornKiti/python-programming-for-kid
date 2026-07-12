VENV := .venv
PYTHON := python3

.PHONY: setup activate notebook lab clean

setup:
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
