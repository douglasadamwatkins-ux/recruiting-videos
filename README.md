# recruiting-videos

[![CI](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/ci.yml/badge.svg)](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/ci.yml) [![Boxscore Analyzer](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/boxscore-analyzer.yml/badge.svg)](https://github.com/douglasadamwatkins-ux/recruiting-videos/actions/workflows/boxscore-analyzer.yml)

Grayson's Catching and Batting Video archive for recruiting
---

## CI status

- `CI` runs the repository-wide test suite on every push and pull request.
- `Boxscore Analyzer` is the dedicated workflow for the `skills/boxscore_analyzer` package, including parser and integration tests for the box score skill.

These badges reflect the current pass/fail status of each workflow.

# Workspace Skeleton

This repository contains a minimal Python project skeleton with a dedicated `boxscore_analyzer` skill package.

Structure:

- `README.md` - this file
- `.gitignore` - standard ignores
- `requirements.txt` - runtime/test dependencies
- `pyproject.toml` - build metadata
- `skills/boxscore_analyzer/` - dedicated skill package with parser, OCR, stats, CLI, and tests

Quick start

Install requirements and editable skill package:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pip install -e skills/boxscore_analyzer
```

Run tests:

```bash
pytest
```

Run the boxscore analyzer skill locally:

```bash
python3 -m boxscore_analyzer.cli path/to/boxscore_image.png
```

Replace `path/to/boxscore_image.png` with the path to your sample image file.
