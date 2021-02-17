# 0007: Multiple users in an event
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-02-17** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

Many log events refer to more than one user at the same time.
Examples of this are remote logons as someone else, user management and privilege escalation.
ECS supports some of these situations already, via the fact that the "user" fields are reused inside other field sets (e.g. `source.user.*` and `destination.user.*`).

The purpose of this proposal is two-fold:

1. Define additional places where the user fields can be used, to support situations that aren't currently covered.
2. Review and clarify the purpose of all the places the user fields are currently defined. If some of them appear unneeded, we will also consider removing them.

## Fields

As of ECS 1.6, user fields can be present in an event in all of the following places:

* `user.*`
* `host.user.*`
* `source.user.*`
* `destination.user.*`
* `client.user.*`
* `server.user.*`

The new fields discussed in this RFC are the following:

* `user.effective.*`
* `user.target.*`
* `user.changes.*`

Notice that in these new additions, the user fields are now being nested as a different name.
The purpose is to hint at their role when used in these locations.

It's also important to point out that the reuses of `user` inside other field sets
are not meant to inherit these new subsections inside the user field set.
For example: `source.user.*` will **not** contain `source.user.effective.*` and so on.

The current reusable locations `user` will be amended to include a few more entries,
as demonstrated below.

```YAML
# schemas/user.yml excerpt
  reusable:
    top_level: true
    expected:
      - client
      - destination
      - host
      - server
      - source
      # Added for this RFC
      - at: user
        as: target
      - at: user
        as: effective
      - at: user
        as: changes
```

The `user` field set contains 6 leaf fields, 2 of which have a `.text` multi-field,
for a total of 8 fields. These 3 new nestings will therefore add a total of 24 fields.
This can be seen in more detail on PR [ecs#869](https://github.com/elastic/ecs/pull/869).

## Usage

The examples below will only populate `user.name` and sometimes `user.id` inside
the various `user` nestings, for readability.
However in implementations, unless otherwise noted, all `user` fields that can reasonably
be populated in each location should be populated.

### User fields at the Root of an Event

The user fields at the root of an event must be used to capture the user
performing the main action described by the event. This is especially important
when there's more than one user present on the event. `user.*` fields at the root
of the event represent the user performing the action.

In many cases, events that only mention one user should populate the user fields
at the root of the event, even if the user is not the one performing the action.

In cases where a purpose-specific user field such as `url.username` is populated,
`user.name` should also be populated with the same user name.

### Remote Logons

When users are crossing host boundaries, the users are captured at
`source.user` and `destination.user`.

Examples of data sources where this is applicable:

* Remote logons via ssh, kerberos
* Firewalls observing network traffic

In order to align with ECS' design of having `user` at the root of the event as the
user performing the action, all `source.user` fields should be copied to `user` at the root.

Here's an example where user "alice" logs on to another host as user "deus":

```JSON
{
  "user": {
    "name": "alice"
  },
  "source": {
    "user": {
      "name": "alice"
    },
    "ip": "10.42.42.42"
  },
  "destination": {
    "user": {
      "name": "deus"
    },
    "ip": "10.42.42.43"
  }
}
```

Whenever an event source populates the `client` and `server` fields in addition
to `source` and `destination`, the user fields should be copied accordingly as well.

### Privilege Changes

The `user.effective` fields are relevant when there's a privilege escalation or demotion
and it's possible to determine the user requesting/performing the escalation.

Use the `user` fields at the root to capture who is requesting the privilege change,
and `user.effective` to capture the requested privilege level, whether or not the
privilege change was successful.

Here are examples where this is applicable:

* A user changing identity on a host.
  * Examples: sudo, su, Run as.
* Running a program as a different user. Examples:
  * A trusted user runs a specific admin command as root via a mechanism such as the Posix setuid/setgid.
  * A service manager with administrator privileges starts child processes as limited
    users, for security purposes (e.g. root runs Apache HTTPD as user "apache")

In cases where the event source only gives information about the effective user
and not who requested different privileges, the `user` fields at the root of the
event should be used instead.

Here's an example of user "alice" running a command as root via sudo:

```JSON
{
  "user": {
    "name": "alice",
    "id": "1001",
    "effective": {
      "name": "root",
      "id": "0"
    }
  }
}
```

When it's not possible (or it's prohibitive) to determine which user is requesting
different privilege levels, it's acceptable to capture the effective user at the
root of the event. Typically a privilege change event will already have happened,
for example: bob "su" as root; and subsequent events will show the root user
performing the actions.

