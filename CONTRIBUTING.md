# Contributing to Elastic Common Schema (ECS)

All information related to ECS is versioned in the [elastic/ecs](https://github.com/elastic/ecs) repository. All changes to ECS
happen through Pull Requests submitted through Git.

ECS is an open source project and we love to receive contributions from our community - you!

## Table of Contents

- [How to Contribute](#how-to-contribute)
  - [Dev Tools](#dev-tools)
  - [Submitting Changes](#submitting-changes)
- [Git and Github Guidelines](#git-and-github-guidelines)
  - [Forking](#forking)
  - [Commits and Merging](#commits-and-merging)
  - [Issues](#issues)
- [Documentation](#documentation)
- [Schema Files](#schema-files)
- [Additional Resources](#additional-resources)

## How to Contribute

### Dev Tools

You need these tools to contribute to ECS:

* [Git](https://git-scm.com/)
* [Python 3.6+](https://www.python.org/)
* [Go 1.13](https://golang.org/)

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
* Commit your changes locally.
  - Run `git commit -a -m "your message"`
* Push your changes to your own github.com fork.
  - Run `git push --set-upstream origin branch-name`
  - In this command, `origin` is an alias that references your fork.
* Request feedback about your changes.
  - Create a [Pull Request](https://help.github.com/articles/creating-a-pull-request/) against the ECS repo.
    - (Look for the `Compare & pull request` button on your branch in github.com.)
  - Wait for reviews on your PR.
  - Incorporate review comments and push updates if needed.
* Thank you for your contribution!

**Important:** Be sure to push changes only to your own fork. Changes must be approved before they are merged into the main repository.

## Git and Github Guidelines

### Forking

We follow the [Github forking model](https://help.github.com/articles/fork-a-repo/) for collaboration in the ECS repo. Typically contributors will add a remote repository called `upstream` to point to the Elastic ECS repo to add latest changes from the repo to their fork.

### Commits and Merging

* When submitting a PR for review, please perform and interactive rebase to clean up the commit history. A logical commit history is easier for reviewers to follow.
* Use meaningful and helpful commit messages on your changes and an explanation of _why_ you made those changes.
* When merging, maintainers will squash your commits into a single commit.

### Pull Requests

Please follow these guidelines when submitting PRs:

* Include an explanation of your changes in the PR description.
* Links to relevant issues, external resources, or related PRs are helpful and useful.
* Update any tests or add new tests where appropriate.

### Issues

Please follow these guidelines when submitting Issues:

* Go to the ECS repo: https://github.com/elastic/ecs
* Click `Issues` in the nav bar under the repo name.
* Click `New issue`. Provide as many details as possible to help reviewers and other contributors understand your proposal.
* Add your text, and click `Submit new issue`.


## Documentation

ECS documentation is written in [asciidoc](http://asciidoc.org/) format in the `docs/` directory.

To build the docs and open them in your browser:

```bash
make docs
```

## Schema Files

The [schemas](schemas) directory contains the files which define the Elastic Common Schema data model. The file structure is documented in [schemas/README.md](schemas). Field additions and modifications will be made to the `schemas/*.yml` files.

Users consuming ECS to generate something for other use cases should use the `generated/ecs/*.yml` files. More detail can be found [here](generated/README.md).

## Additional Resources

* [ECS Guidelines and Best Practices](https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html)
* [ECS Documentation](https://www.elastic.co/guide/en/ecs/current/index.html)
* [ECS on Elastic Discuss Forums](https://discuss.elastic.co/tag/elastic-common-schema)
* [#ecs on the Elasticstack Community Slack](https://elasticstack.slack.com)
