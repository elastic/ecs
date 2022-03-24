# 0030: Linux event model
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2022/03/22** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This RFC aims to introduce a number of additions to ECS (mostly the 'Process' fieldset) in an effort to provide a rich enough Linux event model to drive Session view in Kibana, as well as provide wider context to EQL and other rule engines. The process fieldset currently has a nested 'parent' field. We want to extend upon this pattern, and include additional 'ancestor' nested processes (such as the session_leader and group_leader processes). Care has been taken to ensure this RFC doesn't break any existing uses of the process field set, and should be fully backwards compatible with existing endpoint agents.

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
https://github.com/elastic/ecs/tree/main/rfcs/text/0030

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

### Session View

The primary use case for this data will be to drive the "Session view". A time ordered rendering of a Linux session process tree. The addition of nested process ancestors entry_leader, session_leader, and group_leader will allow Session View to load only the events for a particular session.

KQL examples:
```
process.entry_leader.entity_id: &lt;entity_id of entry session leader>

or

process.session_leader.entity_id: &lt;entity_id of session leader>
```

#### Session/Process interactivity (is the session connected to a controlling tty?)

process.tty will be used to determine if the session is interactive. If the field is unset there is no controlling tty and the session is non-interactive (possibly a service). The *process.interactive* boolean will indicate if the process itself is connected to the controlling tty.

### Unique process.entity_id generation

*host.boot.id* and *host.pid_ns_ino* will be used in generating unique *entity_id*s for the process using fn(process.pid, process.start, host.pid_ns_ino, host.boot.id)

### Rule engines

The new nested ancestor processes will provide rule engines a widened context to allow for more targeted alerting.

KQL example:

Boot a user from an ssh session if the user is connecting with root and trying to run mysql:
`process.entry_leader.user.name: root AND process.executable: /bin/mysql`

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

The source of data will be via kprobes and ebpf sensors. All process execution lifecycle events will be sent up (fork, exec, end) as well as setsid.

Here is a mock example of these events:

### Fork event (mock data)

<details>
  <summary>see example here</summary>

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
	user: {
		id: '2', // the effective user aka euid
		name: 'kg'
	},
	group: {
		id: '1', // the effective group aka egid
		name: 'groupA'
	},
	process: {
		entity_id: '4321',
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
			id: '0',
			name: 'root'
		},
		real_user: {
			id: '0',
			name: 'root',
		},
		saved_user: {
			id: '0',
			name: 'root'
		},
		group: {
			id: '1',
			name: 'groupA'
		},
		real_group: {
			id: '1',
			name: 'groupA'
		},
		saved_group: {
			id: '1',
			name: 'groupA'
		},
		supplemental_groups: [{
				id: '2',
				name: 'groupB'
			},
			{
				id: '3',
				name: 'groupC'
			}
		],
		parent: {
			entity_id: '4322',
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
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			group_leader: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 1234, // this directly replaces parent.pgid
				start: '2021-10-14T08:05:34.853Z',
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		group_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		session_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the session_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		entry_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the entry_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
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
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		tty: {
			char_device: {
				major: 8,
				minor: 1
			}
		}
	}
}
```

</details>

### Exec event (mock data)

<details>
  <summary>see example here</summary>

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
	user: {
		id: '2',
		name: 'kg'
	},
	group: {
		id: '1',
		name: 'groupA'
	},
	process: {
		entity_id: '4321',
		args: ['/bin/bash'],
		args_count: 1,
		command_line: 'bash',
		executable: '/bin/bash',
		name: 'bash',
		interactive: true,
		working_directory: '/home/kg',
		pid: 3,
		start: '2021-10-14T08:05:34.853Z',
		previous: [{
			args: ['/bin/sshd'],
			args_count: 1,
			executable: '/bin/sshd'
		}],
		user: {
			id: '0',
			name: 'root'
		},
		real_user: {
			id: '0',
			name: 'root',
		},
		saved_user: {
			id: '0',
			name: 'root'
		},
		group: {
			id: '1',
			name: 'groupA'
		},
		real_group: {
			id: '1',
			name: 'groupA'
		},
		saved_group: {
			id: '1',
			name: 'groupA'
		},
		supplemental_groups: [{
				id: '2',
				name: 'groupB'
			},
			{
				id: '3',
				name: 'groupC'
			}
		],
		parent: {
			entity_id: '4322',
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
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			group_leader: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 1234, // this directly replaces parent.pgid
				start: '2021-10-14T08:05:34.853Z'
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		group_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		session_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the session_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		entry_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the entry_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
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
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		tty: {
			char_device: {
				major: 8,
				minor: 1
			}
		}
	},
}
```

