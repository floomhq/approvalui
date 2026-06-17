# Using ApprovalUI with Codex

## 1. Ask Codex to generate the spec

```text
I need to review the UI fixes you just made. Output a JSON file called
fixes.json in the approvalui format: title, instructions, and items with
id, title, root_cause, and screenshot.
```

## 2. Generate the approval page

```bash
approvalui fixes.json approval.html
```

## 3. Open and review

```bash
open approval.html
```

Use the radio buttons to approve or reject each item. Add a comment for anything rejected.

## 4. Feed the review back to Codex

Paste the generated review text into the next prompt:

```text
Here is my review. Please close the approved fixes and fix the rejected ones.

[APPROVE] #1218 — Brain split-view divider now runs FULL HEIGHT to the bottom
[REJECT] #1219 — Sidebar scrolls horizontally on mobile — comment: still broken on iPhone SE
```
