# 0010: Email
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2020-11-30** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC proposes a new top-level field to facilitate email use cases.

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

Email specific fields:

| field | type | description |
| --- | --- | --- |
| `email.bcc.addresses` | `wildcard[]` | Addresses of Bcc's |
| `email.cc.addresses` | `wildcard[]` | Addresses of Cc's |
| `email.attachments_count` | long | A field outside the flattened structure to control how many attachments are included in the email |
| `email.attachments` | flattened | A flattened field for anything related to attachments. This allows objects being stored with all information for each file when you have multiple attachments |
| `email.direction` | keyword | Direction of the message based on the sending and receving domains |
| `email.sender.address` | wildcard | Senders email address |
| `email.sender.domain` | wildcard | Domain of the sender |
| `email.sender.top_level_domain` | keyword | Top level domain of the sender |
| `email.sender.registered_domain` | wildcard | Registered domain of the sender |
| `email.sender.subdomain` | keyword | Subdomain of the sender |
| `email.message_id` | keyword | Internet message ID of the message |
| `email.reply_to.address` | wildcard | Reply-to address |
| `email.return_path.address` | wildcard | The return address for the message |
| `email.size` | long | Total size of the message, in bytes, including attachments |
| `email.subject` | wildcard | Subject of the message |
| `email.recipients.addresses` | `keyword[]` | Recipient addresses |
| `email.domains` | `keyword[]` | domains related to the email |


Other ECS fields used together with email usecases:
| field | description |
| --- | --- |
| `event.duration` | The duration related to the email event. Could be the total duration in Quarantine, how long the email took to send from source to destination etc |
| `event.start` | When the email event started
| `event.end` | When the email event ended
| `process.name` | When the event is related to a server or client. Does not take MTA into account which is part of a ongoing discussion |
| `network.protocol` | Type of email protocol used |
| `tls.*` | Used for TLS related information for the connection to for example a SMTP server over TLS |



## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Email use cases stretch across all three Elastic solutions - Search, Observe, Protect. Whether it's searching for content within email, ensuring email infrastrucure is operational or detecting email based attacks, there are many possibilities for email fields within ECS.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

- **Email Analytics**: [Hubspot](https://legacydocs.hubspot.com/docs/methods/email/email_events_overview), Marketo, Salesforce Pardot
- **Email Server**: [O365 Message Tracing](https://docs.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/run-a-message-trace-and-view-results), [Postfix](https://nxlog.co/documentation/nxlog-user-guide/postfix.html)
- **Email Security**: [Barracuda](https://campus.barracuda.com/product/emailsecuritygateway/doc/12193950/syslog-and-the-barracuda-email-security-gateway/), [Forcepoint](https://www.websense.com/content/support/library/email/v85/email_siem/siem_log_map.pdf), [Mimecast](https://www.mimecast.com/tech-connect/documentation/tutorials/understanding-siem-logs/), [Proofpoint](https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API)

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->
```json
{
	"EndDate": "2020-11-10T22:12:34.8196921Z",
	"FromIP": "8.8.8.8",
	"Index": 25,
	"MessageId": "\\u003c95689d8d5e7f429390a4e3646eef75e8-JFBVALKQOJXWILKBK4YVA7APGM3DKTLFONZWCZ3FINSW45DFOJ6EAQ2ENFTWK43UL4YTCMBYGIYHYU3NORYA====@microsoft.com\\u003e",
	"MessageTraceId": "ff1a64a3-cafb-41b7-1efb-08d8848aedc3",
	"Organization": "testdomain.onmicrosoft.com",
	"Received": "2020-11-09T04:50:06.3312635",
	"RecipientAddress": "john@testdomain.onmicrosoft.com",
	"SenderAddress": "o365mc@microsoft.com",
	"Size": 64329,
	"StartDate": "2020-11-08T22:12:34.8196921Z",
	"Status": "Delivered",
	"Subject": "Weekly digest: Microsoft service updates",
	"ToIP": null
}

{
	"EndDate": "2020-11-10T22:12:34.8196921Z",
	"FromIP": null,
	"Index": 8,
	"MessageId": "\\u003c72872e16-f4c2-4eef-a393-e5621748a0ff@AS8P19vMB1605.EURP191.PROD.OUTLOOK.COM\\u003e",
	"MessageTraceId": "a4bd8c4c-3a4f-427f-8952-08d8850f9c20",
	"Organization": "testdomain.onmicrosoft.com",
	"Received": "2020-11-10T00:28:56.3306834",
	"RecipientAddress": "o365mc@microsoft.com",
	"SenderAddress": "postmaster@testdomain.onmicrosoft.com",
	"Size": 96627,
	"StartDate": "2020-11-08T22:12:34.8196921Z",
	"Status": "Delivered",
	"Subject": "Undeliverable: Message Center Major Change Update Notification",
	"ToIP": "8.8.8.8"
}
```



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
Current concerns or topics still being discussed from stage 1:

- Whether we want to add specific fields for email protocols, either as a root field or nested under email.* (SMTP, IMAP, POP etc).
- Need to make sure that the ECS fieldset for email catches all common usecases, for example spam, metrics and deliverables and logging.
- Whether we want to create a new event.category field (email) and which event.type it should be combined with.
- The email RFC will be the first ECS fieldset that uses the flattened datatype (for attachments), need to ensure that there will be major issues related to this.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

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

* @p1llus | Author
* @jamiehynds | Sponsor

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

- [Hubspot](https://legacydocs.hubspot.com/docs/methods/email/email_events_overview)
- [O365 Message Tracing](https://docs.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/run-a-message-trace-and-view-results)
- [Postfix](https://nxlog.co/documentation/nxlog-user-guide/postfix.html)
- [Barracuda](https://campus.barracuda.com/product/emailsecuritygateway/doc/12193950/syslog-and-the-barracuda-email-security-gateway/)
- [Forcepoint](https://www.websense.com/content/support/library/email/v85/email_siem/siem_log_map.pdf)
- [Mimecast](https://www.mimecast.com/tech-connect/documentation/tutorials/understanding-siem-logs/)
- [Proofpoint](https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1 (formerly proposal stage): https://github.com/elastic/ecs/pull/999
  * RFC ID correction: https://github.com/elastic/ecs/pull/1157
* Stage 1 (draft): https://github.com/elastic/ecs/pull/1219
