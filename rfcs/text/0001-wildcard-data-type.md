# 0001: Wildcard Field Adoption into ECS
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **1 (proposal)** <!-- Update to reflect target stage -->
- Date: **TBD** <!-- Update to reflect date of most recent stage advancement -->

Wildcard is a data type for Elasticsearch string fields being introduced in Elasticsearch 7.9. Wildcard optimizes performance for queries using wildcards (`*`) and regex, allowing users to perform `grep`-like searches without the limitations of the existing
text[0] and keyword[1] types.

## Fields

<!--
Stage: 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

For a field to use wildcard, it will require changing the the field's defined schema `type` from `keyword` to `wildcard`. The following fieldsets are expected to adopt `wildcard` in at least one of their fields:

* `agent.*`
* `destination.*`
* `error.*`
* `file.*`
* `host.*`
* `http.*`
* `os.*`
* `process.*`
* `registry.*`
* `source.*`
* `url.*`
* `user.*`

Here's an example of applying this change to the `process.command_line` field:

**Current definition as of ECS 1.5.0**

Schema definition:

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

Mapping definition:

```json
{
  "mappings": {
    "properties": {
      "command_line": {
        "fields": {
          "text": {
            "norms": false,
            "type": "text"
          }
        },
        "ignore_above": 1024,
        "type": "keyword"
      }
    }
  }
}
```

**Example of the proposed change**

Schema definition:

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

Mapping definition:

```json
{
  "mappings": {
    "properties": {
      "command_line": {
        "fields": {
          "text": {
            "norms": false,
            "type": "text"
          }
        },
        "type": "wildcard"
      }
    }
  }
}
```

> Note: the existing `text` data type multi-field will remain only if there is a need to support tokenized searches.

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Wildcard is well-suited for cases requiring partial matching of string values across long unstructured or semi-structured fields. Often machine generated events, such as logs, metrics, and traces, aren't well suited for the analysis applied on `text` fields. Using keyword allows for exact value searching and introduces filtering, sorting, and aggregations. Keyword fields do also support regex and wildcard queries, however the field's search performance can become vary largely for certain queries (e.g. leading wildcard) and the cardinality of the data.

Often ECS approaches semi-structured fields by breaking their values down into structured ones. These structured fields then enable better use of keyword fields' characteristics. For example, a URL can break down into its constituent parts: scheme, domain,  port, path, etc., and those parts can in turn be mapped to unique fields. However, not all fields are structured enough for this approach.

In the security discipline, threat hunting searches and detection rules often rely on `grep`-like wildcard and regex patterns. Many other security platforms and SIEMs support wildcard and regex in this way, and it often can be confusing to security practitioners trying to adopt their detections and techniques to Elastic. These users require detailed pattern-matching operations that perform consistently well across large data sets. Wildcard is optimized for this type of need.

A final interesting property of wildcard is its unlimited max character field size. Elasticsearch keyword field default to a max allowed string size of 256 characters which ECS ups to 1024 using `ignore_above`. Keyword can't be increased infinitely because Lucene has a hard set max limit of 32766 bytes for a single term. Due to how wildcard strings are indexed, they do not share this limitation. This makes wildcard the ideal data type for a very large string field (>32kB) that still needs to be indexed.

The next sections details use cases which could benefit wildcard.

### Paths

Flexible nesting of a file path: `file.path:*\\Users\\*\\Temp\\*`
Match under registry path: `registry.path:\\HKLM\\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\Debugger`
A unique URL path: `url.full:https://api.example.com/account/*/foobar`

The following are common categories

* File and directory paths
* URLs
* Registry data

### Names

Similar to paths, different names components many need to be searched using one or more wildcard.

Flexible host name searching: `host.name:prod-*-db*`
Likewise, flexible searching of user names or accounts: `user.email:foo*@example.com`

Common categories:

* Usernames
* Host names
* Process names
* OS names
* Email addresses
* Domains

### Stack traces

Program stack traces tend to be well-structured but with long text and varied contents. There are too many subtleties and application-specific patterns to map all of them accurately with ECS' field definitions. Better performing wildcard searches can help the user formulate their own queries easier and with a smaller performance hit.

Looking at the following example of a stack trace:

```java
bootstrap method initialization exception
at java.base/java.lang.invoke.BootstrapMethodInvoker.invoke(BootstrapMethodInvoker.java:194)
at java.base/java.lang.invoke.CallSite.makeSite(CallSite.java:315)
at java.base/java.lang.invoke.MethodHandleNatives.linkCallSiteImpl(MethodHandleNatives.java:259)
at java.base/java.lang.invoke.MethodHandleNatives.linkCallSite(MethodHandleNatives.java:249)
at org.elasticsearch.client.RestHighLevelClient.parseEntity(RestHighLevelClient.java:1883)
at org.elasticsearch.client.RestHighLevelClient.lambda$performRequestAndParseEntity$9(RestHighLevelClient.java:1564)
at org.elasticsearch.client.RestHighLevelClient.internalPerformRequest(RestHighLevelClient.java:1628)
at org.elasticsearch.client.RestHighLevelClient.performRequest(RestHighLevelClient.java:1596)
at org.elasticsearch.client.RestHighLevelClient.performRequestAndParseEntity(RestHighLevelClient.java:1563)
at org.elasticsearch.client.IndicesClient.getMapping(IndicesClient.java:282)

Caused by: java.lang.invoke.LambdaConversionException: Invalid receiver type interface org.apache.http.Header; not a subtype of implementation type interface org.apache.http.NameValuePair
at java.base/java.lang.invoke.AbstractValidatingLambdaMetafactory.validateMetafactoryArgs(AbstractValidatingLambdaMetafactory.java:254)
at java.base/java.lang.invoke.LambdaMetafactory.metafactory(LambdaMetafactory.java:327)
at java.base/java.lang.invoke.BootstrapMethodInvoker.invoke(BootstrapMethodInvoker.java:127)
```

