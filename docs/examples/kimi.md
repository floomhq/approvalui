# Using ApprovalUI with Kimi

## 1. Ask Kimi to write the spec

```text
I want to review the UI fixes in a browser. Create a fixes.json file for
approvalui with all the changes you just made.
```

## 2. Render the page

Kimi can run the CLI:

```bash
approvalui fixes.json approval.html
```

## 3. Open the page

```bash
open approval.html
```

## 4. Paste the generated review

After clicking **Generate review**, paste the text back into the Kimi session:

```text
Review:
[APPROVE] #1218 — Brain split-view divider now runs FULL HEIGHT to the bottom
[REJECT] #1219 — Sidebar scrolls horizontally on mobile — comment: still broken on iPhone SE
```

Kimi will act on the binary signal instead of guessing from text descriptions.
