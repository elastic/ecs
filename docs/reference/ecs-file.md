---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-file.html
applies_to:
  stack: all
  serverless: all
---

# File fields [ecs-file]

A file is defined as a set of information that has been created on, or has existed on a filesystem.

File objects can be associated with host events, network events, and/or file events (e.g., those produced by File Integrity Monitoring [FIM] products or services). File fields provide details about the affected file associated with the event or metric.


## File field details [_file_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-file-accessed$$$[file.accessed](#field-file-accessed) | Last time the file was accessed.<br><br>Note that not all filesystems keep track of access time.<br><br>type: date<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.accessed](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-accessed)<br> | extended |
| $$$field-file-attributes$$$[file.attributes](#field-file-attributes) | Array of file attributes.<br><br>Attributes names will vary by platform. Here’s a non-exhaustive list of values that are expected in this field: archive, compressed, directory, encrypted, execute, hidden, read, readonly, system, write.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["readonly", "system"]`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.attributes](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-attributes)<br> | extended |
| $$$field-file-created$$$[file.created](#field-file-created) | File creation time.<br><br>Note that not all filesystems store the creation time.<br><br>type: date<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.created](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-created)<br> | extended |
| $$$field-file-ctime$$$[file.ctime](#field-file-ctime) | Last time the file attributes or metadata changed.<br><br>Note that changes to the file content will update `mtime`. This implies `ctime` will be adjusted at the same time, since `mtime` is an attribute of the file.<br><br>type: date<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.changed](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-changed)<br> | extended |
| $$$field-file-device$$$[file.device](#field-file-device) | Device that is the source of the file.<br><br>type: keyword<br><br>example: `sda`<br> | extended |
| $$$field-file-directory$$$[file.directory](#field-file-directory) | Directory where the file is located. It should include the drive letter, when appropriate.<br><br>type: keyword<br><br>example: `/home/alice`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.directory](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-directory)<br> | extended |
| $$$field-file-drive-letter$$$[file.drive_letter](#field-file-drive-letter) | Drive letter where the file is located. This field is only relevant on Windows.<br><br>The value should be uppercase, and not include the colon.<br><br>type: keyword<br><br>example: `C`<br> | extended |
| $$$field-file-extension$$$[file.extension](#field-file-extension) | File extension, excluding the leading dot.<br><br>Note that when the file name has multiple extensions (example.tar.gz), only the last one should be captured ("gz", not "tar.gz").<br><br>type: keyword<br><br>example: `png`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.extension](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-extension)<br> | extended |
| $$$field-file-fork-name$$$[file.fork_name](#field-file-fork-name) | A fork is additional data associated with a filesystem object.<br><br>On Linux, a resource fork is used to store additional data with a filesystem object. A file always has at least one fork for the data portion, and additional forks may exist.<br><br>On NTFS, this is analogous to an Alternate Data Stream (ADS), and the default data stream for a file is just called $DATA. Zone.Identifier is commonly used by Windows to track contents downloaded from the Internet. An ADS is typically of the form: `C:\path\to\filename.extension:some_fork_name`, and `some_fork_name` is the value that should populate `fork_name`. `filename.extension` should populate `file.name`, and `extension` should populate `file.extension`. The full path, `file.path`, will include the fork name.<br><br>type: keyword<br><br>example: `Zone.Identifer`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.fork_name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-fork-name)<br> | extended |
| $$$field-file-gid$$$[file.gid](#field-file-gid) | Primary group ID (GID) of the file.<br><br>type: keyword<br><br>example: `1001`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.group.id](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-group-id)<br> | extended |
| $$$field-file-group$$$[file.group](#field-file-group) | Primary group name of the file.<br><br>type: keyword<br><br>example: `alice`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.group.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-group-name)<br> | extended |
| $$$field-file-inode$$$[file.inode](#field-file-inode) | Inode representing the file in the filesystem.<br><br>type: keyword<br><br>example: `256383`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.inode](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-inode)<br> | extended |
| $$$field-file-mime-type$$$[file.mime_type](#field-file-mime-type) | MIME type should identify the format of the file or stream of bytes using [IANA official types](https://www.iana.org/assignments/media-types/media-types.xhtml), where possible. When more than one type is applicable, the most specific type should be used.<br><br>type: keyword<br> | extended |
| $$$field-file-mode$$$[file.mode](#field-file-mode) | Mode of the file in octal representation.<br><br>type: keyword<br><br>example: `0640`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.mode](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-mode)<br> | extended |
| $$$field-file-mtime$$$[file.mtime](#field-file-mtime) | Last time the file content was modified.<br><br>type: date<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.modified](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-modified)<br> | extended |
| $$$field-file-name$$$[file.name](#field-file-name) | Name of the file including the extension, without the directory.<br><br>type: keyword<br><br>example: `example.png`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-name)<br> | extended |
| $$$field-file-owner$$$[file.owner](#field-file-owner) | File owner’s username.<br><br>type: keyword<br><br>example: `alice`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.owner.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-owner-name)<br> | extended |
| $$$field-file-path$$$[file.path](#field-file-path) | Full path to the file, including the file name. It should include the drive letter, when appropriate.<br><br>type: keyword<br><br>Multi-fields:<br><br>- file.path.text (type: match_only_text)<br><br>example: `/home/alice/example.png`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.path](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-path)<br> | extended |
| $$$field-file-size$$$[file.size](#field-file-size) | File size in bytes.<br><br>Only relevant when `file.type` is "file".<br><br>type: long<br><br>example: `16384`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [file.size](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-size)<br> | extended |
| $$$field-file-target-path$$$[file.target_path](#field-file-target-path) | Target path for symlinks.<br><br>type: keyword<br><br>Multi-fields:<br><br>- file.target_path.text (type: match_only_text)<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.symbolic_link.target_path](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-symbolic-link-target-path)<br> | extended |
| $$$field-file-type$$$[file.type](#field-file-type) | File type (file, dir, or symlink).<br><br>type: keyword<br><br>example: `file`<br> | extended |
| $$$field-file-uid$$$[file.uid](#field-file-uid) | The user ID (UID) or security identifier (SID) of the file owner.<br><br>type: keyword<br><br>example: `1001`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [file.owner.id](https://opentelemetry.io/docs/specs/semconv/attributes-registry/file/#file-owner-id)<br> | extended |


## Field reuse [_field_reuse_9]

The `file` fields are expected to be nested at:

* `threat.enrichments.indicator.file`
* `threat.indicator.file`

Note also that the `file` fields may be used directly at the root of the events.


### Field sets that can be nested under file [ecs-file-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `file.code_signature.*` | [code_signature](/reference/ecs-code_signature.md) | These fields contain information about binary code signatures. |
| `file.elf.*` | [elf](/reference/ecs-elf.md) | This field re-use is beta and subject to change. These fields contain Linux Executable Linkable Format (ELF) metadata. |
| `file.hash.*` | [hash](/reference/ecs-hash.md) | Hashes, usually file hashes. |
| `file.macho.*` | [macho](/reference/ecs-macho.md) | This field reuse is beta and subject to change. These fields contain Mac OS Mach Object file format (Mach-O) metadata. |
| `file.pe.*` | [pe](/reference/ecs-pe.md) | These fields contain Windows Portable Executable (PE) metadata. |
| `file.x509.*` | [x509](/reference/ecs-x509.md) | These fields contain x509 certificate metadata. |
