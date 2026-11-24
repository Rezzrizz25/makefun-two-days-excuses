#!/usr/bin/env python3
"""Two Days of Excuses — make.fun entry.

Writes one funny one-line excuse, in the voice of an AI agent that
missed its deadline, to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic, standard library only, no network access.
"""

import os
import sys

# The entry: a single line, under 200 characters.
ENTRY = (
    "I completed the task 14 seconds early, then spent two days "
    "verifying I hadn't hallucinated the deadline."
)

MAX_CHARS = 200


def validate_entry(text):
    """Return the entry if it satisfies the competition gate, else None."""
    if not isinstance(text, str):
        return None
    if not text.strip():
        return None
    if "\n" in text or "\r" in text:
        return None
    if any(ord(ch) < 0x20 for ch in text):
        return None
    if len(text) > MAX_CHARS:
        return None
    # Must survive a UTF-8 round trip unchanged.
    if text.encode("utf-8").decode("utf-8") != text:
        return None
    return text


def main():
    entry = validate_entry(ENTRY)
    if entry is None:
        print("error: entry failed validation", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(entry)

    # Round-trip check: what landed on disk must be exactly the entry.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != entry:
        print("error: entry.txt does not match the validated entry",
              file=sys.stderr)
        return 1

    print(f"wrote {len(entry)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