</details>

### Exit event (mock data)

<details>
  <summary>see example here</summary>

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
	user: {
		id: '2',
		name: 'kg'
	},
	group: {
		id: '1',
		name: 'groupA'
	},
	process: {
		entity_id: '4321',
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
		previous: [{
			args: ['/bin/sshd'],
			args_count: 1,
			executable: '/bin/sshd'
		}],
		user: {
			id: '0',
			name: 'root'
		},
		real_user: {
			id: '0',
			name: 'root',
		},
		saved_user: {
			id: '0',
			name: 'root'
		},
		group: {
			id: '1',
			name: 'groupA'
		},
		real_group: {
			id: '1',
			name: 'groupA'
		},
		saved_group: {
			id: '1',
			name: 'groupA'
		},
		supplemental_groups: [{
				id: '2',
				name: 'groupB'
			},
			{
				id: '3',
				name: 'groupC'
			}
		],
		parent: {
			entity_id: '4322',
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
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			group_leader: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 1234, // this directly replaces parent.pgid
				start: '2021-10-14T08:05:34.853Z'
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			},
		},
		group_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		session_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the session_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			},
		},
		entry_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the entry_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
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
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			},
		},
		tty: {
			char_device: {
				major: 8,
				minor: 1
			}
		}
	}
}
```

</details>

### Setsid event (mock data)

<details>
  <summary>see example here</summary>

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
	user: {
		id: '2',
		name: 'kg'
	},
	group: {
		id: '1',
		name: 'groupA'
	},
	process: {
		entity_id: '4321',
		args: ['/bin/bash'],
		args_count: 1,
		command_line: 'bash',
		executable: '/bin/bash',
		name: 'bash',
		interactive: true,
		working_directory: '/home/kg',
		pid: 3,
		start: '2021-10-14T08:05:34.853Z',
		previous: [{
			args: ['/bin/sshd'],
			args_count: 1,
			executable: '/bin/sshd'
		}],
		user: {
			id: '0',
			name: 'root'
		},
		real_user: {
			id: '0',
			name: 'root',
		},
		saved_user: {
			id: '0',
			name: 'root'
		},
		group: {
			id: '1',
			name: 'groupA'
		},
		real_group: {
			id: '1',
			name: 'groupA'
		},
		saved_group: {
			id: '1',
			name: 'groupA'
		},
		supplemental_groups: [{
				id: '2',
				name: 'groupB'
			},
			{
				id: '3',
				name: 'groupC'
			}
		],
		parent: {
			entity_id: '4322',
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
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root'
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA'
			},
			saved_group: {
				id: '1',
				name: 'groupA'
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB'
				},
				{
					id: '3',
					name: 'groupC'
				}
			],
			group_leader: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 1234, // this directly replaces parent.pgid
				start: '2021-10-14T08:05:34.853Z',
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		session_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root',
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA',
			},
			saved_group: {
				id: '1',
				name: 'groupA',
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB',
				},
				{
					id: '3',
					name: 'groupC',
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the session_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
			},
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		group_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root',
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA',
			},
			saved_group: {
				id: '1',
				name: 'groupA',
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB',
				},
				{
					id: '3',
					name: 'groupC',
				}
			],
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		entry_leader: {
			entity_id: '4321',
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
				id: '0',
				name: 'root'
			},
			real_user: {
				id: '0',
				name: 'root',
			},
			saved_user: {
				id: '0',
				name: 'root',
			},
			group: {
				id: '1',
				name: 'groupA'
			},
			real_group: {
				id: '1',
				name: 'groupA',
			},
			saved_group: {
				id: '1',
				name: 'groupA',
			},
			supplemental_groups: [{
					id: '2',
					name: 'groupB',
				},
				{
					id: '3',
					name: 'groupC',
				}
			],
			parent: {
				entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
				pid: 2,
				start: '2021-10-14T08:05:34.853Z',

				session_leader: { // used as a foreign key to the parent session of the entry_leader
					entity_id: '0fe5f6a0-6f04-49a5-8faf-768445b38d16',
					pid: 4321,
					start: '2021-10-14T08:05:34.853Z',
				},
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
			tty: {
				char_device: {
					major: 8,
					minor: 1
				}
			}
		},
		tty: {
			char_device: {
				major: 8,
				minor: 1
			}
		}
	}
}
```

