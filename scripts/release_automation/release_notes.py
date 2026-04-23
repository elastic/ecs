"""Generate and insert release-note sections into docs/release-notes/ files.

Maps changelog categories to the appropriate release-notes files:
  - Added + Improvements -> Features and enhancements (index.md)
  - Bugfixes -> Fixes (index.md)
  - Breaking changes -> breaking-changes.md
  - Deprecated -> deprecations.md
"""

import re
from pathlib import Path

RELEASE_NOTES_DIR = Path("docs/release-notes")


def _version_anchor(version: str) -> str:
    """e.g. 9.4.0 -> ecs-9-4-0"""
    return "ecs-" + version.replace(".", "-")


def _format_entry(entry: str, repo_url: str) -> str:
    """Convert a changelog entry to release-notes format.

    Input:  ``* Description #1234`` or ``* Description. #1234``
    Output: ``* Description [#1234](repo_url/pull/1234)``
    """
    m = re.search(r"[.!?\s]*#(\d+)\s*$", entry)
    if not m:
        return entry
    pr_num = m.group(1)
    prefix = entry[: m.start()].rstrip()
    return f"{prefix} [#{pr_num}]({repo_url}/pull/{pr_num})"


def _insert_after_comment_template(
    content: str, new_section: str, marker_pattern: str
) -> str:
    """Insert *new_section* after the commented-out template block.

    The template block starts with a line matching *marker_pattern* and
    ends when a non-comment, non-blank line is reached.
    """
    lines = content.split("\n")
    insert_idx = None

    in_comment_block = False
    for i, line in enumerate(lines):
        if re.match(marker_pattern, line):
            in_comment_block = True
        elif in_comment_block:
            if line.startswith("%") or line.strip() == "":
                continue
            else:
                insert_idx = i
                break

    if insert_idx is None:
        for i, line in enumerate(lines):
            if line.startswith("## ") and not line.startswith("% "):
                insert_idx = i
                break

    if insert_idx is None:
        insert_idx = len(lines)

    lines.insert(insert_idx, new_section)
    return "\n".join(lines)


def update_index(
    version: str,
    entries: dict[str, list[str]],
    repo_url: str,
    repo_root: str = ".",
) -> None:
    """Insert features/enhancements and fixes sections into ``index.md``."""
    root = Path(repo_root)
    index_path = root / RELEASE_NOTES_DIR / "index.md"
    content = index_path.read_text()

    anchor = _version_anchor(version)

    if f"## {version} [{anchor}-release-notes]" in content:
        print(f"Release notes for {version} already in index.md — skipping.")
        return

    features: list[str] = []
    fixes: list[str] = []
    for key, items in entries.items():
        cat = key.split("_", 1)[1] if "_" in key else key
        if cat in ("added", "improvements"):
            features.extend(items)
        elif cat == "bugfixes":
            fixes.extend(items)

    section_lines = [f"## {version} [{anchor}-release-notes]", ""]

    if features:
        section_lines.append(
            f"### Features and enhancements [{anchor}-features-enhancements]"
        )
        section_lines.append("")
        for e in features:
            section_lines.append(_format_entry(e, repo_url))
        section_lines.append("")

    if fixes:
        section_lines.append(f"### Fixes [{anchor}-fixes]")
        section_lines.append("")
        for e in fixes:
            section_lines.append(_format_entry(e, repo_url))
        section_lines.append("")

    if not features and not fixes:
        section_lines.append("No notable changes in this release.")
        section_lines.append("")

    new_section = "\n".join(section_lines)
    content = _insert_after_comment_template(
        content, new_section, r"^% ## version\.next"
    )
    index_path.write_text(content)
    print(f"Updated {index_path} with {version} release notes.")


def update_breaking_changes(
    version: str,
    entries: dict[str, list[str]],
    repo_url: str,
    repo_root: str = ".",
) -> None:
    root = Path(repo_root)
    path = root / RELEASE_NOTES_DIR / "breaking-changes.md"
    content = path.read_text()
    anchor = _version_anchor(version)

    if f"## {version} [{anchor}-breaking-changes]" in content:
        print(f"Breaking changes for {version} already present — skipping.")
        return

    breaking: list[str] = []
    for key, items in entries.items():
        if key.endswith("breaking_changes"):
            breaking.extend(items)

    section_lines = [f"## {version} [{anchor}-breaking-changes]", ""]
    if breaking:
        for e in breaking:
            formatted = _format_entry(e, repo_url)
            desc = formatted.removeprefix("* ")
            section_lines.append(f":::::::{{dropdown}} {desc}")
            section_lines.append(":::::::")
            section_lines.append("")
    else:
        section_lines.append("None at this time")
    section_lines.append("")

    new_section = "\n".join(section_lines)
    content = _insert_after_comment_template(
        content, new_section, r"^% ## Next version"
    )
    path.write_text(content)
    print(f"Updated {path} with {version} breaking changes.")


def update_deprecations(
    version: str,
    entries: dict[str, list[str]],
    repo_url: str,
    repo_root: str = ".",
) -> None:
    root = Path(repo_root)
    path = root / RELEASE_NOTES_DIR / "deprecations.md"
    content = path.read_text()
    anchor = _version_anchor(version)

    if f"## {version} [{anchor}-deprecations]" in content:
        print(f"Deprecations for {version} already present — skipping.")
        return

    deprecated: list[str] = []
    for key, items in entries.items():
        if key.endswith("deprecated"):
            deprecated.extend(items)

    section_lines = [f"## {version} [{anchor}-deprecations]", ""]
    if deprecated:
        for e in deprecated:
            formatted = _format_entry(e, repo_url)
            desc = formatted.removeprefix("* ")
            section_lines.append(f":::::::{{dropdown}} {desc}")
            section_lines.append(":::::::")
            section_lines.append("")
    else:
        section_lines.append("None at this time")
    section_lines.append("")

    new_section = "\n".join(section_lines)
    content = _insert_after_comment_template(
        content, new_section, r"^% ## Next version"
    )
    path.write_text(content)
    print(f"Updated {path} with {version} deprecations.")


def update_all(
    version: str,
    entries: dict[str, list[str]],
    repo_url: str,
    repo_root: str = ".",
) -> None:
    """Update all release-notes files for *version*."""
    update_index(version, entries, repo_url, repo_root)
    update_breaking_changes(version, entries, repo_url, repo_root)
    update_deprecations(version, entries, repo_url, repo_root)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Update ECS release notes")
    parser.add_argument("version", help="e.g. 9.4.0")
    parser.add_argument(
        "entries_json", help="JSON file with categorized entries (from changelog.py extract)"
    )
    parser.add_argument("repo_url", help="e.g. https://github.com/elastic/ecs")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    with open(args.entries_json) as f:
        entries = json.load(f)

    update_all(args.version, entries, args.repo_url, args.repo_root)
