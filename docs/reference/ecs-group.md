---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-group.html
applies_to:
  stack: all
  serverless: all
---

# Group fields [ecs-group]

The group fields are meant to represent groups that are relevant to the event.


## Group field details [_group_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-group-domain$$$[group.domain](#field-group-domain) | Name of the directory the group is a member of.<br><br>For example, an LDAP or Active Directory domain name.<br><br>type: keyword<br> | extended |
| $$$field-group-id$$$[group.id](#field-group-id) | Unique identifier for the group on the system/platform.<br><br>type: keyword<br> | extended |
| $$$field-group-name$$$[group.name](#field-group-name) | Name of the group.<br><br>type: keyword<br> | extended |


## Field reuse [_field_reuse_11]

The `group` fields are expected to be nested at:

* `process.attested_groups`
* `process.group`
* `process.real_group`
* `process.saved_group`
* `process.supplemental_groups`
* `user.group`

Note also that the `group` fields may be used directly at the root of the events.