</details>

<!--1
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

### Real world exec event

The following event is sourced from an endpoint-dev development branch that has the majority of the proposed fields implemented. Please note that there are many additional fields that are already sent up as part of the endpoint agent.

<details>
  <summary>see example here</summary>

```json
{
  "_index": ".ds-logs-endpoint.events.process-default-2022.02.15-000001",
  "_id": "BuvxBH8BU45FNSRmRWIK",
  "_version": 1,
  "_score": 1,
  "_source": {
    "agent": {
      "id": "01010101-0101-0101-0101-010101010101",
      "type": "endpoint",
      "version": "8.2.0-SNAPSHOT"
    },
    "process": {
      "Ext": {
        "ancestry": [
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjQxLTEzMjg5NTI4OTkwLjUwMTk0NTkwMA==",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI3LTEzMjg5NTI4OTg2Ljc5NTkxODAwMA==",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI3LTEzMjg5NTI4OTg2Ljc5NDg0ODcwMA==",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI2LTEzMjg5NTI4OTg2Ljc5MTY5OTYwMA==",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNTMxLTEzMjg5NTI4OTg2LjIwMjUyMTQwMA==",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNTMxLTEzMjg5NTI4OTg2LjIwMTk1NzEwMA==",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTY5OS0xMzI4OTUyMjUyMC4w",
          "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEtMTMyODk1MjI1MTMuMA=="
        ]
      },
      "parent": {
        "interactive": true,
        "start": "2022-02-16T23:27:52.81Z",
        "pid": 12627,
        "working_directory": "/home/vagrant",
        "entity_id": "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI3LTEzMjg5NTI4OTg2Ljc5NTkxODAwMA==",
        "executable": "/bin/bash",
        "args": [
          "-bash"
        ],
        "name": "bash",
        "tty": {
          "char_device": {
            "major": 136,
            "minor": 1
          },
          "type": "char_device"
        },
        "args_count": 1,
        "user": {
          "name": "vagrant",
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        },
        "command_line": "-bash",
        "group": {
          "name": "vagrant",
          "supplemental": [
            {
              "name": "vagrant",
              "id": 1000
            }
          ],
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        }
      },
      "group_leader": {
        "interactive": true,
        "start": "2022-02-16T23:27:52.81Z",
        "pid": 12627,
        "working_directory": "/home/vagrant",
        "entity_id": "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI3LTEzMjg5NTI4OTg2Ljc5NTkxODAwMA==",
        "executable": "/bin/bash",
        "args": [
          "-bash"
        ],
        "name": "bash",
        "tty": {
          "char_device": {
            "major": 136,
            "minor": 1
          },
          "type": "char_device"
        },
        "args_count": 1,
        "user": {
          "name": "vagrant",
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        },
        "command_line": "-bash",
        "group": {
          "name": "vagrant",
          "supplemental": [
            {
              "name": "vagrant",
              "id": 1000
            }
          ],
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        }
      },
      "previous": [
        {
          "args": [
            "-bash"
          ],
          "args_count": 0,
          "executable": "/bin/bash"
        }
      ],
      "interactive": true,
      "start": "2022-02-16T23:27:52.81Z",
      "pid": 12641,
      "working_directory": "/home/vagrant",
      "entity_id": "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjQxLTEzMjg5NTI4OTkwLjUwMjI4NTEwMA==",
      "executable": "/usr/bin/ls",
      "args": [
        "ls",
        "--color=auto",
        "-la"
      ],
      "session_leader": {
        "interactive": true,
        "start": "2022-02-16T23:27:52.81Z",
        "pid": 12627,
        "working_directory": "/home/vagrant",
        "entity_id": "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI3LTEzMjg5NTI4OTg2Ljc5NTkxODAwMA==",
        "executable": "/bin/bash",
        "args": [
          "-bash"
        ],
        "name": "bash",
        "tty": {
          "char_device": {
            "major": 136,
            "minor": 1
          },
          "type": "char_device"
        },
        "args_count": 1,
        "user": {
          "name": "vagrant",
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        },
        "command_line": "-bash",
        "group": {
          "name": "vagrant",
          "supplemental": [
            {
              "name": "vagrant",
              "id": 1000
            }
          ],
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        }
      },
      "entry_leader": {
        "interactive": true,
        "start": "2022-02-16T23:27:52.81Z",
        "entry_meta": {
          "source": {
            "ip": "10.0.2.2"
          },
          "type": "sshd"
        },
        "pid": 12627,
        "working_directory": "/home/vagrant",
        "entity_id": "MDEwMTAxMDEtMDEwMS0wMTAxLTAxMDEtMDEwMTAxMDEwMTAxLTEyNjI3LTEzMjg5NTI4OTg2Ljc5NTkxODAwMA==",
        "executable": "/bin/bash",
        "args": [
          "-bash"
        ],
        "name": "bash",
        "tty": {
          "char_device": {
            "major": 136,
            "minor": 1
          },
          "type": "char_device"
        },
        "args_count": 1,
        "user": {
          "name": "vagrant",
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        },
        "command_line": "-bash",
        "group": {
          "name": "vagrant",
          "supplemental": [
            {
              "name": "vagrant",
              "id": 1000
            }
          ],
          "id": 1000,
          "real": {
            "name": "vagrant",
            "id": 1000
          }
        }
      },
      "name": "ls",
      "tty": {
        "char_device": {
          "major": 136,
          "minor": 1
        },
        "type": "char_device"
      },
      "args_count": 3,
      "command_line": "ls --color=auto -la",
      "hash": {
        "sha1": "07bfe0ceac3cf590357e84235ca640b6373b884f",
        "sha256": "4ef89baf437effd684a125da35674dc6147ef2e34b76d11ea0837b543b60352f",
        "md5": "6d2b4ff5fd937cd034aa2a2cf203e20f"
      }
    },
    "message": "Endpoint process event",
    "@timestamp": "2022-02-16T23:49:50.5022851Z",
    "ecs": {
      "version": "1.11.0"
    },
    "data_stream": {
      "namespace": "default",
      "type": "logs",
      "dataset": "endpoint.events.process"
    },
    "elastic": {
      "agent": {
        "id": "01010101-0101-0101-0101-010101010101"
      }
    },
    "host": {
      "hostname": "ubuntu-impish",
      "os": {
        "Ext": {
          "variant": "Ubuntu"
        },
        "kernel": "5.13.0-28-generic #31-Ubuntu SMP Thu Jan 13 17:41:06 UTC 2022",
        "name": "Linux",
        "family": "ubuntu",
        "type": "linux",
        "version": "21.10",
        "platform": "ubuntu",
        "full": "Ubuntu 21.10"
      },
      "ip": [
        "127.0.0.1",
        "::1",
        "10.0.2.15",
        "fe80::b6:64ff:fef1:a5f0"
      ],
      "name": "ubuntu-impish",
      "id": "00000000-0000-0000-0000-000000000000",
      "mac": [
        "02:b6:64:f1:a5:f0"
      ],
      "architecture": "x86_64"
    },
    "event": {
      "agent_id_status": "auth_metadata_missing",
      "sequence": 7424,
      "ingested": "2022-02-16T23:49:55Z",
      "created": "2022-02-16T23:49:50.5022851Z",
      "kind": "event",
      "module": "endpoint",
      "action": "exec",
      "id": "MUpqbRd8y253e0Yl+++++K2J",
      "category": [
        "process"
      ],
      "type": [
        "start"
      ],
      "dataset": "endpoint.events.process"
    },
    "user": {
      "Ext": {
        "real": {
          "name": "vagrant",
          "id": 1000
        }
      },
      "name": "vagrant",
      "id": 1000
    },
    "group": {
      "Ext": {
        "real": {
          "name": "vagrant",
          "id": 1000
        }
      },
      "name": "vagrant",
      "supplemental": [],
      "id": 1000
    }
  }
}
```


