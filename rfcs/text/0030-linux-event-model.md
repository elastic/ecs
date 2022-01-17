# 0030: Linux event model
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This RFC aims to introduce a significant number of additions to ECS (mostly the 'Process' fieldset) in an effort to provide a rich enough linux event model to drive Session view in Kibana, as well as provide wider context to EQL and other rule engines. Care has been taken to ensure this RFC doesn't break any existing uses of the process field set, and should be fully backwards compatible with existing endpoint agents.

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

Link to the folder with fieldset yaml (deltas):
https://github.com/elastic/ecs/tree/24fac52a03bea4a984aec511aa47b5243acccbd4/rfcs/text/0030

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

1. Session View

The primary use case for this data will be to drive the "Session view". A time ordered rendering of a linux session process tree. The addition of nested process ancestors entry_leader, session_leader, and group_leader will allow Session View to load only the events for a particular session.

KQL examples:
process.entry_leader.entity_id: &lt;entity_id of entry session leader>

or

process.session_leader.entity_id: &lt;entity_id of session leader>

group_leader process info as well as file descriptors (process.fds) will allow the Session View to properly represent pipes and redirects in a familiar (shell) way.

observer.boot.id and observer.pid_ns_ino will be used in generating unique uuids for the process using fn(process.pid, process.start, observer.pid_ns_ino, observer.boot.id)

process.tty will be used to determine if the session is interactive. If the field is unset there is no controlling tty and the session is non-interactive (possibly a service).

file_description fieldset will primarily be used to render pipes and redirects, but shed light on processes file and socket activities.

2. Rule engines

The new nested ancestor processes will provide rule engines a widened context to allow for improved specificity/scope. Rather than rely on sequences of events to decide when to take action, an informed decision can be made on a single event. This opens up the door for much quicker and pre-emptive actions. Like stopping of processes, or isolating hosts.

KQL example:

Block a session if the user is connecting with root and trying to run mysql:
process.entry_leader.user.name: root AND process.executable: /bin/mysql


## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

The source of data will be via kprobes and ebpf sensors. All process execution lifecycle events will be sent up (fork, exec, end) as well as setsid, and output (tty) events.

Here is a mock example of these events:

### Fork event

```json
{
  '@timestamp': '2021-10-14T08:05:34.853Z',
  event: {
    kind: 'event',
    category: 'process',
    action: 'fork',
  },
  host: {
    architecture: 'x86_64',
    hostname: 'james-fleet-714-2',
    id: '48c1b3f1ac5da4e0057fc9f60f4d1d5d',
    ip: '127.0.0.1,::1,10.132.0.50,fe80::7d39:3147:4d9a:f809',
    mac: '42:01:0a:84:00:32',
    name: 'james-fleet-714-2',
    os: {
      Ext: {
        variant: 'CentOS'
      },
      family: 'centos',
      full: 'CentOS 7.9.2009',
      kernel: '3.10.0-1160.31.1.el7.x86_64 #1 SMP Thu Jun 10 13:32:12 UTC 2021',
      name: 'Linux',
      platform: 'centos',
      version: '7.9.2009'
    }
  },
  process: {
    id: '4321',
    args: ['/bin/sshd'],
    args_count: 1,
    command_line: 'sshd',
    executable: '/bin/sshd',
    name: 'sshd',
    interactive: false,
    working_directory: '/',
    pid: 3,
    start: '2021-10-14T08:05:34.853Z',
    user: {
      id: '2',
      name: 'kg',
    },
    parent: {
      id: '4322',
      args: ['/bin/sshd'],
      args_count: 1,
      command_line: 'sshd',
      executable: '/bin/sshd',
      name: 'sshd',
      interactive: true,
      working_directory: '/',
      pid: 2,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '0',
        name: 'root',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    group_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    session_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    entry_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      entry_meta: {
        type: 'sshd',
        source: {
          ip: '10.132.0.50',
          geo: {
            city_name: 'Vancouver',
            continent_code: 'NA',
            continent_name: 'North America',
            country_iso_code: 'CA',
            country_name: 'Canada',
            location: {
              lon: -73.614830,
              lat: 45.505918
            },
            postal_code: 'V9J1E3',
            region_iso_code: 'BC',
            region_name: 'British Columbia',
            timezone: 'America/Los_Angeles'
          }
        }
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    fds: [
      {
        descriptor:0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
      {
        descriptor:1,
        type:'pipe',
        pipe: {
          inode: '6183207'
        }
      }
    ],
    tty: {
      descriptor: 0,
      type: 'char_device',
      char_device: {
        major: 8,
        minor: 1
      }
    }
  }
}
```

