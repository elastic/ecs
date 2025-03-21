---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-faas.html
applies_to:
  stack: all
  serverless: all
---
% This file is automatically generated. Don't edit it manually!

# FaaS fields [ecs-faas]

The user fields describe information about the function as a service (FaaS) that is relevant to the event.

## FaaS field details [_faas_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-faas-coldstart$$$ [faas.coldstart](#field-faas-coldstart) | Boolean value indicating a cold start of a function.<br><br>type: boolean<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![match](https://img.shields.io/badge/match-93c93e?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [faas.coldstart](https://opentelemetry.io/docs/specs/semconv/attributes-registry/faas/#faas-coldstart) | extended |
| $$$field-faas-execution$$$ [faas.execution](#field-faas-execution) | The execution ID of the current function execution.<br><br>type: keyword<br><br>example: `af9d5aa4-a685-4c5f-a22b-444f80b3cc28`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![equivalent](https://img.shields.io/badge/equivalent-1ba9f5?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [faas.invocation_id](https://opentelemetry.io/docs/specs/semconv/attributes-registry/faas/#faas-invocation-id) | extended |
| $$$field-faas-id$$$ [faas.id](#field-faas-id) | The unique identifier of a serverless function.<br><br>For AWS Lambda it's the function ARN (Amazon Resource Name) without a version or alias suffix.<br><br>type: keyword<br><br>example: `arn:aws:lambda:us-west-2:123456789012:function:my-function` | extended |
| $$$field-faas-name$$$ [faas.name](#field-faas-name) | The name of a serverless function.<br><br>type: keyword<br><br>example: `my-function`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![match](https://img.shields.io/badge/match-93c93e?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [faas.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/faas/#faas-name) | extended |
| $$$field-faas-trigger-request-id$$$ [faas.trigger.request_id](#field-faas-trigger-request-id) | The ID of the trigger request , message, event, etc.<br><br>type: keyword<br><br>example: `123456789` | extended |
| $$$field-faas-trigger-type$$$ [faas.trigger.type](#field-faas-trigger-type) | The trigger for the function execution.<br><br>Expected values for this field:<br><br>* `http`<br>* `pubsub`<br>* `datasource`<br>* `timer`<br>* `other`<br><br>type: keyword<br><br>example: `http`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![equivalent](https://img.shields.io/badge/equivalent-1ba9f5?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [faas.trigger](https://opentelemetry.io/docs/specs/semconv/attributes-registry/faas/#faas-trigger) | extended |
| $$$field-faas-version$$$ [faas.version](#field-faas-version) | The version of a serverless function.<br><br>type: keyword<br><br>example: `123`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![match](https://img.shields.io/badge/match-93c93e?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [faas.version](https://opentelemetry.io/docs/specs/semconv/attributes-registry/faas/#faas-version) | extended |


