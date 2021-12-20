**Copied on Dec-20-2021 from private repo:   
https://github.com/elastic/security-team/blob/main/docs/adaptive-workload-protection-team/architecture/linux-event-model.md  
Please look there for the most up to date version of this document.**

# Introduction

One of Cmd’s main features is the ability to render Linux sessions in
a web browser as a time-ordered series of process executions that
looks similar to an interactive shell session.  This document
introduces the underlying event model used to build this view in order
to facilitate mapping it to Elastic Common Schema (ECS).

It is important to maintain this document and the derived ECS mapping
document as means to precisely define the meaning of each field.  This
document defines the fields by referencing/re-using the field names from the
primary Linux documentation, the man pages, "man 5 proc" and "man 7
credentials" in particular.

We focus on the events necessary to produce the session view -
primarily events related to process execution and terminal
output. Other events Cmd uses for cloud workload capture and augmented
session view, such as file and network accesses, will be added over
time.  Container information will also be added as we approach the
milestones for presenting it.

In general, this approach converges on the ability to see possible
data flows through your systems with a level of detail (who, what data,
how/what software) vastly exceeding what is possible solely from a
network perspective (due pervasive encryption in transit).  For
example this approach would allow tracking a subverted web server
shelling out, with lateral movement to another server, accessing data
from a database and stashing it on another server with network egress
access where it would be exfiltrated a week later.  With data
classification, this would allow for very simple rule specification
such as "alert on secret data potentially leaving the servers
permitted to access secret category data".


# Linux Session Model

Linux follows the Unix process model from the 1970s that was augmented
with the concept sessions in the 1980s. One must have a basic
understanding of this model in order to understand how the events
presented in this document can be rendered into a session view.

## Process Events Are Simpler Than System Call Logs

Note that capturing changes to the session model in terms of new
processes, new sessions, exiting processes etc. is simpler and clearer
than capturing the system calls used to enact those changes.  Linux
has approximately 400 system calls and does not refactor them in order
to retain a stable application binary interface (ABI) - i.e. programs
compiled to run on Linux years ago, should continue to run on Linux
today without recompiling.  Instead of refactoring, new system calls
are added to improve capabilities or security.  The upshot is that
mapping a time ordered list of system calls and their parameters to
the logical actions performed by those that did not return error codes
takes a significant amount of expertise.  Newer system calls such as
those of io_uring make it possible to read and write files and sockets
with no system calls by using automatically monitored request and
result ring buffers memory mapped between kernel and user space. By
contrast the process event model is stable and understandable yet
still comprehensively covers the actions taken on a system.

## Process Formation Starting from Linux Boot

When the Linux kernel has started it creates a special process called
“the init process”.  A process embodies the execution of (typically)
one program.  The init process always has the process id (PID) of 1
and is executed with a user id of 0 (root).  Most modern Linux
distributions use systemd as their init process executable program.
The job of systemd is to start the configured services such as
databases, web servers, and remote access services such as sshd.
These services are typically encapsulated within their own sessions
which simplifies starting and stopping services by grouping all
processes of each service under a single session id (SID).

Remote access such as via ssh to an sshd service, if successfully
authenticated, will create a new Linux session for the accessing user.
This session will execute the program the remote user requested, often
an interactive shell, and the associated process(es) will all have the
same SID.

## The Mechanics of Creating a Process

Every process, except the init process, has a single parent process.
Each process has PPID, the process id of its parent process (0 in the
case of Init).  Reparenting, typically to init/PID 1, can occur if a
parent process exits in a way that does not also terminate the child
process.

To create a child process, the parent clones itself via the fork() or
clone() system call.  Post-clone, execution continues in both the
parent and the child (unless the now deprecated vfork() was used), but
along different code paths by virtue of the return code value from
fork/clone. You read that correctly - one clone/fork system call
provides a return code in two different processes! There are some
cloning nuances with multi-threaded parents and copy-on-write memory
for efficiency that do need to be elaborated on here.  The child
process inherits the memory state of the parent and open files, the
controlling terminal, if any, and network sockets.

