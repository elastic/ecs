---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-device.html
applies_to:
  stack: all
  serverless: all
---

# Device fields [ecs-device]

Fields that describe a device instance and its characteristics. Data collected for applications and processes running on a (mobile) device can be enriched with these fields to describe the identity, type and other characteristics of the device.

This field group definition is based on the Device namespace of the [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/device/).

::::{warning}
These fields are in beta and are subject to change.
::::



## Device field details [_device_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-device-id$$$[device.id](#field-device-id) | The unique identifier of a device. The identifier must not change across application sessions but stay fixed for an instance of a (mobile) device.<br><br>On iOS, this value must be equal to the vendor identifier ([https://developer.apple.com/documentation/uikit/uidevice/1620059-identifierforvendor](https://developer.apple.com/documentation/uikit/uidevice/1620059-identifierforvendor)). On Android, this value must be equal to the Firebase Installation ID or a globally unique UUID which is persisted across sessions in your application.<br><br>For GDPR and data protection law reasons this identifier should not carry information that would allow to identify a user.<br><br>type: keyword<br><br>example: `00000000-54b3-e7c7-0000-000046bffd97`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [device.id](https://opentelemetry.io/docs/specs/semconv/attributes-registry/device/#device-id)<br> | extended |
| $$$field-device-manufacturer$$$[device.manufacturer](#field-device-manufacturer) | The vendor name of the device manufacturer.<br><br>type: keyword<br><br>example: `Samsung`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [device.manufacturer](https://opentelemetry.io/docs/specs/semconv/attributes-registry/device/#device-manufacturer)<br> | extended |
| $$$field-device-model-identifier$$$[device.model.identifier](#field-device-model-identifier) | The machine readable identifier of the device model.<br><br>type: keyword<br><br>example: `SM-G920F`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [device.model.identifier](https://opentelemetry.io/docs/specs/semconv/attributes-registry/device/#device-model-identifier)<br> | extended |
| $$$field-device-model-name$$$[device.model.name](#field-device-model-name) | The human readable marketing name of the device model.<br><br>type: keyword<br><br>example: `Samsung Galaxy S6`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [device.model.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/device/#device-model-name)<br> | extended |
| $$$field-device-serial-number$$$[device.serial_number](#field-device-serial-number) | The unique serial number serves as a distinct identifier for each device, aiding in inventory management and device authentication.<br><br>type: keyword<br><br>example: `DJGAQS4CW5`<br> | core |
