#!/usr/bin/env python3
"""ECS Release: Feature Freeze entry point.

Called by the ``ecs-release-ff.yml`` workflow with a single argument:
the version string (e.g. ``9.4.0``).

Performs:
  1. Validates version format
  2. Checks for outstanding needs_backport PRs (warning only)
  3. Creates the release branch from main
  4. Creates a combined PR on main (version bump + backportrc update)
  5. Creates a changelog PR on the release branch
  6. Writes a GitHub Actions step summary
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], *, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=capture, text=True, check=check)


def _gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return _run(["gh", *args], check=check)


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return _run(["git", *args], check=check)


def write_summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if path:
        with open(path, "a") as f:
            f.write(text + "\n")
    print(text)


def _find_existing_pr(head: str, base: str, repo: str) -> str | None:
    """Return the URL of an existing open PR, or None."""
    r = _gh(
        "pr", "list", "--repo", repo,
        "--head", head, "--base", base, "--state", "open",
        "--json", "number,url", "--limit", "1",
    )
    prs = json.loads(r.stdout)
    return prs[0]["url"] if prs else None


def _create_pr(head: str, base: str, title: str, body: str, repo: str,
               labels: list[str] | None = None) -> str:
    """Create a PR idempotently.  Returns the PR URL."""
    existing = _find_existing_pr(head, base, repo)
    if existing:
        print(f"PR already exists: {existing} — skipping.")
        return existing

    cmd = ["pr", "create", "--repo", repo,
           "--head", head, "--base", base,
           "--title", title, "--body", body]
    if labels:
        for label in labels:
            cmd.extend(["--label", label])
    r = _gh(*cmd)
    pr_url = r.stdout.strip()
    print(f"Created PR: {pr_url}")
    return pr_url


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: run_ff.py <version>", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"::error::Version must be in X.Y.Z format (got: {version})", file=sys.stderr)
        sys.exit(1)

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        print("::error::GITHUB_REPOSITORY not set", file=sys.stderr)
        sys.exit(1)

    major, minor, _ = version.split(".")
    release_branch = f"{major}.{minor}"
    next_minor = int(minor) + 1
    next_version = f"{major}.{next_minor}.0-dev"

    # ── Check outstanding needs_backport PRs ─────────────────────
    r = _gh("pr", "list", "--repo", repo,
            "--label", "needs_backport", "--state", "open",
            "--json", "number,title,url", "--limit", "100")
    backport_prs = json.loads(r.stdout)
    backport_count = len(backport_prs)
    if backport_count > 0:
        print(f"::warning::Found {backport_count} outstanding needs_backport PRs")

    # ── Create release branch ────────────────────────────────────
    r = _git("ls-remote", "--exit-code", "--heads", "origin", release_branch, check=False)
    branch_created = False
    if r.returncode != 0:
        _git("push", "origin", f"main:refs/heads/{release_branch}")
        print(f"Created branch '{release_branch}' from main")
        branch_created = True
    else:
        print(f"Branch '{release_branch}' already exists — skipping creation.")

    # ── PR 1: Version bump + backportrc on main ──────────────────
    pr_branch_main = f"release/{version}/bump-main"
    existing_main = _find_existing_pr(pr_branch_main, "main", repo)
    if existing_main:
        pr_main_url = existing_main
        print(f"Main PR already exists: {existing_main}")
    else:
        _git("checkout", "-b", pr_branch_main, "origin/main")
        Path("version").write_text(next_version + "\n")

        # Update .backportrc.json
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
            _run(["make", "ve"], check=False)
            _run(["make", "generate"], check=False)

        _git("add", "-A")
        _git("config", "user.name", "github-actions[bot]")
        _git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        _git("commit", "-m", f"Bump version to {next_version} and add {release_branch} to backportrc")
        _git("push", "origin", pr_branch_main)

        pr_main_url = _create_pr(
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

    # ── PR 2: FF changelog on release branch ─────────────────────
    pr_branch_cl = f"release/{version}/ff-changelog"
    existing_cl = _find_existing_pr(pr_branch_cl, release_branch, repo)
    if existing_cl:
        pr_cl_url = existing_cl
        print(f"Changelog PR already exists: {existing_cl}")
    else:
        _git("fetch", "origin", release_branch)
        _git("checkout", "-b", pr_branch_cl, f"origin/{release_branch}")

        from ecs_release.changelog import cut_feature_freeze
        cut_feature_freeze(version, repo_root=".")

        _git("add", "-A")
        _git("config", "user.name", "github-actions[bot]")
        _git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        _git("commit", "-m", f"{version} Feature Freeze changelog")
        _git("push", "origin", pr_branch_cl)

        pr_cl_url = _create_pr(
            head=pr_branch_cl, base=release_branch,
            title=f"{version} Feature Freeze changelog",
            body=(
                f"## Automated Feature Freeze Changelog\n\n"
                f"- Creates new empty Unreleased section\n"
                f"- Renames previous Unreleased to \"{version} (Feature Freeze)\"\n"
                f"- Sorts entries by PR ID\n"
                f"- Removes empty sections\n\n"
                f"> If CI fails, push a fix directly to the PR branch.\n\n"
                f"After merge, Mergify will create a forward-port PR to main."
            ),
            repo=repo,
            labels=["needs_forward_port"],
        )

    # ── Summary ──────────────────────────────────────────────────
    summary = f"""# Feature Freeze: ECS {version}

## Outstanding needs_backport PRs: {backport_count}
{"Warning: review these before proceeding." if backport_count > 0 else ""}

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
