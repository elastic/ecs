---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-user-usage.html
applies_to:
  stack: all
  serverless: all
---

# User fields usage and examples [ecs-user-usage]

Here are the subjects covered in this page.

* [Categorization](#ecs-user-usage-categorization)
* [User identifiers](#ecs-user-identifiers)
* [Field reuse](#ecs-user-usage-field-reuse), or all places user fields can appear

    * [User fields at the Root of an Event](#ecs-user-usage-user-at-root)
    * [Remote logons](#ecs-user-usage-remote-logons)
    * [Privilege changes](#ecs-user-usage-privilege-changes)
    * [Identity and access management](#ecs-user-usage-iam)
    * [Combining IAM and privilege change](#ecs-user-usage-combining)
    * [Subtleties around field reuse](#ecs-user-usage-reuse-subtleties)

* [Pivoting via related.user](#ecs-user-usage-pivoting)
* [Mapping examples](#ecs-user-usage-mappings)


## Categorization [ecs-user-usage-categorization]

User fields can be present in any kind of event, without affecting the event’s categorization.

However when the event is about IAM (Identity and Account Management), it should be categorized as follows. In this section we’ll cover specifically `event.category` and `event.type` with regards to IAM activity. Make sure to read the [Categorization section](/reference/ecs-category-field-values-reference.md) to see all allowed values, and read more about `event.kind` and `event.outcome`.

::::{note}
IAM activity is a bit particular in that events are expected to be assigned 2 event types. One of them indicates the type of activity (creation, deletion, change, etc.), and the other indicates whether a user or a group is the target of the management activity.
::::


Many sections of the examples below are elided, in order to focus on the categorization of the events.

Creation of group "test-group":

```JSON
{
  "event": {
    "kind": "event",
    "category": ["iam"], <1>
    "type": ["group", "creation"], <2>
    "outcome": "success"
  },
  "group": { "name": "test-group", ... },
  "user": { ... },
  "related": { "user": [ ... ] }
}
```

1. Category "iam"
2. Both relevant event types to a group creation


Adding "test-user" to "test-group":

```JSON
{
  "event": {
    "kind": "event",
    "category": ["iam"], <1>
    "type": ["user", "change"], <2>
    "action": "user added to group", <3>
    "outcome": "success"
  },
  "user": {
    ...
    "target": { <4>
      "name": "test-user",
      "group": { "name": "test-group" }
    }
  },
  "related": { "user": [ ... ] }
}
```

1. Category "iam"
2. Both relevant event types to a user modification
3. `event.action` is not a categorization field, and has no mandated value. It can be populated based on source event details or by a pipeline, to ensure the event captures all subtleties of what’s happening.
4. How to use all possible user fields is detailed below.



## User identifiers [ecs-user-identifiers]

Different systems use different values for user identifiers. Here are a few pointers to help normalize some simple cases.

* When a system provides a composite value for the user name (e.g. DOMAINNAME\username), capture the domain name in `user.domain` and the user name (without the domain) in `user.name`.
* When a system uses an email address as the main identifier, populate both `user.id` and `user.email` with it.


## Field reuse [ecs-user-usage-field-reuse]

The user fields can be reused (or appear) in many places across ECS. This makes it possible to capture many users relevant to a single event.

Here’s the full list of places where the user fields can appear:

* `user.*`
* `user.effective.*`
* `user.target.*`
* `user.changes.*`
* `source.user.*`
* `destination.user.*`
* `client.user.*`
* `server.user.*`

Let’s go over the meaning of each.

The examples below will only populate `user.name` and sometimes `user.id` inside the various `user` nestings, for readability. However in implementations, unless otherwise noted, all `user` fields that can reasonably be populated in each location should be populated.


### User fields at the Root of an event [ecs-user-usage-user-at-root]

The user fields at the root of an event are used to capture the user performing the main action described by the event. This is especially important when there’s more than one user present on the event. `user.*` fields at the root of the event represent the user performing the action.

In many cases, events that only mention one user should populate the user fields at the root of the event, even if the user is not the one performing the action.

In cases where a purpose-specific user field such as `url.username` is populated, `user.name` should also be populated with the same user name.

```json
{
  "url": { "username": "alice" }, <1>
  "user": { "name": "alice" }, <2>
  "related": { "user": ["alice"] }
}
```

1. Purpose-specific username field
2. Username copied to `user.name` to establish `user.name` as a reliable baseline.



### Remote logons [ecs-user-usage-remote-logons]

When users are crossing host boundaries, the users are captured at `source.user` and `destination.user`.

Examples of data sources where this is applicable:

* Remote logons via ssh, kerberos
* Firewalls observing network traffic

In order to align with ECS' design of having `user` at the root of the event as the user performing the action, all `source.user` fields should be copied to `user` at the root.

Here’s an example where user "alice" logs on to another host as user "deus":

```json
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
  },
  "related": { "user": ["alice", "deus"] }
}
```

Whenever an event source populates the `client` and `server` fields in addition to `source` and `destination`, the user fields should be copied accordingly as well. You can review [Mapping network events](/reference/ecs-mapping-network-events.md) to learn more about mapping network events.


### Privilege changes [ecs-user-usage-privilege-changes]

The `user.effective` fields are relevant when there’s a privilege escalation or demotion and it’s possible to determine the user requesting/performing the escalation.

Use the `user` fields at the root to capture who is requesting the privilege change, and `user.effective` to capture the requested privilege level, whether or not the privilege change was successful.

Here are examples where this is applicable:

* A user changing identity on a host.

    * Examples: sudo, su, Run as.

* Running a program as a different user. Examples:

    * A trusted user runs a specific admin command as root via a mechanism such as the Posix setuid/setgid.
    * A service manager with administrator privileges starts child processes as limited users, for security purposes (e.g. root runs Apache HTTPD as user "apache")


In cases where the event source only gives information about the effective user and not who requested different privileges, the `user` fields at the root of the event should be used instead of `user.effective`.

Here’s an example of user "alice" running a command as root via sudo:

```json
{
  "user": {
    "name": "alice",
    "id": "1001",
    "effective": {
      "name": "root",
      "id": "1"
    }
  },
  "related": { "user": ["alice", "root"] }
}
```

When it’s not possible (or it’s prohibitive) to determine which user is requesting different privilege levels, it’s acceptable to capture the effective user at the root of the event. Typically a privilege change event will already have happened, for example: bob "su" as root; and subsequent events will show the root user performing the actions.


### Identity and access management [ecs-user-usage-iam]

Whenever a user is performing an action that affects another user — typically in IAM scenarios — the user affected by the action is captured at `user.target`. The user performing the IAM activity is captured at the root of the event.

Examples of IAM activity include:

* user-a creates or deletes user-b
* user-a modifies user-b

In the create/delete scenarios, there’s either no prior state (user creation) or no post state (user deletion). In these cases, only `user` at the root and `user.target` must be populated.

Example where "root" creates user "bob":

```json
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
  "related": { "user": ["bob", "root"] }
}
```

When there’s a change of state to an existing user, `user.target` must be used to capture the prior state of the user, and `user.changes` should list only the changes that were performed.

Example where "root" renames user "bob" to "bob.barker":

```json
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
  },
  "related": { "user": ["bob", "bob.barker", "root"] }
}
```

You’ll note in the example above that unmodified attributes like the user ID are not repeated under `user.changes.*`, since they didn’t change.


### Combining IAM and privilege change [ecs-user-usage-combining]

We’ve covered above how `user.target` and `user.changes` can be used at the same time. If privilege escalation is also present in the same IAM event, `user.effective` should of course be used as well.

Here’s the "rename" example from the IAM section above. In the following example, we know "alice" is escalating privileges to "root", in order to modify user "bob":

```json
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
  "related": { "user": ["alice", "bob", "bob.barker", "root"] }
}
```


### Subtleties around field reuse [ecs-user-usage-reuse-subtleties]

Most cases of field reuse in ECS are reusing a field set inside a different field set. Two examples of this are:

* reusing `group` in `user`, resulting in the `user.group.*` fields, or
* reusing `user` in `destination`, resulting in the `destination.user.*` fields, which also include `destination.user.group.*`.

The `user` fields can also be reused within `user` as different names, representing the role of each relevant user. Examples are the `user.target.*` or `user.effective.*` fields.

However, it’s important to note that `user` fields reused within `user` are *not carried around anywhere else*. Let’s illustrate the various permutations of what’s valid and what is not.

| Field | Validity | Notes |
| --- | --- | --- |
| `user.group.*` | Valid | Normal reuse. |
| `destination.user.group.*` | Valid | The `group` reuse gets carried around when `user` is reused elsewhere.Populate only if relevant to the event. |
| `user.target.group.*`, `user.effective.group.*`, `user.changes.group.*` | Valid | The `group` reuse gets carried around even when `user` is reused within itself.Populate only if relevant to the event. |
| `destination.user.target.*`, `destination.user.effective.*`, `destination.user.changes.*` | **Invalid** | The `user` fields reused within `user` are not carried around anywhere else.The same rule applies when `user` is reused under `source`, `client` and `server`. |


## Pivoting via related.user [ecs-user-usage-pivoting]

In all events in this page, we’ve populated the `related.user` fields.

Any event that has users in it should always populate the array field `related.user` with all usernames seen in the event; including event names that appear in custom fields. Note that this field is not a nesting of all user fields, it’s a flat array meant to contain user identifiers.

Taking the example from `user.changes` again, we can see that no matter the role of the each user (before/after privilege escalation, affected user, username after rename), they are all present in `related.user`:

```json
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

Like the other fields in the [related](/reference/ecs-related.md) field set, `related.user` is meant to facilitate pivoting. For example, if you have a suspicion about user "bob.barker", searching for this name in `related.user` will give you all events related to this user, whether it’s the creation / rename of the user, or events where this user was active in a system.


## Mapping examples [ecs-user-usage-mappings]

For examples of mapping events from various sources, you can look at [RFC 0007 in section Source Data](https://github.com/elastic/ecs/blob/main/rfcs/text/0007-multiple-users.md#source-data).

