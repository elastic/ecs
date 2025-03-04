---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-allowed-values-event-outcome.html
applies_to:
  stack: all
  serverless: all
navigation_title: event.outcome
---

# ECS categorization field: event.outcome [ecs-allowed-values-event-outcome]

This is one of four ECS Categorization Fields, and indicates the lowest level in the ECS category hierarchy.

`event.outcome` simply denotes whether the event represents a success or a failure from the perspective of the entity that produced the event.

Note that when a single transaction is described in multiple events, each event may populate different values of `event.outcome`, according to their perspective.

Also note that in the case of a compound event (a single event that contains multiple logical events), this field should be populated with the value that best captures the overall success or failure from the perspective of the event producer.

Further note that not all events will have an associated outcome. For example, this field is generally not populated for metric events, events with `event.type:info`, or any events for which an outcome does not make logical sense.

**Allowed values**

* [failure](#ecs-event-outcome-failure)
* [success](#ecs-event-outcome-success)
* [unknown](#ecs-event-outcome-unknown)


## failure [ecs-event-outcome-failure]

Indicates that this event describes a failed result. A common example is `event.category:file AND event.type:access AND event.outcome:failure` to indicate that a file access was attempted, but was not successful.


## success [ecs-event-outcome-success]

Indicates that this event describes a successful result. A common example is `event.category:file AND event.type:create AND event.outcome:success` to indicate that a file was successfully created.


## unknown [ecs-event-outcome-unknown]

Indicates that this event describes only an attempt for which the result is unknown from the perspective of the event producer. For example, if the event contains information only about the request side of a transaction that results in a response, populating `event.outcome:unknown` in the request event is appropriate. The unknown value should not be used when an outcome doesn’t make logical sense for the event. In such cases `event.outcome` should not be populated.

