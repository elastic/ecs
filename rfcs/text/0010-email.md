# 0010: Email

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2022-02-23** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC proposes a new top-level field set to facilitate email use cases, `email.*`. The `email.*` field set adds fields for the sender, recipient, message header fields, and other attributes of an email message typically seen logs produced by mail transfer agent (MTA) and email gateway applications.

## Fields

### Email specific fields

| field | type | description |
| --- | --- | --- |
| `email.origination_timestamp` | date | The date and time the email message was composed. Many email clients will fill this in automatically when the message is sent by a user. |
| `email.delivery_timestamp` | date | The date and time the email message was received by the service or client. |
| `email.from.address` | keyword (array) | Stores the `from` email address from the RFC5322 `From:` header field. |
| `email.sender.address` | keyword | When the `from` field contains more than one address or the `sender` and `from` are distinct then this field is populated. |
| `email.to.address` | keyword (array)| The email address of message recipient |
| `email.cc.address` | keyword (array) | The email address of a carbon copy (CC) recipient |
| `email.bcc.address` | keyword (array) | The email address of the blind carbon copy (CC) recipient(s) |
| `email.reply_to.address` | keyword (array) | The address that replies should be delivered to from the RFC 5322 `Reply-To:` header field. |
| `email.subject` | keyword (`.text` text multi-field) | A brief summary of the topic of the message |
| `email.content_type` | keyword | Information about how the message is to be displayed. Typically a MIME type |
| `email.message_id` | wildcard |  Identifier from the RFC5322 `Message-ID:` header field that refers to a particular version of a particular message. |
| `email.local_id` | keyword | Unique identifier given to the email by the source (MTA, gateway, etc.) that created the event and is not persistent across hops (for example, the `X-MS-Exchange-Organization-Network-Message-Id` id). |
| `email.direction` | keyword | Direction of the message based on the sending and receiving domains |
| `email.x_mailer` | keyword | What application was used to draft and send the original email. |
| `email.attachments` | nested | Nested object of attachments on the email. |
| `email.attachments.file.mime_type` | keyword | MIME type of the attachment file. |
| `email.attachments.file.name` | keyword | Name of the attachment file including the extension. |
| `email.attachments.file.extension` | keyword | Attachment file extension, excluding the leading dot. |
| `email.attachments.file.size` | long | Attachment file size in bytes. |
| `email.attachments.file.hash.*` | reuse of `hash.*` field set | Field reuse of `hash.*` for file attachments. |

### Additional event categorization allowed values

Email events may benefit from an additional ECS allowed event categorization value: `event.category: email`.

## Usage

Email use cases stretch across all three Elastic solutions - Search, Observe, Protect. Whether it's searching for content within email, ensuring email infrastructure is operational, or detecting email-based attacks, there are many possibilities for email fields within ECS.

## Source data

