# 0001: Wildcard Field Migration
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **2 (candidate)** <!-- Update to reflect target stage -->
- Date: **2021-07-14** <!-- Update to reflect date of most recent stage advancement -->

Wildcard is a data type for Elasticsearch string fields being introduced in Elasticsearch 7.9. Wildcard optimizes performance for queries using wildcards (`*`) and regex, allowing users to perform `grep`-like searches without the limitations of the existing
text[0] and keyword[1] types.

This RFC focuses on migrating a subset of existing ECS fields, all of which are currently using the `keyword` type, to `wildcard`. Any net new fields introduced into ECS and are well-suited are encouraged to use `wildcard` independently of this RFC.

The objectives of this migration:

* Leverage the improved searching using `wildcard` of regular expressions and leading wildcard on high-cardinality fields. Wildcard excels when searching for something in the middle of strings when there are many unique values to evaluate. It also addresses issues with the partial matching of string values important to [security use cases](https://socprime.com/blog/elastic-for-security-analysts-part-1-searching-strings/).
* Remove security blindspots caused by `keyword` field size limits (`ignore_above`) and the Lucence hard limit (32k for each value) when dealing with large event values or messages.
* Potentially less disk usage for high-cardinality fields
* Potentially simpler search expressions

## Fields

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

### Identified Wildcard Fields

For a field to use wildcard, it will require changing the field's defined schema `type` from `keyword` to `wildcard`. The following fields are candidates for `wildcard`:

| Field Set | Field(s) |
| --------- | -------- |
| [`error`](0001/error.yml) | `error.stack_trace` |
| [`http`](0001/http.yml) | `http.request.body.content`<br> `http.response.body.content` |
| [`process`](0001/process.yml) | `process.command_line` |
| [`registry`](0001/registry.yml) | `registry.data.strings` |
| [`url`](0001/url.yml) | `url.full`<br> `url.original`<br> `url.path` |

The full set of schema files which will be transitioning to `wildcard` are located in directory [rfcs/text/0001/](0001/).

### Example definition

Here's an example of applying this change to the `process.command_line` field:

**Definition as of ECS 1.6.0**

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

**Note**: the existing `text` data type multi-field will remain only if there is a need to support tokenized searches.

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Wildcard is well-suited for cases requiring partial matching of string values across long unstructured or semi-structured fields. Often machine generated events, such as logs, metrics, and traces, aren't well suited for the analysis applied on `text` fields. Using `keyword` allows for exact value searching and introduces filtering, sorting, and aggregations. Keyword fields do also support regex and wildcard queries, however the field's search performance can vary a lot, depending on the query (e.g. leading wildcard) and the cardinality of the data.

Often ECS approaches semi-structured fields by breaking their values down into structured ones. These structured fields then enable better use of keyword fields' characteristics. For example, a URL can break down into its constituent parts: scheme, domain,  port, path, etc., and those parts can in turn be mapped to unique fields. However, not all fields are structured enough for this approach.

In the security discipline, threat hunting searches and detection rules often rely on `grep`-like wildcard and regex patterns. Many other security platforms and SIEMs support wildcard and regex in this way, and it often can be confusing to security practitioners trying to adopt their detections and techniques to Elastic. These users require detailed pattern-matching operations that perform consistently well across large data sets. Wildcard is optimized for this type of need.

A final interesting property of wildcard is its unlimited max character field size. Elasticsearch keyword field default to a max allowed string size of 256 characters which ECS ups to 1024 using `ignore_above`. Keyword can't be increased infinitely because Lucene has a hard set max limit of 32766 bytes for a single term. Due to how wildcard strings are indexed, they do not share this limitation. This makes wildcard the ideal data type for a very large string field (>32kB) that still needs to be indexed.

### Comparison with keyword

The following table is a comparison of `wildcard` vs. `keyword` [2]:

| Feature | Keyword | Wildcard |
| ------- | ------- | -------- |
| Sorting speeds | Fast | Not quite as fast (see *1) |
| Aggregation speeds | Fast | Not quite as fast (see *1) |
| Prefix query speeds (foo*) | Fast | Not quite as fast (see *2) |
| Leading wildcard queries on low-cardinality fields (*foo) | Fast | Slower (see *3) |
| Leading wildcard queries on high-cardinality fields (*foo) | Terrible | Much faster |
| Term query. Full value match (foo) | Fast | Not quite as fast (see *2) |
| Fuzzy query | Y (see *4) | Y |
| Regexp query | Y (see *4) | Y |
| Range query | Y (see *4) | Y |
| Supports highlighting | Y | N |
| Searched by "all fields" queries | Y | Y |
| Disk costs for mostly unique values | high (see *5) | lower (see *5) |
| Dist costs for mostly identical values | low (see *5) | medium (see *5) |
| Max character size for a field value | 256 for default JSON string mapping (1024 for ECS), 32766 Lucene max | unlimited |
| Supports normalizers in mappings | Y | N |
| Indexing speeds | Fast | Slower (see *6) |

1. Somewhat slower as doc values retrieved from compressed blocks of 32
2. Somewhat slower because approximate matches with n-grams need verification
3. Keyword field visits every unique value only once but wildcard field assesses every utterance of values
4. If "allow expensive queries" is enabled
5. Depends on common prefixes - keyword fields have common-prefix based compression whereas wildcard fields are whole-value LZ4 compression.
6. Will vary with content but a test indexing weblogs took 499 seconds vs. keyword's 365 seconds.

### Decision Flow

Since deciding between `wildcard` and `keyword` involves weighing tradeoffs, this workflow is a visual to help assess when choosing `wildcard` may provide an advantage [2].

<img width="929" alt="wildcard-field-workflow" src="https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt086af7a2897168a8/5f37050cdb5c28785b6f0413/blog-wildcard-field-workflow.png">

### Use Cases

The following sections detail use cases which could benefit using the `wildcard` type.

#### Names

Similar to paths, different names components may need to be searched using one or more wildcard.

* Flexible host name searching: `host.name:prod-*-db*`
* Likewise, flexible searching of user names or accounts: `user.email:foo*@example.com`

Common categories:

* Usernames
* Host names
* Process names
* OS names
* Email addresses
* Domains

#### Stack traces

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

When looking for similar events that also contain the phrase `lambda$performRequestAndParseEntity$9(RestHighLevelClient.java`, I'd need a field that supports searching in the middle of a string. Keyword would perform poorly and text would require rethinking the query to match the analyzer and tokenization applied at index time.

#### Command-line execution

The arguments, order of those arguments, and values passed can be arbitrary in a command-line execution. If searching across multiple arguments, retaining their ordering, and/or the argument-value pairing is key to the search criteria, multiple wildcards patterns may be needed in a single query. If the presence of the arguments/values is the only criteria regardless of ordering or pairing, using a structured field such as `process.args` would be preferred. Wildcard searching such an unstructured field indexed as keyword, like `process.command_line`, can cause performance challenges.

Example:

```
process.command_line:*\/f foo* AND process.command_line:*\/b bar*
```

Additional cases for wildcard searching against command line executions:

* Multiple spaces in the command line execution
* Isolating specific substrings where ordering matters
* command obfuscation

## Source data

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

### Categories

* Windows events
* Sysmon events
* Powershell events
* Web proxies
* Firewalls
* DNS servers
* Endpoint agents
* Application stack traces

### Real world examples

Each example in this section contains a partial index mapping, a partial event, and one wildcard search query. Each query example uses a leading wildcard on expected high-cardinality fields where `wildcard` is performs far better than `keyword`.

**Windows registry event from sysmon:**

```
### Mapping (partial)
...
        "registry" : {
          "properties" : {
            "key" : {
              "type" : "wildcard"
            }
          }
        }
...

### Event (partial)
...
    "registry": {
      "path": "HKU\\S-1-5-21-1957236100-58272097-297103362-500\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\HideFileExt",
      "hive": "HKU",
      "key": "S-1-5-21-1957236100-58272097-297103362-500\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\HideFileExt",
      "value": "HideFileExt",
      "data": {
        "strings": [
          "1"
        ],
        "type": "SZ_DWORD"
      }
...

### Query

GET winlogbeat-*/_search
{
  "query": {
    "wildcard": {
      "registry.key": {
        "value": "*CurrentVersion*"
      }
    }
  }
}

```

**Windows Powershell logging event:**

```
### Mapping (partial)
...
        "process" : {
          "properties" : {
            "command_line" : {
              "type" : "wildcard",
              "fields" : {
                "text" : {
                  "type" : "text",
                  "norms" : false
                }
              }
            }
          }
        }
...

### Event (partial)

    "process": {
      "pid": 3540,
      ...
      "command_line": "C:\\Windows\\System32\\svchost.exe -k netsvcs -p -s NetSetupSvc"
    }

### Query

GET winlogbeat-*/_search
{
  "_source": false,
  "query": {
    "wildcard": {
      "process.command_line": {
        "value": "*-k netsvcs -p*"
      }
    }
  }
}
```

**Wildcard query against original URL from a squid web proxy event:**

```
### Mapping (partial)

...
        "url" : {
            "original" : {
              "type" : "wildcard",
              "fields" : {
                "text" : {
                  "type" : "text",
                  "norms" : false
                }
              }
            }
...

### Event (partial)

...
    "url": {
      "original": "http://example.com/cart.do?action=view&itemId=HolyGouda",
      "domain": "example.com"
    }
...

### Query

GET filebeat-*/_search
{
  "_source": false,
  "query": {
    "wildcard": {
      "url.original": {
        "value": "*action=view*Gouda"
      }
    }
  }
}
```

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

`keyword` and `wildcard` are both members of the keyword type family but use different underlying data structures. Wildcard uses two data structures to accelerate wildcard and regexp searching:

1. n-gram index of all three character sequences in the string values
2. binary doc value store of the original values

Wildcard fields require more disk space for the additional n-gram index. This disk cost is only recovered if the full doc values that are also stored compress better than the compression of the keyword fields for the doc values. Keyword values are compressed based on common-prefixes in the values, but wildcard values use LZ4 based on blocks of 32 values. These two compression approaches vary depending on size, duplicate values, the cardinality of the data, and so on.

### Storage and Indexing Costs

When assembling the initial list of candidate fields to migrate to `wildcard,` we split focus between query performance improvements and removing security blind spots. However, we overlooked the storage and indexing costs when switching fields to be indexed as `wildcard.`

ECS fields will be re-evaluated now in terms of storage and indexing using the following criteria:

* Underestimating cardinality of particular fields. How many unique fields are expected for a given field? Thousands? Hundreds of Thousands? Millions?
* Disk costs for mostly identical values. Which fields are more likely to have values sharing common prefixes and better compression as `keyword`?

### Query Performance

Query performance of `wildcard` vs. `keyword` hasn't been benchmarked extensively. ECS recognizes some fields may need `wildcard` even with an increase in storage and indexing overhead due to other query benefits.

Keyword vs. wildcard query characteristics:

* `keyword` will perform queries faster for a prefix query (`foo*`) on a low-cardinality field (< hundreds of thousands of unique values) than `wildcard.`
* `wildcard` will perform much faster than `keyword` for leading wildcard or regexp queries but only on a high-cardinality field (> millions of unique values).
* `wildcard` fields should avoid being used extensively for sorting and aggregation features

### Ingestion

Any component producing data (Beats, Logstash, third-party developed, etc.) will need to adopt the mappings in their index templates. The discussion around the handling of OSS vs. Basic field types between OSS and Basic modules/plugins will be handled outside of this proposal.

### Usage mechanisms

Part of the 7.9 release is the introduction of the keyword family[3]. Grouping field types by family is intended to eliminate backwards compatibility issues when replacing an older field type with a new, more specialized type on time-based indices (e.g. `keyword` replaced with `wildcard`). The `wildcard` data type will return `keyword` in the output of the field capabilities API call, and this change will enable both types to behave identically at query time. This feature eliminates concerns arising from Kibana's field compatibility checks in index patterns.

### ECS project

ECS is and will remain an open source licensed project. However, there will be features available under the Elastic license that will benefit the user experience with the Elastic stack and solutions that have a place in the ECS specification. The ECS project's tooling will create an option in the tooling to generate OSS compatible mappings that continue supporting the OSS licensed features of Elastic. The discussion and implementation of this functionality will take place outside this proposal.

## Concerns

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

### Wildcard and case-insensitivity

Some fields require flexibility in how users search. Their content is messy (e.g. user-agent) or popular for threat hunters (e.g. file paths and names, command line processes), and a single character in the opposite casing can bypass a detection today for `keyword` fields. The `wildcard` field provides improved performance of leading `wildcard` and `regex` term-level queries, but is also a step towards case-insensitive search support in Elasticsearch. As Elasticsearch moves forward towards introducing a case-insensitive query option [3], ECS considers the fields adopting `wildcard` to be popular candidates for case-insensitive searching once the feature is available.

#### Resolution

The `case_insensitivity` query parameter is an expected feature in Elasticsearch 7.10 with support for the `regexp`, `term`, `prefix`, and `wildcard` query types[4]. Since this is a query parameter, both `keyword` and `wildcard` types will be supported, and each type's noted [performance characteristics](#comparison-with-keyword) will be consistent.

### Performance differences

Performance and storage characteristics between wildcard and keyword will be different[5], and this difference may have an impact depending on deployment size and/or the level of duplication in the field data. Fields which were previously indexed as keyword will be switched to wildcard. With these fields now indexed as wildcard, users will be querying fields which are indexed as keyword in some indices and as wildcard in others. Any potential indexing or querying differences needs to be understood and captured.

The performance characteristics for both indexing and querying for the two types were explored and observations [noted](#comparison-with-keyword) in the earlier phases of this proposal. However, after additional benchmarking the increases in storage costs and decreasing in index performance was found to be significant enough that we need to revisit our approach. Each candidate field will need to be reassessed against a more rigorous set of criteria for inclusion into this initial type migration.

#### Resolution (Pending)

The following categories are areas that were initially candidates for `wildcard`, but after reviewing the benchmarking data, the fields will not typically have high enough cardinality to make them ideal candidates for `wildcard`.
##### File paths and names

File path values are likely to compress extremely well as `keyword` since `keyword` fields have common-prefix-based compression (`wildcard` values are blocks of 32 values compressed into a single LZ4 blob). On top of the worse doc values compression, the number of `postings` also increases significantly due to n-grams.

##### Host and Organization Naming

Hostname values are very likely duplicated from event to event. Even though an index might have thousands of different hosts, it's unlikely to see millions of unique hostname values.

Depending on an organization's host naming convention, there's also some possibility of common prefixing (hosts named `USNHCDBRD-D001` and `USNHCW2K8-P001` both share the prefix `USNHC`).

Organization names such as `as.organization.name` and `organization.name` might be better suited to `text.`

##### User Identifiers

User identifiers, like usernames or email addresses, are also likely duplicated across events. Common prefixing is also a potential consideration.

##### Specialized Text Analyzers

For certain field and their values, the use of specialized text analysis could be an alternative to using the `wildcard` data type. For example, adopting the [path hierarchy tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-pathhierarchy-tokenizer.html) for file paths.

### Future breaking changes to adopt `wildcard`

Often a large field is mapped a `keyword` to simplify substring searches. But:

* larger field = many unique values = slow substring searches
* size limits for `keyword` will drop overly large values

Unlike a migration from `keyword` to `wildcard,` migrating from `text` to `wildcard` would be a breaking change. The initial wildcard proposal focused on non-breaking changes of existing keyword fields in ECS, but now understanding the storage/indexing characteristics of `wildcard` better and the new implementation timeline may be worth discussing more for the next ECS major.

#### `message`

As of ECS 1.8, `message` is mapped as type `text`. While `text` is great searching fields containing "everyday language", `wildcard` may improve the substring search issues encountered when indexing larger strings vs. migrating to `keyword`.

#### `event.original`

Also as of ECS 1.8, the `event.original` field is not indexed due to the very large value sizes and the significant impact indexes those values could have. However, if users had the need and understood the trade-offs, `wildcard` could be a more appropriate type than `keyword`.

### Wildcard field value character limits

ECS applies the `ignore_above` setting to keyword fields to prevent strings longer than 1024 characters from being indexed or stored. While `ignore_above` can be raised, Lucene implements a term byte-length limit of 32766 which cannot be adjusted. Wildcard supports an unlimited max character size for a field value. The `wildcard` field type will still have the `ignore_above` option available, and a reasonable limit may be need applied to mitigate unexpected side-effects.

#### Resolution

This ability to ingest extremely long values is considered an advantage of `wildcard` compared to `keyword`. Therefore, the `wildcard` fields will not have an `ignore_above` option defined initially.

### Licensing

Until now ECS has relied only on OSS licensed features, but ECS will also support Elastic licensed features. The ECS project will remain OSS licensed with the schema implementing Elastic licensed features as part of the specification.

#### Resolution

When ECS adopts a feature available only under a license, it will be noted in the documentation.

The ECS team will not maintain a second OSS-compatible set of ECS field definitions. However a feature has been added to the ECS generator script allowing for OSS-compatibility versions of the ECS-maintained artifacts to be generated by users. When the generator is called with `--oss`, ECS fields using Basic data types will fallback to their compatible OSS types (if an OSS fallback type is available).

### Version Compatibility

A data shipper which uses the `wildcard` field type may need to verify that the configured output Elasticsearch destination can support it (>= 7.9.0). For example, if a future version of Beats adopts `wildcard` in index mappings, Beats may need to gracefully handle a scenario where the targeted Elasticsearch instance doesn't support the data type.

#### Resolution

Ongoing discussions are taking place to determine how to best address for Beats and Logstash.

### Text fields migrating to wildcard

ECS currently has two `text` fields that would likely benefit from migrating to `wildcard`.
Doing so on the canonical field (as opposed to adding a multi-field) would be a breaking change.
However adding a `.wildcard` multi-field may cause confusion, as they would be the only
places where `wildcard` appears as a multi-field.

The fields are:

- `message`
- `error.message`

Paradoxically, in some cases they also benefit from the `text` data type.
A prime example is Windows Event Logs' main messages, which is stored in the `message` field.

The situation is captured here for addressing at a later stage.

#### Resolution

No resolution yet.

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor
* @webmat | editorial feedback
* @markharwood | subject matter expert
* @rw-access | editorial feedback

## Footnotes

* [0] Wildcard queries on `text` fields are limited to matching individual tokens rather than the original value of the field.
* [1] Keyword fields are not tokenized like `text` fields, so patterns can match multiple words. However they suffer from slow performance with wildcard searching (especially with leading wildcards).
* [2] https://www.elastic.co/blog/find-strings-within-strings-faster-with-the-new-elasticsearch-wildcard-field
* [3] https://github.com/elastic/elasticsearch/issues/61162
* [4] https://github.com/elastic/elasticsearch/issues/61162
* [5] https://github.com/elastic/elasticsearch/pull/58483

## References

<!-- Insert any links appropriate to this RFC in this section. -->

* [Introductory blog post for the wildcard type](https://www.elastic.co/blog/find-strings-within-strings-faster-with-the-new-elasticsearch-wildcard-field)
* [Wildcard field type in the Elasticsearch docs](elastic.co/guide/en/elasticsearch/reference/current/keyword.html#wildcard-field-type)
* https://github.com/elastic/ecs/issues/570
* https://github.com/elastic/mechagodzilla/issues/2
* https://github.com/elastic/ecs/issues/105

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

Due to performance concerns brought up during implementation, the wildcard changes were [rolled back](https://github.com/elastic/ecs/pull/1237) to iterate on this proposal with a focus on performance implications. The original round of PRs are listed under `First Phase`, and the PRs following the rollback are grouped under `Second Phase`.

#### First Phase

* Stage 0 (strawperson): https://github.com/elastic/ecs/pull/890
* Stage 1 (proposal): https://github.com/elastic/ecs/pull/904
* Stage 2 (draft): https://github.com/elastic/ecs/pull/970
* Stage 3 (candidate): https://github.com/elastic/ecs/pull/1015
#### Second Phase

* Stage 1 (draft):
  * Rollback: https://github.com/elastic/ecs/pull/1237
* Stage 2 (candidate): https://github.com/elastic/ecs/pull/1247
