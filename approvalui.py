#!/usr/bin/env python3
"""Generate a self-contained HTML approval page from a JSON spec."""

import argparse
import json
import html
from pathlib import Path


def escape(text: str) -> str:
    return html.escape(str(text))


def render(spec: dict) -> str:
    title = escape(spec.get("title", "Approval"))
    instructions = escape(spec.get("instructions", "Review each item and generate the review."))
    items = spec.get("items", [])

    item_html = []
    for item in items:
        item_id = escape(item.get("id", ""))
        item_title = escape(item.get("title", ""))
        root_cause = escape(item.get("root_cause", ""))
        screenshot = escape(item.get("screenshot", ""))
        screenshot_tag = f'<img src="{screenshot}" alt="screenshot" class="screenshot" />' if screenshot else ""

        item_html.append(f"""
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
        """)

    items_json = json.dumps([{"id": i.get("id", ""), "title": i.get("title", "")} for i in items])

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

    {''.join(item_html)}

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


def main():
    parser = argparse.ArgumentParser(description="Generate an HTML approval page from a JSON spec.")
    parser.add_argument("input", help="Path to JSON spec")
    parser.add_argument("output", help="Path to write HTML file")
    args = parser.parse_args()

    spec = json.loads(Path(args.input).read_text())
    html_output = render(spec)
    Path(args.output).write_text(html_output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