- **Email Analytics**: [Hubspot](https://legacydocs.hubspot.com/docs/methods/email/email_events_overview), Marketo, Salesforce Pardot
- **Email Server**: [O365 Message Tracing](https://docs.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/run-a-message-trace-and-view-results), [Postfix](https://nxlog.co/documentation/nxlog-user-guide/postfix.html)
- **Email Security**: [Barracuda](https://campus.barracuda.com/product/emailsecuritygateway/doc/12193950/syslog-and-the-barracuda-email-security-gateway/), [Forcepoint](https://www.websense.com/content/support/library/email/v85/email_siem/siem_log_map.pdf), [Mimecast](https://www.mimecast.com/tech-connect/documentation/tutorials/understanding-siem-logs/), [Proofpoint](https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API)

### Office365 - Successful Delivery

#### Original log

```json
{
  "EndDate": "2021-11-10T22:12:34.8196921Z",
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
    "from": {
  	  "address": [
        "o365mc@microsoft.com"
      ]
    },
    "to": {
      "address": [
        "john@testdomain.onmicrosoft.com"
      ]
    },
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
        "from": {
          "address": [
            "postmaster@testdomain.onmicrosoft.com"
          ]
        },
        "to": {
          "address": [
            "o365mc@microsoft.com"
          ]
        },
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
<38>1 2021-06-24T21:00:08Z - ProofpointTAP - MSGBLK [tapmsg@21139 messageTime="2021-06-24T21:18:38.000Z" messageID="20160624211145.62086.mail@evil.zz" recipient="clark.kent@pharmtech.zz, diana.prince@pharmtech.zz" sender="e99d7ed5580193f36a51f597bc2c0210@evil.zz" senderIP="192.0.2.255" phishScore="46" spamScore="4" QID="r2FNwRHF004109" GUID="c26dbea0-80d5-463b-b93c-4e8b708219ce" subject="Please find a totally safe invoice attached." quarantineRule="module.sandbox.threat" quarantineFolder="Attachment Defense" policyRoutes="default_inbound,executives" modulesRun="sandbox,urldefense,spam,pdr" headerFrom="\"A. Badguy\" <badguy@evil.zz>" headerTo="\"Clark Kent\" <clark.kent@pharmtech.zz>; \"Diana Prince\" <diana.prince@pharmtech.zz>" headerCC="\"Bruce Wayne\" <bruce.wayne@university-of-education.zz>" headerReplyTo="null" toAddresses="clark.kent@pharmtech.zz,diana.prince@pharmtech.zz" ccAddresses="bruce.wayne@university-of-education.zz" fromAddress="badguy@evil.zz" replyToAddress="null" clusterId="pharmtech_hosted" messageParts="[{\"contentType\":\"text/plain\",\"disposition\":\"inline\",\"filename\":\"text.txt\",\"md5\":\"008c5926ca861023c1d2a36653fd88e2\",\"oContentType\":\"text/plain\",\"sandboxStatus\":\"unsupported\",\"sha256\":\"85738f8f9a7f1b04b5329c590ebcb9e425925c6d0984089c43a022de4f19c281\"},{\"contentType\":\"application/pdf\",\"disposition\":\"attached\",\"filename\":\"Invoice for Pharmtech.pdf\",\"md5\":\"5873c7d37608e0d49bcaa6f32b6c731f\",\"oContentType\":\"application/pdf\",\"sandboxStatus\":\"threat\",\"sha256\":\"2fab740f143fc1aa4c1cd0146d334c5593b1428f6d062b2c406e5efe8abe95ca\"}]" xmailer="Spambot v2.5"]
```

#### Mapped event

```json
{
  "@timestamp": "2021-06-24T21:00:08Z",
  "email": {
    "timestamp": "2021-06-24T21:18:38.000Z",
    "message_id": "20210624211145.62086.mail@evil.zz",
    "local_id": "c26dbea0-80d5-463b-b93c-4e8b708219ce",
    "to": {
      "address": [
        "clark.kent@pharmtech.zz",
        "diana.prince@pharmtech.zz"
      ]
    },
    "cc": {
      "address": [
        "bruce.wayne@university-of-education.zz"
      ]
    },
    "from": {
      "address": [
        "badguy@evil.zz"
      ]
    },
    "sender": {
      "address": "e99d7ed5580193f36a51f597bc2c0210@evil.zz"
    },
    "subject": "Please find a totally safe invoice attached.",
    "reply_to": {
      "address": "null"
    },
    "x_mailer": "Spambot v2.5",
    "attachments": [
      {
        "file": {
          "mime_type": "application/pdf",
          "name": "Invoice for Pharmtech.pdf",
          "extension": "pdf",
          "hash": {
            "md5": "5873c7d37608e0d49bcaa6f32b6c731f",
            "sha256": "2fab740f143fc1aa4c1cd0146d334c5593b1428f6d062b2c406e5efe8abe95ca"
          }
        }
      }
    ]
  },
  "event": {
    "id": "c26dbea0-80d5-463b-b93c-4e8b708219ce",
    "kind": "event",
    "category": "email",
    "action": "MSGBLK"
  },
  "source": {
    "address": "192.0.2.255",
    "ip": "192.0.2.255"
  }
}
```

### Mimecast Receipt log

#### Original log

```
datetime=2021-05-26T16:47:41+0100|aCode=7O7I7MvGP1mj8plHRDuHEA|acc=C0A0|SpamLimit=0|IP=123.123.123.123|Dir=Internal|MsgId=<81ce15$8r2j59@mail01.example.com>|Subject=\message subject\|headerFrom=from@mimecast.com|Sender=from@mimecast.com|Rcpt=auser@mimecast.com|SpamInfo=[]|Act=Acc|TlsVer=TLSv1|Cphr=TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA|SpamProcessingDetail={"spf":{"info":"SPF_FAIL","allow":true},"dkim":{"info":"DKIM_UNKNOWN","allow":true}}|SpamScore=1
```

#### Mapped event

```json
{
  "@timestamp": "2021-05-26T16:47:41+0100",
  "source": {
    "address": "123.123.123.123",
    "ip": "123.123.123.123"
  },
  "email": {
    "message_id": "<81ce15$8r2j59@mail01.example.com>",
    "from": {
      "address": [
        "from@mimecast.com"
      ]
    },
    "to": {
      "address": [
        "auser@mimecast.com"
      ]
    },
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

## Scope of impact

This is a new field set, and the changes introduced will not affect existing ECS implementations.

Integrations or other data sources mapping to ECS will need to map their original events to the new fields.

## Concerns

### Email messages vs. protocols

The fields proposed in this document focus on an email message's content but not on specific fields for email protocols. However, should protocols like SMTP, POP3, IMAP, etc., be represented in ECS?

For example, users may need to compare the email address from the SMTP (envelope) sender to the `From:` header email address.

**Resolution**: Focus on email message content in this initial phase. Additional protocol details can be added later on.

### Email metrics and observability use cases

Does the initial set of `email` fields need to consider observability and email monitoring use cases, for example, spam, metrics, deliverables, and logging?

**Resolution**: This initial field set focuses on email message content.

### Additional event categorization values

Should a new event.category field (email) be created, and, if so, which `event.type` values should be used for the `email` category?

**Resolution**: Propose to add `event.category: email` and make `info` an expected event type for the category.

### Display names

Should the display name be captured separately from the email address for senders and recipients? If so, how do we accomplish this in a document while keeping the 1:1 of a display name to email address?

**Resolution**: Initially, this proposal considered using `nested` types to allows arrays of objects containing both the email address and display name for the `to`, `cc`, and `bcc` recipients. However, after more consideration of the limitations to using `nested` fields types and limited support for `nested` fields in Kibana, that decision was reversed.

### Spam processing details

Should fields intended to capture details around spam processing like sender policy framework (SPF), domainkeys identified mail (DKIM), or domain-based message authentication, reporting, and conformance (DMARC) be in scope for this proposal as well?

**Resolution**: This initial field set focuses on email message content.

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | Co-author
* @P1llus | Co-author, subject matter expert
* @jamiehynds | Co-sponsor
* @devonakerr | Co-sponsor


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
* Stage 2 (candidate): https://github.com/elastic/ecs/pull/1593
* Stage 3 (finished): https://github.com/elastic/ecs/pull/YYYY
