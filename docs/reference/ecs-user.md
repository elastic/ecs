---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-user.html
applies_to:
  stack: all
  serverless: all
---

# User fields [ecs-user]

The user fields describe information about the user that is relevant to the event.

Fields can have one entry or multiple entries. If a user has more than one id, provide an array that includes all of them.


## User field details [_user_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-user-domain$$$[user.domain](#field-user-domain) | Name of the directory the user is a member of.<br><br>For example, an LDAP or Active Directory domain name.<br><br>type: keyword<br> | extended |
| $$$field-user-email$$$[user.email](#field-user-email) | User email address.<br><br>type: keyword<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user.email](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user/#user-email)<br> | extended |
| $$$field-user-full-name$$$[user.full_name](#field-user-full-name) | User’s full name, if available.<br><br>type: keyword<br><br>Multi-fields:<br><br>- user.full_name.text (type: match_only_text)<br><br>example: `Albert Einstein`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user.full_name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user/#user-full-name)<br> | extended |
| $$$field-user-hash$$$[user.hash](#field-user-hash) | Unique user hash to correlate information for a user in anonymized form.<br><br>Useful if `user.id` or `user.name` contain confidential information and cannot be used.<br><br>type: keyword<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user.hash](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user/#user-hash)<br> | extended |
| $$$field-user-id$$$[user.id](#field-user-id) | Unique identifier of the user.<br><br>type: keyword<br><br>example: `S-1-5-21-202424912787-2692429404-2351956786-1000`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user.id](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user/#user-id)<br> | core |
| $$$field-user-name$$$[user.name](#field-user-name) | Short name or login of the user.<br><br>type: keyword<br><br>Multi-fields:<br><br>- user.name.text (type: match_only_text)<br><br>example: `a.einstein`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user/#user-name)<br> | core |
| $$$field-user-roles$$$[user.roles](#field-user-roles) | Array of user roles at the time of the event.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["kibana_admin", "reporting_user"]`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user.roles](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user/#user-roles)<br> | extended |


## Field reuse [_field_reuse_29]

The `user` fields are expected to be nested at:

* `client.user`
* `destination.user`
* `process.attested_user`
* `process.real_user`
* `process.saved_user`
* `process.user`
* `server.user`
* `source.user`
* `user.changes`
* `user.effective`
* `user.target`

Note also that the `user` fields may be used directly at the root of the events.


### Field sets that can be nested under User [ecs-user-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `user.changes.*` | `user` | Captures changes made to a user. |
| `user.effective.*` | `user` | User whose privileges were assumed. |
| `user.group.*` | [group](/reference/ecs-group.md) | User’s group relevant to the event. |
| `user.risk.*` | [risk](/reference/ecs-risk.md) | Fields for describing risk score and level. |
| `user.target.*` | `user` | Targeted user of action taken. |


## User field usage [_user_field_usage]

For usage and examples of the user fields, please see the [User Fields Usage and Examples](/reference/ecs-user-usage.md) section.


