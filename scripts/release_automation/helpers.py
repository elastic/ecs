"""Shared helpers for ECS release automation scripts.

Thin wrappers around subprocess, ``gh``, and ``git``, plus common
validation and GitHub PR/release operations.  Every runner script
imports from here instead of re-defining these utilities.
"""

import json
import os
import re
import subprocess
import sys


# ── Subprocess wrappers ──────────────────────────────────────────


def run(cmd: list[str], *, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=capture, text=True, check=check)


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["gh", *args], check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], check=check)


# ── GitHub Actions helpers ───────────────────────────────────────


def write_summary(text: str) -> None:
    """Append *text* to the GitHub Actions step summary (and stdout)."""
    path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if path:
        with open(path, "a") as f:
            f.write(text + "\n")
    print(text)


# ── Input validation ─────────────────────────────────────────────


def parse_version(argv: list[str], usage: str = "run.py <version>") -> str:
    """Extract and validate a ``X.Y.Z`` version from *argv*.

    Exits with a helpful error if the argument is missing or malformed.
    """
    if len(argv) < 2:
        print(f"Usage: {usage}", file=sys.stderr)
        sys.exit(1)
    version = argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"::error::Version must be in X.Y.Z format (got: {version})", file=sys.stderr)
        sys.exit(1)
    return version


def require_repo() -> str:
    """Return ``GITHUB_REPOSITORY`` or exit with an error."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        print("::error::GITHUB_REPOSITORY not set", file=sys.stderr)
        sys.exit(1)
    return repo


def release_branch_for(version: str) -> str:
    """``'9.4.0'`` -> ``'9.4'``"""
    major, minor, _ = version.split(".")
    return f"{major}.{minor}"


# ── Git identity & branch ops ────────────────────────────────────


def configure_bot_identity() -> None:
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")


def setup_branch(branch_name: str, base_ref: str) -> None:
    """Create and check out a fresh branch from *base_ref*."""
    git("checkout", "-b", branch_name, base_ref)


def commit_and_push(branch_name: str, message: str) -> None:
    """Stage all changes, commit (if any), and push."""
    git("add", "-A")
    configure_bot_identity()
    r = git("diff", "--cached", "--quiet", check=False)
    if r.returncode == 0:
        print("No changes to commit — skipping push.")
        return
    git("commit", "-m", message)
    git("push", "origin", branch_name)


# ── PR operations ────────────────────────────────────────────────


def find_open_pr(head: str, base: str, repo: str) -> dict | None:
    """Return the first open PR matching *head*/*base*, or ``None``.

    The returned dict contains at least ``number``, ``url``, ``title``.
    """
    r = gh(
        "pr", "list", "--repo", repo,
        "--head", head, "--base", base, "--state", "open",
        "--json", "number,url,title", "--limit", "1",
    )
    prs = json.loads(r.stdout)
    return prs[0] if prs else None


def find_merged_pr(head: str, base: str, repo: str) -> dict | None:
    """Return the first merged PR matching *head*/*base*, or ``None``.

    The returned dict contains at least ``number``, ``url``, ``title``.
    """
    r = gh(
        "pr", "list", "--repo", repo,
        "--head", head, "--base", base, "--state", "merged",
        "--json", "number,url,title", "--limit", "1",
    )
    prs = json.loads(r.stdout)
    return prs[0] if prs else None


def create_pr(
    head: str, base: str, title: str, body: str, repo: str,
    labels: list[str] | None = None,
) -> str:
    """Create a PR idempotently.  Returns the PR URL."""
    existing = find_open_pr(head, base, repo)
    if existing:
        print(f"PR already exists: {existing['url']} — skipping.")
        return existing["url"]

    cmd = ["pr", "create", "--repo", repo,
           "--head", head, "--base", base,
           "--title", title, "--body", body]
    if labels:
        for label in labels:
            cmd.extend(["--label", label])
    r = gh(*cmd)
    pr_url = r.stdout.strip()
    print(f"Created PR: {pr_url}")
    return pr_url


def count_labeled_prs(repo: str, label: str, state: str = "open") -> tuple[int, list[dict]]:
    """Return ``(count, [pr_dicts])`` for PRs with *label* in the given *state*."""
    r = gh(
        "pr", "list", "--repo", repo,
        "--label", label, "--state", state,
        "--json", "number,title,url", "--limit", "100",
    )
    prs = json.loads(r.stdout)
    return len(prs), prs


# ── Backport gate ────────────────────────────────────────────────


def require_no_backports(repo: str) -> None:
    """Exit with an error if merged PRs still carry ``needs_backport``.

    Open (unmerged) PRs with the label are expected and ignored — the
    label is forward-looking.  Only merged PRs indicate a backport that
    should have happened but hasn't.
    """
    count, prs = count_labeled_prs(repo, "needs_backport", state="merged")
    if count > 0:
        print(f"::error::Found {count} merged PRs still labeled needs_backport — resolve before proceeding.")
        for pr in prs:
            print(f"  - #{pr['number']}: {pr['title']} — {pr['url']}")
        sys.exit(1)


# ── Forward-port helpers ──────────────────────────────────────


def forward_port_targets(base_branch: str, repo: str, include_main: bool = True) -> list[str]:
    """Return remote branches strictly ahead of *base_branch*.

    For example, if *base_branch* is ``9.3`` and the repo has branches
    ``9.4``, ``9.5``, and ``main``, this returns:
      - ``["9.4", "9.5", "main"]`` when *include_main* is True
      - ``["9.4", "9.5"]`` when *include_main* is False

    Only considers branches matching ``X.Y`` semver format, optionally
    including ``main``.
    """
    r = git("ls-remote", "--heads", "origin")
    all_refs = [line.split("refs/heads/")[-1] for line in r.stdout.strip().splitlines()]

    semver_re = re.compile(r"^(\d+)\.(\d+)$")
    base_match = semver_re.match(base_branch)
    if not base_match:
        return ["main"] if include_main and "main" in all_refs else []

    base_major, base_minor = int(base_match.group(1)), int(base_match.group(2))

    targets = []
    for ref in all_refs:
        m = semver_re.match(ref)
        if m:
            ref_major, ref_minor = int(m.group(1)), int(m.group(2))
            if (ref_major, ref_minor) > (base_major, base_minor):
                targets.append((ref_major, ref_minor, ref))

    targets.sort()
    result = [t[2] for t in targets]

    if include_main and "main" in all_refs:
        result.append("main")

    return result


# ── Release operations ───────────────────────────────────────────


def derive_previous_version(repo: str, version: str = "") -> str:
    """Find the most recent non-prerelease, non-draft release tag.

    When *version* is supplied, the search is scoped to the same
    ``major.minor`` line so that e.g. releasing ``9.3.1`` finds ``9.3.0``
    rather than ``9.4.0``.
    """
    r = gh(
        "release", "list", "--repo", repo,
        "--json", "tagName,isPrerelease,isDraft", "--limit", "50",
    )
    releases = json.loads(r.stdout)

    prefix = ""
    if version:
        parts = version.split(".")
        if len(parts) >= 2:
            prefix = f"{parts[0]}.{parts[1]}."

    for rel in releases:
        if rel["isPrerelease"] or rel["isDraft"]:
            continue
        tag = rel["tagName"].lstrip("v")
        if prefix and not tag.startswith(prefix):
            continue
        return tag

    if prefix:
        for rel in releases:
            if not rel["isPrerelease"] and not rel["isDraft"]:
                return rel["tagName"].lstrip("v")

    print("::warning::Could not determine previous version tag. Using 0.0.0 as fallback.")
    return "0.0.0"