### Identity and Access Management

Whenever a user is performing an action that affects another user -- typically
in IAM scenarios -- the user affected by the action is captured at
`user.target`. The user performing the IAM activity is captured at the root
of the event.

Examples of IAM activity include:

* user-a creates or deletes user-b
* user-a modifies user-b

In the create/delete scenarios, there's either no prior state (user creation)
or no post state (user deletion). In these cases, only `user` at the root and
`user.target` must be populated.

Example where "root" creates user "bob":

```JSON
{
  "user": {
    "name": "root",
    "id": "0",
    "target": {
      "name": "bob",
      "id": "1002",
      ...
    }
  }
}
```

When there's a change of state to an existing user, `user.target` must be used
to capture the prior state of the user, and `user.changes` should list only
the changes that were performed.

Example where "root" renames user "bob" to "bob.barker":

```JSON
{
  "user": {
    "name": "root",
    "id": "0",
    "target": {
      "name": "bob",
      "id": "1002"
    },
    "changes": {
      "name": "bob.barker"
    }
  }
}
```

You'll note in the example above that the user ID is not repeated under `user.changes.*`,
since the ID didn't change.

### Combining IAM and Privilege Escalation

We've covered above how `user.target` and `user.changes` can be used at the same time.
If privilege escalation is captured in the same IAM event, `user.effective`
should of course be used as well.

Here's the "rename" example from the IAM section above. In the following example,
we know "alice" is escalating privileges as "root", in order to modify user "bob":

```JSON
{
  "user": {
    "name": "alice",
    "id": "1001",
    "effective": {
      "name": "root",
      "id": "0"
    },
    "target": {
      "name": "bob",
      "id": "1002"
    },
    "changes": {
      "name": "bob.barker"
    }
  }
}
```

### Pivoting via related.user

Any event that has user(s) in it should always populate the array field `related.user`
with all usernames seen on the event. Note that this field is not a nesting of
all user fields, it's a flat array meant to contain user identifiers.

Taking the example from `user.changes` again, and populating `related.user` as well,
the event now looks like:

```JSON
{
  "user": {
    "name": "alice",
    "id": "1001",
    "effective": {
      "name": "root",
      "id": "0"
    },
    "target": {
      "name": "bob",
      "id": "1002"
    },
    "changes": {
      "name": "bob.barker"
    }
  },
  "related": { "user": ["alice", "root", "bob", "bob.barker"] }
}
```

## Source data

Here are some concrete examples of events with multiple users and user roles.
Note that the design of these fields is meant to allow all of their use at the
same time, *when needed*. However if events don't contain all user roles because
they're spread out across events, only the fields relevant to each event should be used.

### Linux IAM and privilege escalation

Here's a typical set of logs about a user creation on Linux.

```
Sep 29 19:55:09 localhost sudo: vagrant : TTY=pts/0 ; PWD=/home/vagrant ; USER=root ; COMMAND=/sbin/useradd test-user -p test-password
Sep 29 19:55:09 localhost sudo: pam_unix(sudo:session): session opened for user root by vagrant(uid=0)
Sep 29 19:55:09 localhost useradd[2097]: new group: name=test-user, GID=1001
Sep 29 19:55:09 localhost useradd[2097]: new user: name=test-user, UID=1001, GID=1001, home=/home/test-user, shell=/bin/bash
Sep 29 19:55:09 localhost sudo: pam_unix(sudo:session): session closed for user root
```

