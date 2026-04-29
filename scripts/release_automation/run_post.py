#!/usr/bin/env python3
"""ECS Release: Post-release entry point.

Called by ``ecs-release-post.yml`` with the version string.

Performs:
  1. Verifies the release is published (not draft)
  2. Checks for outstanding forward-port, backport PRs
  3. Writes a closeout summary with docs verification URLs
"""

import json
import sys

from release_automation.helpers import (
    count_labeled_prs,
    gh,
    parse_version,
    require_repo,
    write_summary,
)


def main() -> None:
    version = parse_version(sys.argv, usage="run_post.py <version>")
    repo = require_repo()

    tag = f"v{version}"

    # ── Verify release is published ──────────────────────────────
    r = gh(
        "release", "view", tag, "--repo", repo,
        "--json", "tagName,isDraft,isPrerelease,url",
        check=False,
    )
    if r.returncode != 0:
        print(f"::error::Release {tag} not found. Has it been created?", file=sys.stderr)
        sys.exit(1)

    release_data = json.loads(r.stdout)
    if release_data.get("isDraft"):
        print(f"::error::Release {tag} is still a draft. Publish it first.", file=sys.stderr)
        sys.exit(1)

    release_url = release_data.get("url", "")
    print(f"Release {tag} is published: {release_url}")

    # ── Check outstanding PRs ────────────────────────────────────
    fwd_count, fwd_prs = count_labeled_prs(repo, "needs_forward_port")
    fp_count, fp_prs = count_labeled_prs(repo, "forward_port")
    bp_count, bp_prs = count_labeled_prs(repo, "needs_backport")

    if fwd_count > 0:
        print(f"::warning::Found {fwd_count} outstanding needs_forward_port PRs")
    if fp_count > 0:
        print(f"::warning::Found {fp_count} unmerged forward_port PRs (may have conflicts)")
    if bp_count > 0:
        print(f"::warning::Found {bp_count} outstanding needs_backport PRs")

    # ── Summary ──────────────────────────────────────────────────
    def _pr_list(prs: list[dict]) -> str:
        if not prs:
            return "  None\n"
        return "".join(f"  - #{p['number']}: [{p['title']}]({p['url']})\n" for p in prs)

    all_clear = fwd_count == 0 and fp_count == 0 and bp_count == 0
    verdict = (
        f"All clear! Release {version} is complete."
        if all_clear
        else "Action required -- resolve outstanding PRs listed above."
    )

    summary = f"""# Post-release: ECS {version}

## Release Status
Release {tag} is published: {release_url}

## Outstanding PRs
- **needs_forward_port**: {fwd_count}
{_pr_list(fwd_prs)}
- **forward_port** (unmerged Mergify PRs): {fp_count} {"-- may have merge conflicts, check manually" if fp_count > 0 else ""}
{_pr_list(fp_prs)}
- **needs_backport**: {bp_count}
{_pr_list(bp_prs)}

## Docs Verification
Please verify the following URLs show the correct version:
- [ECS Reference](https://www.elastic.co/docs/reference/ecs)
- [ECS Field Reference](https://www.elastic.co/docs/reference/ecs/ecs-field-reference)

## {verdict}
"""
    write_summary(summary)


if __name__ == "__main__":
    main()
