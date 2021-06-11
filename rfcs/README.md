# Elastic Common Schema RFCs

While smaller and less controversial changes can still be made directly through pull requests, more substantial changes follow a multi-stage RFC process to ensure they are sufficiently thought out and vetted before being released for general availability in the schema.

The types of changes that warrant this RFC process include but are not limited to:

* Breaking changes targeting the next major version
* New top level fieldsets
* New fields to accommodate an unaddressed use case
* Changes that would alter the scope of ECS as a whole

Check out [Proposing Changes](./PROCESS.md) for high level information about the RFC process.

Check out the [series of stages](https://elastic.github.io/ecs/stages.html) an RFC will go through to be fully vetted.

## How this works

It's important to understand the overall goals and intentions of the RFC process, so it is recommended that you read this and the document listed above. When you're ready to dive in,

1. Create a new RFC document from the RFC template (described below)
2. Fill in the details for your strawperson
3. Open a PR to commit your RFC to [rfcs/](./)
4. ECS committee and/or team members review
5. ECS committee and/or team member merges RFC, formally accepting the strawperson
6. Expand existing RFC document with additional details
7. Open a PR to commit your proposed changes to the RFC and advance to stage 1
8. ECS committee and/or team members review
9. ECS committee and/or team member merges RFC, formally accepting the proposal
10. Repeat steps 6-9 for stages 2 and 3

## Using the RFC template

All new RFCs should be started by copying [0000-rfc-template.md](./0000-rfc-template.md) with a name format of `0000-<dash-separated-name>.md`. When the first RFC stage is accepted, the ECS team will assign a unique RFC number, which will identify this RFC throughout all stages of the process.

Throughout the RFC template are comments that provide guidance on what type of content to include in each stage. It's ideal if you remove comments from your RFC as you fill out the content and they become obsolete. A pristine, finished RFC will have no explanatory comments remaining.

For the most part, content is additive as you move through the stages. Occasionally, advancing a stage will require modifying existing content. This is OK! This process should be iterative, and the RFC document is considered living until it is finished (i.e. accepted as stage 3).

## Skipping stages

While advancing through multiple stages at a time is possible if all the necessary information is provided and thoroughly vetted, moving changes through stage by stage provides the greatest opportunity to iterate efficiently on changes and a much lower chance of an author wasting a ton of their time.

## Abandoning RFCs

If an RFC proposed change is no longer being pursued or has been inactive for an extended time period, the RFC should be assigned to stage X.
