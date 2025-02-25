---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-service-usage.html
applies_to:
  stack: all
  serverless: all
---

# Service fields usage and examples [ecs-service-usage]

Here are the subjects covered in this page.

* [Field reuse](#ecs-service-usage-field-reuse)

    * [Service fields at the Root of an Event](#ecs-service-usage-service-at-root)
    * [Describing external services in an invocation relationship](#ecs-service-usage-origin-target)



## Field reuse [ecs-service-usage-field-reuse]

The service fields can be used to * [describe the service for or from which the data was collected](#ecs-service-usage-service-at-root) (i.e. observed service) * or to [describe external services that have a direct invocation relationship](#ecs-service-usage-origin-target) to the observed service


### Service fields at the root of an event [ecs-service-usage-service-at-root]

Use the service fields at the root of an event to describe the service the event primarily relates to. An example for this use case is a log entry being recorded for a particular service or appplication (e.g. `MyService`):

```json
{
  "service": { <1>
    "id": "d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6",
    "name": "MyService",
    "version": "1.0.0"
  },
  ...
}
```

1. Describes the service for which the log entry is being captured



### Describing external services in an invocation relationship [ecs-service-usage-origin-target]

Multiple services can be in an invocation relationship. Where it is possible to apply [distributed tracing](docs-content://solutions/observability/apps/traces-2.md) on all the involved services describe the individual services [using root-level service fields](#ecs-service-usage-service-at-root) and use the [tracing fields](/reference/ecs-related.md) to represent the invocation relationship.

There are situations when distributed tracing cannot be applied on some external services that are in an invocation relationship to an observed service. Let’s consider the example of a service `MyService` being deployed on a cloud provider with an upstream API gateway that passes through requests to `MyService` (with additional context information about the API gateway itself). To describe the API gateway as a service from the perspective of `MyService` one can self-nest the service fields under `service.origin`:

```json
{
  "service": { <1>
    "id": "d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6",
    "name": "MyService",
    "version": "1.0.0",
    "origin": { <2>
      "id": "api-gateway-46372994637e2b4567",
      "name": "SomeGateway",
      "version" "2.5.1",
    }
  },
  ...
}
```

1. Describes the observed service that receives the inbound request from an external service
2. Describes the origin external service of the inbound request


Similar to the usage of `service.origin` fields the service fields can be self-nested under `service.target.*` to describe an external target service for an outbound request:

```json
{
  "service": { <1>
    "id": "d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6",
    "name": "MyService",
    "version": "1.0.0",
    "target": { <2>
      "id": "sms-service-0xe6c4272dbeAf0134",
      "name": "ManagedSMSService",
      "version": "1.9.0",
    }
  },
  ...
}
```

1. Describes the observed service that emits the outbound request to an external service
2. Describes the target external service of the outbound request


Note that `service.origin.*` and `service.target.*` fields should only be used on events that represent an invocation relationship.

