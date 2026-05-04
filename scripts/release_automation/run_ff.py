#!/usr/bin/env python3
"""ECS Release: Feature Freeze / Changelog Cut entry point.

Called by the ``ecs-release-ff.yml`` workflow with a single argument:
the version string (e.g. ``9.4.0`` or ``9.3.1``).

For minor releases (patch == 0):
  1. Creates the release branch from main
  2. Creates a combined PR on main (version bump + backportrc update)
  3. Creates a changelog PR on the release branch

For patch releases (patch > 0):
  1. Creates a changelog cut PR on the existing release branch
  (Branch creation and main PR are skipped.)
"""

import json
import sys
from pathlib import Path

from release_automation.helpers import (
    commit_and_push,
    create_pr,
    find_open_pr,
    git,
    parse_version,
    release_branch_for,
    require_no_backports,
    require_repo,
    run,
    setup_branch,
    write_summary,
)


def main() -> None:
    version = parse_version(sys.argv, usage="run_ff.py <version>")
    repo = require_repo()

    release_branch = release_branch_for(version)
    major, minor, patch = version.split(".")
    is_patch = int(patch) > 0

    require_no_backports(repo)

    pr_main_url = None
    branch_created = False

    # ── Minor-only: create release branch + main PR ──────────────
    if not is_patch:
        next_version = f"{major}.{int(minor) + 1}.0-dev"

        r = git("ls-remote", "--exit-code", "--heads", "origin", release_branch, check=False)
        if r.returncode != 0:
            git("push", "origin", f"main:refs/heads/{release_branch}")
            print(f"Created branch '{release_branch}' from main")
            branch_created = True
        else:
            print(f"Branch '{release_branch}' already exists — skipping creation.")

        pr_branch_main = f"release/{version}/bump-main"
        existing_main = find_open_pr(pr_branch_main, "main", repo)
        if existing_main:
            pr_main_url = existing_main["url"]
            print(f"Main PR already exists: {pr_main_url}")
        else:
            setup_branch(pr_branch_main, "origin/main")
            Path("version").write_text(next_version + "\n")

            with open(".backportrc.json") as f:
                data = json.load(f)
            branches = data["branches"]
            existing_names = [b if isinstance(b, str) else b.get("name", "") for b in branches]
            if release_branch not in existing_names:
                branches.insert(1, release_branch)
                data["branches"] = branches
                with open(".backportrc.json", "w") as f:
                    json.dump(data, f, indent=2)
                    f.write("\n")
                print(f"Added {release_branch} to .backportrc.json")

            if Path("Makefile").exists():
                run(["make", "ve"], check=False)
                run(["make", "generate"], check=False)

            commit_and_push(pr_branch_main, f"Bump version to {next_version} and add {release_branch} to backportrc")

            pr_main_url = create_pr(
                head=pr_branch_main, base="main",
                title=f"Bump version to {next_version} + add {release_branch} to .backportrc.json",
                body=(
                    f"## Automated Feature Freeze PR (main)\n\n"
                    f"- Bumps `version` to `{next_version}`\n"
                    f"- Adds `{release_branch}` to `.backportrc.json`\n"
                    f"- Generated files updated via `make generate`\n\n"
                    f"> **Note**: Approve within 24 hours to avoid branch staleness on main.\n"
                    f"> If CI fails, push a fix directly to the PR branch."
                ),
                repo=repo,
            )

    # ── Changelog cut PR on release branch ────────────────────────
    pr_branch_cl = f"release/{version}/ff-changelog"
    existing_cl = find_open_pr(pr_branch_cl, release_branch, repo)
    if existing_cl:
        pr_cl_url = existing_cl["url"]
        print(f"Changelog PR already exists: {pr_cl_url}")
    else:
        git("fetch", "origin", release_branch)
        setup_branch(pr_branch_cl, f"origin/{release_branch}")

        if is_patch:
            from release_automation.changelog import cut_release
            cut_release(version, repo_root=".")
        else:
            from release_automation.changelog import cut_feature_freeze
            cut_feature_freeze(version, repo_root=".")

        cl_commit_msg = f"{version} changelog" if is_patch else f"{version} Feature Freeze changelog"
        commit_and_push(pr_branch_cl, cl_commit_msg)

        if is_patch:
            cl_title = f"{version} changelog"
            cl_body = (
                f"## Automated Changelog Cut\n\n"
                f"- Creates new empty Unreleased section\n"
                f"- Renames previous Unreleased to \"{version}\"\n"
                f"- Sorts entries by PR ID\n"
                f"- Removes empty sections\n\n"
                f"> If CI fails, push a fix directly to the PR branch.\n\n"
                f"After merge, forward-port PRs will be created for branches ahead."
            )
        else:
            cl_title = f"{version} Feature Freeze changelog"
            cl_body = (
                f"## Automated Feature Freeze Changelog\n\n"
                f"- Creates new empty Unreleased section\n"
                f"- Renames previous Unreleased to \"{version} (Feature Freeze)\"\n"
                f"- Sorts entries by PR ID\n"
                f"- Removes empty sections\n\n"
                f"> If CI fails, push a fix directly to the PR branch.\n\n"
                f"After merge, Mergify will create a forward-port PR to main."
            )

        pr_cl_url = create_pr(
            head=pr_branch_cl, base=release_branch,
            title=cl_title, body=cl_body,
            repo=repo,
            labels=["needs_forward_port"],
        )

    # ── Summary ──────────────────────────────────────────────────
    if is_patch:
        summary = f"""# Changelog Cut: ECS {version}

## Changelog PR
- **Release branch** (`{release_branch}`): {pr_cl_url}
  - Label: `needs_forward_port` (forward-port PRs will be created after merge)

## Next Steps
1. Approve and merge the changelog PR on the release branch
2. After merge, forward-port PRs are created automatically -- approve those too
3. Run the **RC Cut** workflow (optional) or proceed to **Release Preparation**

> If CI fails on the auto-generated PR, push a fix directly to the PR branch.
"""
    else:
        summary = f"""# Feature Freeze: ECS {version}

## Release Branch
- Branch `{release_branch}`: {"Created" if branch_created else "Already existed"}

## PRs Created
1. **Main branch** (version bump + backportrc): {pr_main_url}
2. **Release branch** (FF changelog): {pr_cl_url}
   - Label: `needs_forward_port` (Mergify will create forward-port to main after merge)

## Next Steps
1. Approve and merge the PR on main (version bump)
2. Approve and merge the PR on the release branch (changelog)
3. After the changelog PR merges, Mergify creates a forward-port PR to main -- approve that too

> If CI fails on any auto-generated PR, push a fix directly to the PR branch.
"""
    write_summary(summary)


if __name__ == "__main__":
    main()
