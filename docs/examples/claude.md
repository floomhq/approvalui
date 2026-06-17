# Using ApprovalUI with Claude Code

## 1. Ask Claude to describe the fixes as JSON

```text
I just shipped three UI fixes. Write an approvalui fixes.json spec for them
so I can review in browser. Include issue numbers, a one-line title each,
root cause, and the screenshot path.
```

## 2. Run ApprovalUI

Claude can run it directly:

```bash
approvalui fixes.json approval.html
open approval.html
```

## 3. Review in browser

Tick **Approve** or **Reject** for each fix, add comments, then click **Generate review**.

## 4. Paste the review back

Copy the generated text block and paste it into Claude Code:

```text
[APPROVE] #1218 — Brain split-view divider now runs FULL HEIGHT to the bottom
[REJECT] #1219 — Sidebar scrolls horizontally on mobile — comment: still broken on iPhone SE
```

Claude can then close approved issues and re-open rejected ones.
