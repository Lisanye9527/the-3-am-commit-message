#!/usr/bin/env python3
"""Entry program for make.fun contest "The 3 AM Commit Message".

Writes the entry text (a single-line commit message) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt),
deterministically, and verifies the written file by reading it back.
"""

import os
import sys

# Revision 2 (final): close with the model's signature blind spot -- after
# breaking production twice and reverting, its confidence is unchanged.
ENTRY = (
    "fix: at 3 AM I restored production by reverting the fix I wrote at 2 AM "
    "for the fix I wrote at 1 AM. postmortem opened. attendees: me. "
    "action items: also me. confidence: unchanged."
)


def check_gate(text: str) -> None:
    """Self-check the contest gate: UTF-8 text, 1-200 chars, single line."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    encoded = text.encode("utf-8")  # raises if not encodable
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not encoded:
        raise ValueError("entry must not be empty when encoded")


def main() -> int:
    check_gate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY:
        print("verification failed: file contents differ from entry", file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