### Exec event

```json
{
  '@timestamp': '2021-10-14T08:05:35.853Z',
  event: {
    kind: 'event',
    category: 'process',
    action: 'exec',
  },
  host: {
    architecture: 'x86_64',
    hostname: 'james-fleet-714-2',
    id: '48c1b3f1ac5da4e0057fc9f60f4d1d5d',
    ip: '127.0.0.1,::1,10.132.0.50,fe80::7d39:3147:4d9a:f809',
    mac: '42:01:0a:84:00:32',
    name: 'james-fleet-714-2',
    os: {
      Ext: {
        variant: 'CentOS'
      },
      family: 'centos',
      full: 'CentOS 7.9.2009',
      kernel: '3.10.0-1160.31.1.el7.x86_64 #1 SMP Thu Jun 10 13:32:12 UTC 2021',
      name: 'Linux',
      platform: 'centos',
      version: '7.9.2009'
    }
  },
  process: {
    id: '4321',
    args: ['/bin/bash'],
    args_count: 1,
    command_line: 'bash',
    executable: '/bin/bash',
    name: 'bash',
    interactive: true,
    working_directory: '/home/kg',
    pid: 3,
    start: '2021-10-14T08:05:34.853Z',
    user: {
      id: '2',
      name: 'kg',
    },
    parent: {
      id: '4322',
      args: ['/bin/sshd'],
      args_count: 1,
      command_line: 'sshd',
      executable: '/bin/sshd',
      name: 'sshd',
      interactive: true,
      working_directory: '/',
      pid: 2,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '0',
        name: 'root',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    group_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    session_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    entry_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      entry_meta: {
        type: 'sshd',
        source: {
          ip: '10.132.0.50',
          geo: {
            city_name: 'Vancouver',
            continent_code: 'NA',
            continent_name: 'North America',
            country_iso_code: 'CA',
            country_name: 'Canada',
            location: {
              lon: -73.614830,
              lat: 45.505918
            },
            postal_code: 'V9J1E3',
            region_iso_code: 'BC',
            region_name: 'British Columbia',
            timezone: 'America/Los_Angeles'
          }
        }
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    fds: [
      {
        descriptor:0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
      {
        descriptor:1,
        type:'pipe',
        pipe: {
          inode: '6183207'
        }
      }
    ],
    tty: {
      descriptor: 0,
      type: 'char_device',
      char_device: {
        major: 8,
        minor: 1
      }
    }
  },
}
```

### Exit event

```json
{
  '@timestamp': '2021-10-14T08:05:36.853Z',
  event: {
    kind: 'event',
    category: 'process',
    action: 'end',
  },
  host: {
    architecture: 'x86_64',
    hostname: 'james-fleet-714-2',
    id: '48c1b3f1ac5da4e0057fc9f60f4d1d5d',
    ip: '127.0.0.1,::1,10.132.0.50,fe80::7d39:3147:4d9a:f809',
    mac: '42:01:0a:84:00:32',
    name: 'james-fleet-714-2',
    os: {
      Ext: {
        variant: 'CentOS'
      },
      family: 'centos',
      full: 'CentOS 7.9.2009',
      kernel: '3.10.0-1160.31.1.el7.x86_64 #1 SMP Thu Jun 10 13:32:12 UTC 2021',
      name: 'Linux',
      platform: 'centos',
      version: '7.9.2009'
    }
  },
  process: {
    id: '4321',
    args: ['/bin/bash'],
    args_count: 1,
    command_line: 'bash',
    executable: '/bin/bash',
    name: 'bash',
    interactive: true,
    working_directory: '/home/kg',
    pid: 3,
    start: '2021-10-14T08:05:34.853Z',
    end: '2021-10-14T10:05:34.853Z',
    exit_code: 137,
    user: {
      id: '2',
      name: 'kg',
    },
    parent: {
      id: '4322',
      args: ['/bin/sshd'],
      args_count: 1,
      command_line: 'sshd',
      executable: '/bin/sshd',
      name: 'sshd',
      interactive: true,
      working_directory: '/',
      pid: 2,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '0',
        name: 'root',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
    },
    group_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    session_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
    },
    entry_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      entry_meta: {
        type: 'sshd',
        source: {
          ip: '10.132.0.50',
          geo: {
            city_name: 'Vancouver',
            continent_code: 'NA',
            continent_name: 'North America',
            country_iso_code: 'CA',
            country_name: 'Canada',
            location: {
              lon: -73.614830,
              lat: 45.505918
            },
            postal_code: 'V9J1E3',
            region_iso_code: 'BC',
            region_name: 'British Columbia',
            timezone: 'America/Los_Angeles'
          }
        }
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
    },
    fds: [
      {
        descriptor:0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
      {
        descriptor:1,
        type:'pipe',
        pipe: {
          inode: '6183207'
        }
      }
    ],
    tty: {
      descriptor: 0,
      type: 'char_device',
      char_device: {
        major: 8,
        minor: 1
      }
    }
  }
}
```