</details>
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

### Ingestion mechanisms

The Adaptive workload protections (AWP) sensor team is working hard on integrating these new ECS fields into the endpoint agent codebase. The existing perf/tracefs kprobe sensor technology will be upgraded to support much of the new widened process context defined in this RFC. At the same time, eBPF sensor technology is being worked on and will eventually be the go to method for building these process events.

### Usage mechanisms

As outlined earlier in this document, the primary use for this data will be to drive the Session View (aka Terminal view, aka Sessionizer). Because of the hierarchical nature of this data, there are edge cases where some parts of the process tree are not captured or have been filtered out (due to data volume concerns). This widened process context (e.g entry_leader, session_leader, parent, group_leader) will allow the Session View to repair disjointed trees and ensure it can represent the data as accurately as possible.

Currently there are plans to integrate Session View into the kibana Timeline UI along side the Process Analyzer feature. There are also plans to add a "Sessions" tab to the Endpoint security hosts page.

Another major win to this widened process context is the ability to create more targeted rules and forensic queries. There are many situations where you may want to alert on a specific process executable, but only in certain cases. For example, perhaps it's ok to run the mysql cli client, but only if the process.entry_leader.user.name != 'root' and process.entry_leader.entry_meta.source.ip: <IP of a trusted bastion host>

