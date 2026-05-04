#!/usr/bin/env python3
"""ECS Release: Preparation entry point.

Called by ``ecs-release-prep.yml`` with a single argument: the version string.

Performs:
  1. Validates version and derives release branch + previous version
  2. Blocks if outstanding needs_backport PRs exist
  3. Creates PR 1: finalize changelog (needs_forward_port)
  4. Creates PR 2: set version (remove -dev / set patch version)
  5. Creates PR 3: update release notes (needs_forward_port)
  6. Creates a draft release
  7. Logs docs-builder manual instructions
  8. Checks CI status on release branch
  9. Writes a step summary

All PRs are "gated" -- they are NOT auto-merged. The Release Day
workflow instructs the RM to approve them in order.
"""

import json
import re
import sys
from pathlib import Path

from release_automation.helpers import (
    commit_and_push,
    create_pr,
    derive_previous_version,
    find_open_pr,
    gh,
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
    version = parse_version(sys.argv, usage="run_prep.py <version>")
    repo = require_repo()

    release_branch = release_branch_for(version)
    repo_url = f"https://github.com/{repo}"
    prev_version = derive_previous_version(repo, version)
    tag = f"v{version}"

    require_no_backports(repo)

    # ── Fetch release branch ─────────────────────────────────────
    git("fetch", "origin", release_branch)

    # ── Verify changelog has been cut for this version ──────────
    cl_check = git("show", f"origin/{release_branch}:CHANGELOG.next.md", check=False)
    version_found = (
        cl_check.returncode == 0
        and re.search(rf"^## {re.escape(version)}(?:\s|\(|$)", cl_check.stdout, re.MULTILINE)
    )
    if not version_found:
        print(
            f"::error::Changelog section for {version} not found in "
            f"CHANGELOG.next.md on {release_branch}. "
            "Run the Feature Freeze / Changelog Cut workflow first.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Changelog section for {version} found — proceeding.")

    # ── PR 1: Finalize changelog ─────────────────────────────────
    pr_branch_cl = f"release/{version}/finalize-changelog"
    existing_cl = find_open_pr(pr_branch_cl, release_branch, repo)
    if existing_cl:
        pr_cl_url = existing_cl["url"]
        print(f"Changelog PR already exists: {pr_cl_url}")
    else:
        setup_branch(pr_branch_cl, f"origin/{release_branch}")

        from release_automation.changelog import finalize_changelog
        finalize_changelog(version, prev_version, repo_url, repo_root=".")

        commit_and_push(pr_branch_cl, f"Finalize changelog for {version}")
        pr_cl_url = create_pr(
            head=pr_branch_cl, base=release_branch,
            title=f"Finalize changelog for {version}",
            body=(
                f"## Automated Release Prep: Changelog\n\n"
                f"Moves the feature-freeze changelog section from CHANGELOG.next.md "
                f"to CHANGELOG.md with a diff-link title.\n\n"
                f"**Do not merge until Release Day.**\n\n"
                f"> If CI fails, push a fix directly to the PR branch."
            ),
            repo=repo, labels=["needs_forward_port"],
        )

    # ── PR 2: Set version (remove -dev or set patch version) ────
    pr_branch_ver = f"release/{version}/set-version"
    existing_ver = find_open_pr(pr_branch_ver, release_branch, repo)
    if existing_ver:
        pr_ver_url = existing_ver["url"]
        print(f"Version PR already exists: {pr_ver_url}")
    else:
        setup_branch(pr_branch_ver, f"origin/{release_branch}")

        current_ver = Path("version").read_text().strip()
        Path("version").write_text(version + "\n")

        if Path("Makefile").exists():
            run(["make", "ve"], check=False)
            run(["make", "generate"], check=False)

        ver_title = f"Set version to {version}"
        ver_body = (
            f"## Automated Release Prep: Version\n\n"
            f"Sets the `version` file to `{version}` "
            f"(was `{current_ver}`) and regenerates version-dependent files.\n\n"
            f"**Do not merge until Release Day.** Merge this PR **first** "
            f"on Release Day so the release tag points to a clean version.\n\n"
            f"> If CI fails, push a fix directly to the PR branch."
        )

        commit_and_push(pr_branch_ver, ver_title)
        pr_ver_url = create_pr(
            head=pr_branch_ver, base=release_branch,
            title=ver_title, body=ver_body,
            repo=repo,
        )

    # ── PR 3: Update release notes ───────────────────────────────
    pr_branch_rn = f"release/{version}/release-notes"
    existing_rn = find_open_pr(pr_branch_rn, release_branch, repo)
    if existing_rn:
        pr_rn_url = existing_rn["url"]
        print(f"Release notes PR already exists: {pr_rn_url}")
    else:
        setup_branch(pr_branch_rn, f"origin/{release_branch}")

        from release_automation.changelog import extract_section
        from release_automation.release_notes import update_all

        entries = extract_section(version, ".")
        print("Extracted entries:", json.dumps(entries, indent=2))
        update_all(version, entries, repo_url, ".")

        commit_and_push(pr_branch_rn, f"Update release notes for {version}")
        pr_rn_url = create_pr(
            head=pr_branch_rn, base=release_branch,
            title=f"Update release notes for {version}",
            body=(
                f"## Automated Release Prep: Release Notes\n\n"
                f"Updates docs/release-notes/ files with entries from the changelog:\n"
                f"- index.md (features/enhancements, fixes)\n"
                f"- breaking-changes.md\n"
                f"- deprecations.md\n\n"
                f"**Do not merge until Release Day.**\n\n"
                f"> If CI fails, push a fix directly to the PR branch."
            ),
            repo=repo, labels=["needs_forward_port"],
        )

    # ── Create draft release ─────────────────────────────────────
    existing_release = gh(
        "release", "view", tag, "--repo", repo, "--json", "tagName",
        check=False,
    )
    if existing_release.returncode == 0:
        print(f"Release {tag} already exists — skipping.")
        draft_url = f"{repo_url}/releases/tag/{tag}"
    else:
        from release_automation.changelog import get_section_text
        git("checkout", f"origin/{release_branch}", "--", "CHANGELOG.next.md")
        body_text = get_section_text(version) or Path("CHANGELOG.next.md").read_text()[:3000]
        gh(
            "release", "create", tag,
            "--repo", repo,
            "--target", release_branch,
            "--title", f"ECS {version}",
            "--notes", body_text,
            "--draft",
        )
        draft_url = f"{repo_url}/releases/tag/{tag}"
        print(f"Created draft release: {tag}")

    # ── Check CI status ──────────────────────────────────────────
    ci_r = gh(
        "api", f"repos/{repo}/commits/{release_branch}/status",
        "--jq", ".state",
        check=False,
    )
    ci_status = ci_r.stdout.strip() if ci_r.returncode == 0 else "unknown"
    if ci_status != "success":
        print(f"::warning::CI on release branch is not passing (status: {ci_status})")

    # ── Summary ──────────────────────────────────────────────────
    summary = f"""# Release Preparation: ECS {version}

Previous release: v{prev_version}

## PRs Created (all gated -- do NOT merge yet)
1. **Finalize changelog**: {pr_cl_url}
   - Label: `needs_forward_port`
2. **Set version to {version}**: {pr_ver_url}
3. **Update release notes**: {pr_rn_url}
   - Label: `needs_forward_port`

## Draft Release
- {draft_url}

## docs-builder PR (manual)

Create a PR in `elastic/docs-builder` to update the current version selector:

```
# In elastic/docs-builder repo:
# Update config/assembler.yml: set ecs.current to {release_branch}
# Update config/versions.yml: set ecs.current to {release_branch}
```

Do not merge until Release Day.

## Next Steps
All PRs are parked. Run the **Release Day** workflow when ready to release.

> If CI fails on any auto-generated PR, push a fix directly to the PR branch.
"""
    write_summary(summary)


if __name__ == "__main__":
    main()
