# Contributing to Elastic Common Schema (ECS)

All information related to ECS is versioned in the [elastic/ecs](https://github.com/elastic/ecs) repository. All changes to ECS
happen through Pull Requests submitted through Git.


## Requirements

You need these tools to contribute to ECS:

* [Git](https://git-scm.com/)
* [Python 2.7](https://www.python.org/)
* [Go 1.11](https://golang.org/)

## Steps to contribute

Here are the steps for contributing to ECS.

* Set up your git environment.
  - Create [your own fork](https://help.github.com/articles/fork-a-repo/) of the ECS repo.
  - Clone your fork to your machine.
* Create a local branch to hold your changes.
  - Run `git checkout -b branch-name`, where `branch-name` is the name you want to give your local branch
* Do your work.
  - Make changes to the `.yml` files under the `schemas` directory.
* Run `make` to update generated files.
  - Note that the README.md file is generated, and should not be edited directly. Source files are in the /docs directory.
* Commit your changes locally.
  - Run `git commit -a -m "your message"`
* Push your changes to your own github.com fork.
  - Run `git push --set-upstream origin branch-name`
  - In this command, `origin` is an alias that references your fork.
* Request feedback and permission to merge your changes.
  - Create a [Pull Request](https://help.github.com/articles/creating-a-pull-request/) against the ECS repo.
  - (Look for the `Compare & pull request` button on your branch in github.com.)
* Next steps
  - Wait for reviews on your PR.
  - Incorporate review comments and push updates if needed.
* Thank you for your contribution!

**Important:** Be sure to push changes only to your own fork. Changes must be approved before they are merged into the main repository.

### Other ways to contribute

You can contribute even if you are not an experienced Git user. You'll need a github.com account.
* Go to the ECS repo: https://github.com/elastic/ecs
* Click `Issues` in the nav bar under the repo name.
* Click `New issue`. Provide as many details as possible to help reviewers and other contributors understand your proposal.
* Add your text, and click `Submit new issue`.

## Fields.yml

The `fields.yml` files describe the Elastic Common Schema in a structured way. We can use these files to generate an Elasticsearch index template, a Kibana index pattern, or documentation output.

The file structure is documented in [schemas/README.md](schemas).

It looks similar to this:

```
- name: agent
  title: Agent
  group: 2
  description: >
    The agent fields contain the data about the software entity, if any, that collects, detects, or observes events on a host, or takes measurements on a host. Examples include Beats. Agents may also run on observers. ECS agent.* fields shall be populated with details of the agent running on the host or observer where the event happened or the measurement was taken.
  footnote: >
    Examples: In the case of Beats for logs, the agent.name is filebeat. For APM, it is the
    agent running in the app/service. The agent information does not change if
    data is sent through queuing systems like Kafka, Redis, or processing systems
    such as Logstash or APM Server.
  type: group
  fields:

    - name: version
      level: core
      type: keyword
      description: >
        Version of the agent.

      example: 6.0.0-rc2
```

Each prefix has its own file. The fields for each prefix are stored in the file. `title` and `description` describe the prefix. `footnote` adds more information following the field table. `level` is for sorting in the documentation output.

In the `fields` section, the `name` of the field is the first entry.
The `type` is the [Elasticsearch field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).
`description` adds details about the field.
`example` adds an sample value.

## Guidelines for implementing ECS

Look at our [Guidelines and Best Practices](https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html) on the ECS documentation website.