### Setsid event

```json
{
  '@timestamp': '2021-10-14T08:05:35.853Z',
  event: {
    kind: 'event',
    category: 'process',
    action: 'setsid',
  },
  host: {
    architecture: 'x86_64',
    hostname: 'james-fleet-714-2',
    id: '48c1b3f1ac5da4e0057fc9f60f4d1d5d',
    ip: '127.0.0.1,::1,10.132.0.50,fe80::7d39:3147:4d9a:f809',
    mac: '42:01:0a:84:00:32',
    name: 'james-fleet-714-2',
    os: {
      Ext: {
        variant: 'CentOS'
      },
      family: 'centos',
      full: 'CentOS 7.9.2009',
      kernel: '3.10.0-1160.31.1.el7.x86_64 #1 SMP Thu Jun 10 13:32:12 UTC 2021',
      name: 'Linux',
      platform: 'centos',
      version: '7.9.2009'
    }
  },
  process: {
    id: '4321',
    args: ['/bin/bash'],
    args_count: 1,
    command_line: 'bash',
    executable: '/bin/bash',
    name: 'bash',
    interactive: true,
    working_directory: '/home/kg',
    pid: 3,
    start: '2021-10-14T08:05:34.853Z',
    user: {
      id: '2',
      name: 'kg',
    },
    parent: {
      id: '4322',
      args: ['/bin/sshd'],
      args_count: 1,
      command_line: 'sshd',
      executable: '/bin/sshd',
      name: 'sshd',
      interactive: true,
      working_directory: '/',
      pid: 2,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '0',
        name: 'root',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    session_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    group_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    entry_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      entry_meta: {
        type: 'sshd',
        source: {
          ip: '10.132.0.50',
          geo: {
            city_name: 'Vancouver',
            continent_code: 'NA',
            continent_name: 'North America',
            country_iso_code: 'CA',
            country_name: 'Canada',
            location: {
              lon: -73.614830,
              lat: 45.505918
            },
            postal_code: 'V9J1E3',
            region_iso_code: 'BC',
            region_name: 'British Columbia',
            timezone: 'America/Los_Angeles'
          }
        }
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      }
    },
    fds: [
      {
        descriptor:0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
      {
        descriptor:1,
        type:'pipe',
        pipe: {
          inode: '6183207'
        }
      }
    ],
    tty: {
      descriptor: 0,
      type: 'char_device',
      char_device: {
        major: 8,
        minor: 1
      }
    }
  }
}
```

