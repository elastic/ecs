#!/usr/bin/env python3
"""ECS Release: RC Cut entry point.

Called by ``ecs-release-rc.yml`` with version and rc_number arguments.

Performs:
  1. Validates inputs
  2. Verifies the changelog has been cut for this version
  3. Creates a PR on the release branch to set version to X.Y.Z-rcN
  4. Writes a GitHub Actions step summary

The pre-release tag is created automatically when the version PR merges,
via the ``ecs-release-rc-tag.yml`` event-driven workflow.
"""

import sys
from pathlib import Path

from release_automation.changelog import get_section_text
from release_automation.helpers import (
    commit_and_push,
    create_pr,
    find_open_pr,
    git,
    parse_version,
    release_branch_for,
    require_repo,
    run,
    setup_branch,
    write_summary,
)


def main() -> None:
    version = parse_version(sys.argv, usage="run_rc.py <version> [rc_number]")
    rc_number = sys.argv[2] if len(sys.argv) > 2 else "1"
    repo = require_repo()

    release_branch = release_branch_for(version)
    rc_version = f"{version}-rc{rc_number}"
    tag = f"v{rc_version}"

    # ── Verify changelog has been cut for this version ────────────
    git("fetch", "origin", release_branch)
    git("checkout", f"origin/{release_branch}", "--", "CHANGELOG.next.md")
    section_text = get_section_text(version)
    if not section_text:
        print(
            f"::error::No changelog section found for {version} in "
            f"CHANGELOG.next.md on {release_branch}. "
            f"Run the Feature Freeze / Changelog Cut workflow first.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Changelog section for {version} found.")

    # ── PR: Set version file to X.Y.Z-rcN ────────────────────────
    pr_branch = f"release/{version}/set-rc{rc_number}"
    existing = find_open_pr(pr_branch, release_branch, repo)
    if existing:
        pr_url = existing["url"]
        print(f"RC version PR already exists: {pr_url}")
    else:
        git("fetch", "origin", release_branch)
        setup_branch(pr_branch, f"origin/{release_branch}")
        Path("version").write_text(rc_version + "\n")

        if Path("Makefile").exists():
            run(["make", "ve"], check=False)
            run(["make", "generate"], check=False)

        commit_and_push(pr_branch, f"Set version to {rc_version}")
        pr_url = create_pr(
            head=pr_branch, base=release_branch,
            title=f"Set version to {rc_version}",
            body=(
                f"## Automated RC Cut: Version\n\n"
                f"Sets the `version` file to `{rc_version}` to match the RC tag.\n\n"
                f"**Merging this PR will automatically create and publish "
                f"the `{tag}` pre-release.**\n\n"
                f"> If CI fails, push a fix directly to the PR branch."
            ),
            repo=repo,
        )

    repo_url = f"https://github.com/{repo}"

    # ── Summary ──────────────────────────────────────────────────
    summary = f"""# RC Cut: ECS {version} RC{rc_number}

## Version PR
- **Set version to {rc_version}**: {pr_url}

## Next Steps
1. Verify CI passes on the version PR
2. Approve and merge it
3. The `{tag}` pre-release will be created automatically on merge
4. Share the RC with stakeholders for testing

> The release tag always points to a commit where `version` = `{rc_version}`.
"""
    write_summary(summary)


if __name__ == "__main__":
    main()
