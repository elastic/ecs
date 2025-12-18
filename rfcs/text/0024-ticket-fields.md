# 0024: Ticket fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->


<!-- - Stage: **0 (strawperson)** --> <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
<!-- - Date: **2021-05-11** --> <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

- Stage: **1 (Draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->
<!--
Stage 0: Provide a schema definition for fields related to tickets.  Tickets, include, but are not limited to, Change Requests,
Incidents, User Stories, Hardware/Software Requests, etc.  This enables storing information about tickets in Elasticsearch
in a common format enabling Elasticsearch to function as a backing DB for ticketing systems, it also enables storing ticket
meta-data for use in Enterprise Search, and it plays a role in security & observability with relating log and metric data to open
Event, Incident or Security Vulnerability tickets. [Sample schema](https://github.com/elastic/ecs/compare/master...kc-comcast:ticket-block)
-->
<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->
Stage 1: Proposed field additions are documented in [ticket.yml](./0024/ticket.yml)

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->
The following new fields are proposed to be added to the ECS schema to provide details about tickets opened in various ticketing
systems.

- ticket.assignee
- ticket.created
- ticket.description
- ticket.id
- ticket.priority
- ticket.requester
- ticket.severity
- ticket.source
- ticket.state
- ticket.submitter
- ticket.summary
- ticket.type
- ticket.updated

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
Ticket fields would be used to store high-level basic characteristics of tickets for storage in Elasticsearch.  By
centralizing details on tickets, Enterprise Search opportunities are opened up allowing for a single place to search for
tickets created that may exist in a myriad of ticketing system sources.

Users can store details of their tickets in a centralized repository enabling a single source for querying, and retrieving
details about tickets which are opened as well as reporting many reporting capabilities on the characteristics of said
tickets.  Often times, tickets are stored in multiple sources requiring the need to open each source separately to query
for the information needed.

The core Use Case for searching tickets helps with ITIL / ITSM processing.  With a centralized source for ticket details,
users can identify if there are any current, or recent, Change Requests opened against a particular system to know if they
can approve a new change request to modify that system.  At the same time, when an Incident is opened, they can quickly scan
back through recent Change Requests to try and identify recent deployments which may be causing the problem.  Once the recent
Change Request is identified, drilling down to User Stories, Feature Requests, etc. which were included as part of
the deployment will help isolate the exact code change which may be causing the issue.  Conversely, pending Change Requests
can quickly be identified if an active high-severity Incident is underway to notify teams to hold off on deployment until
the issue is resolved.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

- Jira
- Remedy
- ServiceNow
- Trello
- Zendesk
- Any ticket management system

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

- **Ingest:** Extracting the details of tickets from these systems could potentially prove to be a challenge.  All are backed by a DB
and organizations are usually able to extract details from them to another source wherein they generally do their reporting.
These alternate sources are typically SQL databases themselves.  Accordingly, it should be possible to attach an ETL process
to these DB sources to overcome this challenge.

- **Synchronization of tickets:**  Tickets are not static documents, they change as they progress through their lifecycle.  The timing,
handling, and application of updates from the source to Elasticsearch would have to be cared for.  Too much delay, and the
benefits of a centralized Enterprise Search solution are lost; too many updates and teh Elasticsearch instance can suffer performance
challenges and/or become too costly to manage as it has to be scaled to support the load.

- **Index management:** Enterprise Search Use Cases usually rely on querying indexes of static data and not time series data.
With tickets, they could be considered static data, however, the number of unique documents keeps growing, and some sort
of roll over policy has to be applied.  They could be considered time series because tickets are created at a point in time,
and therefore could be aligned to a time series index.

- **Ticket correlation:** As each type of ticket is its own distinct and separate document, it doesn't necessarily indicate a
relationship to any other ticket.  This is where things like `tags` comes into play to create an association between the
various types of tickets and what other common associations they may have for things like sprints, releases, etc.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @kc-comcast | author

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1383

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