### Output event
```json
{
  '@timestamp': '2021-10-14T08:05:36.853Z',
  event: {
    kind: 'event',
    category: 'process',
    action: 'output',
  },
  host: {
    architecture: 'x86_64',
    hostname: 'james-fleet-714-2',
    id: '48c1b3f1ac5da4e0057fc9f60f4d1d5d',
    ip: '127.0.0.1,::1,10.132.0.50,fe80::7d39:3147:4d9a:f809',
    mac: '42:01:0a:84:00:32',
    name: 'james-fleet-714-2',
    os: {
      Ext: {
        variant: 'CentOS'
      },
      family: 'centos',
      full: 'CentOS 7.9.2009',
      kernel: '3.10.0-1160.31.1.el7.x86_64 #1 SMP Thu Jun 10 13:32:12 UTC 2021',
      name: 'Linux',
      platform: 'centos',
      version: '7.9.2009'
    }
  },
  process: {
    id: '4321',
    args: ['/bin/bash'],
    args_count: 1,
    command_line: 'bash',
    executable: '/bin/bash',
    name: 'bash',
    interactive: true,
    working_directory: '/home/kg',
    pid: 3,
    start: '2021-10-14T08:05:34.853Z',
    end: '2021-10-14T10:05:34.853Z',
    exit_code: 137,
    user: {
      id: '2',
      name: 'kg',
    },
    parent: {
      id: '4322',
      args: ['/bin/sshd'],
      args_count: 1,
      command_line: 'sshd',
      executable: '/bin/sshd',
      name: 'sshd',
      interactive: true,
      working_directory: '/',
      pid: 2,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '0',
        name: 'root',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
    },
    session_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
    },
    entry_leader: {
      id: '4321',
      args: ['bash'],
      args_count: 1,
      command_line: 'bash',
      executable: '/bin/bash',
      name: 'bash',
      interactive: true,
      working_directory: '/home/kg',
      pid: 3,
      start: '2021-10-14T08:05:34.853Z',
      user: {
        id: '2',
        name: 'kg',
      },
      entry_meta: {
        type: 'sshd',
        source: {
          ip: '10.132.0.50',
          geo: {
            city_name: 'Vancouver',
            continent_code: 'NA',
            continent_name: 'North America',
            country_iso_code: 'CA',
            country_name: 'Canada',
            location: {
              lon: -73.614830,
              lat: 45.505918
            },
            postal_code: 'V9J1E3',
            region_iso_code: 'BC',
            region_name: 'British Columbia',
            timezone: 'America/Los_Angeles'
          }
        }
      },
      fds: [
        {
          descriptor:0,
          type: 'char_device',
          char_device: {
            major: 8,
            minor: 1
          }
        }
      ],
      tty: {
        descriptor: 0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
    },
    fds: [
      {
        descriptor:0,
        type: 'char_device',
        char_device: {
          major: 8,
          minor: 1
        }
      },
      {
        descriptor:1,
        type:'pipe',
        pipe: {
          inode: '6183207'
        }
      }
    ],
    tty: {
      descriptor: 0,
      type: 'char_device',
      char_device: {
        major: 8,
        minor: 1
      }
    }
  },
  terminal: {
    size: {
      rows: 200,
      columns: 80
    },
    termio: {
      c_iflag: 0,
      c_oflag: 1,
      c_cflag: 2,
      c_lflag: 3
    }
  },
  output: {
    fd: {
      descriptor: 1,
      type: 'char_device',
      char_device: {
        major: 1,
        minor:4
      }
    },
    echoed: true,
    data: 'G1szMW10aGlzIHRleHQgaXMgcmVkCg==',
    text: 'this text is red'
  }
}
```

<!--1
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

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

Potential concerns for me are primary tied to message size. The nested ancestors and their many fields could add up. That being said, there is a larger concern wrt number of events that will dwarf any issue around message size. That effort will come down to defining a set of event filters to eliminate unwanted noise. Scraping /proc and sending up all process executions can be very load heavy task. This issue is probably outside of the scope of ECS though.

Another point of concern is the re-use of process.entity_id. There is nuance around how this ID is calculated, and we are proposing a new hash/calculation based of a different set of fields. This issue is being tracked here: https://github.com/elastic/security-team/issues/2458

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @mitodrummer | author
* @mitodrummer & @m-sample | sponsor
* @m-sample | subject matter expert
* @norrietaylor | subject matter expert

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

https://github.com/elastic/security-team/blob/main/docs/adaptive-workload-protection-team/architecture/linux-event-model.md
https://github.com/elastic/security-team/pull/2071/files

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1684
* Stage 1: https://github.com/elastic/ecs/pull/1684

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
