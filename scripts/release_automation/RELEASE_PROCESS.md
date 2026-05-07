# ECS Release Process

> All workflows are triggered from the [Actions tab](https://github.com/elastic/ecs/actions).

## Overview

| Phase | Workflow | Input | RM actions |
|---|---|---|---|
| Feature Freeze | `ecs-release-ff.yml` | `version` | Approve PRs |
| RC Cut | `ecs-release-rc.yml` | `version`, `rc_number` | Approve version PR |
| Release Preparation | `ecs-release-prep.yml` | `version` | Create docs-builder PR (manual) |
| Release Day | `ecs-release-day.yml` | `version` | Approve PRs, publish release |
| Post-release | `ecs-release-post.yml` | `version` | Resolve flagged items |

Event-driven workflows (no manual trigger):

| Workflow | Trigger | Purpose |
|---|---|---|
| `ecs-release-rc-tag.yml` | RC version PR merged (`release/*/set-rc*`) | Creates and publishes the RC pre-release tag |
| `backport-trigger.yml` | PR merged with `needs_backport` | Posts `/backport` for Mergify |
| `forward-port-trigger.yml` | PR merged with `needs_forward_port` on a release branch | Forward-ports to intermediate release branches |
| `port-label-cleanup.yml` | Port PR opened/labeled (`backport` or `forward_port`) | Removes `needs_backport` / `needs_forward_port` from source PRs once expected port PRs are opened |

---

## Minor Release (e.g. 9.4.0)

### 1. Feature Freeze

**Trigger**: "ECS Release: Feature Freeze" with `version` = `9.4.0`

The workflow blocks on merged PRs still labeled `needs_backport`, creates the `9.4` branch from `main`, then creates two PRs:
- **Main**: bumps version to `9.5.0-dev`, adds `9.4` to `.backportrc.json`, runs `make generate`
- **Release branch** (`9.4`): cuts changelog, labeled `needs_forward_port`

**RM actions**:
1. Verify CI passes on each PR (see [Bot-authored PR CI](#bot-authored-pr-ci) if it hasn't triggered)
2. Approve and merge the main PR
3. Approve and merge the release branch PR
4. Approve the forward-port PR(s) that Mergify creates after the changelog merges

### 2. RC Cut

**Trigger**: "ECS Release: RC Cut" with `version` = `9.4.0`, `rc_number` = `1`

Verifies the changelog section exists, then creates a PR on the release branch that sets the `version` file to `9.4.0-rc1` and runs `make generate`. Merging this PR automatically triggers the RC Tag workflow, which creates and publishes the `v9.4.0-rc1` pre-release. The tag always points to a commit where the version file matches the RC tag.

**RM actions**: Approve and merge the version PR. The pre-release is created automatically on merge. Share the RC with stakeholders.

### 3. Release Preparation

**Trigger**: "ECS Release: Preparation" with `version` = `9.4.0`

Blocks on merged PRs still labeled `needs_backport`, then creates three gated PRs on the release branch (changelog finalize, version set, release notes), a draft GitHub release, and logs instructions for the `docs-builder` PR.

**RM actions**: Create the `docs-builder` PR manually (instructions in the workflow summary). All other PRs are parked for Release Day.

### 4. Release Day

**Trigger**: "ECS Release: Release Day" with `version` = `9.4.0`

Prints a step summary with PR status and merge instructions.

**RM actions (in order)**:
1. Merge the version PR (sets to `9.4.0`)
2. Merge the changelog PR
3. Merge the release notes PR
4. Approve and merge the forward-port PRs to main (click "Update branch" if prompted)
5. Merge the `docs-builder` PR in `elastic/docs-builder`
6. **Publish** the draft release in GitHub UI
7. Ask the docs team in #docs Slack to trigger a build

### 5. Post-release

**Trigger**: "ECS Release: Post-release" with `version` = `9.4.0`

Verifies the release is published, flags outstanding `needs_forward_port` / `needs_backport` PRs, outputs docs verification URLs.

**RM actions**: Resolve any flagged items. Verify docs links.

---

## Patch Release (e.g. 9.3.1)

Patch releases use the same five workflows. Only the Feature Freeze step differs.

**Prerequisites**: Release branch (`9.3`) already exists, changes are backported, `CHANGELOG.next.md` entries are present.

### 1. Changelog Cut

**Trigger**: "ECS Release: Feature Freeze" with `version` = `9.3.1`

The workflow detects `patch > 0` and skips branch creation and the main PR. It only creates a changelog cut PR on the release branch (titled `9.3.1` without "Feature Freeze"), labeled `needs_forward_port`.

**RM actions**: Approve and merge the changelog PR, then approve the forward-port PRs.

### 2-5. RC Cut through Post-release

Same as minor release.

---

## Bot-authored PR CI

Bot PRs (`github-actions[bot]`) don't trigger `pull_request` CI automatically (GitHub security restriction). Current workaround:

- **Docs build**: comment `run docs-build` (handled by `elastic/docs-actions`)
- **Unit tests**: no comment-trigger exists yet. Close and re-open the PR, or push a trivial commit to the branch, to trigger CI.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Changelog section not found" | Run Feature Freeze / Changelog Cut first; ensure the PR is merged |
| "Outstanding needs_backport PRs" | Ensure expected backport PRs were created; if cleanup automation missed one, remove stale label manually |
| CI not running on bot PR | See [Bot-authored PR CI](#bot-authored-pr-ci) |
| CI fails on auto-generated PR | Push a fix to the PR branch; approvals are preserved |
| Forward-port PR has conflicts | Check out the branch, resolve, push |

All workflows are **idempotent** -- re-running after a partial failure is safe.

---

## Manual Fallback

All scripts run locally (stdlib + `gh` CLI only).

| Step | Command |
|---|---|
| Branch creation | `git push origin main:refs/heads/X.Y` |
| Version bump | Edit `version`, `make generate`, commit, push, create PR |
| Changelog cut (minor) | `python scripts/release_automation/changelog.py feature-freeze X.Y.Z` |
| Changelog cut (patch) | `python scripts/release_automation/changelog.py cut-release X.Y.Z` |
| Changelog finalize | `python scripts/release_automation/changelog.py finalize X.Y.Z PREV_VERSION REPO_URL` |
| RC / Release | GitHub UI > Releases > Draft a new release |
| Release notes | Extract entries then update: `python scripts/release_automation/changelog.py extract X.Y.Z > entries.json` then `python scripts/release_automation/release_notes.py X.Y.Z entries.json REPO_URL` |
| Porting | Comment `/backport <branches>` on the merged PR |
