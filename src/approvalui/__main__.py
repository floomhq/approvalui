"""Allow running ApprovalUI as a module: python -m approvalui."""

from __future__ import annotations

import sys

from approvalui.cli import main

if __name__ == "__main__":
    sys.exit(main())
