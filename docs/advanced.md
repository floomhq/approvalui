# Advanced usage

## Custom styling

The generated HTML uses a single `<style>` block. You can override styles by editing `src/approvalui/_core.py` or by post-processing the output.

For example, to make the page wider:

```python
html = render(spec)
html = html.replace("max-width: 900px", "max-width: 1200px")
Path("approval.html").write_text(html)
```

## Programmatic usage

Import and call `render()` directly:

```python
from approvalui import render

spec = {
    "title": "My Fixes",
    "items": [
        {"id": 1, "title": "Fix the header", "root_cause": "padding issue"},
    ],
}

html = render(spec)
Path("approval.html").write_text(html)
```

## Embedding in an agent workflow

A terminal agent can:

1. Collect the UI fixes it made.
2. Write `fixes.json`.
3. Shell out to `approvalui fixes.json approval.html`.
4. Ask the user to open `approval.html`.
5. Paste the user's generated review back into the chat.

Because the review text is deterministic, the agent can close approved issues automatically and re-open rejected ones.

## Adding fields to items

The spec accepts arbitrary string fields. If you add a new field, display it in the item template in `_core.py`:

```python
priority = _escape(item.get("priority", ""))
```

Then include it in the HTML body.