#### Logical events

A solution that coalesces log events to produce higher level logical events could
capture them all in the following way.

Group creation:

```JSON
{
  "event": {
    "kind": "event",
    "category": ["iam"],
    "type": ["group", "creation"]
  },
  "group": {
    "name": "test-user",
    "id": "1001"
  },
  "user": {
    "name": "vagrant",
    "id": "1000",
    "effective": {
      "name": "root",
      "id": "0"
    },
  },
  "related": { "user": ["vagrant", "root"] }
}
```

User creation:

```JSON
{
  "event": {
    "kind": "event",
    "category": ["iam"],
    "type": ["user", "creation"]
  },
  "user": {
    "name": "vagrant",
    "id": "1000",
    "effective": {
      "name": "root",
      "id": "0"
    },
    "target": {
      "name": "test-user",
      "id": "1001",
      "group": {
        "name": "test-user",
        "id": "1001"
      }
    }
  },
  "related": { "user": ["vagrant", "root", "test-user"] }
}
```

#### Raw events

A solution that produces one event per log without coalescing would instead only
represent users with the information available in the given log event.

event 1:

```JSON
{
  "event": {
    "kind": "event",
    "category": ["process"],
    "type": "creation"
  },
  "user": {
    "name": "vagrant",
    "effective": {
      "name": "root"
    }
  },
  "process": {
    "name": "sudo",
    "command_line": "/sbin/useradd test-user -p test-password"
  }
}
```

event 2 (privilege escalation):

```JSON
{
  "event": {
    "kind": "event",
    "category": ["session"],
    "type": ["creation"],
    "outcome": "success"
  },
  "user": {
    "name": "vagrant",
    "effective": {
      "name": "root"
    }
  },
  "process": {
    "name": "sudo"
  }
}
```

event 3 (IAM):

```JSON
{
  "event": {
    "kind": "event",
    "category": ["iam"],
    "type": ["group", "creation"],
    "outcome": "success"
  },
  "group": {
    "name": "test-user",
    "id": "1001"
  },
  "process": {
    "name": "useradd",
    "pid": 2097
  }
}
```

event 4 (IAM):

```JSON
{
  "event": {
    "kind": "event",
    "category": ["iam"],
    "type": ["user", "creation"]
  },
  "user": {
    "name": "test-user",
    "id": "1001"
  },
  "process": {
    "name": "useradd",
    "pid": 2097
  }
}
```

Notice: in the event above, since the log mentions only the user being created,
we capture the user at the root of the event. We do this despite the fact that
they are not the one performing the action.

event 5:

```JSON
{
  "event": {
    "kind": "event",
    "category": ["session"],
    "type": ["end"]
  },
  "user": {
    "name": "root"
  },
  "process": {
    "name": "sudo"
  }
}
```

### Windows privilege escalation

A successful local Windows Admin logon where user "testuser" escalates to Administrator:

```XML
<System>
  <Provider Name="Microsoft-Windows-Security-Auditing"...>
  <EventID>4624</EventID>
  ...
</System>
<EventData>
  <Data Name="SubjectUserSid">5-1-5-21-202424912787-2692429404-2351956786-1000</Data>
  <Data Name="SubjectUserName">testuser</Data>
  <Data Name="SubjectDomainName">TEST</Data>
  <Data Name="SubjectLogonId">0xb976c</Data>
  <Data Name="TargetUserSid">S-1-5-21-2024912787-2692429404-2351956786-500</Data>
  <Data Name="TargetUserName">Administrator</Data>
  <Data Name="TargetDomainName">TEST</Data>
  <Data Name="TargetLogonId">0x11b621</Data>
  ...
</EventData>
```

Would translate to

