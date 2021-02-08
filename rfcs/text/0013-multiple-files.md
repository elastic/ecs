# 0013: Multiple files in an event

<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (Draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

Many security events refer to more than one file at the same time or contain duplicated attributes for files.
Examples of this are file copies or modifications.
ECS has current support for multiple users in an event that was originally introduced in a previous RFC, this builds on the ideas introduced there, but for files.

## Fields

The new fields discussed in this RFC are the following:

- `file.target.*`
- `file.changes.*`

Note that `file` would need to be made reusable with the following entries.

```YAML
# schemas/file.yml excerpt
  reusable:
    top_level: true
    expected:
      # Added for this RFC
      - at: file
        as: target
      - at: file
        as: changes
```

Currently `file` has 21 top-level fields and has a good number of fields that can be nested under it such as `code_signature`, `hash`, `pe`, and `x509`, so we may want to clarify exactly which fields we want to include (maybe just the top-level?).

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

### File Modifications

This can happen, for example if file permissions change, a file is renamed, or a file is written to (size/hash modification).

Examples of data sources where this is applicable:

- General FIM events
- Syscall monitoring of `fchmod`-style calls
- Windows Security log events including [#4670](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4670)

Here's an example where a file's permissions octet on Linux is changed from `0700` to `0755`:

```JSON
{
  "file": {
    "name": "test.txt",
    "mode": "0700",
    "changes": {
      "mode": "0755"
    }
  }
}
```

Here's an example of a file rename event;

```JSON
{
  "file": {
    "name": "abc.txt",
    "changes": {
      "name": "def.txt"
    }
  }
}
```

Notice that `changes` only captures the fields that changed, not the fields that remain the same between modifications.

Additionally, in some cases we're not always going to have access to the original field value (i.e. running `chmod 755 ...` isn't going to contain data about the original file permissions). Users should actively fill in all data that they can for the top-level fields, but, even if there is no corresponding top-level field, `changes` may contain the fields that are assumed to be modified.

### File Copies

This is a bit more complex than a modification. This can happen, for example if a file is duplicated via `cp` or some other utility, if a file is remotely transfered, or if a symlink or hardlink is created that references back to the original file. Unlike the modification events, I would imagine that copying would likely require most of the fields from the top-level of the file fields to be present in `target`, as file ownership, location, extensions, devices, timestamps, and names can all change during a copy event.

The following example shows a minimum of fields, but the idea is that all fields could be present in both the top-level and `target` nesting in the event.

```JSON
{
  "file": {
    "name": "abc.txt",
    "directory": "/home/user",
    "extension": "txt",
    "target": {
      "name": "def.exe",
      "directory": "/tmp",
      "extension": "exe"
    }
  }
}
```

## Source data

Here are some concrete examples of events with file modifications or multiple files.

### Linux chmod auditd rules

Here's an example of auditd monitoring the `chmod` command.

```
type=PROCTITLE msg=audit(1581217915.853:1357): proctitle=63686D6F6400373737002F746D702F74657374
type=PATH msg=audit(1581217915.853:1357): item=1 name="/lib64/ld-linux-x86-64.so.2" inode=306773 dev=103:01 mode=0100755 ouid=0 ogid=0 rdev=00:00 obj=system_u:object_r:ld_so_t:s0 objtype=NORMAL cap_fp=0000000000000000 cap_fi=0000000000000000 cap_fe=0 cap_fver=0
type=PATH msg=audit(1581217915.853:1357): item=0 name="/bin/chmod" inode=25188546 dev=103:01 mode=0100755 ouid=0 ogid=0 rdev=00:00 obj=system_u:object_r:bin_t:s0 objtype=NORMAL cap_fp=0000000000000000 cap_fi=0000000000000000 cap_fe=0 cap_fver=0
type=CWD msg=audit(1581217915.853:1357): cwd="/etc/audit/rules.d"
type=EXECVE msg=audit(1581217915.853:1357): argc=3 a0="chmod" a1="777" a2="/tmp/test"
type=SYSCALL msg=audit(1581217915.853:1357): arch=c000003e syscall=59 success=yes exit=0 a0=1284850 a1=1283f30 a2=14627f0 a3=7ffeb56f35a0 items=2 ppid=2242 pid=4700 auid=1002 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts0 ses=5 comm="chmod" exe="/usr/bin/chmod" subj=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 key="chmod_rule"
```

The corresponding file document would look something like this:

```JSON
{
  "event": {
    "kind": "event",
    "category": ["file"],
    "type": ["change"]
  },
  "file": {
    "name": "test",
    "directory": "/tmp",
    "target": {
      "mode": "0777",
    }
  }
}
```

### Linux chown auditd syscall

```
type=SYSCALL msg=audit(1611091464.740:263): arch=c000003e syscall=260 success=yes exit=0 a0=ffffffffffffff9c a1=12d6210 a2=3e9 a3=ffffffff items=1 ppid=9492 pid=9494 auid=1000 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts2 ses=8 comm="chown" exe="/usr/bin/chown" subj=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 key="access"
type=CWD msg=audit(1611091464.740:263): cwd="/home/vagrant"
type=PATH msg=audit(1611091464.740:263): item=0 name="test" inode=921833 dev=fd:02 mode=0100664 ouid=9999 ogid=1000 rdev=00:00 obj=unconfined_u:object_r:user_home_t:s0 objtype=NORMAL cap_fp=0000000000000000 cap_fi=0000000000000000 cap_fe=0 cap_fver=0
type=PROCTITLE msg=audit(1611091464.740:263): proctitle=63686F776E002D5200616C6963650074657374
```

The uid is captured in `a2` in hexidecimal and corresponds to the value `1001`, so this would be"

```JSON
{
  "event": {
    "kind": "event",
    "category": ["file"],
    "type": ["change"]
  },
  "file": {
    "name": "test",
    "directory": "/home/vagrant",
    "inode": 921833,
    "mode": "0664",
    "target": {
      "uid": "1001"
    }
  }
}
```

<!--
Get Windows event log examples or log entries from other products
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

The fields `file.[changes|target].*` are new fields,
so they don't represent a breaking change. They are especially important
for security-related data sources around FIM and audit logs.
These event sources should be adjusted to populate these new fields.

## Concerns

### Field mapping explosions for nested field sets

The primary concern for this RFC is that `file` has numerous field sets that might be nested under it. I believe that a potential solution for this would be limiting `target` and `changes` to only contain the top-level `file` fields (i.e. no `file.changes.pe`), in which case we would introduce 42 new fields, corresponding to two copies of the 21 existing `file.*` fields duplicated under `target` and `changes`.

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate the risk of churn and instability by resolving outstanding concerns.
-->

## People

The following are the people that consulted on the contents of this RFC.

- @andrewstucki | author

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

- Stage 1: https://github.com/elastic/ecs/pull/1231
