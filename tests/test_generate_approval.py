"""Tests for approvalui."""

import json
import subprocess
import sys
from pathlib import Path

import approvalui


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


def test_render_includes_title_and_instructions():
    html = approvalui.render(SAMPLE_SPEC)
    assert "<title>Test Approval</title>" in html
    assert "Tick the boxes." in html


def test_render_includes_items():
    html = approvalui.render(SAMPLE_SPEC)
    assert "Fix the divider" in html
    assert "Fix the header" in html
    assert "min-height collapsed the flex child" in html


def test_render_includes_screenshot():
    html = approvalui.render(SAMPLE_SPEC)
    assert '<img src="divider.png" alt="screenshot"' in html


def test_render_handles_missing_optional_fields():
    spec = {
        "title": "Minimal",
        "items": [{"id": 1, "title": "Only required fields"}],
    }
    html = approvalui.render(spec)
    assert "Only required fields" in html
    assert '"id": 1' in html  # referenced in JS items list


def test_render_escapes_html_in_spec():
    spec = {
        "title": "<script>alert(1)</script>",
        "items": [
            {"id": 1, "title": '<img src=x onerror="alert(1)">'}
        ],
    }
    html = approvalui.render(spec)
    # Title and item text must be escaped in the HTML body/head.
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;' in html


def test_cli_generates_html(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    out_path = tmp_path / "approval.html"
    spec_path.write_text(json.dumps(SAMPLE_SPEC))

    result = subprocess.run(
        [sys.executable, "approvalui.py", str(spec_path), str(out_path)],
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert out_path.exists()
    assert "Fix the divider" in out_path.read_text()
