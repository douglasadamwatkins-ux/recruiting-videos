# recruiting-videos

[![CI](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/ci.yml/badge.svg)](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/ci.yml) [![Boxscore Analyzer](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/boxscore-analyzer.yml/badge.svg)](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/boxscore-analyzer.yml)

Grayson's Catching and Batting Video archive for recruiting
---

## CI status

- `CI` runs the repository-wide test suite on every push and pull request.
- `Boxscore Analyzer` is a dedicated workflow for the `skills/boxscore_analyzer` package, including parser and integration tests for the box score skill.

These badges reflect the current pass/fail status of each workflow.

# Workspace Skeleton

This repository contains a minimal Python project skeleton created by GitHub Copilot.

Structure:

- README.md - this file
- .gitignore - standard ignores
- src/ - source code
- tests/ - tests (pytest)
- requirements.txt - runtime/test deps
- pyproject.toml - build metadata

Quick start

Install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Run the boxscore analyzer skill locally:

```bash
PYTHONPATH=skills/boxscore_analyzer/src python3 -m boxscore_analyzer.cli path/to/boxscore_image.png
```

Replace `path/to/boxscore_image.png` with the path to your sample image file.