```JSON
{
  "event": {
    "code": "4624",
    "provider": "Microsoft-Windows-Security-Auditing",
    "kind": "event",
    "category": ["authentication"],
    "type": ["start"],
    "outcome": "success"
  },
  "user": {
    "name": "testuser",
    "domain": "TEST",
    "id": "S-1-5-21-202424912787-2692429404-2351956786-1000",
    "effective": {
      "name": "Administrator",
      "domain": "TEST",
      "id": "S-1-5-21-2024912787-2692429404-2351956786-500"
    }
  },
  "related": { "user": ["testuser", "Administrator"] }
}
```

### Windows IAM

Modifying an existing user account, where the administrator renames user John to John2:

```XML
<System>
  <Provider Name="Microsoft-Windows-Security-Auditing"...>
  <EventID>4781</EventID>
  ...
</System>
<EventData>
  <Data Name="SubjectUserSid">S-1-5-21-2024912787-2692429404-2351956786-500</Data>
  <Data Name="SubjectUserName">Administrator</Data>
  <Data Name="SubjectDomainName">TEST</Data>
  <Data Name="SubjectLogonId">0x11b621</Data>
  <Data Name="TargetUserSid">S-1-5-21-2024912787-2692429404-2351956786-1000</Data>
  <Data Name="OldTargetUserName">John</Data>
  <Data Name="NewTargetUserName">John2</Data>
  <Data Name="TargetDomainName">TEST</Data>
  ...
</EventData>
```

Would translate to

```JSON
{
  "event": {
    "code": "4781",
    "provider": "Microsoft-Windows-Security-Auditing",
    "kind": "event",
    "category": ["iam"],
    "type": ["user", "change"],
    "outcome": "success"
  },
  "user": {
    "name": "Administrator",
    "domain": "TEST",
    "id": "S-1-5-21-2024912787-2692429404-2351956786-500",
    "target": {
      "name": "John",
      "id": "S-1-5-21-2024912787-2692429404-2351956786-1000",
      "domain": "TEST",
    },
    "changes": {
      "name": "John2"
    }
  },
  "related": { "user": ["John", "John2", "Administrator"] }
}
```

### Cloud privilege escalation

Cloud systems also have privilege change concepts.

Here's an example using AWS' assume role, in the event where AWS user "JohnRole1"
assumes the role of "DBARole". A simplified version of the Cloudtrail event could look like:

```JSON
{
  "eventName": "AssumeRole",
  "requestParameters": {
    "roleArn": "arn:aws:iam::111111111111:role/JohnRole2",
  },
  "resources": [
    {
      "ARN": "arn:aws:iam::111122223333:role/JohnRole2",
      "accountId": "111111111111",
      "type": "AWS::IAM::Role"
    }
  ],
  "responseElements": {
    "assumedRoleUser": {
      "arn": "arn:aws:sts::111111111111:assumed-role/test-role/DBARole",
      "assumedRoleId": "AROAIFR7WHDTSOBEEFSTU:DBARole"
    },
    "userIdentity": {
      "accessKeyId": "AKIAI44QH8DHBEXAMPLE",
      "accountId": "111111111111",
      "arn": "arn:aws:sts::111111111111:assumed-role/JohnDoe/JohnRole1",
      "principalId": "AROAIN5ATK5U7KEXAMPLE:JohnRole1",
      "type": "AssumedRole"
    }
  }
}
```

And would translate to:

```JSON
{
  "event": {
    "action": "AssumeRole",
    "kind": "event",
    "category": ["authentication"],
    "type": ["start"],
    "outcome": "success"
  },
  "user": {
    "id": "AROAIN5ATK5U7KEXAMPLE:JohnRole1",
    "effective": {
      "id": "AROAIFR7WHDTSOBEEFSTU:DBARole",
    }
  },
  "cloud": {
    "account": { "id": "111111111111" } ...
  },
  "related": { "user": ["AROAIN5ATK5U7KEXAMPLE:JohnRole1", "AROAIFR7WHDTSOBEEFSTU:DBARole"] }
}
```

