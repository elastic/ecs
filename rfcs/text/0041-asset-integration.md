# 0041: Asset Integration
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2023-07-07** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This proposal extends the existing ECS field set to store inventory metadata for hosts and users from external application repositories. Using ECS to store such fields will improve metadata querying and retrieval across various use cases.

Terminologies:
The `Entity Analytics` initiative within Security refers to hosts and users as `entities`. Other generic security and observability use cases may refer to hosts/ users as `assets`. Certain directory services or asset management applications use the term 'device' when referring to a host.  In this RFC, I have simplified these terminologies to `users` and `hosts` and these will represent all the neighboring terms.

This proposal includes the following:
* Additional fields in the `users` and `os` objects.
* Introduces a new field set called `assets`.
<!-- * Additional fields in the `host` object --->

This proposal will also facilitate storing host and user inventory within the security solution (the entity store).


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
user.profile.organization	| keyword |	Elasticsearch Inc.	| Organization name associated with the account.
user.profile.location	| keyword |	US - Washington - Distributed	| Assigned location for the user account.
user.profile.mobile_phone	| keyword |	222-222-2222
user.profile.primaryPhone	| keyword |	222-222-2222
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
* We have a set of risk.* fields in ECS that can be further nested under the asset.* object. Reference to [Risk RFC](https://github.com/elastic/ecs/blob/main/rfcs/text/0031-risk-fields.md).



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

* As part of Entity Analytics, we are ingesting metadata about Users and from various external vendor applications. We are storing all ingested metadata in Elasticsearch. After we map these fields to ECS, we will enrich these ingested events for risk-scoring scenarios (e.g., context enrichments) and detecting advanced analytics (UBA) use cases.

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

<!--
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

* Ingestion mechanisms: Entity Analytics fleet integrations are the primary ingesting mechanism for this dataset.

* Usage mechanism: Elastic Security solution (Entity Analytics & Threat Hunting workflows) will be the primary user of the proposed ECS fields and values.



## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

* We have a couple of fleet integrations under development. We want them to use these proposed ECS before being released.
* Schema/ field sets defined here focus on asset inventory data sources. Additional fields may need to be appended (ideally within this RFC lifecycle) to support the entity store needs.
* Due diligence is needed to avoid the proliferation of field sets and validate business requirements.
* In stage1, @jasonrhodes identified fields from o11y use cases and a potential conflict: https://github.com/elastic/ecs/pull/2215#pullrequestreview-1498781860

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
* ?

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

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
