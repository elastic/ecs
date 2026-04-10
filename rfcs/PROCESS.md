# Proposing changes to ECS

Changes to ECS are proposed as Requests for Comments (RFCs) in [rfcs/](./). A contributor opens a single **Proposal** pull request that is reviewed holistically by the ECS team. The goal is to thoroughly evaluate and verify the assumptions being made about a change before committing it to the schema.

Each RFC is a markdown document following the [template](./0000-rfc-template.md). If the RFC proposes new or changed fields, it should also include a corresponding folder in [rfcs/text/](./text/) named with the next available RFC number (check existing folders to find it; any duplicates will be corrected at merge) containing the proposed schema changes as standalone YAML files or extended example mappings and larger source documents.

## How a Proposal works

1. A contributor copies the [RFC template](./0000-rfc-template.md), fills in all sections, and opens a pull request.
2. The contributor specifies a **target maturity** of **alpha** or **beta** for the proposed fields. See [Field stability](../docs/reference/ecs-principles-design.md#_field_stability) for definitions.
3. The ECS team reviews the proposal in a single pass, evaluating the key questions below.
4. On approval the ECS team merges the PR and confirms the RFC number.
5. The proposed fields are added to the schema at the accepted maturity level (by the contributor or the ECS team). This step will be automated in the future so that field definitions are applied to the schema on merge of the Proposal PR.

GA promotion is handled separately through the field lifecycle process and does not require a new RFC. In the future, fields will be automatically promoted from beta to GA once an adoption threshold is met. If a proposal is no longer being pursued, the PR is simply closed.

## Key questions

* Is this change appropriate for ECS?
* Does this change provide enough utility for its intended use cases?
* Does this change strike a sufficient balance between introducing new fields and reusing existing common fields?
* Is ownership for the ongoing maintenance of this change clearly defined and accepted?
* Is the scope of impact of this change to ingestion, existing applications, and the ECS project itself understood?
* Are the technical details of the change defined clearly enough to implement in the schema?
* Are we confident these changes can be stable at the proposed maturity level?

## Responsibilities

The **ECS team**:
* evaluate whether the changes are appropriate in terms of the goals of the ECS project
* provide recommendations on which common fields would be best suited for reuse versus adding new fields
* determine the accepted maturity level (alpha or beta) and merge the Proposal PR
* provide procedural guidance for contributors
* curate the RFC process, including closing stalled or abandoned RFCs
* report on the status of open RFCs

The **contributor**:
* take responsibility for the legwork required to move their RFC forward, including responding to feedback, identifying and bringing in subject matter experts, and researching the scope of impact
* demonstrate how the proposed fields are expected to be used, from data source through to consumption
* create and iterate on the Proposal PR
