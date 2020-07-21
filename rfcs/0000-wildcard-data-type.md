# 0000: Wildcard Field Adoption into ECS
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage -->
- Date: **TBD** <!-- Update to reflect date of most recent stage advancement -->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Wildcard is a data type for Elasticsearch string fields being introduced in Elastic 7.9.0. Wildcard optimizes performance for queries using the wildcard (`*`) character to perform `grep`-like searches but without the limitations of the existing
text[0] and keyword[1] types.

Candidate fields for wildcard will be selected based on input from ECS committee members, other Elastic subject matter experts, and which fields will benefit most from the performance improvements. When adopted data sources populating those fields will need
to update their mappings to support wildcard to remain ECS compliant.

## Fields

<!--
Stage: 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

Adopting wildcard in a field will require changing the defined `type` in the schema from `keyword` to `wildcard`. One example is provided for this initial proposal as an example; a later stage proposal will include the entire list of proposed fields.

Current definition as of ECS 1.5.0:

```yaml
    - name: command_line
      level: extended
      type: keyword
      short: Full command line that started the process.
...
      multi_fields:
      - type: text
        name: text
```

Proposed type change:

```yaml
    - name: command_line
      level: extended
      type: wildcard
      short: Full command line that started the process.
...
      multi_fields:
      - type: text
        name: text
```

Note the existing `text` data type multi-field will remain only if there is a need to support tokenized searches.

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Many use cases benefit from wildcard search performance across long unstructured or semi-structured fields. Particularly in the security threat hunting and detection disciplines, reliable and efficient wildcard usage is a requirement from users. The following
sections list common use cases which would benefit from improved wildcard searching.

#### Paths and names

Searching across various permutations of various file system and URL structures to find a particular file, path, or other resource. Leading wildcard searches on these fields may be necessary to users, but (as keywords) are known to produce very poor search performance
(e.g. let's search for all instances of a known file without an unknown path: `file.path:*syslog.log`).

Example data categories:

* File paths
* URLs
* Usernames
* User agent
* Process names
* Email addresses
* OS names
* Domain names
* Host names
* Registry data

#### Stack traces

Program stack traces tend to be well-structured but with long text and varied contents. There are too many subtleties and application-specific patterns to map all of them accurately with ECS' field definitions. Better performing wildcard searches can help the user formulate their own queries easier and with a smaller performance hit.

### Command-line execution

Building accurate queries again a full command line string field like the `process.command_line` field, also benefit from wildcard improvements:

* Multiple spaces
* Isolating specific substrings
*

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

* Windows events
* Sysmon events
* Powershell events
* Web proxies
* Firewalls
* DNS servers
* Endpoint agents
* Application stack traces


## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

ECS-compliant data consumers should not be impacted due to the `keyword` field family[2], however ECS-compliant producers will be required for their field mappings to use `wildcard` where defined by the spec. The ECS project will need to evaluate how best to
evolve its tooling to support `wildcard`; wildcard will be the first time a Elastic licensed feature is specified in ECS.

### Ingestion

Any component producing data (Beats, Logstash, third-party developed, etc.) will need to comply with the new mappings.

### Usage

Part of the 7.9 release is the introduction of the first field family[2], `keyword`. Grouping field types by family is intended to eliminate backwards compatibility issues when replacing an old field with a new specialized type on time-based indices (e.g. `keyword` replaced
with `wildcard`). The `wildcard` data type will return `keyword` in the output of the field capabilities API call, and this change will enable both types to behave identically at query time. This feature eliminates concerns arising from Kibana's field compatibility checks
in index patterns.

### ECS project

ECS is and will remain an open source licensed project. However, there will be features available under the Elastic license that will benefit the user experience with the Elastic stack and solutions that have a place in the ECS specification. The ECS project's tooling will
create an option in the tooling to generate OSS compatible mappings that continue supporting the OSS licensed features of Elastic.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

As mentioned previously in the proposal, integrating the wildcard data type into ECS will be the first instance of an Elastic licensed feature being adopted by the schema. Until now ECS has relied only on OSS licensed features, but we do not want to limit ECS from supporting Elastic licensed features moving forward. ECS will remain OSS licensed even if the schema implements certain Elastic licensed features. When ECS adopts a feature available only under a license, it will be noted in the documentation.

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor

## Footnotes

* [0] Wildcard queries on `text` fields are limited to matching individual tokens rather than the original value of the field.
* [1] Keyword fields are not tokenized like `text` fields, so patterns can match multiple words. However they suffer from slow performance with wildcard searching (especially with leading wildcards).
* [2] https://github.com/elastic/elasticsearch/pull/58483
