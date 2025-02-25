---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-dns.html
applies_to:
  stack: all
  serverless: all
---

# DNS fields [ecs-dns]

Fields describing DNS queries and answers.

DNS events should either represent a single DNS query prior to getting answers (`dns.type:query`) or they should represent a full exchange and contain the query details as well as all of the answers that were provided for this query (`dns.type:answer`).


## DNS field details [_dns_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-dns-answers$$$[dns.answers](#field-dns-answers) | An array containing an object for each answer section returned by the server.<br><br>The main keys that should be present in these objects are defined by ECS. Records that have more information may contain more keys than what ECS defines.<br><br>Not all DNS data sources give all details about DNS answers. At minimum, answer objects must contain the `data` key. If more information is available, map as much of it to ECS as possible, and add any additional fields to the answer objects as custom fields.<br><br>type: object<br><br>Note: this field should contain an array of values.<br> | extended |
| $$$field-dns-answers-class$$$[dns.answers.class](#field-dns-answers-class) | The class of DNS data contained in this resource record.<br><br>type: keyword<br><br>example: `IN`<br> | extended |
| $$$field-dns-answers-data$$$[dns.answers.data](#field-dns-answers-data) | The data describing the resource.<br><br>The meaning of this data depends on the type and class of the resource record.<br><br>type: keyword<br><br>example: `10.10.10.10`<br> | extended |
| $$$field-dns-answers-name$$$[dns.answers.name](#field-dns-answers-name) | The domain name to which this resource record pertains.<br><br>If a chain of CNAME is being resolved, each answer’s `name` should be the one that corresponds with the answer’s `data`. It should not simply be the original `question.name` repeated.<br><br>type: keyword<br><br>example: `www.example.com`<br> | extended |
| $$$field-dns-answers-ttl$$$[dns.answers.ttl](#field-dns-answers-ttl) | The time interval in seconds that this resource record may be cached before it should be discarded. Zero values mean that the data should not be cached.<br><br>type: long<br><br>example: `180`<br> | extended |
| $$$field-dns-answers-type$$$[dns.answers.type](#field-dns-answers-type) | The type of data contained in this resource record.<br><br>type: keyword<br><br>example: `CNAME`<br> | extended |
| $$$field-dns-header-flags$$$[dns.header_flags](#field-dns-header-flags) | Array of 2 letter DNS header flags.<br><br>Expected values for this field:<br><br>* `AA`<br>* `TC`<br>* `RD`<br>* `RA`<br>* `AD`<br>* `CD`<br>* `DO`<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["RD", "RA"]`<br> | extended |
| $$$field-dns-id$$$[dns.id](#field-dns-id) | The DNS packet identifier assigned by the program that generated the query. The identifier is copied to the response.<br><br>type: keyword<br><br>example: `62111`<br> | extended |
| $$$field-dns-op-code$$$[dns.op_code](#field-dns-op-code) | The DNS operation code that specifies the kind of query in the message. This value is set by the originator of a query and copied into the response.<br><br>type: keyword<br><br>example: `QUERY`<br> | extended |
| $$$field-dns-question-class$$$[dns.question.class](#field-dns-question-class) | The class of records being queried.<br><br>type: keyword<br><br>example: `IN`<br> | extended |
| $$$field-dns-question-name$$$[dns.question.name](#field-dns-question-name) | The name being queried.<br><br>If the name field contains non-printable characters (below 32 or above 126), those characters should be represented as escaped base 10 integers (\DDD). Back slashes and quotes should be escaped. Tabs, carriage returns, and line feeds should be converted to \t, \r, and \n respectively.<br><br>type: keyword<br><br>example: `www.example.com`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [dns.question.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/dns/#dns-question-name)<br> | extended |
| $$$field-dns-question-registered-domain$$$[dns.question.registered_domain](#field-dns-question-registered-domain) | The highest registered domain, stripped of the subdomain.<br><br>For example, the registered domain for "foo.example.com" is "example.com".<br><br>This value can be determined precisely with a list like the public suffix list ([https://publicsuffix.org](https://publicsuffix.org)). Trying to approximate this by simply taking the last two labels will not work well for TLDs such as "co.uk".<br><br>type: keyword<br><br>example: `example.com`<br> | extended |
| $$$field-dns-question-subdomain$$$[dns.question.subdomain](#field-dns-question-subdomain) | The subdomain is all of the labels under the registered_domain.<br><br>If the domain has multiple levels of subdomain, such as "sub2.sub1.example.com", the subdomain field should contain "sub2.sub1", with no trailing period.<br><br>type: keyword<br><br>example: `www`<br> | extended |
| $$$field-dns-question-top-level-domain$$$[dns.question.top_level_domain](#field-dns-question-top-level-domain) | The effective top level domain (eTLD), also known as the domain suffix, is the last part of the domain name. For example, the top level domain for example.com is "com".<br><br>This value can be determined precisely with a list like the public suffix list ([https://publicsuffix.org](https://publicsuffix.org)). Trying to approximate this by simply taking the last label will not work well for effective TLDs such as "co.uk".<br><br>type: keyword<br><br>example: `co.uk`<br> | extended |
| $$$field-dns-question-type$$$[dns.question.type](#field-dns-question-type) | The type of record being queried.<br><br>type: keyword<br><br>example: `AAAA`<br> | extended |
| $$$field-dns-resolved-ip$$$[dns.resolved_ip](#field-dns-resolved-ip) | Array containing all IPs seen in `answers.data`.<br><br>The `answers` array can be difficult to use, because of the variety of data formats it can contain. Extracting all IP addresses seen in there to `dns.resolved_ip` makes it possible to index them as IP addresses, and makes them easier to visualize and query for.<br><br>type: ip<br><br>Note: this field should contain an array of values.<br><br>example: `["10.10.10.10", "10.10.10.11"]`<br> | extended |
| $$$field-dns-response-code$$$[dns.response_code](#field-dns-response-code) | The DNS response code.<br><br>type: keyword<br><br>example: `NOERROR`<br> | extended |
| $$$field-dns-type$$$[dns.type](#field-dns-type) | The type of DNS event captured, query or answer.<br><br>If your source of DNS events only gives you DNS queries, you should only create dns events of type `dns.type:query`.<br><br>If your source of DNS events gives you answers as well, you should create one event per query (optionally as soon as the query is seen). And a second event containing all query details as well as an array of answers.<br><br>type: keyword<br><br>example: `answer`<br> | extended |

