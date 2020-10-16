# 0000: Name of RFC
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

VirusTotal is an online repository of malicious software (malware). It provides free services that allow security professionals (hunters, intelligence analysts, SOC operators, incident responders, etc.) to search the VirusTotal database for file metadata such as hashes, Internet domains, and IP addresses.

In addition to searching for URLs, IP addresses, and file hashes, VirusTotal accepts the submission of files, URLs, and IP addresses and inspects submissions with over 70 antivirus scanners and URL/domain blacklisting services, in addition to a myriad of tools to extract signals from the studied content. Any user can select a file from their computer using their browser and send it to VirusTotal.

VirusTotal not only tells you whether a given antivirus solution detected a submitted file as malicious, but also displays each engine's detection label (e.g., I-Worm.Allaple.gen). The same is true for URL scanners, most of which will discriminate between malware sites, phishing sites, suspicious sites, etc.

VirusTotal is the standard in tier one malware threat hunting.

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->
```
- name: virustotal
  description: >
    Fields from the VirusTotal logs.
  default_field: false
  release: beta
  type: group
  fields:
    - name: analysis
      description: >
        Analysis information about the sample.
      default_field: false
      release: beta
      type: group
      fields:
        - name: date
          description: >
            Date and time sample was analyzed by VirusTotal.
          type: date
          default_field: false
        - name: results
          description: >
            Contains each engine's resulting data about sample
          type: nested
          fields:
            - name: method
              description: >
                Method used by VirusTotal for analysis.
              type: keyword
            - name: category
              description: >
                Category of the sample.
              type: keyword
            - name: result
              description: >
                Result of the VirusTotal analysis.
              type: keyword
            - name: engine_name
              description: >
                Name of the engine used for analysis.
              type: keyword
            - name: engine_version
              description: >
                Version of the engine used for analysis.
              type: keyword
            - name: engine_update
              description: >
                Last update of the engine used for analysis.
              type: date
        - name: stats
          default_field: false
          description: >
            Summary of the results field
          release: beta
          type: group
          fields:
            - name: failure
              type: integer
              description: >
                number of AV engines that fail when analysing that file
            - name: undetected
              type: integer
              description: >
                number of reports saying that is undetected
            - name: confirmed-timeout
              type: integer
              description: >
                Number of AV engines that reach a timeout when analyzing that file
            - name: harmless
              type: integer
              description: >
                number of reports saying that is harmless
            - name: malicious
              type: integer
              description: >
                number of reports saying that is malicious
            - name: suspicious
              type: integer
              description: >
                number of reports saying that is suspicious
            - name: timeout
              type: integer
              description: >
                number of timeouts when analyzing this URL/file
            - name: type-unsupported
              type: integer
              description: >
                number of AV engines that don't support that type of file

    - name: attributes
      type: flattened
      release: beta
      default_field: false
      description: >
        Fields returned by VirusTotal that are not yet mapped into a standard schema

    - name: community
      type: group
      release: beta
      default_field: false
      description: >
        Community metadata about the sample.
      fields:
        - name: total_votes
          type: group
          release: beta
          default_field: false
          description: >
            Community votes about the sample.
          fields:
            - name: harmless
              type: integer
              description: >
                Total number community of harmless votes.
            - name: malicious
              type: integer
              description: >
                Total number community of malicious votes.
        - name: reputation
          description: >
            Score calculated from all votes posted by the VirusTotal community
          type: float
        - name: rule
          description: >
            YARA matches for the file
          type: group
          fields:
            - name: name
              description: >
                matched rule name
              type: keyword
            - name: description
              description: >
                matched rule description
              type: text
            - name: match_in_subfile
              description: >
                whether the match was in a subfile or not
              type: boolean
            - name: ruleset_id
              description: >
                VirusTotal's ruleset ID
              type: keyword
            - name: ruleset
              description: >
                matched rule's ruleset name
              type: keyword
            - name: reference
              description: >
                ruleset source
              type: keyword
    - name: notification
      default_field: false
      description: >
        VirusTotal's context notification tags.
      release: beta
      type: group
      fields:
        - name: date
          description: >
            Time of live hunt notification.
          type: date
          default_field: false
        - name: snippet
          description: >
            VirusTotal's context notification snippets.
          type: text
        - name: tags
          type: keyword
    - name: submission
      description: >
        Metadata about this submission
      release: beta
      type: group
      fields:
        - name: source.geo.country_iso_code
          description: >
            ISO country code of source of submission
          type: keyword
        - name: source.key
          description: >
            Unique identifier of source of submission
          type: keyword
        - name: first_submitted
          description: >
            Date when the file was first seen in VirusTotal
          type: date
          default_field: false
        - name: last_submitted
          description: >
            Most recent date the file was posted to VirusTotal
          type: date
          default_field: false
        - name: submission_count
          description: >
            Number of times the sample has been submitted to VirusTotal
          type: integer
        - name: unique_sources
          description: >
            Unique sources that have submitted the sample to VirusTotal
          type: integer
    - name: downloadable
      description: >
        This sample is able to be downloaded from VirusTotal.
      type: boolean
    - name: last_modified
      description: >
        Date when the object itself was last modified.
      type: date
      default_field: false
    - name: androguard
      default_field: false
      description: >
        Shows information about Android APK, DEX and AXML files, extracted with the Androguard tool
      release: beta
      type: group
      fields:
        - name: activities
          description: >
            Contains the app's activity names
          type: keyword

        - name: version
          description: >
            AndroGuard version used
          type: keyword

        - name: android_application
          description: >
            android file type in integer format
          type: integer

        - name: android_application_error
          description: >
            Whether there was an error processing the application or not
          type: boolean

        - name: android_application_info
          description: >
            Android file type in readable form ("apk", "dex", "axml")
          type: keyword

        - name: android_version_code
          description: >
            Android version code, read from the manifest
          type: keyword

        - name: android_version_name
          description: >
            Android version name, read from the manifest
          type: keyword

        - name: libraries
          description: >
            Library names used in the app
          type: keyword

        - name: main_activity
          description: >
            Main activity name, read from the manifest
          type: keyword

        - name: minimum_sdk_version
          description: >
            Minimum supported sdk version
          type: keyword

        - name: package
          description: >
            Package name, read from the manifest
          type: keyword

        - name: providers
          description: >
            Providers used by the app
          type: keyword

        - name: receivers
          description: >
            Receivers used by the app
          type: keyword

        - name: risk_indicator
          description: >
            contains two keys: "apk" (structure) and "perm" (permissions) risk indicators
          type: flattened

        - name: services
          description: >
            Services used by the app
          type: keyword

        - name: strings_information
          description: >
            contains interesting strings found in the app
          type: keyword

        - name: target_sdk_version
          description: >
            Android version the app has been tested for
          type: keyword

        - name: vt_android_info
          description: >
            internal version of the Androguard tool used by VT
          type: float

        - name: certificate
          description: >
            app certificate details. Check SSL Certificate object to know more about its structure
          type: flattened

        - name: intent_filters
          description: >
            contains the app's intent filters
          type: flattened

        - name: permission_details
          description: >
            Details about the app's required permissions. Keys are permission names and values are dictionaries containing the following fields
          type: flattened

    - name: capabilities
      description: >
        List of representative tags related to the file's capabilities.
      type: keyword
    - name: bytehero_info
      type: keyword
      description: >
        TODO
      release: beta
    - name: exiftool
      default_field: false
      description: >
        Exiftool information about the sample.
      release: beta
      type: group
      fields:
        - name: character_set
          description: >
            Exiftool character set
          type: keyword
        - name: code_size
          description: >
            Exiftool code size
          type: keyword
        - name: company_name
          description: >
            Exiftool company name
          type: keyword
        - name: entry_point
          description: >
            Exiftool entry point
          type: keyword
        - name: file_description
          description: >
            Exiftool file description
          type: keyword
        - name: file_flags_mask
          description: >
            Exiftool file flags mask
          type: keyword
        - name: file_os
          description: >
            Exiftool file os
          type: keyword
        - name: file_size
          description: >
            Exiftool file size
          type: keyword
        - name: file_subtype
          description: >
            Exiftool file subtype
          type: keyword
        - name: file_type
          description: >
            Exiftool file type
          type: keyword
        - name: file_type_extension
          description: >
            Exiftool file type extension
          type: keyword
        - name: file_version
          description: >
            Exiftool file version
          type: keyword
        - name: file_version_number
          description: >
            Exiftool file version number
          type: keyword
        - name: image_version
          description: >
            Exiftool image version
          type: keyword
        - name: image_file_characteristics
          description: >
            Exiftool detected characteristics of executable
          type: keyword
        - name: initialized_data_size
          description: >
            Exiftool initialized data size
          type: keyword
        - name: internal_name
          description: >
            Exiftool internal name
          type: keyword
        - name: language_code
          description: >
            Exiftool language code
          type: keyword
        - name: legal_copyright
          description: >
            Exiftool legal copyright
          type: keyword
        - name: linker_version
          description: >
            Exiftool linker version
          type: keyword
        - name: mime_type
          description: >
            Exiftool mime type
          type: keyword
        - name: machine_type
          description: >
            Exiftool machine type
          type: keyword
        - name: os_version
          description: >
            Exiftool os version
          type: keyword
        - name: object_file_type
          description: >
            Exiftool object file type
          type: keyword
        - name: original_file_name
          description: >
            Exiftool original file name
          type: keyword
        - name: pe_type
          description: >
            Exiftool pe type
          type: keyword
        - name: product_name
          description: >
            Exiftool product name
          type: keyword
        - name: product_version
          description: >
            Exiftool product version
          type: keyword
        - name: product_version_number
          description: >
            Exiftool product version number
          type: keyword
        - name: subsystem
          description: >
            Exiftool subsystem
          type: keyword
        - name: subsystem_version
          description: >
            Exiftool subsystem version
          type: keyword
        - name: timestamp
          description: >
            Exiftool timestamp
          type: keyword
        - name: uninitialized_data_size
          description: >
            Exiftool uninitialized data size
          type: keyword
        - name: create_date
          description: >
            Exiftool create date
          type: keyword
        - name: creator
          description: >
            Exiftool creator
          type: keyword
        - name: creator_tool
          description: >
            Exiftool creator tool
          type: keyword
        - name: document_id
          description: >
            Exiftool document id
          type: keyword
        - name: linearized
          description: >
            Exiftool linearized
          type: keyword
        - name: modify_date
          description: >
            Exiftool modify date
          type: keyword
        - name: pdf_version
          description: >
            Exiftool pdf version
          type: keyword
        - name: page_count
          description: >
            Exiftool page count
          type: keyword
        - name: producer
          description: >
            Exiftool producer
          type: keyword
        - name: xmp_toolkit
          description: >
            Exiftool xmp toolkit
          type: keyword
        - name: cpu_architecture
          description: >
            Exiftool cpu architecture
          type: keyword
        - name: cpu_byte_order
          description: >
            Exiftool cpu byte order
          type: keyword
        - name: cpu_count
          description: >
            Exiftool cpu count
          type: keyword
        - name: cpu_type
          description: >
            Exiftool cpu type
          type: keyword
        - name: cpu_subtype
          description: >
            Exiftool cpu subtype
          type: keyword
        - name: object_flags
          description: >
            Exiftool object flags
          type: keyword
    - name: hash.vhash
      default_field: false
      description: >
        VirusTotal's proprietary fuzzy hashing
      release: beta
      type: keyword
    - name: id
      description: >
        VirusTotal's identifier for the sample.
      type: keyword
    - name: magic
      description: >
        A guess of the file type, based on a popular parsing tool from unix
      type: keyword
    - name: packers
      type: group
      description: >
        List of packer detection tools and their result.
      fields:
        - name: tool_name
          description: >
            Name of tool used to detect packer used.
          type: keyword
        - name: name
          description: >
            Name of identified packer(s).
          type: keyword
    - name: sigma_analysis
      type: flattened
      description: >
        Contains number of matched sigma rules group by its severity, same as sigma_analysis_stats
        but split by ruleset
    - name: sigma_analysis_stats
      type: group
      description: >
        Contains the number of matched sigma rules, grouped by its severity.
      fields:
        - name: critical
          type: integer
        - name: high
          type: integer
        - name: medium
          type: integer
        - name: low
          type: integer
    - name: tags
      description: >
        List of representative attributes according to VirusTotal
      type: keyword
    - name: trid
      default_field: false
      description: >
        TrID is a utility designed to identify file types from their binary signatures. It may give several detections,
        ordered by higher to lower probability of file format identification.
      release: beta
      type: group
      fields:
        - name: file_type
          description: Identified file type
          type: keyword
        - name: probability
          description: >
            Probability for a positive identification
          format: percent
          type: float
    - name: type_description
      description: >
        Describes the file type
      type: keyword
    - name: type_tag
      description: >
        Tags representing the file type
      type: keyword
```
## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

People can use this fieldset to organize data that is provided by VirusTotal.

This can be used to identify new threats within a protected or contested network as well as enrich data with additional metadata about files and network connections.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

Filebeat, specifically leveraging the VirusTotal Live Hunt module. https://github.com/elastic/beats/pull/21815

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
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate the risk of churn and instability by resolving outstanding concerns.
-->

<!--
Stage 4: Document any new concerns and their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## Real-world implementations

<!--
Stage 4: Identify at least one real-world, production-ready implementation that uses these updated field definitions. An example of this might be a GA feature in an Elastic application in Kibana.
-->

## People

The following are the people that consulted on the contents of this RFC.

* Derek Ditch (@dcode) | author, subject matter expert, grammar, spelling, prose
* Andrew Pease (@variable) | author, subject matter expert, grammar, spelling, prose
* Devon Kerr (@devon.kerr) | sponsor

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

* Stage 0: https://github.com/elastic/ecs/pull/1034

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
