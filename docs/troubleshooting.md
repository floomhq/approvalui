# Troubleshooting

## `approvalui` command not found

Install the package:

```bash
pip install approvalui
```

Or, if running from the repo:

```bash
pip install -e ".[dev]"
```

## Screenshot does not show up

The `"screenshot"` path in the JSON spec is passed directly to the `<img src>` attribute. Make sure the path is relative to the generated HTML file or an absolute URL.

```json
{
  "screenshot": "screenshot.png"
}
```

## Generated page is blank

Open the browser console and check for JavaScript errors. The most common cause is an invalid `items` structure. Run `approvalui` from the command line — it validates the spec and prints a clear error.

## Validation errors

ApprovalUI requires:

- A top-level `title` string.
- A top-level `items` list with at least one object.
- Each item must have an `id` (string or integer) and a `title` (string).

Optional fields must be strings if provided.
