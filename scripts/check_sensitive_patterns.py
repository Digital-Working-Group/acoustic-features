#!/usr/bin/env python
"""Pre-commit hook: block staged commits that contain organization-specific
sensitive identifiers (e.g. participant IDs).

detect-secrets recognizes the shape of credentials (base64/hex entropy,
known token prefixes) but has no concept of what a participant ID looks
like, so that gap needs an explicit, editable rule maintained here.
"""
import re
import subprocess
import sys

# Participant IDs: a single digit, a dash, then 3-5 digits (e.g. "1-234", "7-12345").  # pragma: allowlist secret
PARTICIPANT_ID_PATTERN = re.compile(r"\b\d-\d{3,5}\b")

SENSITIVE_PATTERNS = {
    "participant ID": PARTICIPANT_ID_PATTERN,
}

# De-identified sample/reference data that is intentionally checked in and may
# incidentally match one of the patterns above (e.g. numeric IDs in generated
# output filenames or data dictionaries).
EXEMPT_PATHS = (
    "sample_audio/",
    "opensmile/data_dictionaries/",
    "opensmile/comparison/",
    "opensmile/output/",
    "librosa/output/",
)

PRAGMA = "pragma: allowlist secret"


def get_staged_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f for f in result.stdout.splitlines() if f]


def is_exempt(path):
    normalized = path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in EXEMPT_PATHS)


def check_file(path):
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except (FileNotFoundError, IsADirectoryError, OSError):
        return findings

    for lineno, line in enumerate(lines, start=1):
        if PRAGMA in line:
            continue
        for name, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(line):
                findings.append((path, lineno, name, line.strip()))
    return findings


def main():
    staged_files = [f for f in get_staged_files() if not is_exempt(f)]

    all_findings = []
    for path in staged_files:
        all_findings.extend(check_file(path))

    if all_findings:
        print(
            "check-sensitive-patterns: possible sensitive identifiers found in staged changes:\n",
            file=sys.stderr,
        )
        for path, lineno, name, snippet in all_findings:
            print(f"  {path}:{lineno}: possible {name} -> {snippet}", file=sys.stderr)
        print(
            "\nIf this is a real identifier, remove it before committing.\n"
            "If it's a false positive, add '# pragma: allowlist secret' on that line,\n"
            "or adjust SENSITIVE_PATTERNS / EXEMPT_PATHS in scripts/check_sensitive_patterns.py.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
