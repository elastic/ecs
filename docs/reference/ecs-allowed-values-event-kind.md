---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-allowed-values-event-kind.html
applies_to:
  stack: all
  serverless: all
navigation_title: event.kind
---

# ECS categorization field: event.kind [ecs-allowed-values-event-kind]

This is one of four ECS Categorization Fields, and indicates the highest level in the ECS category hierarchy.

`event.kind` gives high-level information about what type of information the event contains, without being specific to the contents of the event. For example, values of this field distinguish alert events from metric events.

The value of this field can be used to inform how these kinds of events should be handled. They may warrant different retention, different access control, it may also help understand whether the data is coming in at a regular interval or not.

**Allowed values**

* [alert](#ecs-event-kind-alert)
* [asset](#ecs-event-kind-asset)
* [enrichment](#ecs-event-kind-enrichment)
* [event](#ecs-event-kind-event)
* [metric](#ecs-event-kind-metric)
* [state](#ecs-event-kind-state)
* [pipeline_error](#ecs-event-kind-pipeline_error)
* [signal](#ecs-event-kind-signal)


## alert [ecs-event-kind-alert]

This value indicates an event such as an alert or notable event, triggered by a detection rule executing externally to the Elastic Stack.

`event.kind:alert` is often populated for events coming from firewalls, intrusion detection systems, endpoint detection and response systems, and so on.

This value is not used by Elastic solutions for alert documents that are created by rules executing within the Kibana alerting framework.


## asset [ecs-event-kind-asset]

::::{warning}
These fields are in beta and are subject to change.
::::

This value indicates events whose primary purpose is to store an inventory of assets/entities and their attributes. Assets/entities are objects (such as users and hosts) that are expected to be subjects of detailed analysis within the system.

Examples include lists of user identities or accounts ingested from directory services such as Active Directory (AD), inventory of hosts pulled from configuration management databases (CMDB), and lists of cloud storage buckets pulled from cloud provider APIs.

This value is used by Elastic Security for asset management solutions. `event.kind: asset` is not used for normal system events or logs that are coming from an asset/entity, nor is it used for system events or logs coming from a directory or CMDB system.


## enrichment [ecs-event-kind-enrichment]

The `enrichment` value indicates an event collected to provide additional context, often to other events.

An example is collecting indicators of compromise (IOCs) from a threat intelligence provider with the intent to use those values to enrich other events. The IOC events from the intelligence provider should be categorized as `event.kind:enrichment`.


## event [ecs-event-kind-event]

This value is the most general and most common value for this field. It is used to represent events that indicate that something happened.


## metric [ecs-event-kind-metric]

This value is used to indicate that this event describes a numeric measurement taken at given point in time.

Examples include CPU utilization, memory usage, or device temperature.

Metric events are often collected on a predictable frequency, such as once every few seconds, or once a minute, but can also be used to describe ad-hoc numeric metric queries.


## state [ecs-event-kind-state]

The state value is similar to metric, indicating that this event describes a measurement taken at given point in time, except that the measurement does not result in a numeric value, but rather one of a fixed set of categorical values that represent conditions or states.

Examples include periodic events reporting Elasticsearch cluster state (green/yellow/red), the state of a TCP connection (open, closed, fin_wait, etc.), the state of a host with respect to a software vulnerability (vulnerable, not vulnerable), and the state of a system regarding compliance with a regulatory standard (compliant, not compliant).

Note that an event that describes a change of state would not use `event.kind:state`, but instead would use *event.kind:event* since a state change fits the more general event definition of something that happened.

State events are often collected on a predictable frequency, such as once every few seconds, once a minute, once an hour, or once a day, but can also be used to describe ad-hoc state queries.


## pipeline_error [ecs-event-kind-pipeline_error]

This value indicates that an error occurred during the ingestion of this event, and that event data may be missing, inconsistent, or incorrect. `event.kind:pipeline_error` is often associated with parsing errors.


## signal [ecs-event-kind-signal]

This value is used by Elastic solutions (e.g., Security, Observability) for alert documents that are created by rules executing within the Kibana alerting framework.

Usage of this value is reserved, and data ingestion pipelines must not populate `event.kind` with the value "signal".

