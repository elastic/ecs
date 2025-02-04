# 0048: File Origin Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (Candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2024-XX-XX** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

It is known that when downloading files from the internet using a web browser (eg. Chrome, Edge, etc), information about the file's source is added to the file.
In Windows, it is known as the Mark of the Web and stored in file's Alternate Data Stream (ADS). In MacOS, it is stored in file's extended file attributes (metadata).

For example, in Windows, when you download an image file (`image17.webp`) from [this webpage](https://www.elastic.co/security-labs/pikabot-i-choose-you) using a web browser, the download source URL is automatically added to the file's Alternate Data Stream (ADS) as following.

<img width="578" alt="image" src="https://github.com/user-attachments/assets/b3dba571-1155-4226-88a0-fb9d67424d64">

* Inside `image17.webp:Zone.Identifier:$DATA`
<img width="804" alt="image" src="https://github.com/user-attachments/assets/f6058d40-d060-4dcb-9bdc-760e76389b45">

In ensuring endpoint security, the origin information of a file is crucial for determining whether a downloaded file or executable from the internet comes from a safe source and if it is safe to execute.

Thus, this PR adds new fields to store the URL of the file's origin information for `file`, `process`, and `dll`.
The ReferrerUrl is intended to be stored in the `origin_referrer_url` field, and the `HostUrl` is inteded to be stored in the `origin_url` field. 

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

The new fields proposed are:

Field | Type | Description /Usage
-- | -- | -- 
file.origin_referrer_url | keyword | The URL of the webpage that linked to the file.
file.origin_url | keyword | The URL where the file is hosted.
process.origin_referrer_url | keyword | The URL of the webpage that linked to the process's executable file.
process.origin_url | keyword | The URL where the process's executable file is hosted.
dll.origin_referrer_url | keyword | The URL of the webpage that linked to the dll file.
dll.origin_url | keyword | The URL where the dll file is hosted.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

* File
  * A file open event may be generated when a file is opened. By including the file's origin information in the event, the system can assess whether the file might be malware downloaded from a malicious website based on those URLs.
* Process
  * Generally, a process is generated from an executable file. However, there's a possibility that the executable file originating the process could be malware. To enhance security, we aim to include the executable file’s origin information at the process creation event and use the origin URL to help determine if the file is malicious.
* DLL
  * A process may load DLLs (libraries) as needed. However, there are cases where a malicious DLL prepared by an attacker might be loaded. To enhance security, we would like to check whether the loaded DLL was downloaded from the internet and, if so, where it was downloaded from. This information can help in determining whether the loaded DLL is malicious.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

Example sources of data is shown in the above.

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

The following is the real world example and usage for these fields.

### File (use case)
As mentioned above, when a file is downloaded from a web browser, the source URL information is recorded and attached to it.
<img width="804" alt="image" src="https://github.com/user-attachments/assets/f6058d40-d060-4dcb-9bdc-760e76389b45">

These fields could be invaluable in determining whether a file is downloaded from a malicious website, or a file which was previously downloaded originated from a newly identified malicious website. Just as an example, let’s say `https://outlook.office.com/` was discovered today to be a malicious website. These fields would help answer questions like, "How many files were downloaded from this website?"
![image](https://github.com/user-attachments/assets/9a546e7d-a0dd-4a1a-929d-12d8cbcc7c72)

Note - These fields are currently intended for use in file creation events, but I believe they could also be applied to file open events and other similar cases.

### Process (use case)
A process is created from an executable file, which contains the program's code and instructions.
Running a legitimate executable file is not an issue, but there is a risk that the file could be malware downloaded from a malicious website set up by an attacker. Therefore, if an executable file was downloaded from the internet, verifying its source is important for security.

Therefore, for security purposes, we would like to add these file origin fields to the process creation event. During process creation, the path of the executable file from which the process originates is typically included as following, and we expect to use this to identify the executable file path and collect the file origin information.

![image](https://github.com/user-attachments/assets/d95e35bc-7f92-4708-ba2c-3cc51c96ed62)

### DLL (use case)
DLL (shared code libraries) events indicate information about the libraries loaded by a process, and each event field contains details about the loaded DLL. As written in ECS(dll) yaml file, shared code libraries are used across all major operating systems, and each OS refers to them as follows:
* Windows: Commonly, Dynamic-link library (`.dll`)
* Unix-like operating systems: Commonly, Shared Object (`.so`)
* MacOS: Commonly, dynamic library (`.dylib`)

For reference, I investigated how many DLLs the Windows notepad.exe process loads. The results showed that over 100 DLLs are loaded. This indicates that checking which DLLs are loaded is crucial for both security and observability when analyzing a process's behavior.

![image](https://github.com/user-attachments/assets/7b5dadea-fd27-4c63-8d14-0b66ce39caef)

In security use cases, it is used to determine whether a DLL loaded by a process is a malicious one prepared by an attacker.
You might think that a legitimate process wouldn't load an unrelated third-party library, but in reality, there are techniques to force such libraries to be loaded (for example, a method known as DLL injection). Thus, in Elastic Defend, we monitor the behavior of processes loading DLLs in order to detect such attack techniques.

Additionally, there have been recent cases where legitimate programs were tampered with to load libraries prepared by attackers. For more details, please refer to the explanation below.
https://www.elastic.co/security-labs/sinking-macos-pirate-ships

Note - These fields are currently intended for use in DLL load events.


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

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @AsuNa-jp | author
* @joe-desimone
* @trisch-me 
* @mjwolf 

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

<!-- Insert any links appropriate to this RFC in this section. -->


### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2387
* Stage 1: https://github.com/elastic/ecs/pull/2395
* Stage 2: https://github.com/elastic/ecs/pull/2441

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
