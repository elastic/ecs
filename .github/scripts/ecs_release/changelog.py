"""Changelog manipulation for ECS releases.

Operates on ``CHANGELOG.next.md`` using only the Python standard library.
"""

import re
from pathlib import Path

NEXT = "CHANGELOG.next.md"

_TEMPLATES_DIR = Path(__file__).parent / "templates"


def _load_template(name: str) -> str:
    return (_TEMPLATES_DIR / name).read_text()


_PR_RE = re.compile(r"#(\d+)\s*$")


def _pr_sort_key(line: str) -> int:
    m = _PR_RE.search(line)
    return int(m.group(1)) if m else 0


# ── Internal helpers ───────────────────────────────────────────────


def _has_bullet_entries(lines: list[str]) -> bool:
    """Return True if any line in *lines* is a ``*`` bullet entry."""
    return any(line.strip().startswith("*") for line in lines)


def _remove_empty_sections(text: str) -> str:
    """Remove ``###`` / ``####`` sections that contain no bullet entries.

    Parses the markdown into (heading, body) pairs, then reassembles
    only those sections whose body contains at least one ``*`` entry.
    ``##`` headings are always preserved.
    """
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_body: list[str] = []

    for line in text.split("\n"):
        if line.startswith("## ") or line.startswith("### ") or line.startswith("#### "):
            if current_heading is not None or current_body:
                sections.append((current_heading or "", current_body))
            current_heading = line
            current_body = []
        else:
            current_body.append(line)

    sections.append((current_heading or "", current_body))

    result: list[str] = []
    # Track whether the parent ### had any kept #### children so we
    # can suppress empty ### groups too.
    pending_h3: str | None = None
    h3_has_content = False

    for heading, body in sections:
        if heading.startswith("## ") and not heading.startswith("### "):
            # Flush pending ### if it had content
            if pending_h3 and h3_has_content:
                result.append(pending_h3)
            pending_h3 = None
            h3_has_content = False
            result.append(heading)
            result.extend(body)
        elif heading.startswith("### "):
            if pending_h3 and h3_has_content:
                result.append(pending_h3)
            pending_h3 = heading
            h3_has_content = False
        elif heading.startswith("#### "):
            if _has_bullet_entries(body):
                h3_has_content = True
                result.append(heading)
                result.extend(body)
        elif not heading:
            result.extend(body)

    if pending_h3 and h3_has_content:
        result.append(pending_h3)

    return "\n".join(result)


def _sort_entries_in_section(text: str) -> str:
    """Sort ``*`` bullet entries within each ``####`` section by PR ID."""
    lines = text.split("\n")
    result: list[str] = []
    bucket: list[str] = []

    def flush():
        entries = [l for l in bucket if l.strip().startswith("*")]
        non_entries = [l for l in bucket if not l.strip().startswith("*")]
        entries.sort(key=_pr_sort_key)
        result.extend(non_entries)
        result.extend(entries)
        bucket.clear()

    for line in lines:
        if line.startswith("#"):
            flush()
            result.append(line)
        else:
            bucket.append(line)
    flush()
    return "\n".join(result)


# ── Public API ──────────────────────────────────────────────────────


def cut_feature_freeze(version: str, repo_root: str = ".") -> str:
    """Feature-freeze cut of CHANGELOG.next.md.

    - Renames ``## Unreleased`` to ``## {version} (Feature Freeze)``
    - Sorts entries by PR ID within sections
    - Removes empty sections
    - Prepends a fresh empty Unreleased block
    - Returns the changelog section content (for use in RC release body)
    """
    root = Path(repo_root)
    content = (root / NEXT).read_text()

    content = content.replace("## Unreleased", f"## {version} (Feature Freeze)", 1)
    content = _sort_entries_in_section(content)
    content = _remove_empty_sections(content)

    fresh_unreleased = _load_template("unreleased_section.md")
    comment_end = content.find("-->")
    insert_pos = content.find("\n", comment_end) + 1 if comment_end != -1 else 0
    content = content[:insert_pos] + fresh_unreleased + content[insert_pos:]

    (root / NEXT).write_text(content)

    ff_start = content.find(f"## {version} (Feature Freeze)")
    return content[ff_start:] if ff_start != -1 else ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ECS changelog tools")
    sub = parser.add_subparsers(dest="command")

    ff = sub.add_parser("feature-freeze", help="Cut changelog for feature freeze")
    ff.add_argument("version", help="e.g. 9.4.0")
    ff.add_argument("--repo-root", default=".")

    args = parser.parse_args()
    if args.command == "feature-freeze":
        section = cut_feature_freeze(args.version, args.repo_root)
        print(section)
    else:
        parser.print_help()
