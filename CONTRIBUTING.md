# Contributing to Elastic Common Schema (ECS)

All information related to ECS is versioned in the [elastic/ecs](https://github.com/elastic/ecs) repository. All changes to ECS
happen through Pull Requests submitted through Git.

ECS is an open source project and we love to receive contributions from our community - you!

## Table of Contents

- [How to contribute](#how-to-contribute)
- - [Special guidance during OTel donation of ECS](#special-guidance-during-otel-donation-of-ecs)
  - [Dev Tools](#dev-tools)
  - [Submitting Changes](#submitting-changes)
- [Git and Github Guidelines](#git-and-github-guidelines)
  - [Forking](#forking)
  - [Commits and Merging](#commits-and-merging)
  - [Issues](#issues)
- [Feature freezes and branching](#feature-freezes-and-branching)
  - [Changelogs](#changelogs)
  - [Backports](#backports)
    - [Tooling](#tooling)
- [Documentation](#documentation)
  - [Generated Documentation Files](#generated-documentation-files)
  - [Jinja Templates](#jinja-templates)
- [Schema Files](#schema-files)
  - [OTel Mappings](#otel-mappings)
  - [Subset Files](#subset-files)
- [Additional Resources](#additional-resources)


## How to contribute

### ECS donation to OpenTelemetry

In April 2023, Elastic and OpenTelemetry made an [important joint announcement](https://opentelemetry.io/blog/2023/ecs-otel-semconv-convergence/): Elastic intends to align the Elastic Common Schema (ECS) with
OpenTelemetry (OTel) Semantic Conventions, aiming to create a unified, community-maintained standard under OpenTelemetry.

During the contribution process, several guidelines have been added to allow contributions to ECS, ensuring they are aligned with OpenTelemetry.

#### How to contribute during ECS donation to OpenTelemetry

While ECS is being contributed to OpenTelemetry, schema changes are still possible—but they should align with how the changes could eventually be integrated into OpenTelemetry.

For significant changes—like new top-level fieldsets, use cases, or anything potentially controversial—follow the [ECS RFC process](rfcs/PROCESS.md).

Minor changes (e.g., bug fixes or small field additions) can go directly through pull requests to the ECS repository.

When writing RFCs or designing fields, keep compatibility with OTel in mind. Pay close attention to naming, data types, and potential overlaps or conflicts with existing or proposed semantic conventions. Contributors should seek guidance from ECS maintainers or the Semantic Conventions community if in doubt.

Any changes proposed for ECS should also be submitted to the [OpenTelemetry Semantic Conventions repository](https://github.com/open-telemetry/semantic-conventions)—either before or in parallel; however, your Otel PR does not need to be merged first.

#### ECS releases during the donation to OpenTelemetry

ECS will be released at the discretion of the ECS team as schema changes are approved. Releases will not necessarily align with every Elastic Stack release.

While ECS updates will coincide with Elastic Stack releases, not every stack version will trigger an ECS release.

### Dev Tools

You need these tools to contribute to the ECS repo:

* [Git](https://git-scm.com/)
* [Python 3.8+](https://www.python.org/)
* Python dependencies: run `pip install -r scripts/requirements.txt` after cloning.
  Using a virtualenv is recommended. Running `make ve` will create one automatically.

### Submitting Changes

* Sign the [Contributor License Agreement](http://www.elastic.co/contributor-agreement/).
* Set up your git environment.
  - Create [your own fork](https://help.github.com/articles/fork-a-repo/) of the ECS repo.
  - Clone your fork to your machine.
* Create a local branch to hold your changes.
  - Run `git checkout -b branch-name`, where `branch-name` is the name you want to give your local branch
* Do your work.
  - Schema changes will be done in the `.yml` files under the `schemas` directory. Review the [Schema Files](#schema-files) section below.
  - Generator scripts and other tooling reside in the `scripts` directory.
  - Generated artifacts fall under the `generated` directory.
  - Documentation files are located in the `docs` directory.
* Run `make` to update generated files.
* If necessary, make sure tests pass.
  - Run `make test`
  - Add tests for your changes, if necessary
* Run `make check` to verify that all generated files are up-to-date.
* Commit your changes locally.
  - Run `git commit -a -m "your message"`
* Push your changes to your own github.com fork.
  - Run `git push --set-upstream origin branch-name`
  - In this command, `origin` is an alias that references your fork.
* Request feedback about your changes.
  - Create a [Pull Request](https://help.github.com/articles/creating-a-pull-request/) against the ECS repo.
    - (Look for the `Compare & pull request` button on your branch in github.com.)
  - Include an explanation of your changes in the PR description.
  - Add links to relevant issues, external resources, or related PRs.
  - Add an entry to [CHANGELOG.next.md](CHANGELOG.next.md).
  - Wait for reviews on your PR.
  - Incorporate review comments and push updates if needed.
* Thank you for your contribution!

**Important:** Be sure to push changes only to your own fork. Changes must be approved before they are merged into the main repository.

## Git and Github Guidelines

### Forking

We follow the [Github forking model](https://help.github.com/articles/fork-a-repo/) for collaboration in the ECS repo. Typically contributors will add a remote repository called `upstream` to point to the Elastic ECS repo to add latest changes from the repo to their fork.

### Commits and Merging

* Use meaningful and helpful commit messages on your changes and an explanation of _why_ you made those changes.
* When merging, maintainers will squash your commits into a single commit.

### Pull Requests

Please follow these guidelines when submitting PRs:

* Include an explanation of your changes in the PR description.
* Links to relevant issues, external resources, or related PRs are helpful and useful.
* Update any tests or add new tests where appropriate.
* Include a changelog entry summarizing your changes with a link to the PR.

### Issues

Please follow these guidelines when submitting Issues:

* Go to the ECS repo: https://github.com/elastic/ecs
* Click `Issues` in the nav bar under the repo name.
* Click `New issue`. Provide as many details as possible to help reviewers and other contributors understand your proposal.
* Add your text, and click `Submit new issue`.

## Feature freezes and branching

For an upcoming release, ECS uses a feature freeze (FF) approach. A release branch is cut from `main` for an upcoming
release. When a branch is frozen, changes are limited to bug fixes or doc updates.

Any schema changes or tooling updates will be merged into `main` for the next ECS version.

### Changelogs

ECS maintains two changelog files:

* [CHANGELOG.md](CHANGELOG.md) contains a list of notable changes for each released version of ECS.
* [CHANGELOG.next.md](CHANGELOG.next.md) contains a list of unreleased ECS changes.

Breaking changes intended for the next major version should be included underneath the `Breaking changes` sections in `CHANGELOG.next.md`.

### Backports

ECS maintains multiple release branches in the repo. The `main` branch is where all new contributions should be submitted, and features and bug fixes will be backported into other branches when appropriate. Any backporting needs will be handled by the ECS team.

#### Tooling

Refer to the backport tool's [repo](https://github.com/sqren/backport#requirements) for requirements and install guide. A [project config](.backportrc.json) is maintained in the root of this repo.

Run:

```bash
$ npx backport --pr 1234
```

Select target branch(es) to backport to:

```bash
? Select commit #1234 (cb79e8f5)
? Select branch (Press <space> to select, <a> to toggle all, <i> to invert selection)
❯◯ 8.1
 ◯ 8.0
 ◯ 1.12
...
```

New PR(s) will be opened against the targeted branch(es).

## Documentation

ECS documentation is written in [Markdown](https://www.markdownguide.org/) format in the `docs/` directory.

To build and preview the docs locally in your browser:

```bash
make docs
```

This downloads the Elastic [`docs-builder`](https://github.com/elastic/docs-builder) tool automatically (cached in `build/docs/`) and starts a local documentation server.

### Generated Documentation Files

The following files are generated from the current schema by [scripts/generators/markdown_fields.py](scripts/generators/markdown_fields.py) using [Jinja2](https://jinja.palletsprojects.com/) templates located in [scripts/templates/](scripts/templates/):

| Output file | Template |
| --- | --- |
| [docs/reference/index.md](docs/reference/index.md) | [index.j2](scripts/templates/index.j2) |
| [docs/reference/ecs-field-reference.md](docs/reference/ecs-field-reference.md) | [ecs_field_reference.j2](scripts/templates/ecs_field_reference.j2) |
| `docs/reference/ecs-{name}.md` (one per fieldset) | [fieldset.j2](scripts/templates/fieldset.j2) |
| [docs/reference/ecs-otel-alignment-overview.md](docs/reference/ecs-otel-alignment-overview.md) | [otel_alignment_overview.j2](scripts/templates/otel_alignment_overview.j2) |
| [docs/reference/ecs-otel-alignment-details.md](docs/reference/ecs-otel-alignment-details.md) | [otel_alignment_details.j2](scripts/templates/otel_alignment_details.j2) |

Running `make` regenerates all of these files. They should **not** be modified directly. Any changes produced by a schema update and subsequent `make` run **should** be committed.

### Jinja Templates

The templates in `scripts/templates/` use [Jinja2](https://jinja.palletsprojects.com/) syntax. Formatting or structural changes to the generated docs can be made by editing the relevant `.j2` file without touching the Python generator.

Key syntax elements:

* Statements: `{% ... %}`
* Expressions: `{{ ... }}`
* Comments: `{# ... #}`
* Whitespace stripping: add `-` to the start or end of a block tag (e.g. `{%- ... -%}`)

Each page-generation function in `markdown_fields.py` is decorated with `@templated('template_name.j2')` and returns a dict that becomes the template's rendering context.

For a full guide to the template system—including how to add new page types, modify field display order, and troubleshoot rendering issues—see [scripts/docs/markdown-generator.md](scripts/docs/markdown-generator.md).

## Schema Files

The [schemas](schemas) directory contains the files which define the Elastic Common Schema data model. The file structure is documented in [schemas/README.md](schemas). Field additions and modifications will be made to the `schemas/*.yml` files.

Users consuming ECS to generate something for other use cases should use the `generated/ecs/*.yml` files. More detail can be found [here](generated/README.md).

### OTel Mappings

Because ECS is being aligned with OpenTelemetry Semantic Conventions, ECS fields that overlap with or relate to OTel Semantic Conventions should declare that relationship via an `otel:` block in the relevant `schemas/*.yml` file. This metadata is validated during generation and used to produce the [OTel alignment documentation](docs/reference/ecs-otel-alignment-overview.md).

A field's `otel:` entry is a list of mappings, each with a `relation` type:

| Relation | Meaning |
| --- | --- |
| `match` | Identical name and semantics in OTel |
| `equivalent` | Semantically equivalent but different name; requires `attribute` |
| `related` | Related concept, not identical; requires `attribute` |
| `conflict` | Conflicting definition; requires `attribute`; `note` is recommended |
| `metric` | Maps to an OTel metric (not an attribute); requires `metric` |
| `otlp` | Maps to an OTLP protocol field; requires `otlp_field` and `stability` |
| `na` | Not applicable to OTel |

Example:

```yaml
- name: request.method
  otel:
    - relation: match
```

```yaml
- name: version
  otel:
    - relation: related
      attribute: network.protocol.version
      note: In OTel, network.protocol.version specifies the HTTP version only when network.protocol.name is "http".
```

Fields without an `otel:` block will produce a warning during generation if an OTel attribute with a matching name exists. Add `otel: [{relation: na}]` to suppress the warning for fields that intentionally have no OTel mapping.

For the full reference—including all relation types, validation rules, and how to update the OTel semconv version—see [scripts/docs/otel-integration.md](scripts/docs/otel-integration.md).

### Subset Files

The [schemas/subsets](schemas/subsets/) directory contains the configuration to control advanced field nesting use cases.
The config is used with the `--subset` option to control which field sets or specific fields appear in the final generated
artifacts.

## Additional Resources

* [ECS Guidelines and Best Practices](https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html) — field naming and design conventions
* [ECS Documentation](https://www.elastic.co/guide/en/ecs/current/index.html) — official published reference
* [ECS on Elastic Discuss Forums](https://discuss.elastic.co/tag/ecs-elastic-common-schema) — community questions and discussion
* [#stack-ecs on the Elasticstack Community Slack](https://elasticstack.slack.com) — real-time community chat
* [Tooling Usage Guide](USAGE.md) — how to run the generator, subset generation, custom fields, and all generator options
* [Developer Documentation Index](scripts/docs/README.md) — in-depth guides for the schema pipeline, each generator module, and how to extend them
* [OTel Integration Guide](scripts/docs/otel-integration.md) — OTel mapping reference, validation rules, and updating the semconv version