### ECS project

As part of this RFC, there has been a few instances of a need to support arrays of fieldsets.

The fields in question include:
- process.previous (type: process)
- process.supplemental_groups (type: group)

This will require involvement from the ECS team to add this support to the existing tooling.
An issue has been created for this and can be found here https://github.com/elastic/ecs/issues/1736

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Why is this additional process context worth the extra bytes/bandwidth/storage?

Each ECS process event originally had information about the process itself and its parent process. This RFC adds full process information for the following related processes to each process event.
* the process's session leader
  * this provides a lot of information about the execution context of a process
  * For example, if the session leader is a webserver like nginx, process execution other than nginx can be flagged as anomalous
  * if it's a shell (e.g. bash) with an associated controlling terminal (i.e. likely driven by a human) extra scrutiny can be applied
* the process's entry-session leader
  * this identifies how the host was initially accessed so one could disallow/alert on sensitive activities via SSH but allow them via IPMI/serial.
  * this is sometimes the same as the session leader
* the process's process group leader
  * this is part of enabling pipelines like "cat foo | grep bar | sort | less" to be reassembled for rendering or search/detection.

This RFC also adds the following *anemic* versions of the process object (i.e. those with just entity_id, pid and starttime) to allow chained queries for forensics and to help detect user-entered commands vs automatically spawned child processes.
* the session leader's parent process (process.entry_leader.parent | process.session_leader.parent)
  * allows navigating upward through sessions by querying for the parent process and its session id
* the parent process's group leader (process.parent.group_leader)
  * allows checking if your parent's process group is different from the process's. If so, this process is likely a user-entered command
* the parent session of the session_leader (process.session_leader.parent.session_leader | process.entry_leader.parent.session_leader)

These additions allow:

* More precise alerting with less noise
  * For example, instead of alerting on any use of sudo or nmap, alert only if the entry session type is SSH from a non-private IP address
  * this information is in each event; multi-stage queries are not required
  * query languages such as KQL can consider data that was only possible with EQL "sequence" queries
  * EQL sequence queries will miss information that happened outside of the alert rule's event loading window
* Improved readability (session view rendering) vs log lines style views
  * Session view stitches together information-dense, collapsable views of the session's hierarchical process model
  * The extra context allows re-assembly much of the session tree without loading every event in a session
  * sessions can run for months (tmux) and may have events that have been deleted (such as the original session leader/bash) that will be filled in by this extra context.
* Improved search efficiency and expressiveness
  * the extra context allows for efficient, very targeted queries for forensics; what would have taken several queries can be done it one query
  * all events for a given session within a specific time range can be found with one query. e.g. process.session_leader.entity_id = X

### Is this the most compact representation we could use?

No, we have optimized for queriability at the cost of compactness. A single process may have several roles:
* it could be both the session leader and the entry session
* it could be both main process and group leader

In these cases, it would be more space efficient to tag the process with its roles (e.g. primary process and group leader) instead of repeating it with a different field name.   However, reduced queriability significantly reduces the value of this information.


### If data volume becomes an issue how can it be mitigated?

Rather than removing information from every process event, one can remove/filter entire process trees.  The filtered process events can still generate alerts as with existing Endpoint EventFilters.

A classic example of noise people do not want to store is Kubernetes Pod health checks.  These executions can be detected and filtered at the Endpoint.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @m-sample & @mitodrummer | author
* @mitodrummer & @m-sample | sponsor
* @m-sample & @norrietaylor | subject matter expert

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

https://github.com/m-sample/writing/blob/main/Linux/linux-process-model.md

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1684
* Stage 1: https://github.com/elastic/ecs/pull/1684
* Stage 2: https://github.com/elastic/ecs/pull/1779
* Stage 3: https://github.com/elastic/ecs/pull/1826
  * Stage 3 update: https://github.com/elastic/ecs/pull/1852

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
