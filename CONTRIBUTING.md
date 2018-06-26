# Contributing to Elastic Common Schema (ECS)

All information related to ECS is versioned in this repository. All changes to ECS
happen through Git and Pull Requests.


## Requirements

You need these tools to contribute to ECS:

* [Git](https://git-scm.com/)
* [Python](https://www.python.org/)
* [Go](https://golang.org/)

## Steps to contribute

Here are the steps for contributing to ECS.

* Set up your git environment.
  - Create [your own fork](https://help.github.com/articles/fork-a-repo/) of the ECS repo.
  - Clone your fork to your machine.
* Create a working branch on your machine.
  - Run `git checkout -b branch-name`, where `branch-name` is the name you want to give your local branch
* Do your work. 
  - Make changes to the `.yml` files as needed
* Run `make` to update generated files such as `schema.csv` and `schema.md`
* Commit your changes locally. 
  - Run `git commit -a -m "your message"`
* Commit your changes to your own github.com fork.
  - Run `git push --set-upstream origin branch-name` 
  - In this command, `origin` is an alias that references your fork )
* Request feedback and permission to merge your changes. 
  - Create a [Pull Request](https://help.github.com/articles/creating-a-pull-request/) against the ECS repo. 
  - (Look for the `Compare & pull request` button on your branch in github.com)
* Next steps
  - Wait for reviews on your PR.
  - Incorporate review comments and push updates if needed.
* Thank you for your contribution!
  
Important: Make sure to push changes only to your own fork. Changes must be approved before they are merged into the main repository.

## Fields.yml

The `fields.yml` files describe the Elastic Common Schema in a structured way. We can use these files to generate an Elasticsearch index template, a Kibana index pattern, or documentation output .

The file structure is similar to this:

```
- name: agent
  title: Agent fields
  group: 2
  description: >
    The agent fields contain all the data about the agent/client/shipper that collected/generated the events.

    As an example in case of beats for logs this is `agent.name` is `filebeat`.

  footnote: >
    This tag is optional. Use it if you want to add more information after the field table. 
    For example, you can use to show examples of how several fields might work together. 
  fields:
    - name: version
      type: keyword
      description: >
        Agent version.
      example: 6.0.0-rc2
      phase: 0
```

Each namespace has its own file. The fields for each namespace are stored in the file. `title` and `description` describe the namespace. `level` is for sorting in the documentation output.

In the `fields` section, the `name` of the field is the first entry. 
The `type` is the [Elasticsearch field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html). 
`description` adds details about the field. 
`example` adds an sample value.
The `phase` field indicates the development status of the field. If `phase` is left out, the default is 0. See 

## Phases

A field's `phase` indicates where it is in its development. Different phases exist to make it easy for you to contribute new fields, while allowing for more iteration. Here are the phases:

* 0 (alpha): The field is new and is up for discussion as to whether or not it should be added. The field might be removed at any time.
* 1 (beta): It's clear that there is value of having the field in ECS and discussions about naming/namespaces have started. It's unlikely that the field will be removed, but naming might change at any time.
* 2 (rc): The field has been accepted and is unlikely to change. It is now tested in the field.
* 3 (GA): The field is part of ECS. Any breaking changes will happen only at a major release.

## Guidelines for implementing ECS

* The document MUST have the `@timestamp` field.
* The [data type](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/mapping-types.html) defined for an ECS field MUST be used.
* It SHOULD have the field `event.version` to define which version of ECS it uses.
* As many fields as possible should be mapped to ECS.

### Writing fields

* All fields must be lower case
* Combine words using underscore
* No special characters except `_`

### Naming fields

* *Present tense.* Use present tense unless field describes historical information.
* *Singular or plural.* Use singular and plural names properly to reflect the field content. For example, use `requests_per_sec` rather than `request_per_sec`.
* *General to specific.* Organise the prefixes from general to specific to allow grouping fields into objects with a prefix like `host.*`.
* *Avoid repetition.* Avoid stuttering of words. If part of the field name is already in the prefix, do not repeat it. Example: `host.host_ip` should be `host.ip`.
* *Use prefixes.* Fields must be prefixed except for the base fields. For example all `host` fields are prefixed with `host.`. See `dot` notation in FAQ for more details.
* Do not use abbreviations. (A few exceptions like `ip` exist.)

### Implementation details

* Host can contain hostname and port (hostname:port)
* Hostname never contains a port number

