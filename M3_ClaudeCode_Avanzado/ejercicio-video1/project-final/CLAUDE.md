# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Flask REST API demo for managing Rebel Alliance operations. Stack: Python 3.x, Flask, SQLite (file `rebel_ops.db`), pytest.

## Commands

```bash
# Activate virtual environment (required before running anything)
source .venv/bin/activate

# Run the development server
python demo.py

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run a single test
pytest tests/test_app.py::test_function_name -v

# Run tests with coverage
pytest tests/ --cov=demo --cov-report=term-missing
```

## Architecture

- `demo.py` — all Flask routes and DB logic in one file; no ORM, raw `sqlite3` queries
- `tests/test_app.py` — integration tests using Flask's test client
- SQLite database `rebel_ops.db` is created at runtime; schema must be initialized before first use

## Code conventions

- Route functions named `verb_resource` (e.g. `get_missions`, `post_mission`)
- All responses are JSON: `{"data": ..., "error": null}` on success, `{"data": null, "error": "..."}` on failure
- HTTP error codes: 400 invalid input, 401 auth failure, 404 not found, 500 server error
- Any new endpoint must include authentication validation (header `X-API-KEY`)
- Never log mission data in plain text

## Notes on `.claude/CLAUDE.md`

The project-level instructions in `.claude/CLAUDE.md` reference `app.py` and `config.py` — these files do not exist. The actual entry point is `demo.py`. Update `.claude/CLAUDE.md` if the project structure evolves.
