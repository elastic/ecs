---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-process.html
applies_to:
  stack: all
  serverless: all
---

# Process fields [ecs-process]

These fields contain information about a process.

These fields can help you correlate metrics information with a process id/name from a log message.  The `process.pid` often stays in the metric itself and is copied to the global field for correlation.


## Process field details [_process_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-process-args$$$[process.args](#field-process-args) | Array of process arguments, starting with the absolute path to the executable.<br><br>May be filtered to protect sensitive information.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["/usr/bin/ssh", "-l", "user", "10.0.0.16"]`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [process.command_args](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-command-args)<br> | extended |
| $$$field-process-args-count$$$[process.args_count](#field-process-args-count) | Length of the process.args array.<br><br>This field can be useful for querying or performing bucket analysis on how many arguments were provided to start a process. More arguments may be an indication of suspicious activity.<br><br>type: long<br><br>example: `4`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.args_count](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-args-count)<br> | extended |
| $$$field-process-command-line$$$[process.command_line](#field-process-command-line) | Full command line that started the process, including the absolute path to the executable, and all arguments.<br><br>Some arguments may be filtered to protect sensitive information.<br><br>type: wildcard<br><br>Multi-fields:<br><br>- process.command_line.text (type: match_only_text)<br><br>example: `/usr/bin/ssh -l user 10.0.0.16`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.command_line](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-command-line)<br> | extended |
| $$$field-process-end$$$[process.end](#field-process-end) | The time the process ended.<br><br>type: date<br><br>example: `2016-05-23T08:05:34.853Z`<br> | extended |
| $$$field-process-entity-id$$$[process.entity_id](#field-process-entity-id) | Unique identifier for the process.<br><br>The implementation of this is specified by the data source, but some examples of what could be used here are a process-generated UUID, Sysmon Process GUIDs, or a hash of some uniquely identifying components of a process.<br><br>Constructing a globally unique identifier is a common practice to mitigate PID reuse as well as to identify a specific process over time, across multiple monitored hosts.<br><br>type: keyword<br><br>example: `c2c455d9f99375d`<br> | extended |
| $$$field-process-entry-meta-type$$$[process.entry_meta.type](#field-process-entry-meta-type) | The entry type for the entry session leader. Values include: init(e.g systemd), sshd, ssm, kubelet, teleport, terminal, console<br><br>Note: This field is only set on process.session_leader.<br><br>type: keyword<br> | extended |
| $$$field-process-env-vars$$$[process.env_vars](#field-process-env-vars) | Array of environment variable bindings. Captured from a snapshot of the environment at the time of execution.<br><br>May be filtered to protect sensitive information.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["PATH=/usr/local/bin:/usr/bin", "USER=ubuntu"]`<br> | extended |
| $$$field-process-executable$$$[process.executable](#field-process-executable) | Absolute path to the process executable.<br><br>type: keyword<br><br>Multi-fields:<br><br>- process.executable.text (type: match_only_text)<br><br>example: `/usr/bin/ssh`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [process.executable.path](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-executable-path)<br> | extended |
| $$$field-process-exit-code$$$[process.exit_code](#field-process-exit-code) | The exit code of the process, if this is a termination event.<br><br>The field should be absent if there is no exit code for the event (e.g. process start).<br><br>type: long<br><br>example: `137`<br> | extended |
| $$$field-process-interactive$$$[process.interactive](#field-process-interactive) | Whether the process is connected to an interactive shell.<br><br>Process interactivity is inferred from the processes file descriptors. If the character device for the controlling tty is the same as stdin and stderr for the process, the process is considered interactive.<br><br>Note: A non-interactive process can belong to an interactive session and is simply one that does not have open file descriptors reading the controlling TTY on FD 0 (stdin) or writing to the controlling TTY on FD 2 (stderr). A backgrounded process is still considered interactive if stdin and stderr are connected to the controlling TTY.<br><br>type: boolean<br><br>example: `True`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.interactive](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-interactive)<br> | extended |
| $$$field-process-io$$$[process.io](#field-process-io) | A chunk of input or output (IO) from a single process.<br><br>This field only appears on the top level process object, which is the process that wrote the output or read the input.<br><br>type: object<br> | extended |
| $$$field-process-io-bytes-skipped$$$[process.io.bytes_skipped](#field-process-io-bytes-skipped) | An array of byte offsets and lengths denoting where IO data has been skipped.<br><br>type: object<br><br>Note: this field should contain an array of values.<br> | extended |
| $$$field-process-io-bytes-skipped-length$$$[process.io.bytes_skipped.length](#field-process-io-bytes-skipped-length) | The length of bytes skipped.<br><br>type: long<br> | extended |
| $$$field-process-io-bytes-skipped-offset$$$[process.io.bytes_skipped.offset](#field-process-io-bytes-skipped-offset) | The byte offset into this event’s io.text (or io.bytes in the future) where length bytes were skipped.<br><br>type: long<br> | extended |
| $$$field-process-io-max-bytes-per-process-exceeded$$$[process.io.max_bytes_per_process_exceeded](#field-process-io-max-bytes-per-process-exceeded) | If true, the process producing the output has exceeded the max_kilobytes_per_process configuration setting.<br><br>type: boolean<br> | extended |
| $$$field-process-io-text$$$[process.io.text](#field-process-io-text) | A chunk of output or input sanitized to UTF-8.<br><br>Best efforts are made to ensure complete lines are captured in these events. Assumptions should NOT be made that multiple lines will appear in the same event. TTY output may contain terminal control codes such as for cursor movement, so some string queries may not match due to terminal codes inserted between characters of a word.<br><br>type: wildcard<br> | extended |
| $$$field-process-io-total-bytes-captured$$$[process.io.total_bytes_captured](#field-process-io-total-bytes-captured) | The total number of bytes captured in this event.<br><br>type: long<br> | extended |
| $$$field-process-io-total-bytes-skipped$$$[process.io.total_bytes_skipped](#field-process-io-total-bytes-skipped) | The total number of bytes that were not captured due to implementation restrictions such as buffer size limits. Implementors should strive to ensure this value is always zero<br><br>type: long<br> | extended |
| $$$field-process-io-type$$$[process.io.type](#field-process-io-type) | The type of object on which the IO action (read or write) was taken.<br><br>Currently only *tty* is supported. Other types may be added in the future for *file* and *socket* support.<br><br>type: keyword<br> | extended |
| $$$field-process-name$$$[process.name](#field-process-name) | Process name.<br><br>Sometimes called program name or similar.<br><br>type: keyword<br><br>Multi-fields:<br><br>- process.name.text (type: match_only_text)<br><br>example: `ssh`<br> | extended |
| $$$field-process-pgid$$$[process.pgid](#field-process-pgid) | Deprecated for removal in next major version release. This field is superseded by `process.group_leader.pid`.<br><br>Identifier of the group of processes the process belongs to.<br><br>type: long<br> | extended |
| $$$field-process-pid$$$[process.pid](#field-process-pid) | Process id.<br><br>type: long<br><br>example: `4242`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.pid](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-pid)<br> | core |
| $$$field-process-same-as-process$$$[process.same_as_process](#field-process-same-as-process) | This boolean is used to identify if a leader process is the same as the top level process.<br><br>For example, if `process.group_leader.same_as_process = true`, it means the process event in question is the leader of its process group. Details under `process.*` like `pid` would be the same under `process.group_leader.*` The same applies for both `process.session_leader` and `process.entry_leader`.<br><br>This field exists to the benefit of EQL and other rule engines since it’s not possible to compare equality between two fields in a single document. e.g `process.entity_id` = `process.group_leader.entity_id` (top level process is the process group leader) OR `process.entity_id` = `process.entry_leader.entity_id` (top level process is the entry session leader)<br><br>Instead these rules could be written like: `process.group_leader.same_as_process: true` OR `process.entry_leader.same_as_process: true`<br><br>Note: This field is only set on `process.entry_leader`, `process.session_leader` and `process.group_leader`.<br><br>type: boolean<br><br>example: `True`<br> | extended |
| $$$field-process-start$$$[process.start](#field-process-start) | The time the process started.<br><br>type: date<br><br>example: `2016-05-23T08:05:34.853Z`<br> | extended |
| $$$field-process-thread-capabilities-effective$$$[process.thread.capabilities.effective](#field-process-thread-capabilities-effective) | This is the set of capabilities used by the kernel to perform permission checks for the thread.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["CAP_BPF", "CAP_SYS_ADMIN"]`<br> | extended |
| $$$field-process-thread-capabilities-permitted$$$[process.thread.capabilities.permitted](#field-process-thread-capabilities-permitted) | This is a limiting superset for the effective capabilities that the thread may assume.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["CAP_BPF", "CAP_SYS_ADMIN"]`<br> | extended |
| $$$field-process-thread-id$$$[process.thread.id](#field-process-thread-id) | Thread ID.<br><br>type: long<br><br>example: `4242`<br> | extended |
| $$$field-process-thread-name$$$[process.thread.name](#field-process-thread-name) | Thread name.<br><br>type: keyword<br><br>example: `thread-0`<br> | extended |
| $$$field-process-title$$$[process.title](#field-process-title) | Process title.<br><br>The proctitle, some times the same as process name. Can also be different: for example a browser setting its title to the web page currently opened.<br><br>type: keyword<br><br>Multi-fields:<br><br>- process.title.text (type: match_only_text)<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.title](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-title)<br> | extended |
| $$$field-process-tty$$$[process.tty](#field-process-tty) | Information about the controlling TTY device. If set, the process belongs to an interactive session.<br><br>type: object<br> | extended |
| $$$field-process-tty-char-device-major$$$[process.tty.char_device.major](#field-process-tty-char-device-major) | The major number identifies the driver associated with the device. The character device’s major and minor numbers can be algorithmically combined to produce the more familiar terminal identifiers such as "ttyS0" and "pts/0". For more details, please refer to the Linux kernel documentation.<br><br>type: long<br><br>example: `4`<br> | extended |
| $$$field-process-tty-char-device-minor$$$[process.tty.char_device.minor](#field-process-tty-char-device-minor) | The minor number is used only by the driver specified by the major number; other parts of the kernel don’t use it, and merely pass it along to the driver. It is common for a driver to control several devices; the minor number provides a way for the driver to differentiate among them.<br><br>type: long<br><br>example: `1`<br> | extended |
| $$$field-process-tty-columns$$$[process.tty.columns](#field-process-tty-columns) | The number of character columns per line. e.g terminal width<br><br>Terminal sizes can change, so this value reflects the maximum value for a given IO event. i.e. where event.action = *text_output*<br><br>type: long<br><br>example: `80`<br> | extended |
| $$$field-process-tty-rows$$$[process.tty.rows](#field-process-tty-rows) | The number of character rows in the terminal. e.g terminal height<br><br>Terminal sizes can change, so this value reflects the maximum value for a given IO event. i.e. where event.action = *text_output*<br><br>type: long<br><br>example: `24`<br> | extended |
| $$$field-process-uptime$$$[process.uptime](#field-process-uptime) | Seconds the process has been up.<br><br>type: long<br><br>example: `1325`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/metric-cb00cb?style=flat "metric") [process.uptime](https://github.com/search?q=repo%3Aopen-telemetry%2Fsemantic-conventions+%22%3C%21--+semconv+metric.process.uptime+--%3E%22&type=code)<br> | extended |
| $$$field-process-vpid$$$[process.vpid](#field-process-vpid) | Virtual process id.<br><br>The process id within a pid namespace. This is not necessarily unique across all processes on the host but it is unique within the process namespace that the process exists within.<br><br>type: long<br><br>example: `4242`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.vpid](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-vpid)<br> | core |
| $$$field-process-working-directory$$$[process.working_directory](#field-process-working-directory) | The working directory of the process.<br><br>type: keyword<br><br>Multi-fields:<br><br>- process.working_directory.text (type: match_only_text)<br><br>example: `/home/alice`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [process.working_directory](https://opentelemetry.io/docs/specs/semconv/attributes-registry/process/#process-working-directory)<br> | extended |


## Field reuse [_field_reuse_20]

The `process` fields are expected to be nested at:

* `process.entry_leader`
* `process.entry_leader.parent`
* `process.entry_leader.parent.session_leader`
* `process.group_leader`
* `process.parent`
* `process.parent.group_leader`
* `process.previous`
* `process.responsible`
* `process.session_leader`
* `process.session_leader.parent`
* `process.session_leader.parent.session_leader`

Note also that the `process` fields may be used directly at the root of the events.


### Field sets that can be nested under process [ecs-process-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `process.attested_groups.*` | [group](/reference/ecs-group.md) | Reusing the `group` fields in this location is currently considered beta.<br>The externally attested groups based on an external source such as the Kube API.<br>Note: this reuse should contain an array of group field set objects. |
| `process.attested_user.*` | [user](/reference/ecs-user.md) | Reusing the `user` fields in this location is currently considered beta.<br>The externally attested user based on an external source such as the Kube API. |
| `process.code_signature.*` | [code_signature](/reference/ecs-code_signature.md) | These fields contain information about binary code signatures. |
| `process.elf.*` | [elf](/reference/ecs-elf.md) | This field reuse is beta and subject to change.<br>These fields contain Linux Executable Linkable Format (ELF) metadata. |
| `process.entry_leader.*` | `process` | First process from terminal or remote access via SSH, SSM, etc OR a service directly started by the init process. |
| `process.entry_leader.parent.*` | `process` | Information about the entry leader’s parent process. Only pid, start and entity_id fields are set. |
| `process.entry_leader.parent.session_leader.*` | `process` | Information about the parent session of the entry leader. Only pid, start and entity_id fields are set. |
| `process.entry_meta.source.*` | [source](/reference/ecs-source.md) | Remote client information such as ip, port and geo location. |
| `process.group.*` | [group](/reference/ecs-group.md) | The effective group (egid). |
| `process.group_leader.*` | `process` | Information about the process group leader. In some cases this may be the same as the top level process. |
| `process.hash.*` | [hash](/reference/ecs-hash.md) | Hashes, usually file hashes. |
| `process.macho.*` | [macho](/reference/ecs-macho.md) | This field reuse is beta and subject to change.<br>These fields contain Mac OS Mach Object file format (Mach-O) metadata. |
| `process.parent.*` | `process` | Information about the parent process. |
| `process.parent.group_leader.*` | `process` | Information about the parent’s process group leader. Only pid, start and entity_id fields are set. |
| `process.pe.*` | [pe](/reference/ecs-pe.md) | These fields contain Windows Portable Executable (PE) metadata. |
| `process.previous.*` | `process` | An array of previous executions for the process, including the initial fork. Only executable and args are set.<br>Note: this reuse should contain an array of process field set objects. |
| `process.real_group.*` | [group](/reference/ecs-group.md) | The real group (rgid). |
| `process.real_user.*` | [user](/reference/ecs-user.md) | The real user (ruid). Identifies the real owner of the process. |
| `process.responsible.*` | `process` | This field is beta and subject to change.<br>Responsible process in macOS tracks the originating process of an app, key for understanding permissions and hierarchy. |
| `process.saved_group.*` | [group](/reference/ecs-group.md) | The saved group (sgid). |
| `process.saved_user.*` | [user](/reference/ecs-user.md) | The saved user (suid). |
| `process.session_leader.*` | `process` | Often the same as entry_leader. When it differs, it represents a session started within another session. e.g. using tmux |
| `process.session_leader.parent.*` | `process` | Information about the session leader’s parent process. Only pid, start and entity_id fields are set. |
| `process.session_leader.parent.session_leader.*` | `process` | Information about the parent session of the session leader. Only pid, start and entity_id fields are set. |
| `process.supplemental_groups.*` | [group](/reference/ecs-group.md) | An array of supplemental groups.<br>Note: this reuse should contain an array of group field set objects. |
| `process.user.*` | [user](/reference/ecs-user.md) | The effective user (euid). |
