---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-allowed-values-event-category.html
applies_to:
  stack: all
  serverless: all
navigation_title: event.category
---

# ECS categorization field: event.category [ecs-allowed-values-event-category]

This is one of four ECS Categorization Fields, and indicates the second level in the ECS category hierarchy.

`event.category` represents the "big buckets" of ECS categories. For example, filtering on `event.category:process` yields all events relating to process activity. This field is closely related to `event.type`, which is used as a subcategory.

This field is an array. This will allow proper categorization of some events that fall in multiple categories.

**Allowed values**

* [api](#ecs-event-category-api)
* [authentication](#ecs-event-category-authentication)
* [configuration](#ecs-event-category-configuration)
* [database](#ecs-event-category-database)
* [driver](#ecs-event-category-driver)
* [email](#ecs-event-category-email)
* [file](#ecs-event-category-file)
* [host](#ecs-event-category-host)
* [iam](#ecs-event-category-iam)
* [intrusion_detection](#ecs-event-category-intrusion_detection)
* [library](#ecs-event-category-library)
* [malware](#ecs-event-category-malware)
* [network](#ecs-event-category-network)
* [package](#ecs-event-category-package)
* [process](#ecs-event-category-process)
* [registry](#ecs-event-category-registry)
* [session](#ecs-event-category-session)
* [threat](#ecs-event-category-threat)
* [vulnerability](#ecs-event-category-vulnerability)
* [web](#ecs-event-category-web)


## api [ecs-event-category-api]

Events in this category annotate API calls that occured on a system. Typical sources for those events could be from the Operating System level through the native libraries (for example Windows Win32, Linux libc, etc.), or managed sources of events (such as ETW, syslog), but can also include network protocols (such as SOAP, RPC, Websocket, REST, etc.)

**Expected event types for category api:**

access, admin, allowed, change, creation, deletion, denied, end, info, start, user


## authentication [ecs-event-category-authentication]

Events in this category are related to the challenge and response process in which credentials are supplied and verified to allow the creation of a session. Common sources for these logs are Windows event logs and ssh logs. Visualize and analyze events in this category to look for failed logins, and other authentication-related activity.

**Expected event types for category authentication:**

start, end, info


## configuration [ecs-event-category-configuration]

Events in the configuration category have to deal with creating, modifying, or deleting the settings or parameters of an application, process, or system.

Example sources include security policy change logs, configuration auditing logging, and system integrity monitoring.

**Expected event types for category configuration:**

access, change, creation, deletion, info


## database [ecs-event-category-database]

The database category denotes events and metrics relating to a data storage and retrieval system. Note that use of this category is not limited to relational database systems. Examples include event logs from MS SQL, MySQL, Elasticsearch, MongoDB, etc. Use this category to visualize and analyze database activity such as accesses and changes.

**Expected event types for category database:**

access, change, info, error


## driver [ecs-event-category-driver]

Events in the driver category have to do with operating system device drivers and similar software entities such as Windows drivers, kernel extensions, kernel modules, etc.

Use events and metrics in this category to visualize and analyze driver-related activity and status on hosts.

**Expected event types for category driver:**

change, end, info, start


## email [ecs-event-category-email]

This category is used for events relating to email messages, email attachments, and email network or protocol activity.

Emails events can be produced by email security gateways, mail transfer agents, email cloud service providers, or mail server monitoring applications.

**Expected event types for category email:**

info


## file [ecs-event-category-file]

Relating to a set of information that has been created on, or has existed on a filesystem. Use this category of events to visualize and analyze the creation, access, and deletions of files. Events in this category can come from both host-based and network-based sources. An example source of a network-based detection of a file transfer would be the Zeek file.log.

**Expected event types for category file:**

access, change, creation, deletion, info


## host [ecs-event-category-host]

Use this category to visualize and analyze information such as host inventory or host lifecycle events.

Most of the events in this category can usually be observed from the outside, such as from a hypervisor or a control plane’s point of view. Some can also be seen from within, such as "start" or "end".

Note that this category is for information about hosts themselves; it is not meant to capture activity "happening on a host".

**Expected event types for category host:**

access, change, end, info, start


## iam [ecs-event-category-iam]

Identity and access management (IAM) events relating to users, groups, and administration. Use this category to visualize and analyze IAM-related logs and data from active directory, LDAP, Okta, Duo, and other IAM systems.

**Expected event types for category iam:**

admin, change, creation, deletion, group, info, user


## intrusion_detection [ecs-event-category-intrusion_detection]

Relating to intrusion detections from IDS/IPS systems and functions, both network and host-based. Use this category to visualize and analyze intrusion detection alerts from systems such as Snort, Suricata, and Palo Alto threat detections.

**Expected event types for category intrusion_detection:**

allowed, denied, info


## library [ecs-event-category-library]

Events in this category refer to the loading of a library, such as (dll / so / dynlib), into a process. Use this category to visualize and analyze library loading related activity on hosts.  Keep in mind that driver related activity will be captured under the "driver" category above.

**Expected event types for category library:**

start


## malware [ecs-event-category-malware]

Malware detection events and alerts. Use this category to visualize and analyze malware detections from EDR/EPP systems such as Elastic Endpoint Security, Symantec Endpoint Protection, Crowdstrike, and network IDS/IPS systems such as Suricata, or other sources of malware-related events such as Palo Alto Networks threat logs and Wildfire logs.

**Expected event types for category malware:**

info


## network [ecs-event-category-network]

Relating to all network activity, including network connection lifecycle, network traffic, and essentially any event that includes an IP address. Many events containing decoded network protocol transactions fit into this category. Use events in this category to visualize or analyze counts of network ports, protocols, addresses, geolocation information, etc.

**Expected event types for category network:**

access, allowed, connection, denied, end, info, protocol, start


## package [ecs-event-category-package]

Relating to software packages installed on hosts. Use this category to visualize and analyze inventory of software installed on various hosts, or to determine host vulnerability in the absence of vulnerability scan data.

**Expected event types for category package:**

access, change, deletion, info, installation, start


## process [ecs-event-category-process]

Use this category of events to visualize and analyze process-specific information such as lifecycle events or process ancestry.

**Expected event types for category process:**

access, change, end, info, start


## registry [ecs-event-category-registry]

Having to do with settings and assets stored in the Windows registry. Use this category to visualize and analyze activity such as registry access and modifications.

**Expected event types for category registry:**

access, change, creation, deletion


## session [ecs-event-category-session]

The session category is applied to events and metrics regarding logical persistent connections to hosts and services. Use this category to visualize and analyze interactive or automated persistent connections between assets. Data for this category may come from Windows Event logs, SSH logs, or stateless sessions such as HTTP cookie-based sessions, etc.

**Expected event types for category session:**

start, end, info


## threat [ecs-event-category-threat]

Use this category to visualize and analyze events describing threat actors' targets, motives, or behaviors.

**Expected event types for category threat:**

indicator


## vulnerability [ecs-event-category-vulnerability]

Relating to vulnerability scan results. Use this category to analyze vulnerabilities detected by Tenable, Qualys, internal scanners, and other vulnerability management sources.

**Expected event types for category vulnerability:**

info


## web [ecs-event-category-web]

Relating to web server access. Use this category to create a dashboard of web server/proxy activity from apache, IIS, nginx web servers, etc. Note: events from network observers such as Zeek http log may also be included in this category.

**Expected event types for category web:**

access, error, info

