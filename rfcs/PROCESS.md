# Proposing material changes to ECS

Changes to ECS are proposed as Requests for Comments (RFC) in [rfcs/](./) and iterated on through a series of [stages](https://elastic.github.io/ecs/stages.html). To advance to a specific stage, an RFC must meet the documented requirements for that stage. After being accepted into a given stage, there are stage-specific expectations and goals to be met. The overall goal of this process is to thoroughly evaluate and verify the assumptions being made about a change before formally committing it to the schema.

Each RFC is represented as a markdown document following a prescribed template that gets committed to the repo. Each stage of the RFC is represented as a pull request against that document.

If proposing new fields or changing existing fields, the RFC should also have a corresponding folder (named after the RFC number) in [rfcs/text/](./text/). The folder should contain the proposed schema changes as standalone YAML files or extended example mappings and larger source documents.

Generally speaking, the ECS team will help steward the process, but the work of researching and iterating on aspects of an RFC will be owned by that RFC's contributor. If an RFC is being contributed by a community member, then someone at Elastic will need to act as a sponsor of the change to act as a long term owner after completion of the process. The ECS team can help community users with identifying an internal sponsor. If it's not obvious who such a sponsor might be, then the ECS committee will assign a sponsor.

## Key questions we seek to answer through RFC process

* Is this change appropriate for ECS?
* Does this change provide enough utility for its intended use cases?
* Does this change strike a sufficient balance between introducing new fields and reusing existing common fields?
* Is ownership for the ongoing maintenance of this change clearly defined and accepted?
* Is the scope of impact of this change to ingestion, existing applications, and the ECS project itself understood?
* Are the technical details of the change defined clearly enough to implement in the schema?
* Are we confident these changes can be stable upon release without requiring revisions or breaking changes?
* Have our assumptions about the shape and utility of these changes been verified by real-world, production-ready usage?

## Goals with this contributing process

* Allow contributors to quickly iterate and receive feedback on their fields in a transparent way without the high bar set for general availability in the schema
* Clarify the level of stability to expect from a change in ECS while still allowing early adopters to try it out and provide feedback
* Offer assurance that once an RFC reaches stage 3, we're able to guarantee backward compatibility

## Responsibilities in this process

Member(s) of the **ECS committee**:
* evaluates whether the changes are appropriate in terms of the goals of the ECS project
* provides recommendations on which common fields would be best suited for reuse versus adding new fields
* determines whether each RFC is accepted into the next target stage by merging the RFC PR

The **ECS team**:
* provides procedural guidance for moving an RFC through stages
* curates the overall RFC process, including closing stalled or abandoned RFCs
* reports on the status of open RFCs
* acts on behalf of the committee for some but not all PRs
* helps community users identify a sponsor at Elastic

The **contributor**:
* takes responsibility for doing all necessary legwork to move their RFC forward including but not limited to responding to feedback, identifying and bringing in subject matter experts, and researching the scope of impact
* demonstrates how the fields in the RFC are expected to be used: from the data source, all the way to its consumption
* commits to iterating on the RFCs through to stage 3 if necessary
* creates and iterate on RFC PRs
* implements all necessary changes to their RFC PRs

The **sponsor** at Elastic:
* can be the same person as the contributor if they're someone at Elastic that can take ownership of this change through membership on the ECS committee
* is involved at least from stage 1 onward if a different person than the contributor
* signs off on each stage if a different person than the contributor
* takes or coordinates ownership of the addition in terms of support and maintenance after the RFC process is completed
