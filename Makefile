VENV := .venv
PYTHON ?= python3
PYTHON_WINDOWS ?= py -3

ifeq ($(OS),Windows_NT)
	VENV_PYTHON := $(VENV)\Scripts\python.exe
	VENV_PIP := $(VENV)\Scripts\pip.exe
	VENV_JUPYTER := $(VENV)\Scripts\jupyter.exe
	RM_VENV := if exist $(VENV) rmdir /s /q $(VENV)
	PYTHON_CHECK := $(PYTHON_WINDOWS) --version >NUL 2>NUL
	CREATE_VENV := $(PYTHON_WINDOWS) -m venv $(VENV)
	ACTIVATE_HINT := $(VENV)\Scripts\activate
else
	VENV_PYTHON := $(VENV)/bin/python
	VENV_PIP := $(VENV)/bin/pip
	VENV_JUPYTER := $(VENV)/bin/jupyter
	RM_VENV := rm -rf $(VENV)
	PYTHON_CHECK := command -v $(PYTHON) >/dev/null 2>&1
	CREATE_VENV := $(PYTHON) -m venv $(VENV)
	ACTIVATE_HINT := source $(VENV)/bin/activate
endif

.PHONY: help setup check-python notebook lab start activate lesson clean journey

help:
	@echo "🐢 Py's Python Adventure"
	@echo ""
	@echo "Grown-up first step:"
	@echo "  make setup      Build the safe lesson toolbox in .venv"
	@echo ""
	@echo "Kid-friendly buttons:"
	@echo "  make start      Open the lessons in Jupyter Notebook"
	@echo "  make lesson     Same as make start"
	@echo "  make journey    Show the happy learning path"
	@echo ""
	@echo "Other helpers:"
	@echo "  make lab        Open JupyterLab"
	@echo "  make clean      Remove the local .venv toolbox"

check-python:
ifeq ($(OS),Windows_NT)
	@$(PYTHON_CHECK) || (echo ❌ Python was not found. & echo Please install Python 3.10+ from https://www.python.org/downloads/ & echo IMPORTANT: tick "Add python.exe to PATH" during install. & echo Then open a new terminal and run: make setup & exit /b 1)
else
	@$(PYTHON_CHECK) || { \
		echo "❌ Python 3 was not found."; \
		echo "Please install Python 3.10+ from https://www.python.org/downloads/"; \
		echo "Then open a new terminal and run: make setup"; \
		exit 1; \
	}
endif

setup: check-python
	$(CREATE_VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	@echo ""
	@echo "✅ Setup done!"
	@echo "   Kid start command: make start"
	@echo "   First notebook: lessons/00_welcome/00_welcome.ipynb"

start: notebook

lesson: notebook

notebook:
	$(VENV_JUPYTER) notebook lessons/00_welcome/00_welcome.ipynb

lab:
	$(VENV_JUPYTER) lab lessons

journey:
	@echo "🐢 Student journey"
	@echo "  1. A grown-up runs: make setup"
	@echo "  2. The student runs: make start"
	@echo "  3. Jupyter opens the welcome lesson"
	@echo "  4. Click a cell, press Shift + Enter, and follow Py!"
	@echo "  5. Next lessons live in the lessons/ folder."

activate:
	@echo "Run this in your terminal if a grown-up wants the toolbox shell:"
	@echo "    $(ACTIVATE_HINT)"

clean:
	$(RM_VENV)
ifeq ($(OS),Windows_NT)
	@for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@for /d /r %%d in (.ipynb_checkpoints) do @if exist "%%d" rmdir /s /q "%%d"
else
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
endif
