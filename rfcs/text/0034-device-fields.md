# 0034: Adding device fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2022-08-16** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

With mobile use cases (e.g. tracing and logging on mobile devices, such as iOS, Android, etc.) it is important to capture device information that would allow to correlate and slice and dice information by device properties (such as device manufacturer, device model id, etc.).

The [OpenTelemetry semantic conventions specify the following fields for devices](https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/device/):
- `device.id`
- `device.model.identifier`
- `device.model.name`
- `device.manufacturer`

With this RFC, we propose to adopt the device fields specified by OpenTelemetry to support product use cases at Elastic that are related to mobile devices (e.g. APM for iOS and Android).

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

A new `Device` field group will be added with the fields defined by [OpenTelemetry Semantic Conventions for Devices](https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/device/).



<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

APM data (i.e. transaction and spans that are part of end-to-end traces) is also collected for mobile devices (i.e. iOS and Android applications). Enriching this APM data would allow for rhich performance and business-related analysis of the data. E.g. user could filter performance issues, errors, crashes, etc. by device model types, versions, manufacturers.
The APM correlations feature can be improved for mobile applications by including these fields as it would identify statistical correlations if problems occur, for example, only for specific device models.
A unique device.id allows in addition to derive statistics on recurring users vs. new users. 


## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

The information will be retrieved by the APM agents for iOS and Android. The Android agent will use the [Build API](https://developer.android.com/reference/android/os/Build#MANUFACTURER) to retrieve the above information. For iOS, the [vendor identifier property](https://developer.apple.com/documentation/uikit/uidevice/1620059-identifierforvendor) will be used to retrieve the device ID. iOS also provides an API to retrive the `device.model.identifier`.

For both, iOS and Android, the `device.model.name` cannot be retrieved on the Device itself but need to be mapped from the `device.model.identifier` value. We will use an Elasticsearch ingest node processor for this mapping ([this is the corresponding ES issue for it](https://github.com/elastic/elasticsearch/issues/88865)).


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
- `device.model.name` cannot be collected directly on the device but needs to be mapped from the `device.model.identifier`. This requires backend-side mapping. We will solve this through an Elasticsearch ingest node processor (similar to the GeoIP processor that maps IPs to geo locations). 

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @AlexanderWert | author
* @felixbarny | subject matter expert
* @bryce-b | subject matter expert
* @LikeTheSalad | subject matter expert
* @akhileshpok | PM Mobile APM


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
* [OpenTelemetry specification for device](https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/device/)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2013
    * Correction: https://github.com/elastic/ecs/pull/2021
* Stage 1: https://github.com/elastic/ecs/pull/2026
* Stage 2: https://github.com/elastic/ecs/pull/2030
<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
