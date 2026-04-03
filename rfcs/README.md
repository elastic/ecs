# Elastic Common Schema RFCs

While smaller and less controversial changes can still be made directly through pull requests, more substantial changes follow the RFC process to ensure they are sufficiently thought out and vetted before being added to the schema.

The types of changes that warrant an RFC include but are not limited to:

* Breaking changes targeting the next major version
* New top level fieldsets
* New fields to accommodate an unaddressed use case
* Changes that would alter the scope of ECS as a whole

Check out [Proposing Changes](./PROCESS.md) for high level information about the RFC process.

## How this works

1. Copy the [RFC template](./0000-rfc-template.md) with a name format of `0000-<dash-separated-name>.md`.
2. Fill in all sections of the template, including the target maturity (alpha or beta) for the proposed fields.
3. Open a PR to commit your RFC to [rfcs/](./).
4. The ECS committee reviews the proposal and provides feedback.
5. On approval the committee merges the PR, and the ECS team assigns a unique RFC number.

If the RFC includes field additions or modifications, create a folder named after the RFC number under [rfcs/text/](./text/). This is where proposed schema changes as standalone YAML files, extended example mappings, and larger source documents should go.

Throughout the RFC template are comments that provide guidance on what to include. Remove comments as you fill out the content and they become obsolete. A finished RFC will have no explanatory comments remaining.

## Closing an RFC

If a proposed change is no longer being pursued or has been inactive for an extended period, the PR should be closed.
