# 0040: Volume device
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2023-09-11** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This RFC propose adding the volume device fieldset to describe volume storage devices such as hard disks, removable USB, mountable virtual disks such as ISO.

 * volume.mount_name
 * volume.device_name
 * volume.dos_name
 * volume.nt_name
 * volume.bus_type
 * volume.writable
 * volume.default_access
 * volume.file_system_type
 * volume.product_id
 * volume.product_name
 * volume.vendor_id
 * volume.vendor_name
 * volume.serial_number
 * volume.device_type
 * volume.size
 * volume.removable

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->
Details of the proposed fields:

```
---
- name: volume
  title: Volume
  group: 2
  short: Fields relevant to storage volumes.
  description: >
    Fields that describe the storage volumes.
  type: group
  fields:
    - name: mount_name
      level: extended
      type: keyword
      description: >
        Mount name of the volume device.
        The field is relevant to Posix only.

    - name: device_name
      level: extended
      type: keyword
      description: >
        Full path of the device.
        The field is relevant to Posix only.

    - name: dos_name
      level: extended
      type: keyword
      short: DOS name of the device.
      description: >
        DOS name of the device.
        DOS device name is in the format of uppercase driver letter followed by colon, such as C:, D:,...
        The field is relevant to Windows only.

    - name: nt_name
      level: extended
      type: keyword
      short: NT name of the device.
      description: >
        NT name of the device.
        NT device name is in the format such as:
        \Device\HarddiskVolume2
        The field is relevant to Windows only.

    - name: bus_type
      level: extended
      type: keyword
      short: Bus type of the device.
      description: >
        Bus type of the device, such as Nvme, Usb, FileBackedVirtual,... etc.

    - name: writable
      level: extended
      type: boolean
      description: >
        This field indicates if the volume is writable.

    - name: default_access
      level: extended
      type: keyword
      short: Bus type of the device.
      description: >
        A string to describe the default access(es) of the volume.

    - name: file_system_type
      level: extended
      type: keyword
      short: Volume device file system type.
      description: >
        Volume device file system type.

        Following are examples of the most frequently seen volume device file system types:
        NTFS
        UDF

    - name: product_id
      level: extended
      type: keyword
      short: ProductID of the device.
      description: >
        ProductID of the device. It is provided by the vendor of the device if any.

    - name: product_name
      level: extended
      type: keyword
      description: >
        Product name of the volume device. It is provided by the vendor of the device.

    - name: vendor_id
      level: extended
      type: keyword
      short: VendorID of the device.
      description: >
        VendorID of the device. It is provided by the vendor of the device.

    - name: vendor_name
      level: extended
      type: keyword
      short: Vendor name of the device.
      description: >
        Vendor name of the volume device. It is provided by the vendor of the device.

    - name: serial_number
      level: extended
      type: keyword
      short: Serial Number of the device.
      description: >
        Serial Number of the device. It is provided by the vendor of the device if any.

    - name: device_type
      level: extended
      type: keyword
      short: Volume device type.
      description: >
        Volume device type.

        Following are examples of the most frequently seen volume device types:
        Disk File System
        CD-ROM File System

    - name: size
      level: extended
      type: long
      description: >
        Size of the volume device in bytes.

    - name: removable
      level: extended
      type: boolean
      description: >
        This field indicates if the volume is removable.

```

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
These volume device fields can be used to describe some events and alerts associated with a volume device, which was proven to be [useful](https://www.elastic.co/security-labs/Hunting-for-Suspicious-Windows-Libraries-for-Execution-and-Evasion) for Elastic Defend.

These fields can also be used by the products and features to manage such devices based on their properties such as serial number and vendor name, etc.

## Source data

The source of this data comes from monitoring a host, a Virtual Machine, or a k8s node.

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->
```json
{
    "@timestamp":"2023-08-24T12:37:59.9817807Z",
    "agent":
    {
        "id":"ada69fee-8801-4248-9ea5-acada41cef88",
        "type":"endpoint",
        "version":"8.10.0-SNAPSHOT"
    },
    "data_stream":
    {
        "dataset":"endpoint.events.volume_device",
        "namespace":"default",
        "type":"logs"
    },
    "ecs":
    {
        "version":"1.11.0"
    },
    "elastic":
    {
        "agent":
        {
            "id":"ada69fee-8801-4248-9ea5-acada41cef88"
        }
    },
    "event":
    {
        "action":"mount",
        "category": [
            "volume_device"
        ],
        "created":"2023-08-24T12:37:59.9817807Z",
        "dataset":"endpoint.events.volume_device",
        "id":"NCRD4OiOt10Kj8r9++++++e0",
        "kind":"event",
        "module":"endpoint",
        "outcome":"success",
        "sequence":1759,
        "type": [
            "start"
        ]
    },
    "host":
    {
        "architecture":"x86_64",
        "hostname":"win11vm",
        "id":"01d52cf8-1917-4fab-8317-100076ab9aab",
        "ip":
        [
            "192.168.2.3","127.0.0.1","::1"
        ],
        "mac": [
            "00-0a-9d-b2-55-61"
        ],
        "name":"win11vm",
        "os":
        {
            "Ext":
            {
                "variant":"Windows 11 Pro"
            },
            "family":"windows",
            "full":"Windows 11 Pro 22H2 (10.0.22621.2134)",
            "kernel":"22H2 (10.0.22621.2134)",
            "name":"Windows",
            "platform":"windows",
            "type":"windows",
            "version":"22H2 (10.0.22621.2134)"
        }
    },
    "message":"Endpoint volume device event",
    "process":
    {
        "Ext":
        {
            "code_signature": [
                {
                    "exists":true,
                    "status":"trusted",
                    "subject_name":"Microsoft Windows",
                    "trusted":true
                }
            ]
        },
        "code_signature":
        {
            "exists":true,
            "status":"trusted",
            "subject_name":"Microsoft Windows",
            "trusted":true
        },
        "entity_id":"NWRhNjlkZWUtODgwNS00MjZiLTllYTUtYmM5ZGE0MGMwZjc3LTY1ODAtMTY5Mjc1ODgyNC40OTIxMjU5MDA=",
        "executable":"C:\\Windows\\explorer.exe",
        "name":"explorer.exe",
        "pid":6580
    },
    "user":
    {
        "domain":"WIN11VM",
        "id":"S-1-5-21-3464081356-156823451-1687200008-1001",
        "name":"john"
    },
    "volume":
    {
        "bus_type":"FileBackedVirtual",
        "device_type":"CD-ROM File System",
        "dos_name":"E:",
        "file_system_type":"UDF",
        "nt_name":"\\Device\\CdRom1",
        "product_name":"Virtual DVD-ROM",
        "serial_number":"",
        "vendor_name":"Msft",
        "size": 1000,000,000,
        "removable": true
    }
}
```

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->
As this RFC involves the creation of an entirely new fieldset, no breaking
changes are envisaged. Some existing tooling might need updates to factor in the
new fieldset's availability, however.


## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->
Implementing volume device related functions usually will be relying on low level operating system support. Due to the multitudes of operating system kernels we want to support and the potential stability,compatibility issues, the complexity level of the solution could increase.   Therefore we'll adopt a staged approach to implement it.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

 * @Trinity2019      | author, sponsor
 * @ricardoungureanu | reviewer
 * @stanek-michal    | reviewer
 * @intxgo           | reviewer

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

https://github.com/microsoft/mdatp-devicecontrol/blob/main/Removable%20Storage%20Access%20Control%20Samples/macOS/policy/device_control_policy_schema.json

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2201

* Stage 1: https://github.com/elastic/ecs/pull/2229

* Stage 2: https://github.com/elastic/ecs/pull/2260

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
