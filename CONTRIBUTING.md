# Contributing

Thanks for helping make Agent UI Approval better.

## Quick start

1. Fork the repo and clone your fork.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run the tests:
   ```bash
   pytest
   ```

## What to contribute

- Bug fixes for JSON parsing or HTML generation.
- Tests for edge cases in the spec format.
- Documentation improvements.
- UI/UX improvements to the generated approval page.

## Guidelines

- Keep the tool small and focused.
- Add tests for any new behavior.
- Update the README if you change the JSON spec or CLI.
- One logical change per pull request.

## Reporting issues

Open an issue with:
- The command you ran.
- The input JSON (or a minimal version of it).
- What you expected vs. what happened.
