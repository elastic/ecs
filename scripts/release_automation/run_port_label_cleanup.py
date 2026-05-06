#!/usr/bin/env python3
"""Auto-clean source PR porting labels when child PRs are created.

Triggered by port PR creation events.  The script:
  1. Parses source PR number from child title: (backport #123) / (forwardport #123)
  2. Determines expected target branches for source labels:
     - needs_backport
     - needs_forward_port
  3. Removes source labels once all expected child PRs are present
"""

import json
import re
import sys
from pathlib import Path

from release_automation.helpers import (
    forward_port_targets,
    gh,
    require_repo,
)

SOURCE_PR_RE = re.compile(r"\((?:backport|forwardport) #(\d+)\)")


def _parse_source_pr_number(title: str) -> int | None:
    match = SOURCE_PR_RE.search(title)
    return int(match.group(1)) if match else None


def _load_backport_targets(source_base: str) -> list[str]:
    with open(".backportrc.json") as fh:
        config = json.load(fh)

    semver_re = re.compile(r"^(\d+)\.(\d+)$")
    if source_base == "main":
        version = Path("version").read_text().strip()
        parts = version.split(".")
        if len(parts) < 2 or not parts[0].isdigit() or not parts[1].isdigit():
            return []
        floor_major = int(parts[0])
        floor_minor = max(int(parts[1]) - 1, 0)
    else:
        base_match = semver_re.match(source_base)
        if not base_match:
            return []
        floor_major = int(base_match.group(1))
        floor_minor = int(base_match.group(2))

    targets: list[tuple[int, int, str]] = []
    for branch in config.get("branches", []):
        name = branch if isinstance(branch, str) else branch.get("name", "")
        match = semver_re.match(name)
        if not match:
            continue
        major, minor = int(match.group(1)), int(match.group(2))
        if (major, minor) >= (floor_major, floor_minor) and name != source_base:
            targets.append((major, minor, name))

    targets.sort()
    return [target[2] for target in targets]


def _load_child_port_prs(repo: str, source_pr_number: int) -> list[dict]:
    matching_title_re = re.compile(rf"\((?:backport|forwardport) #{source_pr_number}\)")

    all_prs: dict[int, dict] = {}
    for label in ("backport", "forward_port"):
        result = gh(
            "pr",
            "list",
            "--repo",
            repo,
            "--label",
            label,
            "--state",
            "all",
            "--json",
            "number,title,url,baseRefName",
            "--limit",
            "200",
        )
        for pr in json.loads(result.stdout):
            if matching_title_re.search(pr["title"]):
                all_prs[pr["number"]] = pr

    return list(all_prs.values())


def _remove_source_label(repo: str, source_pr_number: int, label: str) -> None:
    result = gh(
        "pr",
        "edit",
        str(source_pr_number),
        "--repo",
        repo,
        "--remove-label",
        label,
        check=False,
    )
    if result.returncode == 0:
        print(f"Removed '{label}' from source PR #{source_pr_number}")
    else:
        print(f"::warning::Failed to remove '{label}' from source PR #{source_pr_number}")


def _all_targets_opened(expected_targets: list[str], child_prs: list[dict]) -> bool:
    opened_targets = {pr["baseRefName"] for pr in child_prs}
    missing = [target for target in expected_targets if target not in opened_targets]
    if missing:
        print(f"Missing child PRs for targets: {', '.join(missing)}")
        return False
    return True


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: run_port_label_cleanup.py <child_pr_number>", file=sys.stderr)
        sys.exit(1)

    repo = require_repo()
    child_pr_number = int(sys.argv[1])

    child = json.loads(
        gh(
            "pr",
            "view",
            str(child_pr_number),
            "--repo",
            repo,
            "--json",
            "number,title,url",
        ).stdout
    )
    source_pr_number = _parse_source_pr_number(child["title"])
    if not source_pr_number:
        print("Child PR title does not contain a backport/forwardport source marker; skipping.")
        return

    source = json.loads(
        gh(
            "pr",
            "view",
            str(source_pr_number),
            "--repo",
            repo,
            "--json",
            "number,title,url,baseRefName,labels",
        ).stdout
    )
    source_labels = {label["name"] for label in source.get("labels", [])}
    source_base = source["baseRefName"]
    child_prs = _load_child_port_prs(repo, source_pr_number)

    if "needs_backport" in source_labels:
        expected_backports = _load_backport_targets(source_base)
        print(f"Expected backport targets for source PR #{source_pr_number}: {expected_backports}")
        if _all_targets_opened(expected_backports, child_prs):
            _remove_source_label(repo, source_pr_number, "needs_backport")

    if "needs_forward_port" in source_labels:
        expected_forward_ports = forward_port_targets(source_base, repo, include_main=True)
        print(f"Expected forward-port targets for source PR #{source_pr_number}: {expected_forward_ports}")
        if _all_targets_opened(expected_forward_ports, child_prs):
            _remove_source_label(repo, source_pr_number, "needs_forward_port")


if __name__ == "__main__":
    main()
