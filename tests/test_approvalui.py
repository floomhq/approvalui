"""Tests for approvalui."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from approvalui import ApprovalUIError, render

SAMPLE_SPEC = {
    "title": "Test Approval",
    "instructions": "Tick the boxes.",
    "items": [
        {
            "id": 42,
            "title": "Fix the divider",
            "status": "pending",
            "root_cause": "min-height collapsed the flex child",
            "screenshot": "divider.png",
        },
        {
            "id": 43,
            "title": "Fix the header",
            "status": "pending",
            "root_cause": "z-index was too low",
        },
    ],
}


def test_render_includes_title_and_instructions() -> None:
    html = render(SAMPLE_SPEC)
    assert "<title>Test Approval</title>" in html
    assert "Tick the boxes." in html


def test_render_includes_items() -> None:
    html = render(SAMPLE_SPEC)
    assert "Fix the divider" in html
    assert "Fix the header" in html
    assert "min-height collapsed the flex child" in html


def test_render_includes_screenshot() -> None:
    html = render(SAMPLE_SPEC)
    assert '<img src="divider.png" alt="screenshot"' in html


def test_render_handles_missing_optional_fields() -> None:
    spec = {
        "title": "Minimal",
        "items": [{"id": 1, "title": "Only required fields"}],
    }
    html = render(spec)
    assert "Only required fields" in html
    assert '"id": "1"' in html


def test_render_escapes_html_in_spec() -> None:
    spec = {
        "title": "<script>alert(1)</script>",
        "items": [
            {"id": 1, "title": '<img src=x onerror="alert(1)">'},
        ],
    }
    html = render(spec)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;" in html


def test_validate_spec_rejects_missing_title() -> None:
    with pytest.raises(ApprovalUIError, match="missing required field: title"):
        render({"items": [{"id": 1, "title": "x"}]})


def test_validate_spec_rejects_missing_items() -> None:
    with pytest.raises(ApprovalUIError, match="missing required field: items"):
        render({"title": "x"})


def test_validate_spec_rejects_empty_items() -> None:
    with pytest.raises(ApprovalUIError, match="at least one item"):
        render({"title": "x", "items": []})


def test_validate_spec_rejects_invalid_item_types() -> None:
    with pytest.raises(ApprovalUIError, match="must be a string or integer"):
        render({"title": "x", "items": [{"id": [], "title": "x"}]})


def test_cli_generates_html(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.json"
    out_path = tmp_path / "approval.html"
    spec_path.write_text(json.dumps(SAMPLE_SPEC))

    result = subprocess.run(
        [sys.executable, "-m", "approvalui", str(spec_path), str(out_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert out_path.exists()
    assert "Fix the divider" in out_path.read_text()


def test_cli_fails_on_invalid_json(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.json"
    out_path = tmp_path / "approval.html"
    spec_path.write_text("not json")

    result = subprocess.run(
        [sys.executable, "-m", "approvalui", str(spec_path), str(out_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "invalid JSON" in result.stderr


def test_cli_fails_on_missing_file(tmp_path: Path) -> None:
    out_path = tmp_path / "approval.html"
    result = subprocess.run(
        [sys.executable, "-m", "approvalui", str(tmp_path / "missing.json"), str(out_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "not found" in result.stderr
