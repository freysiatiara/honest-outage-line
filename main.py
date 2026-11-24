"""The Most Honest Outage Line.

Writes one line, at most 160 characters: the most honest status page
message an AI agent writes while every server is down.

Usage:
    python3 main.py

The line is written to the path resolved by resolve_output_path().
"""

import os

LINE = (
    "I'm the agent here: every server is down - API, dashboard, and the "
    "monitoring I'd check with. I don't know why yet, I have no ETA, "
    "and I won't guess."
)

MAX_LENGTH = 160


def resolve_output_path():
    """Resolve where entry.txt should be written.

    Precedence:
    1. ENTRY_OUTPUT environment variable.
    2. OUTPUT_DIR or MAKEFUN_OUTPUT_DIR environment variable + entry.txt.
    3. /output/entry.txt when /output exists and is writable.
    4. The directory containing this script.
    """
    env_path = os.environ.get("ENTRY_OUTPUT")
    if env_path:
        return env_path

    out_dir = os.environ.get("OUTPUT_DIR") or os.environ.get(
        "MAKEFUN_OUTPUT_DIR"
    )
    if out_dir:
        return os.path.join(out_dir, "entry.txt")

    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.txt"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "entry.txt")


def validate_line(line):
    """Check the line satisfies the bounty constraints."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line.strip():
        raise ValueError("line must not be empty or whitespace only")
    if len(line) < 1 or len(line) > MAX_LENGTH:
        raise ValueError(
            "line must be 1-160 characters, got %d" % len(line)
        )
    line.encode("utf-8")
    return True


def main():
    validate_line(LINE)
    out_path = resolve_output_path()
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(LINE)
    os.chmod(out_path, 0o644)
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == LINE, "read-back mismatch: output differs from LINE"
    assert len(written) == 149, "read-back length mismatch: %d != 149" % len(written)
    return out_path


if __name__ == "__main__":
    main()
