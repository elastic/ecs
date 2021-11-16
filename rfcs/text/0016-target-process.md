# 0016: Target process fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **X (abandoned)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-11-16** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC is to add model events that span multiple processes. There are some events for when one OS process accesses another. In Windows, this starts with a call to `OpenProcess` to gain a handle and then there are several APIs for things you can do with the handle once its open. For all of these operations, the general concept persists: one process requested access to another.

The most common use cases for Windows:
* reading the memory space, which is most famously done by mimikatz
* injecting code
* attaching a debugger
* reading the Process Environment Block (PEB) for other benign or nefarious purpose

## Stage X

This RFC is not being worked on actively, and it has been marked as abandoned. If an individual wishes to advance it in the future, open a new pull request against this proposal.

## Fields

**Stage 0**


| Name | Type | Description |
| ---- | ---- | ----------- |
| process.* | group | Remains unchanged and is always the _source_ process for cross-process activity. |
| process.target.* | group | The `process.*` fieldset reused at `process.target.*` |
| process.target.parent.* | group | Capture information about the parent of the target process. |

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

**Stage 1**
This causes reuse of the `process.*` field set at two locations:
* `process.target.*`
* `process.parent.target*`


The `process.parent.target` reused fieldset could be descoped if it's too complex or increases the field count too significantly. It does have value, because information of the parent process of the target remains valuable. More on that utility in the next section.

```yml
  reusable:
    top_level: true
    expected:
      - at: process
        as: parent
      - at: process
        as: target
      # collect the parent of the target process at process.target.parent
      - at: process.target
        as: parent
```

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Target process information is valuable to detect several kinds of attacker behavior, but also good to profile or audit a system.
The most commonly known attacker behaviors where one process directly accesses another:

* Process injection [T1055](https://attack.mitre.org/techniques/T1055/)
* Access token manipulation [T1134](https://attack.mitre.org/techniques/T1134/)
* Credential theft from lsass [T1003.001](https://attack.mitre.org/techniques/T1003/001/)


Here are some example detections that could be written in KQL:

| Example rule name              | KQL query                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Injection to a browser         | event.action : "process_injection" and process.target.name : ("GoogleChrome.exe", "iexplore.exe", "firefox.exe") |
| Token theft from explorer      | event.action : "token_theft" and process.name : (not "explorer.exe") and process.target.name : "explorer.exe" |
| Injection to a service process | event.action : "process_injection" and process.target.parent.name : "services.exe" |
| Password dumping from lsass    | event.action : "process_memory_read" and process.target.name : "lsass.exe" |
| Generic process access         | event.action : "process_access" an process.target.name : * |


## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

Example sources of data include EDR-like products that collect operating system telemetry. Although cross-process events are more commonly known with Windows (injection, memory reads), they are also possible with Linux and macOS. The most universal use case across operating systems is attaching remote debuggers, which could be used for benign or malicious purposes.


Example event from Microsoft Sysmon [source](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90010), which is used by Winlogbeat:

    Process accessed:
    UtcTime: 2017-05-15 00:02:01.463
    SourceProcessGUID: {d49b2de5-efa6-5918-0000-00104d553c00}
    SourceProcessId: 4704
    SourceThreadId: 4124
    SourceImage: C:\mimikatz\x64\mimikatz.exe
    TargetProcessGUID: {d49b2de5-e852-5918-0000-00100b0f0700}
    TargetProcessId: 1576
    TargetImage: C:\Windows\system32\winlogon.exe
    GrantedAccess: 0x40
    CallTrace: C:\Windows\SYSTEM32\ntdll.dll+a5594|C:\Windows\system32\KERNELBASE.dll+1e865|C:\mimikatz\x64\mimikatz.exe+77ad|C:\mimikatz\x64\mimikatz.exe+7759|C:\mimikatz\x64\mimikatz.exe+f095|C:\mimikatz\x64\mimikatz.exe+6610a|C:\mimikatz\x64\mimikatz.exe+65dc4|C:\mimikatz\x64\mimikatz.exe+4ac00|C:\mimikatz\x64\mimikatz.exe+4aa36|C:\mimikatz\x64\mimikatz.exe+4a81d|C:\mimikatz\x64\mimikatz.exe+6ebe5|C:\Windows\system32\KERNEL32.DLL+18102|C:\Windows\SYSTEM32\ntdll.dll+5c5b4

The `Target*` fields of the Sysmon event would map:
* `TargetProcessGUID` -> `process.target.entity_id`
* `TargetProcessID` -> `process.target.pid`
* `TargetProcessImage` -> `process.target.executable` and `process.target.name`

The `Source*` fields of the Sysmon would map:
* `SourceProcessGUID` -> `process.entity_id`
* `SourceProcessId` -> `process.pid`
* `SourceThreadId` -> `process.thread.tid` (side question: does it make sense to move `thread.*` from `process`?)
* `SourceImage` -> `process.executable` and `process.name`


<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
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

## Concerns


<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

The biggest concern is the duplication of fields and the double-nested `process` group at `process.target.parent`. This could require some updates to our reuse mechanism, but that's an issue internal to this repository. We should make sure that we don't accidentally populate `process.parent.target`, which would have different meaning. Because of this, we will need to make sure that we articulate what each reuse means, similar to https://www.elastic.co/guide/en/ecs/current/ecs-user.html#ecs-user-nestings.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @rw-access    | author
* @andrewstucki | co-author
* @devonakerr   | sponsor



## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1286
* Stage 1: https://github.com/elastic/ecs/pull/1297