Typically the parent process will capture the PID of the child to
monitor its lifecycle.  The child process behavior depends on the
program that cloned itself.

A web server such as nginx might clone itself, creating a child
process to handle http connections.  In cases like this, the child
process does not execute a new program but simply runs a different
code path in the same program, to handle http connections in this
case. Recall that the return value from clone or fork tells the child
that it is the child so it can choose this code path.

Interactive shell processes (e.g. one of bash, sh, fish, zsh, etc),
possibly from an ssh session, clone themselves whenever a command is
entered. The child process does a bunch of work setting up file
descriptors for IO redirection, setting the process group, and more
before the code path in the child calls execve() or similar to run a
different program inside that process.  If you type ls into your
shell, it forks your shell, the setup described above is done by the
shell/child and then ls is executed to replace the contents of that
process with the code for ls.

It is important to note that a process can call execve() more than
once, and therefore workload capture data models must handle this as
well.  This means that a process can become many different programs
before it exits – not just its parent process program optionally
followed by one program.  See the shell exec command for a way to do
this in a shell (i.e. replace the shell program with another in the
same process).  Another aspect of executing a program in a process is
that some open file descriptors (those marked as close-on-exec) may be
closed prior to the exec of the new program, while others may remain
available to the new program.  Recall that a single fork/clone call
provides a return code in two processes, the parent and the child.
The exec system call is strange as well in that a successful exec has
no return code because it results in a new program execution (nowhere
to return to).

\[TODO: section on reaping child processes, zombies and reparenting\]

## Creating New Sessions

Linux currently creates new sessions with a single system call,
setsid(), which is called by the process becoming the session leader.
This call is often part of the cloned child’s code path run before
exec’ing another program in that process (i.e. it’s planned by and
included in the parent process’ code).  All processes within a session
share the same SID, which is the same as the PID of the process that
called setsid(), also known as the session leader. In other words, a
session leader is any process with a PID that matches its SID.  The
exit of the session leader process will trigger termination of its
immediate children processes.

## Creating New Process Groups

Linux uses process groups to identify a group of processes working
together within a session. They will always have the same SID and
process group id (PGID).  The PGID is the PID of the process group
leader. There is no special status for the process group leader; it
may exit with no effect on other members of the process group and they
retain the same PGID, even though the process with that PID no longer
exists.  Note that even with pid-wrap (re-use of a recently used pid
on busy systems), the Linux kernel ensures the PGID pid of an exited
process group leader is not reused until all members of that process
group have exited.


Process groups are valuable for shell pipeline commands like: 

```shell
cat foo.txt | grep bar | wc -l
```

which creates three processes for three different programs (cat, grep
and wc) and connects them with pipes.  Shells will create a new
process group even for single program commands like “ls”.  The purpose
of process groups is to permit targeting of signals to a set of
processes and to identify a set of processes, the foreground process
group, that are permitted full read and write access to their
session’s controlling terminal, if any. In other words control-C in
your shell will send a signal to all processes in the foreground
process group (the negative PGID value as the signal’s pid target
discriminates between the group versus the process group leader
process itself).  The controlling terminal association ensures that
processes reading input from the terminal don’t compete with each
other and cause issues (terminal output may be permitted from
non-foreground process groups).  Special Sessions and Processes [To
Add - paragraphs on entry point services - sshd, getty, ssm, etc
sessions that exist as means to create sessions remotely, and the
importance of retaining the provenance of these sessions]

\[TODO: add definition of entry/inception session, session leader,
last-known user-entered-process(group)\]

\[TODO: add why capturing/denormalizing these ancestor processes with
each fork & exec provides essential context for efficient/join-free
search/forensics and search-free ingest-time alerting\]

## Terminal Output

Session view shows terminal output for interactive sessions (those
that have an associated controlling terminal/tty).  This output is
important as it represents an avenue for data exfiltration; the remote
user could copy and paste the text they see, perhaps a private key, in
the terminal application on their laptop. It may also identify the
information a potential attacker is seeking such as the output of a
database query. For example, “SELECT * FROM some_badly_named_table”
may only reveal the fields of value in the output.  Terminal output
also captures shell, Python REPL, Ruby REPL, etc. commands as entered
by the user.

