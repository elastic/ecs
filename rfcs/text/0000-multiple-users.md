# 0000: Multiple Users in an Event
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (proposal)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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
However in implementations, otherwise noted all `user` fields that can reasonably
be populated in each location should be populated.

### User fields at the Root of an Event

The user fields at the root of an event must be used to capture the user
performing the main action described by the event. This is especially important
when there's more than one user present on the event. `user.*` fields at the root
of the event represent the user performing the action.

In many cases, events that only mention one user are fine populating the user fields
at the root of the event.

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
      "id": "1"
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
    "id": "1",
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
    "id": "1",
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
      "id": "1"
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
      "id": "1"
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

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

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

<!-- TODO

Depending on the outcome of the discussion on `host.user.*`, mention it here.
It's currently listed in the concerns below.

-->

## Concerns

### Deprecating host.user fields

In past discussions and recent research, we have not identified a clear purpose
for the user fields nested at `host.user.*`.

We are considering deprecating these fields with the intent to remove them completely.
Please let us know if you disagree with this, and share how you're using them.

#### Resolution

No resolution yet.

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
* TBD | sponsor
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

Note: This RFC was initially proposed via a PR that targeted stage 2,
given the amount of discussion that has already has happened on this subject.
