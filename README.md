# ApprovalUI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)
[![Tests](https://github.com/floomhq/approvalui/actions/workflows/ci.yml/badge.svg)](https://github.com/floomhq/approvalui/actions)

A tiny open-source loop for reviewing UI fixes inside terminal-based AI agents.

Terminal agents are great for code. They are bad at UI feedback, because UI feedback needs eyes, not paragraphs.

ApprovalUI renders a clickable HTML approval page from a simple JSON spec. You open it in a browser, tick approve or reject per item, generate a review, and paste it back into the agent.

Binary signal. Screenshot attached. No drift.

---

## Why

When you iterate on frontend with a terminal agent, the feedback loop is verbal:

> “The divider looks weird — can you make it full height?”

The agent reads text, not pixels. You end up describing the same fix five times.

ApprovalUI short-circuits that loop. The agent writes a structured spec of the fixes, you review them visually, and the page gives you a structured text block to paste back.

Works with Claude Code, Codex, Kimi, or any terminal agent that can write JSON and open a browser.

---

## How it works

1. The agent writes a JSON spec describing each UI fix: title, issue number, screenshot, root cause.
2. `approvalui` turns the spec into a self-contained HTML page.
3. You open the page, review each item, tick **Approve** or **Reject**, add comments.
4. Click **Generate review** to get a structured text block you paste back into the agent.

---

## Install

```bash
pip install approvalui
```

Or clone and install in editable mode:

```bash
git clone https://github.com/floomhq/approvalui.git
cd approvalui
pip install -e ".[dev]"
```

---

## Quick start

```bash
approvalui example/fixes.json example/approval.html
open example/approval.html
```

Tick approve or reject, add a comment, and click **Generate review**.

---

## JSON spec format

```json
{
  "title": "Workeros — Fix Approval",
  "instructions": "Tick the ones you approve, click Generate review, paste it back to me.",
  "items": [
    {
      "id": 1218,
      "title": "Brain split-view divider now runs FULL HEIGHT to the bottom",
      "status": "pending",
      "root_cause": "wrapper used min-h-full so Collection height:100% could not resolve",
      "screenshot": "screenshot.svg"
    }
  ]
}
```

Only `id` and `title` are required. `root_cause`, `screenshot`, and `instructions` are optional.

---

## Generated review format

```text
[APPROVE] #1218 — Brain split-view divider now runs FULL HEIGHT to the bottom
[REJECT] #1219 — Sidebar scrolls horizontally on mobile — comment: still broken on iPhone SE
```

---

## Files

- `approvalui.py` — CLI that turns JSON into HTML.
- `example/` — sample spec, screenshot, and generated page.
- `SKILL.md` — Floom skill instructions for agent integration.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT. See [LICENSE](LICENSE).