Note that most services such as web servers, databases, etc. started
by the Init process do not have a controlling terminal. One exception
is the getty program which may be started by Init to permit logins on
the console, an attached terminal or an IPMI BMC masquerading as a
serial port. SSH and SSM also permit remote creation of
non-interactive sessions if requested by the remote user.

Terminal output typically includes what was typed into the terminal by
the remote user, the terminal input, because most terminals are
configured to echo back what they receive.  This is the simplest place
to capture shell commands as they are entered by the user, rather than
instrumenting all the versions of all the shells with eBPF uprobes or
similar.  The terminal subsystem is part of the Linux kernel so there
are specific kernel functions that can be monitored with eBPF to
capture terminal output.  This is more desirable than monitoring every
write to every file descriptor to check if the device’s major and
minor numbers identify it as a terminal/tty.

## Linux Namespaces and CGroups

[TODO: define purpose of namespaces and cgroups, the 8 namespaces and
how they are identifed by inode numbers in nsfs ]

[TODO: observe from the host pid namespace and others if possible and
why]

# Event Model for Capturing Sessions

As described above, Linux workloads consist of a hierarchy of
processes starting, executing programs zero or more times, and
eventually terminating.  The events described below are designed to
capture a workload as a series of change events that could be applied,
in-order, to a snapshot of the process state to precisely record the
state of the workloads over time. With care (idempotency, before and
after data in each event), the events could be applied forwards or
backwards from a snapshot.  This approach is ideal for capture for
forensics and being able to alert and respond to all changes compared
to point-in-time snapshots by themselves (e.g. like an OSQuery
results).  Linux process lifetimes may be sub-second, so
point-in-time, query-based approaches will miss information unless
their underlying data model retains historic information for longer
periods than the query interval.

## Shared Data Types for Event Composition

The next subsections define data types that are reused across the
event types.

The field names in the shared data types below are named to align with
the names used in the Linux man pages.  This alignment reduces
documentation overhead (no Rosetta Stone type mapping documents
required) and reduces chances of misinterpretation of the semantics of
each field.

The following man pages are valuable as a starting point for learning more:
* man 5 proc
* man 7 namespaces
* man 7 credentials
* man 7 pty
* man 2 setsid

### Observer - observation perspective

Multiple sensors may run on the same Linux server, possibly in
containers. Concurrent use of the same identifiers such as process ids
can lead to confusing telemetry unless they are related to the
perspective from which they are observed.

The fields of the Observer shared data type are:

1. boot_id, uuid as per /proc/sys/kernel/random/boot_id,
   e.g. 88a1f0ed-5ae5-41ee-af6b-41921c311872.  Note the boot_id value
   from /proc may or may not be the same in containers as on the
   host. Some container runtimes will bind mount a new boot_id value
   onto the proc file in each container.

2. pid_ns_id, unsigned int inum in include/linux/ns_common.h. This is
   the inode number of the namespace in the namespace file system
   (nsfs).

### User

Note that file system user id and name are not retained given that
they closely shadow the effective user id (see “man 7 credentials”).

It is possible for the name portion to be unknown due to an incomplete
/etc/passwd file (common in container images) or incorrectly
configured name service switch. Unknown names are represented by
absent name fields or empty string names.

The fields of the User shared data type are:

1. real: \{ id, name \}
2. effective: \{ id, name \}
3. saved: \{ id, name \}

### Group

The comments in the User subsection apply here to for group names and file system group.

The fields of the Group shared data type are:

1. real: \{ id, name \}
2. effective: \{ id, name \}
3. saved: \{ id, name \}
4. supplemental: \[ \{ id, name \},...\]

### Namespace

Ideally namespace creation events are sent up as they occur and when
they are modified with their relevant information in order give a
dynamic view of their lifecycle.  With this model, process events can
reference the namespaces in which they are operating without needing
to re-iterate the full details of those namespace.  For example, a
filesystem mount namespace may have several kB of information about
the filesystems mounted on it which we would not want to send with
every process execution in that namespace.

