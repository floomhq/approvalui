"""Core HTML generator and spec validation for ApprovalUI."""

from __future__ import annotations

import html
import json
from typing import Any


class ApprovalUIError(Exception):
    """Raised when the input spec is invalid or generation fails."""


def validate_spec(spec: Any) -> None:
    """Validate that *spec* is a well-formed ApprovalUI JSON spec.

    Raises:
        ApprovalUIError: If the spec is missing required fields or has invalid types.
    """
    if not isinstance(spec, dict):
        raise ApprovalUIError("Spec must be a JSON object.")

    if "title" not in spec:
        raise ApprovalUIError("Spec is missing required field: title.")
    if not isinstance(spec["title"], str):
        raise ApprovalUIError("Spec field 'title' must be a string.")

    instructions = spec.get("instructions", "")
    if instructions and not isinstance(instructions, str):
        raise ApprovalUIError("Spec field 'instructions' must be a string.")

    if "items" not in spec:
        raise ApprovalUIError("Spec is missing required field: items.")
    if not isinstance(spec["items"], list):
        raise ApprovalUIError("Spec field 'items' must be a list.")
    if not spec["items"]:
        raise ApprovalUIError("Spec field 'items' must contain at least one item.")

    for idx, item in enumerate(spec["items"]):
        if not isinstance(item, dict):
            raise ApprovalUIError(f"Item {idx} must be an object.")
        if "id" not in item:
            raise ApprovalUIError(f"Item {idx} is missing required field: id.")
        if not isinstance(item["id"], (str, int)):
            raise ApprovalUIError(f"Item {idx} field 'id' must be a string or integer.")
        if "title" not in item:
            raise ApprovalUIError(f"Item {idx} is missing required field: title.")
        if not isinstance(item["title"], str):
            raise ApprovalUIError(f"Item {idx} field 'title' must be a string.")

        for optional in ("status", "root_cause", "screenshot"):
            value = item.get(optional)
            if value is not None and not isinstance(value, str):
                raise ApprovalUIError(
                    f"Item {idx} field '{optional}' must be a string if provided."
                )


def _escape(text: Any) -> str:
    """Return an HTML-escaped string representation of *text*."""
    return html.escape(str(text))


def render(spec: dict[str, Any]) -> str:
    """Render a self-contained HTML approval page from *spec*.

    Args:
        spec: A dictionary conforming to the ApprovalUI JSON spec format.

    Returns:
        A complete HTML document as a string.

    Raises:
        ApprovalUIError: If the spec is invalid.
    """
    validate_spec(spec)

    title = _escape(spec.get("title", "Approval"))
    instructions = _escape(spec.get("instructions", "Review each item and generate the review."))
    items = spec["items"]

    item_html: list[str] = []
    for item in items:
        item_id = _escape(item["id"])
        item_title = _escape(item["title"])
        root_cause = _escape(item.get("root_cause", ""))
        screenshot = _escape(item.get("screenshot", ""))
        screenshot_tag = (
            f'<img src="{screenshot}" alt="screenshot" class="screenshot" />' if screenshot else ""
        )

        item_html.append(
            f"""
        <div class="item" data-id="{item_id}">
            <div class="header">
                <label><input type="radio" name="status-{item_id}" value="approve" /> Approve</label>
                <label><input type="radio" name="status-{item_id}" value="reject" checked /> Reject</label>
                <strong>#{item_id} — {item_title}</strong>
            </div>
            <div class="body">
                {screenshot_tag}
                <p>{root_cause}</p>
                <textarea class="comment" placeholder="Comment if rejecting..."></textarea>
            </div>
        </div>
        """
        )

    items_json = json.dumps(
        [{"id": str(item["id"]), "title": str(item["title"])} for item in items]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 40px 20px; background: #fafafa; color: #111; }}
        h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .subtitle {{ color: #666; margin-bottom: 32px; }}
        .item {{ background: #fff; border: 1px solid #e5e5e5; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
        .header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 12px; flex-wrap: wrap; }}
        .header label {{ cursor: pointer; font-size: 14px; }}
        .header input {{ margin-right: 6px; }}
        .header strong {{ font-size: 16px; }}
        .body p {{ color: #444; line-height: 1.5; margin: 0 0 12px; }}
        .screenshot {{ max-width: 100%; border-radius: 8px; border: 1px solid #eee; margin-bottom: 12px; }}
        textarea {{ width: 100%; min-height: 80px; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; box-sizing: border-box; }}
        .actions {{ display: flex; gap: 12px; margin-top: 24px; align-items: center; flex-wrap: wrap; }}
        button {{ padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }}
        .primary {{ background: #111; color: #fff; }}
        .secondary {{ background: #fff; color: #111; border: 1px solid #111; }}
        pre {{ background: #f4f4f4; padding: 16px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; word-break: break-word; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p class="subtitle">{instructions}</p>

    {"".join(item_html)}

    <div class="actions">
        <button class="primary" onclick="generateReview()">Generate review →</button>
        <button class="secondary" onclick="copyReview()">Copy</button>
    </div>

    <h3>Review</h3>
    <pre id="review">Tick items and click Generate review.</pre>

    <script>
        const items = {items_json};

        function generateReview() {{
            const lines = [];
            items.forEach(item => {{
                const statusEl = document.querySelector(`input[name="status-${{item.id}}"]:checked`);
                const commentEl = document.querySelector(`.item[data-id="${{item.id}}"] textarea`);
                const status = statusEl ? statusEl.value.toUpperCase() : "REJECT";
                const comment = commentEl ? commentEl.value.trim() : "";
                let line = `[${{status}}] #${{item.id}} — ${{item.title}}`;
                if (status === "REJECT" && comment) {{
                    line += ` — comment: ${{comment}}`;
                }}
                lines.push(line);
            }});
            document.getElementById("review").textContent = lines.join("\\n");
        }}

        function copyReview() {{
            const text = document.getElementById("review").textContent;
            navigator.clipboard.writeText(text).then(() => alert("Copied."));
        }}
    </script>
</body>
</html>"""
