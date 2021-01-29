# 0001: Wildcard Field Migration
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **1 (draft)** <!-- Update to reflect target stage -->
- Date: **2021-01-29** <!-- Update to reflect date of most recent stage advancement -->

Wildcard is a data type for Elasticsearch string fields being introduced in Elasticsearch 7.9. Wildcard optimizes performance for queries using wildcards (`*`) and regex, allowing users to perform `grep`-like searches without the limitations of the existing
text[0] and keyword[1] types.

This RFC focuses on migrating a subset of existing ECS fields, all of which are currently using the `keyword` type, to `wildcard`. Any net new fields introduced into ECS and are well-suited are encouraged to use `wildcard` independently of this RFC.

## Fields

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

### Identified Wildcard Fields

For a field to use wildcard, it will require changing the field's defined schema `type` from `keyword` to `wildcard`. The following fields are candidates for `wildcard`:

| Field Set | Field(s) |
| --------- | -------- |
| [`agent`](0001/agent.yml) | `agent.build.original` |
| [`as`](0001/as.yml) | `as.organization.name` |
| [`client`](0001/client.yml) | `client.domain`<br> `client.registered_domain` |
| [`destination`](0001/destination.yml) | `destination.domain`<br> `destination.registered_domain` |
| [`dns`](0001/dns.yml) | `dns.question.name`<br> `dns.answers.data` |
| [`error`](0001/error.yml) | `error.stack_trace`<br> `error.type` |
| [`file`](0001/file.yml) | `file.directory`<br> `file.path`<br> `file.target_path` |
| [`geo`](0001/geo.yml) | `geo.name` |
| [`host`](0001/host.yml) | `host.hostname`<br> |
| [`http`](0001/http.yml) | `http.request.referrer`<br> `http.request.body.content`<br> `http.response.body.content` |
| [`log`](0001/log.yml) | `log.file.path`<br> `log.logger` |
| [`organization`](0001/organization.yml) | `organization.name` |
| [`os`](0001/os.yml) | `os.name`<br> `os.full` |
| [`pe`](0001/pe.yml) | `pe.original_file_name` |
| [`process`](0001/process.yml) | `process.command_line`<br> `process.executable`<br> `process.name`<br> `process.thread.name`<br> `process.title`<br> `process.working_directory`<br> |
| [`registry`](0001/registry.yml) | `registry.key`<br> `registry.path`<br> `registry.data.strings` |
| [`server`](0001/server.yml) | `server.domain`<br> `server.registered_domain` |
| [`source`](0001/source.yml) | `source.domain`<br> `source.registered_domain` |
| [`tls`](0001/tls.yml) | `tls.client.issuer`<br> `tls.client.subject`<br> `tls.server.issuer`<br> `tls.server.subject` |
| [`url`](0001/url.yml) | `url.full`<br> `url.original`<br> `url.path`<br> `url.domain`<br> `url.registered_domain` |
| [`user`](0001/user.yml) | `user.name`<br> `user.full_name`<br> `user.email` |
| [`user_agent`](0001/user_agent.yml) | `user_agent.original` |
| [`x509`](0001/x509.yml) | `x509.issuer.distinguished_name`<br> `x509.subject.distinguished_name` |

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

#### Paths

* Flexible nesting of a file path: `file.path:*\\Users\\*\\Temp\\*`
* Match under registry path: `registry.path:\\HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\*\\Debugger`
* A unique URL path: `url.full:https://api.example.com/account/*/foobar`

The following are common categories

* File and directory paths
* URLs
* Registry data

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

#### Resolution

The performance characteristics for both indexing and querying for the two types has been explored and observations [noted](#comparison-with-keyword).

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

* Stage 0: https://github.com/elastic/ecs/pull/890
* Stage 1: https://github.com/elastic/ecs/pull/904
* Stage 2: https://github.com/elastic/ecs/pull/970
* Stage 3: https://github.com/elastic/ecs/pull/1015
#### Second Phase

* Stage 1:
  * Rollback: https://github.com/elastic/ecs/pull/1237