One strategy to keep namespace modifications from creating too many
events, such as an event as each filesystem is mounted in a mount
namspace would be trigger namespace events upon the first process exec
in that namespace.  It is unlikely the namespaces will change after
this.

Snapshots would ideally contain namespace details as well and
associate the processes in a snapshot with a namespace.  Recall that
snapshots provide a summary of the current state so one does not have
to find a process or namespace creation event that could have occurred
weeks ago, and may have fallen out of the retention window.

\[TODO: exact recording TBD. It will be different for each of the 8
namespaces\]

### Kubernetes Process - per process Kubernetes information

\[TODO: define process environment to capture (Pod etc) that a
Kubernetes operator can relate to such as kube: \{ cluster, namespace,
pod_name\}\]

### Kubernetes Node - per server node Kubernetes information

\[TODO: define server/node information to capture that a Kubernetes
operator can relate to such as node id, host OS info etc\]


### Container Image

\[TODO: define container information that would allow correlation back
build system and the associated software manifests,
e.g. container_image: \{ name/url, manifest_hash, tag\} \]

### File Description

Note the terminology here aligned with correct usage as seen in “man 5
proc” where the file descriptor is the user space integer “address” to
the actual file description information held in the kernel.

Inode numbers in Linux are C unsigned long values. This means they may
be 8 bytes/64 bits on 64 bit CPUs. Inode number fields are specified
as strings below because JSON positive integer values should be less
than 2^53 for interoperability. These string values are the inode
number in decimal (e.g. "12345").

The fields of the File Description shared data type are:

1. type: string, one of "file", "char_device"(tty), "pipe", "fifo", "socket", "epoll", "signal",
   "inotify", "bpf", "event", "perf_event", "timer", "userfault", "namespace",
   "io_uring"
2. descriptor:int (e.g. 0 for stdin, etc)
2. char_device: \{ major:int, minor:int \}
3. file: \{ block_device {major:int, minor:int\}, inode.num:string, path:string \}
4. socket: \{
   * domain:int (AF_INET, AF_UNIX etc)
   * type:int (SOCK_STREAM, SOCK_DGRAM, etc)  // note: MIPS arch swaps STREAM and DGRAM values!!
   * protocol:int (typically 0, e.g. AF_INET+SOCK_STREAM+0 is TCP)
   * tcp \{ local_addr.port:ushort, local_addr.ip, remote_addr.port:ushort, remote_addr.ip, is_listening:bool \} // local_addr info present if bind() called, remote_addr present if connected. is_listening is true iff listen() has been called on a bound socket.
   * udp \{ local_addr.port:ushort, local_addr.ip, remote_addr.port:ushort, remote_addr.ip \} // local_addr info present if bind() called, remote_addr present if connect() called
   * unix \{ local_addr.path:string, local_addr.inode.num:string, remote_addr.path:string, remote_addr.inode.num:string \} // local_addr.path present if bind() called, remote_addr.path present if connect() called
   * \}
6. pipe: \{ inode.num:string, read_end:bool \}
7. fifo: \{ inode.num:string, path:string, read_end:bool }

### Terminal

These values define how applications such as editors and shells have
configured the terminal and how they decide how to display things like
colors and highlighting.  Important aspects of the c_* bit flags
fields include whether UTF-8 is supported and if echoing of input is
enabled.  Terminal row count, column count, TERM environment variable
and other fields can be a user fingerprint as well. See “man 5
terminfo” and “man 2 ioctl_tty” for more information.

The fields of the Terminal shared data type are:

1. env.term is the TERM environment variable, which may have values
like “xterm-256color”.  This defines how terminal aware programs
determine how to change terminal colors etc.
2. winsize.row: unsigned short
3. winsize.col: unsigned short
4. termio.c_iflag: unsigned short
5. termio.c_oflag: unsigned short
6. termio.c_cflag: unsigned short
7. termio.c_lflag: unsigned short
8. termio.c_line: unsigned char
8. termio.c_cc: unsigned char[N] - characters used to send signals.  No need to capture.


