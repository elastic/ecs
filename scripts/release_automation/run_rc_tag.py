#!/usr/bin/env python3
"""ECS Release: RC Tag entry point.

Called by ``ecs-release-rc-tag.yml`` when the RC version PR merges.
Arguments are extracted from the merged branch name by the workflow.

Performs:
  1. Validates inputs
  2. Verifies the version file on the release branch matches X.Y.Z-rcN
  3. Extracts the changelog section for the release body
  4. Idempotently creates and publishes a pre-release
  5. Writes a GitHub Actions step summary
"""

import os
import sys
import tempfile

from release_automation.changelog import get_section_text
from release_automation.helpers import (
    gh,
    git,
    parse_version,
    release_branch_for,
    require_repo,
    write_summary,
)


def main() -> None:
    version = parse_version(sys.argv, usage="run_rc_tag.py <version> <rc_number>")
    if len(sys.argv) < 3:
        print("Usage: run_rc_tag.py <version> <rc_number>", file=sys.stderr)
        sys.exit(1)
    rc_number = sys.argv[2]
    repo = require_repo()

    release_branch = release_branch_for(version)
    rc_version = f"{version}-rc{rc_number}"
    tag = f"v{rc_version}"
    title = f"ECS {version} RC{rc_number}"

    # ── Verify version file matches expected RC version ──────────
    git("fetch", "origin", release_branch)
    ver_check = git("show", f"origin/{release_branch}:version", check=False)
    actual_version = ver_check.stdout.strip() if ver_check.returncode == 0 else ""
    if actual_version != rc_version:
        print(
            f"::error::Version file on {release_branch} is `{actual_version}`, "
            f"expected `{rc_version}`. Ensure the version PR is merged before tagging.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Version file confirmed: {rc_version}")

    # ── Extract release body from changelog ──────────────────────
    git("checkout", f"origin/{release_branch}", "--", "CHANGELOG.next.md")
    section_text = get_section_text(version)
    body = section_text or f"Release candidate for ECS {version}"

    body_file = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
    body_file.write(body)
    body_file.close()

    # ── Create pre-release ───────────────────────────────────────
    existing = gh(
        "release", "view", tag, "--repo", repo, "--json", "tagName",
        check=False,
    )
    if existing.returncode == 0:
        print(f"Release {tag} already exists — skipping.")
    else:
        gh(
            "release", "create", tag,
            "--repo", repo,
            "--target", release_branch,
            "--title", title,
            "--notes-file", body_file.name,
            "--prerelease",
        )
        print(f"Published RC release: {tag}")

    os.unlink(body_file.name)

    repo_url = f"https://github.com/{repo}"

    # ── Summary ──────────────────────────────────────────────────
    summary = f"""# RC Tag Created: {title}

Published pre-release: [{tag}]({repo_url}/releases/tag/{tag})

## Next Steps
- Share the RC with stakeholders for testing
- Begin Release Preparation when ready
"""
    write_summary(summary)


if __name__ == "__main__":
    main()
