# Contributing to Elastic Common Schema (ECS)

All information related to ECS is versioned in this repository. All changes to ECS
happen through Git and Pull Requests.


## Requirements

To contribute to ECS the following tools are expected to be running on your machine:

* [Git](https://git-scm.com/)
* [Python](https://www.python.org/)
* [Go](https://golang.org/)

## Steps to contribute

To contribute changes to ECS follow the steps below:

* Create [your own fork](https://help.github.com/articles/fork-a-repo/) of the ECS repo.
* Clone your fork to your machine.
* Run `git checkout -b branch-name` and replace `branch-name` according to your change
* Apply your changes to the `.yml` files as needed
* Run `make` to update generated files like `schema.csv` and `schema.md`
* Run `git commit -a -m "your message"`
* Run `git push --set-upstream origin branch-name` (assumes your clone remote is called `origin`)
* Create a [Pull Request](https://help.github.com/articles/creating-a-pull-request/) against the ECS repo. (if you go to the website, it should pop up as a button with your branch directly)
* Wait for reviews on your PR and collaborate.

Notes: Make sure to always only push changes against your own fork.


## Fields.yml

`fields.yml` files are used to describe the Elastic Common Schema in a structured way. These files allow to generate an Elasticsearch index template, Kibana index pattern or documentation output out of it in an automated way.

The structure of the of each document looks as following:

```
- name: agent
  title: Agent fields
  group: 2
  description: >
    The agent fields contain all the data about the agent/client/shipper that collected / generated the events.

    As an example in case of beats for logs this is `agent.name` is `filebeat`.
  fields:
    - name: version
      type: keyword
      description: >
        Agent version.
      example: 6.0.0-rc2
      phase: 0
```

Each namespace has it's own file to keep the files itself small. Each namespace contains a list of fields which has all the fields inside. `title` and `description`  are used to describe the namespace. `level` is for pure sorting purpose in the documentation output.

Each field under `fields` has first the field `name`. The `type` is the [Elasticsearch field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html). `description` is used to add details about the field itself. With `example` an example value can be provided. The `phase` field is used to indicate in which `phase` the current field is (more about this below). In case `phase` is left out, it defaults to 0.

## Phases

The goal of the phase value for each field is to indicate if a field is already part of the standard or not. Different phases exist to make it easy to contribute new fields but still be able to iterate on top of it. The phases are defined as following:

* 0 (alpha): The field is new and is up for discussion if it should be added. The field might be removed at any time again.
* 1 (beta): It's clear that there is value of having the field in ECS and discussions about naming / namespaces etc. started. It's unlikely that the field is removed again but naming might change at any time.
* 2 (rc): The field has been accepted and is unlikely to change. It is now tested in the field.
* 3 (GA): The field is part of ECS and breaking changes to it happen only on major releases.

## Notes

### Host vs Hostname

* Host can contain hostname and port hostname:port
* Hostname never contains a port number