Subsequent actions taken under this assumed role will have both the principal user
and the assumed role in the `userIdentity`. This makes it easy to keep track of both
the real user at `user.*` and the escalated privileges at `user.effective.*` in
all subsequent activity after privilege escalation.

## Scope of impact

### New fields for IAM

The fields `user.[changes|effective|target].*` are net new fields,
so they don't represent a breaking change. They are especially important
for security-related data sources around IAM and audit logs.
These event sources should be adjusted to populate these new fields, as they are
very important in getting a complete picture of user management activity.

Some event sources for user management activity may have used `user.*` fields at the
root to describe the user being modified, rather than the user performing the action.
These sources will have to be modified to be consistent with the fact that user
fields at the root are meant to represent who's performing the action.

### New user field duplication guidance

In order to firmly establish the user fields at the root of the event as the user
performing the action, this RFC introduces new guidance:

* Remote logons `source.user.*` should be copied to `user.*`
* Purpose-specific fields such as `url.username` should be copied at `user.name`

These came up while working on this RFC; this is not guidance that was given
in the past. Data sources that populate these fields will need to be revisited
and adjusted accordingly.

### host.user fields are deprecated for removal

Seeing no use in the wild, it was decided to remove the reuse of the user fields at `host.user.*`.
We will start by deprecating them in ECS 1.8, and will remove them at the next major version.

Please let us know before the next major ECS release if you disagree with this, and share how you're using them.

## Concerns

### Deprecating host.user fields

In past discussions and recent research, we have not identified a clear purpose
for the user fields nested at `host.user.*`.

We are considering deprecating these fields with the intent to remove them completely.

#### Resolution

They will be marked as deprecated starting with ECS 1.8, and will be removed in
the next ECS major release.

### Documenting the purpose of each usage of the user fields

As of ECS 1.6, the ECS documentation doesn't have a good place to explain at length
how to properly use the multiple nesting locations for `user`.
This is already a problem for the usage of `user` at the root vs its 5 reuse locations.
The addition of 3 new reuse locations adds to this situation.

#### Resolution

Adding a way to document field sets via free form text is being worked on independently
of this proposal ([ecs#943](https://github.com/elastic/ecs/issues/943)).

For now the guidance on the meaning of each location where `user` can be used is in the
[Usage](#usage) section of this RFC. This guidance will be moved to the main ECS
documentation when the appropriate mechanism is available.

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

* @webmat | author
* @jonathan-buttner | sponsor
* @leehinman | subject matter expert
* @janniten | subject matter expert
* @willemdh | subject matter expert

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

* PR to add the new fields described in this RFC: [ecs#869](https://github.com/elastic/ecs/pull/869)
* Past issues discussing this addition in ECS, starting with the most recent:
  * https://github.com/elastic/ecs/issues/809
  * https://github.com/elastic/ecs/issues/678
  * https://github.com/elastic/ecs/issues/589
  * https://github.com/elastic/ecs/issues/234
  * https://github.com/elastic/ecs/issues/117
* Discussions about this in Beats:
  * https://github.com/elastic/beats/pull/10192
  * https://github.com/elastic/beats/issues/10111
  * https://github.com/elastic/beats/pull/9963
* Adding a free form documentation section per field set, to allow documenting
  them in a more holistic manner https://github.com/elastic/ecs/issues/943

### RFC Pull Requests

* Stage 2: https://github.com/elastic/ecs/pull/914
  * Stage 2 correction: https://github.com/elastic/ecs/pull/996
* Legacy Stage 3: https://github.com/elastic/ecs/pull/1017
* Stage 3 (Finished): https://github.com/elastic/ecs/pull/1239

Note: This RFC was initially proposed via a PR that targeted stage 2,
given the amount of discussion that has already has happened on this subject.
