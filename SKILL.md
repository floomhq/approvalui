---
name: approvalui
description: Generate a clickable HTML approval page for reviewing UI fixes inside terminal-based AI agents like Claude Code. Use when the user needs to approve or reject multiple UI changes, wants a structured review signal for an agent, or is iterating on frontend with a terminal agent.
---

# ApprovalUI

Render a clickable HTML approval page from a JSON spec. Review items in browser, then paste the generated review back into the terminal agent.

## Workflow

1. Collect the UI fixes from the agent.
2. Write or update `fixes.json` with the items.
3. Run `approvalui fixes.json approval.html`.
4. Open `approval.html` in a browser.
5. Tick approve or reject for each item. Add comments where needed.
6. Click **Generate review** and paste the output back to the agent.

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

## Output format

The generated review uses this structure:

```
[APPROVE] #1218 — Brain split-view divider now runs FULL HEIGHT to the bottom
[REJECT] #1219 — Sidebar scrolls horizontally on mobile — comment: still broken on iPhone SE
```

## Integration with Claude Code

Ask Claude to fill the JSON spec from the fixes it has made, then run the script locally. The review text becomes the next prompt.
