---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-user_agent.html
applies_to:
  stack: all
  serverless: all
---

# User agent fields [ecs-user_agent]

The user_agent fields normally come from a browser request.

They often show up in web service logs coming from the parsed user agent string.


## User agent field details [_user_agent_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-user-agent-device-name$$$[user_agent.device.name](#field-user-agent-device-name) | Name of the device.<br><br>type: keyword<br><br>example: `iPhone`<br> | extended |
| $$$field-user-agent-name$$$[user_agent.name](#field-user-agent-name) | Name of the user agent.<br><br>type: keyword<br><br>example: `Safari`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user_agent.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user_agent/#user-agent-name)<br> | extended |
| $$$field-user-agent-original$$$[user_agent.original](#field-user-agent-original) | Unparsed user_agent string.<br><br>type: keyword<br><br>Multi-fields:<br><br>- user_agent.original.text (type: match_only_text)<br><br>example: `Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user_agent.original](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user_agent/#user-agent-original)<br> | extended |
| $$$field-user-agent-version$$$[user_agent.version](#field-user-agent-version) | Version of the user agent.<br><br>type: keyword<br><br>example: `12.0`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [user_agent.version](https://opentelemetry.io/docs/specs/semconv/attributes-registry/user_agent/#user-agent-version)<br> | extended |


## Field reuse [_field_reuse_30]


### Field sets that can be nested under user agent [ecs-user_agent-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `user_agent.os.*` | [os](/reference/ecs-os.md) | OS fields contain information about the operating system. |

