# 0041: Asset Integration
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (Draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2023-07-07** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

This proposal extends the existing ECS field set to store inventory metadata for hosts and users from external application repositories. Using ECS to store such fields will improve metadata querying and retrieval across various use cases.

Terminologies:
The `Entity Analytics` initiative within Security refers to hosts and users as `entities`. Other generic security and observability use cases may refer to hosts/ users as `assets`. Certain directory services or asset management applications use the term 'device' when referring to a host.  In this RFC, I have simplified these terminologies to `users` and `hosts` and these will represent all the neighboring terms.

This proposal includes the following:
* Additional fields in the `users` and `os` objects.
* Introduces a new field set called `assets`.
<!-- * Additional fields in the `host` object --->
* Fields required for storing host and user metadata as the Elastic Security entity store/ index. 

We will create new enhancement RFCs to extend these schemas as needed.

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

### Proposed New Fields for User object

Field | Type | Example | Description
--- | --- | --- | ---
user.profile.id	| keyword	| 1234	| User ID from the identity datasource.
user.profile.type	| keyword	| Employee	| Type of user account.
user.profile.status	| keyword |	On board	| Status of the user account.
user.profile.first_name	| keyword |	First	| First Name of the User.
user.profile.last_name	| keyword |	Last	| Last Name of the user.
user.profile.other_identities	| keyword, text |	first.last@elk.elastic.co	| Array of additional user identities (usually email addresses).
user.profile.manager	| keyword |	John Doe	| Assigned Manager for the user account.
user.profile.employee_type	| keyword |	Regular | Further classification type for the user account.
user.profile.job_family	| keyword |	65-Sales	| Job family associated with the user account.
user.profile.job_family_group	| keyword |	GTM	| Job family group associated with the user account.
user.profile.management_level	| keyword |	Individual Contributor	| If the user account is identified as a Manager or Individual contributor.
user.profile.job_title	| keyword |	Field Sales	| Job title assigned to the user account.
user.profile.department	| keyword |	x256	| Department name associated with the user account.
user.profile.location	| keyword |	US - Washington - Distributed	| Assigned location for the user account.
user.profile.secondEmail	| keyword |	first.l@elastic.co	| Additional email addresses associated with the user account.
user.profile.sup_org_id	| keyword |	SUP-ORG-75	| Primary organization ID for the user account.
user.profile.supervisory_Org	| keyword |	Field Sales	| Primary organization name for the user account.
user.profile.assigned_mdm_id	| keyword |	2950	| The primary host identifier (usually `asset.id` value) assigned to the user. This field acts as a correlation identifier for the host event document.
user.account.create_date	| date |	June 5, 2023 @ 18:25:57.000	| Date account was created.
user.account.activated_date	| date |	June 5, 2023 @ 18:25:57.000	| Date account was activated.
user.account.change_date	| date |	June 5, 2023 @ 18:25:57.000	| Date user account record was last updated at source
user.account.status.recovery	| boolean |	true/ false	| A flag indicating if account is in recovery
user.account.status.locked_out	| boolean |	true/ false	| A flag indicating if account is currently locked out
user.account.status.suspended	| boolean |	true/ false	| A flag indicating if account has been suspended
user.account.isAdmin	| boolean |	true/ false	| A flag indicating if account is an Admin account
user.account.isDelegatedAdmin	| boolean |	true/ false	| A flag indicating if account has Delegated Admin rights
user.account.isPriviledged	| boolean |	true/ false	| A flag indicating if account is a Privileged account
user.account.status.password_expired	| boolean |	true/ false	| A flag indicating if account password has expired.
user.account.status.deprovisioned	| boolean |	true/ false	| A flag indicating if account has been deprovisioned
user.account.password_change_date	| date |	June 5, 2023 @ 18:25:57.000	| Last date/time when account password was updated

**Update:**
Updated proposal to redact the below field. ECS guidance is to reuse existing organization.* fields instead 

> user.profile.organization	| keyword |	Elasticsearch Inc.	| Organization name associated with the account.

### Proposed New Fields for Asset object

Field | Type | Generic Example |	User Entity Example | Host Entity Example | Description
--- | --- | --- | --- | --- | ---
asset.category	| keyword |	-	        | Null	                | hardware	                | A further classification of the asset type beyond event.category. For example, for host assets {hardware, virtual, container, node}. For user assets {NULL ?}
asset.type	    | keyword |	-	        | Null	                | workstation	            | A sub classification of asset. For host assets {workstation, S3, Compute}. For user assets {NULL?}.
asset.id	    | keyword |	-	        | 00uhs72c27s6PiK7x1t7	| 2950	                    | A unique ID for the asset. For inventory integrations, it's the id generated from inventory data source.
asset.name	    | keyword |	-	        | Sourin Paul	        | Sourin Paul Macbook Pro	| A common name for the asset.
asset.vendor	| keyword |	-           |	-	                | Apple	                    | Used primarily for 'Host' entities, the vendor name or brand associated with the asset.
asset.product	| keyword |	-           |	-	                | MacBook Pro	            | Used primarily for 'Host' entities, the product name associated with the asset.
asset.model	    | keyword |	-           |	-	                |TBD	                    | Used primarily for 'Host' entities, the model name or number associated with this asset.
asset.version	| keyword |	-           |	-	                | TBD	                    | Used primarily for 'Host' entities, the version or year associated with the asset.
asset.owner	    | keyword |	-           |	-	                | sourin.paul@elastic.co	| The primary user entity identifier (usually an email address) who owns the 'Host' asset.
asset.priority	| keyword |	Priority 1	| -                     | -                         | A priority classification for the asset obtained from outside the solution, such as from some external CMDB or Directory service.
asset.criticality	| keyword |	Critical	| - | -                                         | A criticality classification obtained from outside the solution, such as from some external CMDB or Directory service.
asset.business_unit	| keyword |	Analyst Experience	| - | -                                 | Business Unit associated with the asset (user or host).
asset.costCenter	| keyword |	Security - Protections | - | -                              | Cost Center associated with the asset (user or host).
asset.cost_center_hierarchy	| keyword |	Engineering	 | - | -                                | Additional cost center information associated with the asset (user or host).
asset.status	    | keyword         |	ACTIVE      | - | -                                 | Current status of the asset in the inventory datasource.
asset.last_status_change_date	| date |	June 5, 2023 @ 18:25:57.000	| - | -             | The most recent date/time when the asset.status was updated.
asset.create_date	            | date |	June 5, 2023 @ 18:25:57.001	| - | -             | For users, it's the hire date. For other assets, it's the in-service date.
asset.end_date	                | date |	June 5, 2023 @ 18:25:57.002	| - | -             | For users, it's the termination date; for other assets, it's the out-of-service date.
asset.first_seen	            | date |	June 5, 2023 @ 18:25:57.003	| - | -             | The first date/time the directory service or the security solution observed this asset.
asset.last_seen	                | date |	June 5, 2023 @ 18:25:57.004	| - | -             | The most recent date/time the directory service or the security solution observed this asset.
asset.last_updated	            | date |	June 5, 2023 @ 18:25:57.005	| - | -             | The most recent date/time this asset was updated in directory services.
asset.serial_number	            | keyword	| C02FG1G1MD6T	| - | -             |		Serial number of the asset.
asset.tags	                    | keyword	  | watch, mdmaccess		| - | -             |	Tags assigned at the MDM.
asset.assigned_users	          | keyword	  | user1@email.com, user2@email.com		| - | -             |	List of user ids (usually email addresses) assigned to the asset. The value from the `asset.owner` field should always be included.
asset.assigned_users_are_admin	| boolean	  | TRUE	| - | -             |		Flag to identify if the assigned users have admin privileges.
asset.is_managed	              | boolean	  | TRUE			| - | -             | If asset is managed by the organization.
asset.last_enrolled_date	      | date	    | June 5, 2023 @ 18:25:57.005		| - | -             |	The most recent date/time the asset checked in with MDM.
asset.data_classification	      | keyword	  | restricted		| - | -             |	Data classification tier for the asset.
asset.installed_extensions 	| keyword	  | Nested objects	  | List of installed extensions along with their metadata
asset.installed_applications	| keyword	    | Nested objects	  | List of installed applications along with their metadata

#### Nesting of existing risk.* fields under asset object

We have a set of risk.* fields in ECS. A quick reference to past risk.* RFCs:

* [Initial Risk RFC](https://github.com/elastic/ecs/blob/main/rfcs/text/0031-risk-fields.md)
* [Risk Score Extenstions](https://github.com/elastic/ecs/pull/2236)

These risk.* fields can be further nested under the asset.*

### Proposed New Fields for os.* object
Field | Type | Example | Description
--- | --- | --- | ---
os.build	| keyword		| 22F66   | Host OS Build information



<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

* As part of Entity Analytics, we are ingesting metadata about Users and from various external vendor applications. We are storing all ingested metadata in Elasticsearch. After we map these fields to ECS, we will enrich these ingested events for risk-scoring scenarios (e.g., context enrichments) and detecting advanced analytics (UEBA) use cases.

### Example of Hosts and Users stored in ES

* This schema will persist `Observed` (queried) entities from the ingested security log dataset in an Entity store. This entity store can be further extended to meet broader Asset Management needs.

* Additional enrichment use cases for existing prebuilt detection rules will leverage these ECS fields.




## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

There are many sources of asset inventory repositories. In the mid-term, we are planning to ingest data from the following application providers:

### User (Identity) repository sources:
* Azure Active Directory
* Active Directory DS
* Okta
* Workday
* GSuite
* GitHub

### Host repository sources:
* Azure Active Directory
* Jamf
* Active Directory DS
* MS Intune
* ServiceNow Asset CMDB

### Examples of source data:

#### Subset of User fields from Okta:

```json
{
  "@timestamp": "2023-07-04T09:57:19.786056-05:00",
  "event": {
    "action": "user-discovered"
  },
  "okta": {
    "id": "userid",
    "status": "RECOVERY",
    "created": "2023-06-02T09:33:00.189752+09:30",
    "activated": "0001-01-01T00:00:00Z",
    "statusChanged": "2023-06-02T09:33:00.189752+09:30",
    "lastLogin": "2023-06-02T09:33:00.189752+09:30",
    "lastUpdated": "2023-06-02T09:33:00.189753+09:30",
    "passwordChanged": "2023-06-02T09:33:00.189753+09:30",
    "type": {
      "id": "typeid"
    },
    "profile": {
      "login": "name.surname@example.com",
      "email": "name.surname@example.com",
      "firstName": "name",
      "lastName": "surname"
    },
    "credentials": {
      "password": {},
      "provider": {
        "type": "OKTA",
        "name": "OKTA"
      }
    },
    "_links": {
      "self": {
        "href": "https://localhost/api/v1/users/userid"
      }
    }
  },
  "user": {
    "id": "userid"
  },
  "labels": {
    "identity_source": "okta-1"
  }
}
```

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->


<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

### Examples of Real-world mapping: 

#### Mapping User object from Okta into ECS (partial):
```yml
description: Pipeline for processing User logs.
processors:
  - set:
      field: ecs.version
      tag: set_ecs_version
      value: 8.8.0
  - set:
      field: event.kind
      tag: set_event_kind
      value: asset
  - set:
      field: event.category
      tag: set_event_category
      value: ['iam']
  - set:
      field: event.type
      tag: set_event_type
      value: ['user','info']
  - rename:
      field: okta.id
      target_field: entityanalytics_okta.user.id
      tag: rename_user_id
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.id}}}'
      tag: append_user_id_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.id != null
  - script:
      lang: painless
      description: Set User Account Status properties.
      tag: painless_set_user_account_status
      if: ctx.okta?.status != null
      source: |-
        if (ctx.user == null) {
          ctx.user = new HashMap();
        }
        if (ctx.user.account == null) {
          ctx.user.account = new HashMap();
        }
        if (ctx.user.account.status == null) {
          ctx.user.account.status = new HashMap();
        }
        ctx.user.account.status.put('recovery', false);
        ctx.user.account.status.put('locked_out', false);
        ctx.user.account.status.put('suspended', false);
        ctx.user.account.status.put('password_expired', false);
        ctx.user.account.status.put('deprovisioned', false);
        def status = ctx.okta.status.toLowerCase();
        if (['recovery', 'locked_out', 'suspended', 'password_expired', 'deprovisioned'].contains(status)) {
          ctx.user.account.status[status] = true;
        }
      on_failure:
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - rename:
      field: okta.status
      target_field: entityanalytics_okta.user.status
      tag: rename_user_status
      ignore_missing: true
  - set:
      field: asset.status
      copy_from: entityanalytics_okta.user.status
      tag: set_asset_status
      ignore_empty_value: true
  - set:
      field: user.profile.status
      copy_from: entityanalytics_okta.user.status
      tag: set_user_profile_status
      ignore_empty_value: true
  - date:
      field: okta.created
      target_field: entityanalytics_okta.user.created
      tag: date_user_created
      formats:
        - ISO8601
      if: ctx.okta?.created != null && ctx.okta.created != ''
      on_failure:
        - remove:
            field: okta.created
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - set:
      field: user.account.create_date
      copy_from: entityanalytics_okta.user.created
      tag: set_user_account_create_date
      ignore_empty_value: true
  - set:
      field: asset.create_date
      copy_from: entityanalytics_okta.user.created
      tag: set_asset_create_date
      ignore_empty_value: true
  - date:
      field: okta.activated
      target_field: entityanalytics_okta.user.activated
      tag: date_user_activated
      formats:
        - ISO8601
      if: ctx.okta?.activated != null && ctx.okta.activated != ''
      on_failure:
        - remove:
            field: okta.activated
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - set:
      field: user.account.activated_date
      copy_from: entityanalytics_okta.user.activated
      tag: set_user_account_activated_date
      ignore_empty_value: true
  - date:
      field: okta.statusChanged
      target_field: entityanalytics_okta.user.status_changed
      tag: date_user_status_changed
      formats:
        - ISO8601
      if: ctx.okta?.statusChanged != null && ctx.okta.statusChanged != ''
      on_failure:
        - remove:
            field: okta.statusChanged
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - set:
      field: user.account.change_date
      copy_from: entityanalytics_okta.user.status_changed
      tag: set_user_account_change_date
      ignore_empty_value: true
  - set:
      field: asset.last_status_change_date
      copy_from: entityanalytics_okta.user.status_changed
      tag: set_asset_last_status_change_date
      ignore_empty_value: true
  - date:
      field: okta.lastLogin
      target_field: entityanalytics_okta.user.last_login
      tag: date_user_last_login
      formats:
        - ISO8601
      if: ctx.okta?.lastLogin != null && ctx.okta.lastLogin != ''
      on_failure:
        - remove:
            field: okta.lastLogin
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - set:
      field: asset.last_seen
      copy_from: entityanalytics_okta.user.last_login
      tag: set_asset_last_seen
      ignore_empty_value: true
  - date:
      field: okta.lastUpdated
      target_field: entityanalytics_okta.user.last_updated
      tag: date_user_last_updated
      formats:
        - ISO8601
      if: ctx.okta?.lastUpdated != null && ctx.okta.lastUpdated != ''
      on_failure:
        - remove:
            field: okta.lastUpdated
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - set:
      field: asset.last_updated
      copy_from: entityanalytics_okta.user.last_updated
      tag: set_asset_last_seen
      ignore_empty_value: true
  - date:
      field: okta.passwordChanged
      target_field: entityanalytics_okta.user.password_changed
      tag: date_user_password_changed
      formats:
        - ISO8601
      if: ctx.okta?.passwordChanged != null && ctx.okta.passwordChanged != ''
      on_failure:
        - remove:
            field: okta.passwordChanged
        - append:
            field: error.message
            value: 'Processor {{{_ingest.on_failure_processor_type}}} with tag {{{_ingest.on_failure_processor_tag}}} in pipeline {{{_ingest.pipeline}}} failed with message: {{{_ingest.on_failure_message}}}'
  - set:
      field: user.account.password_change_date
      copy_from: entityanalytics_okta.user.password_changed
      tag: set_user_account_password_change_date
      ignore_empty_value: true
  - rename:
      field: okta.type
      target_field: entityanalytics_okta.user.type
      tag: rename_user_type
      ignore_missing: true
  - rename:
      field: okta.transitioningToStatus
      target_field: entityanalytics_okta.user.transitioning_to_status
      tag: user_transitioning_to_status
      ignore_missing: true
  - rename:
      field: okta.profile.login
      target_field: entityanalytics_okta.user.profile.login
      tag: rename_user_profile_login
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.login}}}'
      tag: append_user_profile_login_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.login != null
  - set:
      field: user.name
      copy_from: entityanalytics_okta.user.profile.login
      tag: set_user_name
      ignore_empty_value: true
  - rename:
      field: okta.profile.email
      target_field: entityanalytics_okta.user.profile.email
      tag: rename_user_profile_email
      ignore_missing: true
  - set:
      field: user.email
      copy_from: entityanalytics_okta.user.profile.email
      tag: set_user_email
      ignore_empty_value: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.email}}}'
      tag: append_user_profile_email_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.email != null
  - rename:
      field: okta.profile.secondEmail
      target_field: entityanalytics_okta.user.profile.second_email
      tag: rename_user_profile_second_email
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.second_email}}}'
      tag: append_user_profile_second_email_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.second_email != null
  - set:
      field: user.profile.other_identities
      copy_from: entityanalytics_okta.user.profile.second_email
      tag: set_user_profile_other_identities
      ignore_empty_value: true
  - set:
      field: user.profile.secondEmail
      copy_from: entityanalytics_okta.user.profile.second_email
      tag: set_user_profile_secondEmail
      ignore_empty_value: true
  - rename:
      field: okta.profile.firstName
      target_field: entityanalytics_okta.user.profile.first_name
      tag: rename_user_profile_first_name
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.first_name}}}'
      tag: append_user_profile_first_name_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.first_name != null
  - set:
      field: user.profile.first_name
      copy_from: entityanalytics_okta.user.profile.first_name
      tag: set_user_profile_first_name
      ignore_empty_value: true
  - rename:
      field: okta.profile.lastName
      target_field: entityanalytics_okta.user.profile.last_name
      tag: rename_user_profile_last_name
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.last_name}}}'
      tag: append_user_profile_last_name_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.last_name != null
  - set:
      field: user.profile.last_name
      copy_from: entityanalytics_okta.user.profile.last_name
      tag: set_user_profile_last_name
      ignore_empty_value: true
  - rename:
      field: okta.profile.middleName
      target_field: entityanalytics_okta.user.profile.middle_name
      tag: rename_user_profile_middle_name
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.middle_name}}}'
      tag: append_user_profile_middle_name_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.middle_name != null
  - rename:
      field: okta.profile.honorificPrefix
      target_field: entityanalytics_okta.user.profile.honorific.prefix
      tag: rename_user_profile_honorific_prefix
      ignore_missing: true
  - rename:
      field: okta.profile.honorificSuffix
      target_field: entityanalytics_okta.user.profile.honorific.suffix
      tag: rename_user_profile_honorific_suffix
      ignore_missing: true
  - rename:
      field: okta.profile.title
      target_field: entityanalytics_okta.user.profile.title
      tag: rename_user_profile_title
      ignore_missing: true
  - set:
      field: user.profile.job_title
      copy_from: entityanalytics_okta.user.profile.title
      tag: set_user_profile_job_title
      ignore_empty_value: true
  - rename:
      field: okta.profile.displayName
      target_field: entityanalytics_okta.user.profile.display_name
      tag: rename_user_profile_display_name
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.display_name}}}'
      tag: append_user_profile_display_name_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.display_name != null
  - set:
      field: user.full_name
      copy_from: entityanalytics_okta.user.profile.display_name
      tag: set_user_full_name
      ignore_empty_value: true
  - set:
      field: asset.name
      copy_from: entityanalytics_okta.user.profile.display_name
      tag: set_asset_name
      ignore_empty_value: true
  - rename:
      field: okta.profile.nickName
      target_field: entityanalytics_okta.user.profile.nick_name
      tag: rename_user_profile_nick_name
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.nick_name}}}'
      tag: append_user_profile_nick_name_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.nick_name != null
  - rename:
      field: okta.profile.profileUrl
      target_field: entityanalytics_okta.user.profile.url
      tag: rename_user_profile_url
      ignore_missing: true
  - rename:
      field: okta.profile.primaryPhone
      target_field: entityanalytics_okta.user.profile.primary_phone
      tag: rename_user_profile_primary_phone
      ignore_missing: true
  - set:
      field: user.profile.primaryPhone
      copy_from: entityanalytics_okta.user.profile.primary_phone
      tag: set_user_profile_primaryPhone
      ignore_empty_value: true
  - rename:
      field: okta.profile.mobilePhone
      target_field: entityanalytics_okta.user.profile.mobile_phone
      tag: rename_user_profile_mobile_phone
      ignore_missing: true
  - set:
      field: user.profile.mobile_phone
      copy_from: entityanalytics_okta.user.profile.mobile_phone
      tag: set_user_profile_mobile_phone
      ignore_empty_value: true
  - rename:
      field: okta.profile.streetAddress
      target_field: entityanalytics_okta.user.profile.street_address
      tag: rename_user_profile_street_address
      ignore_missing: true
  - rename:
      field: okta.profile.city
      target_field: entityanalytics_okta.user.profile.city
      tag: rename_user_profile_city
      ignore_missing: true
  - rename:
      field: okta.profile.state
      target_field: entityanalytics_okta.user.profile.state
      tag: rename_user_profile_state
      ignore_missing: true
  - rename:
      field: okta.profile.zipCode
      target_field: entityanalytics_okta.user.profile.zip_code
      tag: rename_user_profile_zip_code
      ignore_missing: true
  - rename:
      field: okta.profile.countryCode
      target_field: entityanalytics_okta.user.profile.country_code
      tag: rename_user_profile_country_code
      ignore_missing: true
  - rename:
      field: okta.profile.postalAddress
      target_field: entityanalytics_okta.user.profile.postal_address
      tag: rename_user_profile_postal_address
      ignore_missing: true
  - rename:
      field: okta.profile.preferredLanguage
      target_field: entityanalytics_okta.user.profile.preferred_language
      tag: rename_user_profile_preferred_language
      ignore_missing: true
  - rename:
      field: okta.profile.locale
      target_field: entityanalytics_okta.user.profile.locale
      tag: rename_user_profile_locale
      ignore_missing: true
  - rename:
      field: okta.profile.timezone
      target_field: entityanalytics_okta.user.profile.timezone
      tag: rename_user_profile_timezone
      ignore_missing: true
  - rename:
      field: okta.profile.userType
      target_field: entityanalytics_okta.user.profile.user_type
      tag: rename_user_profile_user_type
      ignore_missing: true
  - set:
      field: user.profile.type
      copy_from: entityanalytics_okta.user.profile.user_type
      tag: set_user_profile_type
      ignore_empty_value: true
  - rename:
      field: okta.profile.employeeNumber
      target_field: entityanalytics_okta.user.profile.employee_number
      tag: rename_user_profile_employee_number
      ignore_missing: true
  - append:
      field: related.user
      value: '{{{entityanalytics_okta.user.profile.employee_number}}}'
      tag: append_user_profile_employee_number_into_related_user
      allow_duplicates: false
      if: ctx.entityanalytics_okta?.user?.profile?.employee_number != null
  - set:
      field: user.profile.id
      copy_from: entityanalytics_okta.user.profile.employee_number
      tag: set_user_profile_id
      ignore_empty_value: true
  - rename:
      field: okta.profile.costCenter
      target_field: entityanalytics_okta.user.profile.cost_center
      tag: rename_user_profile_cost_center
      ignore_missing: true
  - set:
      field: asset.costCenter
      copy_from: entityanalytics_okta.user.profile.cost_center
      tag: set_asset_costCenter
      ignore_empty_value: true
  - rename:
      field: okta.profile.organization
      target_field: entityanalytics_okta.user.profile.organization
      tag: rename_user_profile_organization
      ignore_missing: true
  - set:
      field: user.organization.name
      copy_from: entityanalytics_okta.user.profile.organization
      tag: set_user_profile_organization
      ignore_empty_value: true

```

 
#### AzureAD Hosts


## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

* Ingestion mechanisms: Entity Analytics fleet integrations are the primary ingesting mechanism for this dataset.

* Usage mechanism: Elastic Security solution (Entity Analytics & Threat Hunting workflows) will be the primary user of the proposed ECS fields and values.



## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

~~* In stage1, @jasonrhodes identified fields from o11y use cases and a potential conflict: https://github.com/elastic/ecs/pull/2215#pullrequestreview-1498781860~~
--> Resolution: Exclude `asset.ean`, `asset.parents`, and `asset.children` from this RFC proposal and reintroduce these fields at a later time. Refer to: [[PR comment]](https://github.com/elastic/ecs/pull/2233#issuecomment-1917633738).

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @sourinpaul | author
* @andrewkroh | subject matter expert
* @jamiehynds | subject matter expert
* @lauravoicu | subject matter expert
* @MikePaquette | subject matter expert
* @sourinpaul | sponsor

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

* Stage 0: https://github.com/elastic/ecs/pull/2215
* Stage 1: https://github.com/elastic/ecs/pull/2233

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
