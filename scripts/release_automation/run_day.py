#!/usr/bin/env python3
"""ECS Release: Release Day entry point.

Called by ``ecs-release-day.yml`` with the version string.

Performs:
  1. Finds the gated PRs created by Release Prep
  2. Reports their current status
  3. Writes a step summary with merge-order instructions
"""

import json
import sys

from release_automation.helpers import (
    find_merged_pr,
    find_open_pr,
    gh,
    parse_version,
    release_branch_for,
    require_repo,
    write_summary,
)


def main() -> None:
    version = parse_version(sys.argv, usage="run_day.py <version>")
    repo = require_repo()

    release_branch = release_branch_for(version)
    repo_url = f"https://github.com/{repo}"

    # ── Find gated PRs ───────────────────────────────────────────
    pr_types = {
        "set-version": "Set version",
        "finalize-changelog": "Finalize changelog",
        "release-notes": "Update release notes",
    }
    found_prs: dict[str, dict] = {}
    merged_prs: dict[str, dict] = {}
    missing: list[str] = []

    for pr_type, label in pr_types.items():
        branch = f"release/{version}/{pr_type}"
        pr = find_open_pr(branch, release_branch, repo)
        if pr:
            found_prs[pr_type] = pr
            print(f"Found open {label}: {pr['url']}")
        else:
            merged = find_merged_pr(branch, release_branch, repo)
            if merged:
                merged_prs[pr_type] = merged
                print(f"Already merged {label}: {merged['url']}")
            else:
                missing.append(label)
                print(f"::warning::No open or merged PR found for {label} (branch: {branch})")

    # ── Check draft release ──────────────────────────────────────
    tag = f"v{version}"
    release_r = gh(
        "release", "view", tag, "--repo", repo,
        "--json", "tagName,isDraft,url",
        check=False,
    )
    draft_info = ""
    if release_r.returncode == 0:
        release_data = json.loads(release_r.stdout)
        if release_data.get("isDraft"):
            draft_info = f"Draft release ready: {release_data['url']}"
        else:
            draft_info = f"Release already published: {release_data['url']}"
    else:
        draft_info = f"::warning::Draft release {tag} not found. Run Release Prep first."

    # ── Summary ──────────────────────────────────────────────────
    def _pr_url(pr_type: str) -> str:
        if pr_type in found_prs:
            return found_prs[pr_type]["url"]
        if pr_type in merged_prs:
            return f"{merged_prs[pr_type]['url']} *(already merged)*"
        return "NOT FOUND -- run Release Prep first"

    ver_url = _pr_url("set-version")
    cl_url = _pr_url("finalize-changelog")
    rn_url = _pr_url("release-notes")

    summary = f"""# Release Day: ECS {version}

## Merge Order (approve in this sequence)

### Release Branch PRs (1 approval each)
1. **Set version**: {ver_url}
   Merge this FIRST -- the release tag must point to a clean version
2. **Finalize changelog**: {cl_url}
3. **Update release notes**: {rn_url}

### Forward-port PRs (created automatically by Mergify after merge)
4. Mergify will create forward-port PRs to `main` for changelog + release notes
   - Each needs 2 approvals (main branch protection)
   - If the second forward-port shows "branch out of date", click **Update branch**

### docs-builder
5. Approve the docs-builder PR (if created)

### Publish
6. Go to [Releases]({repo_url}/releases) and **publish** the draft release "ECS {version}"
   Do NOT publish until ALL release-branch PRs are merged

## {draft_info}

> If CI fails on any auto-generated PR, push a fix directly to the PR branch.
"""
    if missing:
        summary += f"\n## Missing PRs\n"
        for m in missing:
            summary += f"- {m}\n"
        summary += "\nRun Release Prep first if these haven't been created.\n"

    write_summary(summary)


if __name__ == "__main__":
    main()