## Process

The fields of the Process shared data type are:

1. relation: one or more of  primary, parent, group_leader, session_leader, entry_session_leader, or last_user_entered.  These describe relationships a process has to others captured in this event. For example the parent process may also be a session leader, or the primary process is often the group leader.  This is intended to avoid unnecessary duplication of the same structured values in events.
2. exe - full path of executable
3. cmdline - [ string ] where the array position reflects argument’s position on the command line / to the exec system call
4. global_pid: uuid deterministically derived from f(pid, starttime, observer.pid_ns, observer..boot_id) in order to provide a unique identifier to a process over the life of the sensor. Becomes globally unique when taken in context with the sensor id.
5. pid
5. starttime
6. pgid  - this and the following process ids include starttime for pid wrap disambiguation and because while an event contains information about a set of related processes, that set is not guaranteed to to contain the parent, process group, and sesion leader of every one of those processes.  The process start times are also included here for this reason to allow for disambiguation in case of pid wrap.
7. pg_starttime
8. ppid
9. parent_starttime
10. sid
11. session_leader_starttime
12. user: User shared data type
13. group: Group shared data type
14. cwd
15. tty: \{char_device {major:int, minor: int\}, terminal: Terminal
    shared data type \}. 
    Will be absent if there is no controlling
    terminal for the session. Only needs to present in one process of
    the set of processes in the event (use the primary process).
16. lowest_fds: \[ File Description shared data type \]. First N
    (configurable, e.g. 10) of the process’s lowest numbered file
    descriptors.
17. highest_fds: \[ File Description shared data type \]. Last M
    (configurable, e.g. 5) of the process’s highest file descriptors.

\[TODO: describe exact signatures for process relationship types such as entry_session and last_user_entered etc.\]

\[TODO: Consider: defining signatures of entrypoint services such as sshd, ssm, kubelet, etc as well\]

### Entry Session Metadata

This contains valuable information about Entry Session (aka Inception
session) such as the remote IP address for the ssh entry point.

The fields of the Entry Session Metadata shared data type are:

1. remote_ip: IP address (v4 or v6)
2. entry_service_type: one of (sshd, ssm, kubelet, teleport, terminal, console)


## Process Fork/Clone Event

The fields of the Fork Event are:

1. event_type: “fork”
2. observer: Observer shared data type
3. entry_session_metadata : Entry Session Metadata shared data type
4. processes: [Process shared data type]. Array covering the following
   process relationships with the “primary” process, the child of the
   fork event in this case, at the time of the fork. The length of the
   array doesn't imply the number of relationships as some process
   entries may represent multiple relationships (this also holds for
   exec and exit events)
   * primary - the child process of the fork or clone system call
   * parent
   * group_leader
   * session_leader
   * entry_session_leader
   * last_user_entered

## Program Execution Event

Note that the top level exe and cmdline are distinct from those of the
primary process, and represent the arguments to the exec system call.
Those in the primary process represent those from the previous call to
exec in this process, or if this is the first exec call, those of the
forking parent.

The fields of the Process Execution Event are:

1. event_type: “exec”
2. observer: Observer shared data type
3. exe: path of file being executed
4. cmdline: \[string\] of arguments (argv) to the program be executed
5. env_vars: [{ name,value}] of a small number of specifically
   identified environment variables of interest.  For example,
   LD_PRELOAD has security relevance.
6. entry_session_metadata : Entry Session Metadata shared data type
7. processes: [Process shared data type]. Array covering the following
   process relationships with the “primary” process, the process
   calling exec in this case, at the time of the exec.
   * primary - process call the exec system call
   * parent
   * group_leader
   * session_leader
   * entry_session_leader
   * last_user_entered

## Process Exit Event

The fields of the Process Exit Event are:

