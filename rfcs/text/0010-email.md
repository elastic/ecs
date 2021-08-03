# 0010: Email
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC proposes a new top-level field set to facilitate email use cases, `email.*`. The `email.*` field set adds fields for the sender, recipient, message header fields, and other attributes of an email message typically seen logs produced by mail transfer agent (MTA) and email gateway applications.

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

### Email specific fields

| field | type | description |
| --- | --- | --- |
| `email.from` | keyword | Stores the `from` email address |
| `email.origination_timestamp` | date | The date and time the email message was composed. Many email clients will fill this in automatically when the message is sent by a user. |
| `email.delivery_timestamp` | date | The date and time the email message was received by the service or client. |
| `email.to` | keyword (array) | The email address(es) of the message recipient(s) |
| `email.subject` | keyword; `.text` text multi-field | A brief summary of the topic of the message |
| `email.cc` | keyword (array) | The email address(es) of the carbon copy (CC) recipient(s) |
| `email.bcc` | keyword (array) | The email address(es) of the blind carbon copy (CC) recipient(s) |
| `email.content_type` | keyword | Information about how the message is to be displayed. Typically a MIME type |
| `email.message_id` | wildcard | Unique identifier for the email message that refers to a particular version of a particular message |
| `email.reply_to` | keyword | Address that replies should be delivered to |
| `email.direction` | keyword | Direction of the message based on the sending and receiving domains |
| `email.x_mailer` | keyword | What application was used to draft and send the original email. |

### Additional event categorization allowed values

Email events may benefit from an additional ECS allowed event categorization value: `event.category: email`.

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Email use cases stretch across all three Elastic solutions - Search, Observe, Protect. Whether it's searching for content within email, ensuring email infrastructure is operational or detecting email based attacks, there are many possibilities for email fields within ECS.

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

### Office365 - Successful Delivery

#### Original log

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
```

#### Mapped event

```json
{
  "@timestamp": 1626984241830,
  "email": {
    "timestamp": "2020-11-08T22:12:34.8196921Z",
        "from": [
  	    "o365mc@microsoft.com"
  	],
    "to": [
      "john@testdomain.onmicrosoft.com"
    ],
    "subject": "Weekly digest: Microsoft service updates",
    "message_id": "\\u003c95689d8d5e7f429390a4e3646eef75e8-JFBVALKQOJXWILKBK4YVA7APGM3DKTLFONZWCZ3FINSW45DFOJ6EAQ2ENFTWK43UL4YTCMBYGIYHYU3NORYA====@microsoft.com\\u003e"
  },
  "event": {
    "action": "delivered",
    "kind": "event",
    "category": [
      "email",
      "network"
    ]
  }
}
```

### Office365 - Undeliverable

#### Original log

```json
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

#### Mapped event

```json
{
  "@timestamp": 1626984241830,
  "email": {
    "timestamp": "2020-11-10T22:12:34.8196921Z",
        "from": [
          "postmaster@testdomain.onmicrosoft.com"
        ],
        "to": [
          "o365mc@microsoft.com"
        ],
        "subject": "Undeliverable: Message Center Major Change Update Notification",
        "message_id": "\\u003c72872e16-f4c2-4eef-a393-e5621748a0ff@AS8P19vMB1605.EURP191.PROD.OUTLOOK.COM\\u003e"
    },
  "event": {
    "action": "delivered",
    "kind": "event",
    "category": [
      "email",
      "network"
    ]
  }
}
```

### Proofpoint Tap

#### Original log

```
<38>1 2016-06-24T21:00:08Z - ProofpointTAP - MSGBLK [tapmsg@21139 messageTime="2016-06-24T21:18:38.000Z" messageID="20160624211145.62086.mail@evil.zz" recipient="clark.kent@pharmtech.zz, diana.prince@pharmtech.zz" sender="e99d7ed5580193f36a51f597bc2c0210@evil.zz" senderIP="192.0.2.255" phishScore="46" spamScore="4" QID="r2FNwRHF004109" GUID="c26dbea0-80d5-463b-b93c-4e8b708219ce" xmailer="Spambot v2.5"]
```

#### Mapped event

```json
{
  "@timestamp": "2016-06-24T21:00:08Z",
  "email": {
    "timestamp": "2016-06-24T21:18:38.000Z",
    "message_id": "20160624211145.62086.mail@evil.zz",
    "to": [
      "clark.kent@pharmtech.zz",
      "diana.prince@pharmtech.zz"
    ],
    "from": [
      "e99d7ed5580193f36a51f597bc2c0210@evil.zz"
    ],
    "subject": "Please find a totally safe invoice attached.",
    "reply_to": "null",
    "x_mailer": "Spambot v2.5"
  },
  "event": {
    "id": "c26dbea0-80d5-463b-b93c-4e8b708219ce",
    "kind": "event",
    "category": "email",
    "action": "MSGBLK"
  },
  "source": {
    "address": 192.0.2.255,
    "ip": 192.0.2.255
  }
}
```

### Mimecast Receipt log

#### Original log

```
datetime=2017-05-26T16:47:41+0100|aCode=7O7I7MvGP1mj8plHRDuHEA|acc=C0A0|SpamLimit=0|IP=123.123.123.123|Dir=Internal|MsgId=<81ce15$8r2j59@mail01.example.com>|Subject=\message subject\|headerFrom=from@mimecast.com|Sender=from@mimecast.com|Rcpt=auser@mimecast.com|SpamInfo=[]|Act=Acc|TlsVer=TLSv1|Cphr=TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA|SpamProcessingDetail={"spf":{"info":"SPF_FAIL","allow":true},"dkim":{"info":"DKIM_UNKNOWN","allow":true}}|SpamScore=1
```

#### Mapped event

```json
{
  "@timestamp": "2017-05-26T16:47:41+0100",
  "source": {
    "address": 123.123.123.123,
    "ip": 123.123.123.123
  },
  "email": {
    "message_id": "<81ce15$8r2j59@mail01.example.com>",
    "from": [
      "from@mimecast.com"
    ],
    "to": [
      "auser@mimecast.com"
    ],
    "subject": "message subject",
    "direction": "internal"
  },
  "tls": {
    "cipher": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
    "version": "1.0",
    "version_protocol": "tls"
  }
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

### Email messages vs. protocols

The fields proposed in this document are focused on the contents of an email message but not on specific fields for email protocols. Do protocols like SMTP, POP3, IMAP, etc. be represented in ECS?

### Email metrics and observability use caes

Does the initial set of `email` fields need to consider observability and email monitoring use cases, for example spam, metrics, deliverables, and logging.

### Additional event categorization values

Should a new event.category field (email) be created, and, if so, which `event.type` values the `email` category should be combined with.

### Display names

Should the display name be captured separately from the email address for senders and recipients. If so, how do we accomplish this in a document while keeping the 1:1 of a display name to email address.

### Attachments

Should attachments be considered in this initial proposal? If so, should the fields should mirror (or potentially nest) the `file.*` fields?

### Spam processing details

Should fields intended to capture details around spam processing like sender policy framework (SPF), domainkeys identified mail (DKIM), or domain-based message authentication, reporting, and conformance (DMARC) be in scope for this proposal as well?

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate the risk of churn and instability by resolving outstanding concerns.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | Co-author
* @P1llus | Co-author, subject matter expert
* @jamiehynds | Co-sponsor
* @devonakerr | Co-sponsor


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
