"""Changelog manipulation for ECS releases.

Operates on ``CHANGELOG.next.md`` and ``CHANGELOG.md`` using only the
Python standard library.
"""

import re
from pathlib import Path

NEXT = "CHANGELOG.next.md"
MAIN = "CHANGELOG.md"

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
    pending_h3: str | None = None

    for heading, body in sections:
        if heading.startswith("## ") and not heading.startswith("### "):
            pending_h3 = None
            result.append(heading)
            result.extend(body)
        elif heading.startswith("### "):
            pending_h3 = heading
        elif heading.startswith("#### "):
            if _has_bullet_entries(body):
                if pending_h3:
                    result.append(pending_h3)
                    pending_h3 = None
                result.append(heading)
                result.extend(body)
        elif not heading:
            result.extend(body)

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


def _cut_changelog(version: str, title: str, repo_root: str = ".") -> str:
    """Shared implementation for changelog cutting.

    Renames ``## Unreleased`` to ``## {title}``, sorts entries, removes
    empty sections, prepends a fresh Unreleased block, and returns the
    cut section text.
    """
    root = Path(repo_root)
    content = (root / NEXT).read_text()

    content = content.replace("## Unreleased", f"## {title}", 1)
    content = _sort_entries_in_section(content)
    content = _remove_empty_sections(content)

    fresh_unreleased = _load_template("unreleased_section.md")
    comment_end = content.find("-->")
    insert_pos = content.find("\n", comment_end) + 1 if comment_end != -1 else 0
    content = content[:insert_pos] + fresh_unreleased + content[insert_pos:]

    (root / NEXT).write_text(content)

    start = content.find(f"## {title}")
    return content[start:] if start != -1 else ""


def _find_version_section(text: str, version: str) -> tuple[int, int]:
    """Return (start, end) char offsets of the ``## {version} …`` section.

    Uses a regex boundary so ``9.3.1`` does not match ``9.3.12``.
    """
    esc = re.escape(version)
    pattern = re.compile(rf"^## {esc}(?:\s|\(|$)", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        raise ValueError(f"Section for {version} not found in {NEXT}")
    start = m.start()
    rest = text[m.end():]
    next_h2 = re.search(r"\n## ", rest)
    end = m.end() + next_h2.start() if next_h2 else len(text)
    return start, end


# ── Public API ──────────────────────────────────────────────────────


def cut_feature_freeze(version: str, repo_root: str = ".") -> str:
    """Cut changelog for a feature freeze (minor release).

    Titles the section ``## {version} (Feature Freeze)``.
    """
    return _cut_changelog(version, f"{version} (Feature Freeze)", repo_root)


def cut_release(version: str, repo_root: str = ".") -> str:
    """Cut changelog for a direct release (patch release, no FF).

    Titles the section ``## {version}``.
    """
    return _cut_changelog(version, version, repo_root)


def get_section_text(version: str, repo_root: str = ".") -> str:
    """Return the raw text of the *version* section from ``CHANGELOG.next.md``.

    Returns an empty string if the section is not found, rather than raising.
    """
    root = Path(repo_root)
    content = (root / NEXT).read_text()
    try:
        start, end = _find_version_section(content, version)
    except ValueError:
        return ""
    return content[start:end].strip()


def extract_section(version: str, repo_root: str = ".") -> dict[str, list[str]]:
    """Parse the *version* section from ``CHANGELOG.next.md`` into categories.

    Returns a dict keyed like ``"schema_added"``, ``"tooling_bugfixes"``,
    etc., where each value is a list of raw ``* …`` entry lines.
    """
    root = Path(repo_root)
    content = (root / NEXT).read_text()
    start, end = _find_version_section(content, version)
    section = content[start:end]

    entries: dict[str, list[str]] = {}
    current_h3 = ""
    current_h4 = ""

    for line in section.split("\n"):
        if line.startswith("### "):
            current_h3 = line.removeprefix("### ").strip()
            current_h4 = ""
        elif line.startswith("#### "):
            current_h4 = line.removeprefix("#### ").strip()
        elif line.strip().startswith("*"):
            prefix = "schema" if "Schema" in current_h3 else "tooling"
            cat = current_h4.lower().replace(" ", "_")
            key = f"{prefix}_{cat}" if cat else prefix
            entries.setdefault(key, []).append(line)

    return entries


def finalize_changelog(
    version: str, prev_version: str, repo_url: str, repo_root: str = "."
) -> None:
    """Move the FF section from ``CHANGELOG.next.md`` to ``CHANGELOG.md``.

    The section title is replaced with a compare-link:
    ``[X.Y.Z](repo_url/compare/vPREV...vX.Y.Z)``
    """
    root = Path(repo_root)
    next_content = (root / NEXT).read_text()
    start, end = _find_version_section(next_content, version)
    section_text = next_content[start:end].rstrip() + "\n"

    link_title = f"## [{version}]({repo_url}/compare/v{prev_version}...v{version})"
    for pat in [f"## {version} (Feature Freeze)", f"## {version}"]:
        if pat in section_text:
            section_text = section_text.replace(pat, link_title, 1)
            break

    trimmed_next = next_content[:start] + next_content[end:]
    (root / NEXT).write_text(trimmed_next)

    main_path = root / MAIN
    main_content = main_path.read_text()
    insert_marker = re.search(r"^## ", main_content, re.MULTILINE)
    if insert_marker:
        pos = insert_marker.start()
        main_content = main_content[:pos] + section_text + "\n" + main_content[pos:]
    else:
        main_content += "\n" + section_text
    main_path.write_text(main_content)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="ECS changelog tools")
    sub = parser.add_subparsers(dest="command")

    ff = sub.add_parser("feature-freeze", help="Cut changelog for feature freeze")
    ff.add_argument("version", help="e.g. 9.4.0")
    ff.add_argument("--repo-root", default=".")

    cr = sub.add_parser("cut-release", help="Cut changelog for a direct release (patch)")
    cr.add_argument("version", help="e.g. 9.3.1")
    cr.add_argument("--repo-root", default=".")

    fin = sub.add_parser("finalize", help="Move FF section to CHANGELOG.md")
    fin.add_argument("version", help="e.g. 9.4.0")
    fin.add_argument("prev_version", help="e.g. 9.3.0")
    fin.add_argument("repo_url", help="e.g. https://github.com/elastic/ecs")
    fin.add_argument("--repo-root", default=".")

    ext = sub.add_parser("extract", help="Extract categorized entries as JSON")
    ext.add_argument("version", help="e.g. 9.4.0")
    ext.add_argument("--repo-root", default=".")

    args = parser.parse_args()
    if args.command == "feature-freeze":
        section = cut_feature_freeze(args.version, args.repo_root)
        print(section)
    elif args.command == "cut-release":
        section = cut_release(args.version, args.repo_root)
        print(section)
    elif args.command == "finalize":
        finalize_changelog(args.version, args.prev_version, args.repo_url, args.repo_root)
    elif args.command == "extract":
        entries = extract_section(args.version, args.repo_root)
        print(json.dumps(entries, indent=2))
    else:
        parser.print_help()
