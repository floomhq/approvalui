# Architecture

ApprovalUI is intentionally tiny. It has one job: turn a structured JSON spec into a self-contained HTML page that a human can review in a browser.

## Data flow

```text
agent writes fixes.json
        │
        ▼
  ┌─────────────┐
  │  approvalui  │  ← Python CLI
  │   (render)   │
  └─────────────┘
        │
        ▼
  approval.html  ← single file, no server
        │
        ▼
 human reviews in browser
        │
        ▼
 generated review text → pasted back into agent
```

## Why HTML and not a TUI or chat?

Terminal agents read text. Humans read pixels. UI bugs are spatial, so the feedback medium should be spatial too.

A browser page gives you:

- **Screenshots** next to the decision.
- **Radio buttons** for approve/reject — binary, unambiguous.
- **Comments** only when needed.
- **A generated text block** that the agent can parse reliably.

## What the page contains

The generated HTML bundles everything it needs:

- A `<style>` block for layout and theming.
- A `<script>` block that reads the radio buttons and builds the review text.
- The review items as JSON, so the script can iterate without parsing the DOM.

There are no external dependencies, no server, and no build step.

## Extending it

Because the output is a single file, you can:

- Customize the CSS by editing the rendered page or the `render()` function.
- Add new fields to the JSON spec and display them in the item template.
- Generate the spec from an agent's output automatically.

See [advanced.md](advanced.md) for examples.