1. event_type: “exit”
2. observer: Observer shared data type
3. exit_code:  the process’s exit code
4. entry_session_metadata : Entry Session Metadata shared data type
5. processes: [Process shared data type]. Array covering the following
   process relationships with the “primary” process, the exiting
   process in this case, at the time of exit.
   * primary - the process exiting
   * parent
   * group_leader
   * session_leader
   * entry_session_leader
   * last_user_entered

## Output Event

For now we will only capture output events to controlling terminals so
the fd value will always represent a tty. The primary process will
hold its controlling terminal configuration in its tty field.

Note that echoed back input text for a terminal may be enacted from
tty driver in the kernel (depending on the configuration of the
terminal - e.g. in cooked mode).  So there's no actual primary process
responsible for this output - the tty driver just sends a copy back.
In these cases we try to find the likely process that is receiving
this input to associate with the output event: find this tty's
session's foreground process group leader process (or next process you
can find in that process group if the process group leader has
exited).  Ideally this groups actual output from that process and the
echoed input as coming from the same process to simplify review.

The fields of the Output Event are:

1. event_type: “output”
2. observer: Observer shared data type
3. output: the bytes being written to the fd. If fd is a controlling
   terminal, its configuration captured with the primary process’s
   controlling terminal, and may help interpreting how these bytes
   were rendered.
4. fd: Filedescriptor shared data type that is being written to
4. echoed: boolean - true if the output was echoed terminal input.
5. entry_session_metadata : Entry Session Metadata shared data type
6. processes: [Process shared data type]. Array covering the following
   process relationships with the “primary” process, the process
   writing to the terminal in this case, at the time of exit. For
   echoed input, the primary process should still be the process that
   is on the “pts side”, e.g. bash not the sshd child process reading
   input from the ssh TCP connection (the “pty side”).  Note that more
   than one process may have an open fd to this tty so when picking
   the primary process for echoed text the session's foreground
   process group leader should be chosen (by definition it representes
   the set of processes allowed to write to the tty)
   * primary - the process exiting
   * parent
   * group_leader
   * session_leader
   * entry_session_leader
   * last_user_entered

## New Session Creation Event

Recording new session leaders events ensures we become aware of their
new status since their may not be a following exec to show that they
are now a session leader (pid == sid).

The fields of the Session Creation Event are:

1. event_type: “session_creation”
2. observer: Observer shared data type
3. entry_session_metadata : Entry Session Metadata shared data type
4. processes: [Process shared data type]. Array covering the following
   process relationships with the “primary” process, the process *
   calling setsid in this case, at the time of the call.
   * primary - the process calling setsid, with information prior to
     setsid completion (ie its SID information is as before the call)
   * parent
   * group_leader
   * session_leader
   * entry_session_leader
   * last_user_entered

## Process Tree Snapshot Event

The fields of the Process Tree Snapshot Event are:

1. processes : [ Process shared data type]. Array with an entry for
   each existing processes on the server.  Note that this information
   cannot be captured atomically so it is possible for some
   process references to be inconsistent (e.g. parent process has
   exited and does not exist in the tree).
2. network_config: WIP but should include hostname and IPs
3. version : uname -a type info
4. sys_config: important system configuration information such as /proc/sys/kernel/pid_max (ie whether pid wrap is a concern)


# Elastic Common Schema Mapping

See separate document: https://github.com/elastic/security-team/pull/2071

# Filtering and Views of the Captured Data

\[TODO: finish this section\]

* Why filtering (not saving all events in ES) is valuable
* key filtering configurations and the most important fields to
  consider (e.g. with EQL for filtering)
  * specific event types (fork, exec, exit, setsid, file, network)
  * specific entry points descendants only (ssh, ssm, kublet etc)
  * entry point descendant sessions (note tmux/re-parenting)
  * in-session events vs just session leader/existence
  * executable +/- descendants 0(current is), 1(parent is) or All(ancestor is this exec)
  * Linux users or uids
  * Linux groups or gids (as primary or supplemental group)
  * Remotely attested userid or its absence
  * Remotely attested group or its absence
  * has controlling tty?
  * snapshot frequency & snapshot content
* rendering approaches for the key filtering configurations (ie how to
  deal with the missing/incomplete data while still offering value)