If I wanted to look for similar events that also contain the phrase `lambda$performRequestAndParseEntity$9(RestHighLevelClient.java`, I'd need a field that supports searching in the middle of a string. Keyword would perform poorly and text would require rethinking the query to match the analyzer and tokenization applied at index time.

### Command-line execution

The arguments, order of those arguments, and values passed can be arbitrary in a command-line execution. If searching across multiple arguments, retaining their ordering, and/or the argument-value pairing is key to the search criteria, multiple wildcards patterns may be needed in a single query (if the presence of the arguments/values is the only criteria regardless of ordering or pairing, using a structured field such as `process.args` would be preferred). Wildcard searching such an unstructured field indexed as keyword, like `process.command_line`, can cause performance challenges.

Example:

```
process.command_line:*f/ foo* and process.command_line:*/b bar*
```

Additional cases for wildcard searching against command line executions:

* Multiple spaces in the command line execution
* Isolating specific substrings where ordering matters
* command obfuscation

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

### Ingestion

Any component producing data (Beats, Logstash, third-party developed, etc.) will need to adopt the mappings in their index templates. The discussion around the handling of OSS vs. Basic field types between OSS and Basic modules/plugins will be handled outside of this proposal.

### Usage

Part of the 7.9 release is the introduction of the first field family[2], `keyword`. Grouping field types by family is intended to eliminate backwards compatibility issues when replacing an old field with a new specialized type on time-based indices (e.g. `keyword` replaced with `wildcard`). The `wildcard` data type will return `keyword` in the output of the field capabilities API call, and this change will enable both types to behave identically at query time. This feature eliminates concerns arising from Kibana's field compatibility checks in index patterns.

### ECS project

ECS is and will remain an open source licensed project. However, there will be features available under the Elastic license that will benefit the user experience with the Elastic stack and solutions that have a place in the ECS specification. The ECS project's tooling will create an option in the tooling to generate OSS compatible mappings that continue supporting the OSS licensed features of Elastic. The discussion and implementation of this functionality will take place outside this proposal.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Licensing

Until now ECS has relied only on OSS licensed features, but ECS will also support Elastic licensed features. The ECS project will remain OSS licensed with the schema implementing Elastic licensed features as part of the specification. When ECS adopts a feature available only under a license, it will be noted in the documentation. ECS plans to provide tooling options which continue to support OSS consumers of ECS and the Elastic Stack.

### Performance differences

Performance and storage characteristics between wildcard and keyword will be different[3], and this difference may have an impact depending on deployment size and/or the level of duplication in the field data. As part of the transition, fields which were previously indexed keyword will be switched to wildcard. Queries across indices with field names will be necessary. Understanding the differences at both index and query time will be pursued.

### Wildcard field value character limits

ECS applies the `ignore_above` setting to keyword fields to prevent strings longer than 1024 characters from being indexed or stored. While `ignore_above` can be raised, Lucene implements a term byte-length limit of 32766 which cannot be adjusted. Wildcard supports an unlimited max character size for a field value. The `wildcard` field type will still have the `ignore_above` option available, and a reasonable limit may be need applied to mitigate unexpected side-effects.

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor
* @webmat | editorial feedback
* @markharwood | subject matter expert

## Footnotes

* [0] Wildcard queries on `text` fields are limited to matching individual tokens rather than the original value of the field.
* [1] Keyword fields are not tokenized like `text` fields, so patterns can match multiple words. However they suffer from slow performance with wildcard searching (especially with leading wildcards).
* [2] https://github.com/elastic/elasticsearch/pull/58483
* [3] Slightly [outdated](https://github.com/elastic/elasticsearch/issues/53603#issuecomment-650298759) comparison [here](https://github.com/elastic/elasticsearch/issues/53603#issuecomment-601408720). An updated and more accurate version will be available around the 7.9 release.


## References

<!-- Insert any links appropriate to this RFC in this section. -->

* [Introductory blog post for the wildcard type](https://www.elastic.co/blog/find-strings-within-strings-faster-with-the-new-elasticsearch-wildcard-field)
* https://github.com/elastic/ecs/issues/570
* https://github.com/elastic/mechagodzilla/issues/2
* https://github.com/elastic/ecs/issues/105

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/890
* Stage 1: https://github.com/elastic/ecs/pull/904
