---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-allowed-values-event-type.html
applies_to:
  stack: all
  serverless: all
navigation_title: event.type
---

# ECS categorization field: event.type [ecs-allowed-values-event-type]

This is one of four ECS Categorization Fields, and indicates the third level in the ECS category hierarchy.

`event.type` represents a categorization "sub-bucket" that, when used along with the `event.category` field values, enables filtering events down to a level appropriate for single visualization.

This field is an array. This will allow proper categorization of some events that fall in multiple event types.

**Allowed values**

* [access](#ecs-event-type-access)
* [admin](#ecs-event-type-admin)
* [allowed](#ecs-event-type-allowed)
* [change](#ecs-event-type-change)
* [connection](#ecs-event-type-connection)
* [creation](#ecs-event-type-creation)
* [deletion](#ecs-event-type-deletion)
* [denied](#ecs-event-type-denied)
* [device](#ecs-event-type-device)
* [end](#ecs-event-type-end)
* [error](#ecs-event-type-error)
* [group](#ecs-event-type-group)
* [indicator](#ecs-event-type-indicator)
* [info](#ecs-event-type-info)
* [installation](#ecs-event-type-installation)
* [protocol](#ecs-event-type-protocol)
* [start](#ecs-event-type-start)
* [user](#ecs-event-type-user)


## access [ecs-event-type-access]

The access event type is used for the subset of events within a category that indicate that something was accessed. Common examples include `event.category:database AND event.type:access`, or `event.category:file AND event.type:access`. Note for file access, both directory listings and file opens should be included in this subcategory. You can further distinguish access operations using the ECS `event.action` field.


## admin [ecs-event-type-admin]

The admin event type is used for the subset of events within a category that are related to admin objects. For example, administrative changes within an IAM framework that do not specifically affect a user or group (e.g., adding new applications to a federation solution or connecting discrete forests in Active Directory) would fall into this subcategory. Common example: `event.category:iam AND event.type:change AND event.type:admin`. You can further distinguish admin operations using the ECS `event.action` field.


## allowed [ecs-event-type-allowed]

The allowed event type is used for the subset of events within a category that indicate that something was allowed. Common examples include `event.category:network AND event.type:connection AND event.type:allowed` (to indicate a network firewall event for which the firewall disposition was to allow the connection to complete) and `event.category:intrusion_detection AND event.type:allowed` (to indicate a network intrusion prevention system event for which the IPS disposition was to allow the connection to complete). You can further distinguish allowed operations using the ECS `event.action` field, populating with values of your choosing, such as "allow", "detect", or "pass".


## change [ecs-event-type-change]

The change event type is used for the subset of events within a category that indicate that something has changed. If semantics best describe an event as modified, then include them in this subcategory. Common examples include `event.category:process AND event.type:change`, and `event.category:file AND event.type:change`. You can further distinguish change operations using the ECS `event.action` field.


## connection [ecs-event-type-connection]

Used primarily with `event.category:network` this value is used for the subset of network traffic that includes sufficient information for the event to be included in flow or connection analysis. Events in this subcategory will contain at least source and destination IP addresses, source and destination TCP/UDP ports, and will usually contain counts of bytes and/or packets transferred. Events in this subcategory may contain unidirectional or bidirectional information, including summary information. Use this subcategory to visualize and analyze network connections. Flow analysis, including Netflow, IPFIX, and other flow-related events fit in this subcategory. Note that firewall events from many Next-Generation Firewall (NGFW) devices will also fit into this subcategory.  A common filter for flow/connection information would be `event.category:network AND event.type:connection AND event.type:end` (to view or analyze all completed network connections, ignoring mid-flow reports). You can further distinguish connection events using the ECS `event.action` field, populating with values of your choosing, such as "timeout", or "reset".


## creation [ecs-event-type-creation]

The "creation" event type is used for the subset of events within a category that indicate that something was created. A common example is `event.category:file AND event.type:creation`.


## deletion [ecs-event-type-deletion]

The deletion event type is used for the subset of events within a category that indicate that something was deleted. A common example is `event.category:file AND event.type:deletion` to indicate that a file has been deleted.


## denied [ecs-event-type-denied]

The denied event type is used for the subset of events within a category that indicate that something was denied. Common examples include `event.category:network AND event.type:denied` (to indicate a network firewall event for which the firewall disposition was to deny the connection) and `event.category:intrusion_detection AND event.type:denied` (to indicate a network intrusion prevention system event for which the IPS disposition was to deny the connection to complete). You can further distinguish denied operations using the ECS `event.action` field, populating with values of your choosing, such as "blocked", "dropped", or "quarantined".


## device [ecs-event-type-device]

The device event type is used for the subset of events within a category that are related to device objects. Common example: `event.category:host AND event.type:change AND event.type:device`. You can further distinguish device operations using the ECS `event.action` field.


## end [ecs-event-type-end]

The end event type is used for the subset of events within a category that indicate something has ended. A common example is `event.category:process AND event.type:end`.


## error [ecs-event-type-error]

The error event type is used for the subset of events within a category that indicate or describe an error. A common example is `event.category:database AND event.type:error`. Note that pipeline errors that occur during the event ingestion process should not use this `event.type` value. Instead, they should use `event.kind:pipeline_error`.


## group [ecs-event-type-group]

The group event type is used for the subset of events within a category that are related to group objects. Common example: `event.category:iam AND event.type:creation AND event.type:group`. You can further distinguish group operations using the ECS `event.action` field.


## indicator [ecs-event-type-indicator]

The indicator event type is used for the subset of events within a category that contain details about indicators of compromise (IOCs).

A common example is `event.category:threat AND event.type:indicator`.


## info [ecs-event-type-info]

The info event type is used for the subset of events within a category that indicate that they are purely informational, and don’t report a state change, or any type of action. For example, an initial run of a file integrity monitoring system (FIM), where an agent reports all files under management, would fall into the "info" subcategory. Similarly, an event containing a dump of all currently running processes (as opposed to reporting that a process started/ended) would fall into the "info" subcategory. An additional common examples is `event.category:intrusion_detection AND event.type:info`.


## installation [ecs-event-type-installation]

The installation event type is used for the subset of events within a category that indicate that something was installed. A common example is `event.category:package` AND `event.type:installation`.


## protocol [ecs-event-type-protocol]

The protocol event type is used for the subset of events within a category that indicate that they contain protocol details or analysis, beyond simply identifying the protocol. Generally, network events that contain specific protocol details will fall into this subcategory. A common example is `event.category:network AND event.type:protocol AND event.type:connection AND event.type:end` (to indicate that the event is a network connection event sent at the end of a connection that also includes a protocol detail breakdown). Note that events that only indicate the name or id of the protocol should not use the protocol value. Further note that when the protocol subcategory is used, the identified protocol is populated in the ECS `network.protocol` field.


## start [ecs-event-type-start]

The start event type is used for the subset of events within a category that indicate something has started. A common example is `event.category:process AND event.type:start`.


## user [ecs-event-type-user]

The user event type is used for the subset of events within a category that are related to user objects. Common example: `event.category:iam AND event.type:deletion AND event.type:user`. You can further distinguish user operations using the ECS `event.action` field.

