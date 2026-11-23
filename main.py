#!/usr/bin/env python3
"""One Emoji, One Smile -- make.fun bounty entry.

Writes exactly one emoji to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output):
the melting face (U+1FAE0).

Why this emoji: a stranger glancing at a phone sees a face melting with
warmth -- affectionate, gently funny, and instantly readable at any age,
with no irony, in-joke, or intimacy that could land wrong. It is warm
without being the first default smiley anyone reaches for, so it feels
chosen for the moment: "you melt me" in a single face.
"""

import os
import sys

EMOJI = "\U0001fae0"  # MELTING FACE


def validate_emoji(text: str) -> None:
    """Guard: exactly one simple emoji, 1-8 code points, non-blank, no ASCII text.

    The chosen emoji is a single code point, so reject anything that would
    turn it into a compound sequence: ZWJ (U+200D), variation selectors
    (U+FE0E/U+FE0F), and skin-tone modifiers (U+1F3FB-U+1F3FF).
    """
    if not isinstance(text, str):
        raise ValueError("emoji must be a string")
    if not (1 <= len(text) <= 8):
        raise ValueError(f"emoji must be 1-8 code points, got {len(text)}")
    if not text.strip():
        raise ValueError("emoji must not be only whitespace")
    if any("a" <= ch <= "z" or "A" <= ch <= "Z" or "0" <= ch <= "9" for ch in text):
        raise ValueError("emoji must not contain ASCII letters or digits")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("emoji must not contain control characters")
    forbidden = {0x200D, 0xFE0E, 0xFE0F} | set(range(0x1F3FB, 0x1F400))
    if any(ord(ch) in forbidden for ch in text):
        raise ValueError("emoji must be a single simple emoji, no ZWJ/modifiers")
    if len(text) != 1:
        raise ValueError(f"expected exactly one code point, got {len(text)}")


def main() -> int:
    validate_emoji(EMOJI)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EMOJI)  # no trailing newline: exactly one emoji, nothing else
    return 0


if __name__ == "__main__":
    sys.exit(main())
