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
- [Schema Files](#schema-files)
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

ECS documentation is written in [asciidoc](http://asciidoc.org/) format in the `docs/` directory.

To build the docs and open them in your browser:

```bash
make docs
```

### Generated Documentation Files

The following files are generated based on the current schema using [Jinja](https://jinja.palletsprojects.com/) templates:

| File | Template |
| ------------------ | -------- |
| [fields.asciidoc](docs/fields.asciidoc) | [fields_template.j2](scripts/templates/fields_template.j2) |
| [fields-values.asciidoc](docs/field-values.asciidoc) | [field_values_template.j2](scripts/templates/field_values_template.j2) |
| [field-details.asciidoc](docs/field-details.asciidoc) | [field_details.j2](scripts/templates/field_details.j2) |

Running `make` will update these files using the [scripts/generators/asciidoc_fields.py](scripts/generators/asciidoc_fields.py) generator. These doc files should *not* be modified directly. Any changes as a result of a schema update and subsequent run of `make` *should* be committed.

### Jinja Templates

Jinja templates allow for formatting or styling changes to templates without needing to modify the generator script directly. Some details about the Jinja template engine and our implementation are covered below as a primer; the full syntax and semantics of Jinja is covered in the [project's documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/).

#### Delimiters

* Statements: `{% ... %}`
* Expressions: `{{ ... }}`
* Comments: `{{# ... #}}`

#### Whitespace Control

Whitespace can be stripped by adding the minus sign (`-`) to the start or end of a block. Adding `-` to the start or end of a block will remove the whitespace before or after that block.

```
{% for i in numbers -%}
    {{i}}
{%- endfor %}
```

All elements would be rendered without any separating whitespace. If `numbers` is list of numbers from `0` to `9`, the output would be `0123456789`.

#### Variables

Templates variables are passed to the template by the application. Typically these will either be used in an expression or within a control structure statement (e.g. a `for` loop). In the below example, `users` is passed into the template and is iterated over with a `for` loop.

```python
<ul>
{% for user in users %}
<li>{{ user }}</li>
{% endfor %}
</ul>
```

#### Implementation

The `@templated('template_file_name')` decorator is used to inject the additional functionality that renders and returns the template's content to the generator. Decorated functions should return a dict used to generate the template. When the decorated function returns, the dictionary is passed to the template renderer.

```python
@templated('fields_template.j2')
def page_field_index(intermediate_nested, ecs_version):
    fieldsets = ecs_helpers.dict_sorted_by_keys(intermediate_nested, ['group', 'name'])
    return dict(ecs_version=ecs_version, fieldsets=fieldsets)
```

## Schema Files

The [schemas](schemas) directory contains the files which define the Elastic Common Schema data model. The file structure is documented in [schemas/README.md](schemas). Field additions and modifications will be made to the `schemas/*.yml` files.

Users consuming ECS to generate something for other use cases should use the `generated/ecs/*.yml` files. More detail can be found [here](generated/README.md).

### Subset Files

The [schemas/subsets](schemas/subsets/) directory contains the configuration to control advanced field nesting use cases.
The config is used with the `--subset` option to control which field sets or specific fields appear in the final generated
artifacts.

## Additional Resources

* [ECS Guidelines and Best Practices](https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html)
* [ECS Documentation](https://www.elastic.co/guide/en/ecs/current/index.html)
* [ECS on Elastic Discuss Forums](https://discuss.elastic.co/tag/ecs-elastic-common-schema)
* [#stack-ecs on the Elasticstack Community Slack](https://elasticstack.slack.com)
