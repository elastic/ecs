---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-agent.html
applies_to:
  stack: all
  serverless: all
---

# Agent fields [ecs-agent]

The agent fields contain the data about the software entity, if any, that collects, detects, or observes events on a host, or takes measurements on a host.

Examples include Beats. Agents may also run on observers. ECS agent.* fields shall be populated with details of the agent running on the host or observer where the event happened or the measurement was taken.


## Agent field details [_agent_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-agent-build-original$$$[agent.build.original](#field-agent-build-original) | Extended build information for the agent.<br><br>This field is intended to contain any build information that a data source may provide, no specific formatting is required.<br><br>type: keyword<br><br>example: `metricbeat version 7.6.0 (amd64), libbeat 7.6.0 [6a23e8f8f30f5001ba344e4e54d8d9cb82cb107c built 2020-02-05 23:10:10 +0000 UTC]`<br> | core |
| $$$field-agent-ephemeral-id$$$[agent.ephemeral_id](#field-agent-ephemeral-id) | Ephemeral identifier of this agent (if one exists).<br><br>This id normally changes across restarts, but `agent.id` does not.<br><br>type: keyword<br><br>example: `8a4f500f`<br> | extended |
| $$$field-agent-id$$$[agent.id](#field-agent-id) | Unique identifier of this agent (if one exists).<br><br>Example: For Beats this would be beat.id.<br><br>type: keyword<br><br>example: `8a4f500d`<br> | core |
| $$$field-agent-name$$$[agent.name](#field-agent-name) | Custom name of the agent.<br><br>This is a name that can be given to an agent. This can be helpful if for example two Filebeat instances are running on the same host but a human readable separation is needed on which Filebeat instance data is coming from.<br><br>type: keyword<br><br>example: `foo`<br> | core |
| $$$field-agent-type$$$[agent.type](#field-agent-type) | Type of the agent.<br><br>The agent type always stays the same and should be given by the agent used. In case of Filebeat the agent would always be Filebeat also if two Filebeat instances are run on the same machine.<br><br>type: keyword<br><br>example: `filebeat`<br> | core |
| $$$field-agent-version$$$[agent.version](#field-agent-version) | Version of the agent.<br><br>type: keyword<br><br>example: `6.0.0-rc2`<br> | core |

