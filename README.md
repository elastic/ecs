**WARNING: THIS IS WORK IN PROGRESS**

# Elastic Common Schema (ECS)

The Elastic Common Schema (ECS) for ingesting data into Elasticsearch helps you correlate data from sources like logs and metrics or IT operations analytics and security analytics. 

ECS is still under development and backward compatibility is not guaranteed. Any
feedback on the general structure, missing fields, or existing fields is appreciated.
For contributions please read the [Contributing Guide](CONTRIBUTING.md).

<a name="ecs-version"></a>The current version of ECS is `0.1.0`.

## In this readme

* [Fields](#fields)
  * [Base fields](#base)
  * [Cloud fields](#cloud)
  * [Container fields](#container)
  * [Destination fields](#destination)
  * [Device fields](#device)
  * [Error fields](#error)
  * [Event fields](#event)
  * [File fields](#file)
  * [Geoip fields](#geoip)
  * [Host fields](#host)
  * [Kubernetes fields](#kubernetes)
  * [Log fields](#log)
  * [Network fields](#network)
  * [Organization fields](#organization)
  * [Process fields](#process)
  * [Service fields](#service)
  * [Source fields](#source)
  * [URL fields](#url)
  * [User fields](#user)
  * [User agent fields](#user_agent)
* [Use cases](#use-cases)
* [Implementing ECS](#implementing-ecs)
* [FAQ](#faq-ecs)


## <a name="fields"></a>Fields

[Base fields](#base) 
| [Agent fields](#agent) 
| [Cloud fields](#cloud)
| [Container fields](#container) 
| [Destination fields](#destination) 
| [Device fields](#device)
| [Error fields](#error)
| [Event fields](#event)
| [File fields](#file)
| [Geoip fields](#geoip)
| [Host fields](#host)
| [Kubernetes fields](#kubernetes)
| [Log fields](#log)
| [Network fields](#network)
| [Organization fields](#organization)
| [Process fields](#process)
| [Service fields](#service)
| [Source fields](#source)
| [URL fields](#url)
| [User fields](#user)
| [User agent fields](#user_agent)

### <a name="base"></a> Base fields

The base set contains all fields at the top level. These are fields which are common across all types of events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="@timestamp"></a>`@timestamp`  | Date/time when the event originated.<br/>For log events this should be the date when the event was generated, and not when it was read.<br/>Required field for all events.  | date  |   | `2016-05-23T08:05:34.853Z`  |
| <a name="tags"></a>`tags`  | List of keywords used to tag each event.  | keyword  |   | `["production", "env2"]`  |
| <a name="labels"></a>`labels`  | Key/value pairs.<br/>Can be used to add meta information to events. Should not contain nested objects. All values are stored as keyword.<br/>Example: `docker` and `k8s` labels.  | object  |   | `{key1: value1, key2: value2}`  |
| <a name="message"></a>`message`  | For log events the message field contains the log message.<br/>In other use cases the message field can be used to concatenate different values which are then freely searchable. If multiple messages exist they can be combined into one message.  | text  |   | `Hello World`  |


### <a name="agent"></a> Agent fields

The agent fields contain data about the agent/client/shipper that created the event.

| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="agent.version"></a>`agent.version`  | Version of the agent.  | keyword  |   | `6.0.0-rc2`  |
| <a name="agent.name"></a>`agent.name`  | Name of the agent.  | keyword  |   | `filebeat`  |
| <a name="agent.id"></a>`agent.id`  | Unique identifier for the agent (if one exists).<br/>Example: For Beats this would be beat.id.  | keyword  |   | `8a4f500d`  |
| <a name="agent.ephemeral_id"></a>`agent.ephemeral_id`  | Ephemeral identifier of this agent (if one exists).<br/>This id normally changes across restarts, but `agent.id` does not.  | keyword  |   | `8a4f500f`  |

Examples: In the case of Beats for logs, the `agent.name` is `filebeat`. For APM, it is the agent running in the app/service. The agent information does not change if data is sent through queuing systems like Kafka, Redis, or processing systems like Logstash or APM Server.

### <a name="cloud"></a> Cloud fields

All fields related to the cloud or infrastructure the events are coming from.

| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="cloud.provider"></a>`cloud.provider`  | Name of the cloud provider. Example values are ec2, gce, or digitalocean.  | keyword  |   | `ec2`  |
| <a name="cloud.availability_zone"></a>`cloud.availability_zone`  | Availability zone in which this host is running.  | keyword  |   | `us-east-1c`  |
| <a name="cloud.region"></a>`cloud.region`  | Region in which this host is running.  | keyword  |   | `us-east-1`  |
| <a name="cloud.instance.id"></a>`cloud.instance.id`  | Instance ID of the host machine.  | keyword  |   | `i-1234567890abcdef0`  |
| <a name="cloud.instance.name"></a>`cloud.instance.name`  | Instance name of the host machine.  | keyword  |   |   |
| <a name="cloud.machine.type"></a>`cloud.machine.type`  | Machine type of the host machine.  | keyword  |   | `t2.medium`  |

Examples: If Metricbeat is running on an EC2 host and fetches data from its host, the cloud fields are expected to contain data about the host machine. If Metricbeat is running on a remote machine outside of the cloud and fetches data from a service running in the cloud, cloud fields are expected to reflect the data from the cloud machine which is running the service.

### <a name="container"></a> Container fields

Container fields are used for meta information about the specific container that is the source of information. These fields should help to correlate data based containers from any runtime.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="container.runtime"></a>`container.runtime`  | Runtime managing this container.  | keyword  |   | `docker`  |
| <a name="container.id"></a>`container.id`  | Unique container id.  | keyword  |   |   |
| <a name="container.image.name"></a>`container.image.name`  | Name of the image the container was built on.  | keyword  |   |   |
| <a name="container.image.tag"></a>`container.image.tag`  | Container image tag.  | keyword  |   |   |
| <a name="container.name"></a>`container.name`  | Container name.  | keyword  |   |   |
| <a name="container.labels"></a>`container.labels`  | Image labels.  | object  |   |   |


### <a name="destination"></a> Destination fields

These fields describe details about the destination of a packet/event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="destination.ip"></a>`destination.ip`  | IP address of the destination.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="destination.hostname"></a>`destination.hostname`  | Hostname of the destination.  | keyword  |   |   |
| <a name="destination.port"></a>`destination.port`  | Port of the destination.  | long  |   |   |
| <a name="destination.mac"></a>`destination.mac`  | MAC address of the destination.  | keyword  |   |   |
| <a name="destination.domain"></a>`destination.domain`  | Destination domain.  | keyword  |   |   |
| <a name="destination.subdomain"></a>`destination.subdomain`  | Destination subdomain.  | keyword  |   |   |


### <a name="device"></a> Device fields

These fields are used to provide additional information about the device that is the source of the information. This could be a firewall, network device, etc.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="device.mac"></a>`device.mac`  | MAC address of the device  | keyword  |   |   |
| <a name="device.ip"></a>`device.ip`  | IP address of the device.  | ip  |   |   |
| <a name="device.hostname"></a>`device.hostname`  | Hostname of the device.  | keyword  |   |   |
| <a name="device.vendor"></a>`device.vendor`  | Vendor information for the device.  | text  |   |   |
| <a name="device.version"></a>`device.version`  | Version of the device.  | keyword  |   |   |
| <a name="device.serial_number"></a>`device.serial_number`  | Serial number of the device.  | keyword  |   |   |
| <a name="device.timezone.offset.sec"></a>`device.timezone.offset.sec`  | Timezone offset of the host in seconds.<br/>Number of seconds relative to UTC.<br/> Example: If the offset is -01:30, the value will be -5400.  | long  |   | `-5400`  |
| <a name="device.type"></a>`device.type`  | The type of the device that the data is coming from.<br/>There is no predefined list of device types. <br/>Examples: `endpoint`, `firewall`, `ids`, `ips`, `proxy`.  | keyword  |   | `firewall`  |


### <a name="error"></a> Error fields

The `error` fields can represent errors of any kind. Use them for errors that happen while fetching events or if the event itself contains an error.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="error.id"></a>`error.id`  | Unique identifier for the error.  | keyword  |   |   |
| <a name="error.message"></a>`error.message`  | Error message.  | text  |   |   |
| <a name="error.code"></a>`error.code`  | Error code describing the error.  | keyword  |   |   |


### <a name="event"></a> Event fields

The event fields provide context information about the data itself.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="event.id"></a>`event.id`  | Unique ID to describe the event.  | keyword  |   | `8a4f500d`  |
| <a name="event.category"></a>`event.category`  | Event category.<br/> Define categories that are meaningful to you and your environment.  | keyword  |   | `metrics`  |
| <a name="event.type"></a>`event.type`  | A type given to this kind of event which can be used for grouping.<br/>Define event types that are meaningful to you and your environment.  | keyword  |   | `nginx-stats-metrics`  |
| <a name="event.module"></a>`event.module`  | Name of the module that is the source of the data. Can be used with Beats and Logstash modules, among others. | keyword  |   | `mysql`  |
| <a name="event.dataset"></a>`event.dataset`  | Name of the dataset.<br/>Beats uses the concept of a `dataset` (fileset/metricset) as a subset of modules. It contains the information which is currently stored in metricset.name and metricset.module or fileset.name.  | keyword  |   | `stats`  |
| <a name="event.severity"></a>`event.severity`  | Severity of the event. Severity values can very different across use cases. The implementer should make sure that severities are consistent across events.  | long  |   | `7`  |
| <a name="event.raw"></a>`event.raw`  | Raw text message of entire event. Used to demonstrate log integrity.  | keyword  |   | `Sep 19 08:26:10 host CEF:0&#124;Security&#124; threatmanager&#124;1.0&#124;100&#124; worm successfully stopped&#124;10&#124;src=10.0.0.1 dst=2.1.2.2spt=1232`  |
| <a name="event.hash"></a>`event.hash`  | Hash (perhaps logstash fingerprint) of raw field to be able to demonstrate log integrity.  | keyword  |   | `123456789012345678901234567890ABCD`  |
| <a name="event.version"></a>`event.version`  | The ECS version that an event adheres to.<br/>Required field for all events. <br/> [Current version](#ecs-version) | keyword  |   | `0.1.0`  |
| <a name="event.duration"></a>`event.duration`  | Duration of the event in nanoseconds.  | long  |   |   |
| <a name="event.created"></a>`event.created`  | Date/time the event was created.<br/>This field is distinct from @timestamp, even though the values may be the same in some cases.<br/>Examples: For logs, `@timestamp` contains the timestamp carried in the log line, and `event.created` contains the time when the log line is read. For package captures, `@timestamp` contains the timestamp extracted from the network package, and `event.created` contains the time the event was created. </br>If the two timestamps are identical, use [@timestamp](#timestamp). | date  |   |   |
| <a name="event.risk_score"></a>`event.risk_score`  | Risk score value of the event.  | float  |   |   |


### <a name="file"></a> File fields

File fields provide details about each file.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="file.path"></a>`file.path`  | Path to the file.  | text  |   |   |
| <a name="file.path.raw"></a>`file.path.raw`  | Path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.target_path"></a>`file.target_path`  | Target path for symlinks.  | text  |   |   |
| <a name="file.target_path.raw"></a>`file.target_path.raw`  | Path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.extension"></a>`file.extension`  | File extension.<br/>Enables easy filtering by file extensions.  | keyword  |   | `png`  |
| <a name="file.type"></a>`file.type`  | File type (file, dir, or symlink).  | keyword  |   |   |
| <a name="file.device"></a>`file.device`  | Device that is the source of the file.  | keyword  |   |   |
| <a name="file.inode"></a>`file.inode`  | Inode representing the file in the filesystem.  | keyword  |   |   |
| <a name="file.uid"></a>`file.uid`  | User ID (UID) or security identifier (SID) of the file owner.  | keyword  |   |   |
| <a name="file.owner"></a>`file.owner`  | File owner's username.  | keyword  |   |   |
| <a name="file.gid"></a>`file.gid`  | Primary group ID (GID) of the file.  | keyword  |   |   |
| <a name="file.group"></a>`file.group`  | Primary group name of the file.  | keyword  |   |   |
| <a name="file.mode"></a>`file.mode`  | Mode of the file in octal representation.  | keyword  |   | `416`  |
| <a name="file.size"></a>`file.size`  | File size in bytes (field is only added when `type` is `file`).  | long  |   |   |
| <a name="file.mtime"></a>`file.mtime`  | Last time file content was modified.  | date  |   |   |
| <a name="file.ctime"></a>`file.ctime`  | Last time file metadata changed.  | date  |   |   |


### <a name="geoip"></a> Geoip fields

Geoip fields carry geographical information for an ip address. The Elasticsearch `geoip` plugin can do the conversion to geoip.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="geoip.continent_name"></a>`geoip.continent_name`  | Name of the continent.  | keyword  |   |   |
| <a name="geoip.country_iso_code"></a>`geoip.country_iso_code`  | Country ISO code.  | keyword  |   |   |
| <a name="geoip.location"></a>`geoip.location`  | Longitude and latitude.  | geo_point  |   |   |
| <a name="geoip.region_name"></a>`geoip.region_name`  | Region name.  | keyword  |   |   |
| <a name="geoip.city_name"></a>`geoip.city_name`  | City name.  | keyword  |   |   |


### <a name="host"></a> Host fields

Host fields provide information about the host. A host can be a physical machine, a virtual machine, or a Docker container. Normally host fields are related to the machine that generated/collected the event, but they can be used differently if needed.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="host.timezone.offset.sec"></a>`host.timezone.offset.sec`  | Timezone offset of the host in seconds.<br/>Number of seconds relative to UTC. Example: If the offset is -01:30, the value will be -5400.  | long  |   | `-5400`  |
| <a name="host.name"></a>`host.name`  | Identifier of the host.<br/>It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use.  | keyword  |   |   |
| <a name="host.id"></a>`host.id`  | Unique host id.<br/>As hostname is not always unique, use values that are meaningful in your environment. <br/>Example: The current usage of `beat.name`.  | keyword  |   |   |
| <a name="host.ip"></a>`host.ip`  | Host ip address.  | ip  |   |   |
| <a name="host.mac"></a>`host.mac`  | Host mac address.  | keyword  |   |   |
| <a name="host.type"></a>`host.type`  | Type of host.<br/>For Cloud providers this can be the machine type, such as `t2.medium`. If vm, this could be the container, for example, or other information meaningful to you.  | keyword  |   |   |
| <a name="host.os.platform"></a>`host.os.platform`  | Operating system platform (centos, ubuntu, windows, etc.).  | keyword  |   | `darwin`  |
| <a name="host.os.name"></a>`host.os.name`  | Operating system name.  | keyword  |   | `Mac OS X`  |
| <a name="host.os.family"></a>`host.os.family`  | OS family (redhat, debian, freebsd, windows, etc.).  | keyword  |   | `debian`  |
| <a name="host.os.version"></a>`host.os.version`  | Operating system version.  | keyword  |   | `10.12.6`  |
| <a name="host.architecture"></a>`host.architecture`  | Operating system architecture.  | keyword  |   | `x86_64`  |


### <a name="kubernetes"></a> Kubernetes fields

Kubernetes fields are used for Kubernetes meta information. This information helps correlate data coming out of Kubernetes setups.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="kubernetes.pod.name"></a>`kubernetes.pod.name`  | Kubernetes pod name  | keyword  |   |   |
| <a name="kubernetes.namespace"></a>`kubernetes.namespace`  | Kubernetes namespace  | keyword  |   |   |
| <a name="kubernetes.labels"></a>`kubernetes.labels`  | Kubernetes labels map  | object  |   |   |
| <a name="kubernetes.annotations"></a>`kubernetes.annotations`  | Kubernetes annotations map  | object  |   |   |
| <a name="kubernetes.container.name"></a>`kubernetes.container.name`  | Kubernetes container name. This name is unique within the pod only. </br>This field is different from the underlying [container.name](#container.name) field.  | keyword  |   |   |


### <a name="log"></a> Log fields

Fields which are specific to log events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="log.level"></a>`log.level`  | Log level of the log event.<br/>Some examples are `WARN`, `ERR`, `INFO`.  | keyword  |   | `ERR`  |
| <a name="log.line"></a>`log.line`  | Line number the log event was collected from.  | long  |   | `18`  |
| <a name="log.offset"></a>`log.offset`  | Offset of the beginning of the log event.  | long  |   | `12`  |


### <a name="network"></a> Network fields

All fields related to network data.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="network.protocol"></a>`network.protocol`  | Network protocol name.  | keyword  |   | `http`  |
| <a name="network.direction"></a>`network.direction`  | Direction of the network traffic.<br/>Recommended values are:<br/>  - inbound  <br/>  - outbound<br/>  - unknown  | keyword  |   | `inbound`  |
| <a name="network.forwarded_ip"></a>`network.forwarded_ip`  | Host IP address when the source IP address is the proxy.  | ip  |   | `192.1.1.2`  |
| <a name="network.inbound.bytes"></a>`network.inbound.bytes`  | Network inbound bytes.  | long  |   | `184`  |
| <a name="network.inbound.packets"></a>`network.inbound.packets`  | Network inbound packets.  | long  |   | `12`  |
| <a name="network.outbound.bytes"></a>`network.outbound.bytes`  | Network outbound bytes.  | long  |   | `184`  |
| <a name="network.outbound.packets"></a>`network.outbound.packets`  | Network outbound packets.  | long  |   | `12`  |


### <a name="organization"></a> Organization fields

The organization fields enrich data with information about the company or entity.
These fields are useful if data stored in an index should be arranged or filtered by organization.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="organization.name"></a>`organization.name`  | Organization, company, or entity name.  | text  |   |   |
| <a name="organization.id"></a>`organization.id`  | Unique identifier for the organization.  | keyword  |   |   |


### <a name="process"></a> Process fields

These fields contain information about a process.
These fields can help you correlate metrics information with a process id/name from a log message.  The `process.pid` often stays in the metric itself and is  copied to the global field for correlation.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="process.args"></a>`process.args`  | Process arguments.<br/>May be filtered to protect sensitive information.  | keyword  |   | `['-l', 'user', '10.0.0.16']`  |
| <a name="process.name"></a>`process.name`  | Process name.<br/>Sometimes known as program name or something similar.  | keyword  |   | `ssh`  |
| <a name="process.pid"></a>`process.pid`  | Process id.  | long  |   |   |
| <a name="process.ppid"></a>`process.ppid`  | Process parent id.  | long  |   |   |
| <a name="process.title"></a>`process.title`  | Process title.<br/>Proctitle, often the same as process name.  | keyword  |   |   |


### <a name="service"></a> Service fields

The service fields describe the service for or from which the data was collected. Use these fields help find and correlate logs for a specific service or version.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="service.id"></a>`service.id`  | Unique identifier of the service that is running.<br/>The id must uniquely identify this service. This makes it possible to correlate logs and metrics for one specific service.</br> Example: If one Redis instance is experiencing problems, you can filter on the id to see metrics and logs for that single instance.  | keyword  |   | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6`  |
| <a name="service.name"></a>`service.name`  | Name of the service data is collected from.<br/>The name can be used to group logs and metrics together from one service and correlate them. </br> Example: If you collect logs or metrics from Redis, `service.name` would be `redis`.   | keyword  |   | `elasticsearch`  |
| <a name="service.type"></a>`service.type`  | Service type.  | keyword  |   |   |
| <a name="service.state"></a>`service.state`  | Current state of the service.  | keyword  |   |   |
| <a name="service.version"></a>`service.version`  | Version of the service the data was collected from.<br/>This allows you to look at a data set for a specific version of a service.  | keyword  |   | `3.2.4`  |
| <a name="service.ephemeral_id"></a>`service.ephemeral_id`  | Ephemeral identifier of this service (if one exists).<br/>This id normally changes across restarts, but `service.id` does not.  | keyword  |   | `8a4f500f`  |


### <a name="source"></a> Source fields

Source fields provide details about the source of the event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="source.ip"></a>`source.ip`  | IP address of the source.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="source.hostname"></a>`source.hostname`  | Hostname of the source.  | keyword  |   |   |
| <a name="source.port"></a>`source.port`  | Port of the source.  | long  |   |   |
| <a name="source.mac"></a>`source.mac`  | MAC address of the source.  | keyword  |   |   |
| <a name="source.domain"></a>`source.domain`  | Source domain.  | keyword  |   |   |
| <a name="source.subdomain"></a>`source.subdomain`  | Source subdomain.  | keyword  |   |   |


### <a name="url"></a> URL fields

URL fields provide a complete URL, with scheme, host, and path.
The URL object can be reused in other prefixes like `host.url.*` for example. Be sure to keep the structure consistent whenever you use URL fields.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="url.href"></a>`url.href`  | Full url. The field is stored as keyword.<br/>`href` is an analyzed field so the parsed information can be accessed through `href.analyzed` in queries. </br>  `url.href` is a [multi field](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html#_multi_fields_with_multiple_analyzers). The data is stored as keyword `url.href` and test `url.href.analyzed`. These fields enable you to run a query against part of the url without splitting up the URL at ingest time.| keyword  |   | `https://elastic.co:443/search?q=elasticsearch#top`  |
| <a name="url.href.analyzed"></a>`url.href.analyzed`  |  Partners with `url.href` to facilitate partial URL searches. (See previous entry.) | text  | 1  |   |
| <a name="url.protocol"></a>`url.protocol`  | Protocol of the request, e.g. "https:".  | keyword  |   |   |
| <a name="url.hostname"></a>`url.hostname`  | Hostname of the request, e.g. "example.com".<br/>For correlation the this field can be copied into the `host.name` field.  | keyword  |   |   |
| <a name="url.port"></a>`url.port`  | Port of the request, such as 443.  | keyword  |   |   |
| <a name="url.pathname"></a>`url.pathname`  | Path of the request, such as "/search".  | text  |   |   |
| <a name="url.pathname.raw"></a>`url.pathname.raw`  | URL path. This is a non-analyzed field used for aggregations.  | keyword  | 1  |   |
| <a name="url.search"></a>`url.search`  | The search describes the query string of the request, such as "q=elasticsearch".  | text  |   |   |
| <a name="url.search.raw"></a>`url.search.raw`  | The url search part. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.hash"></a>`url.hash`  | Hash of the request URL, such as "top".  | keyword  |   |   |
| <a name="url.username"></a>`url.username`  | Username of the request.  | keyword  |   |   |
| <a name="url.password"></a>`url.password`  | Password of the request.  | keyword  |   |   |
| <a name="url.extension"></a>`url.extension`  | URL extension field contains the extension of the file associated with the url.<br/>Examples: </br> `http://localhost/logo.png` where the extension is `png`.</br>  `http://localhost/content?asset=logo.png&token=XYZ` where the extension could also be `png`, but depends on the implementation.<br/>Leave off the `extension` field if the extension is not defined.  | keyword  |   | `png`  |

Example based on whatwg URL definition: https://github.com/whatwg/url/issues/337

### <a name="user"></a> User fields

User fields describe information about the user that is relevant to the event.
Fields can have one or multiple entries. If a user has more then one id, provide an array that includes all of them.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user.id"></a>`user.id`  | One or multiple unique identifiers of the user.  | keyword  |   |   |
| <a name="user.name"></a>`user.name`  | Name of the user.<br/>The field is a keyword, and will not be tokenized.  | keyword  |   |   |
| <a name="user.email"></a>`user.email`  | User email address.  | keyword  |   |   |
| <a name="user.hash"></a>`user.hash`  | Unique user hash to correlate information for a user in anonymized form.<br/>Useful if `user.id` or `user.name` contain confidential information and cannot be used.  | keyword  |   |   |


### <a name="user_agent"></a> User agent fields

The user_agent fields  normally come from a browser request.
They commonly appear in web service logs coming from the parsed user agent string.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user_agent.raw"></a>`user_agent.raw`  | Unparsed version of the user_agent.  | text  |   |   |
| <a name="user_agent.device"></a>`user_agent.device`  | Name of the physical device.  | keyword  |   |   |
| <a name="user_agent.version"></a>`user_agent.version`  | Version of the physical device.  | keyword  |   |   |
| <a name="user_agent.major"></a>`user_agent.major`  | Major version of the user agent.  | long  |   |   |
| <a name="user_agent.minor"></a>`user_agent.minor`  | Minor version of the user agent.  | long  |   |   |
| <a name="user_agent.patch"></a>`user_agent.patch`  | Patch version of the user agent.  | keyword  |   |   |
| <a name="user_agent.name"></a>`user_agent.name`  | Name of the user agent.  | keyword  |   | `Chrome`  |
| <a name="user_agent.os.name"></a>`user_agent.os.name`  | Name of the operating system.  | keyword  |   |   |
| <a name="user_agent.os.version"></a>`user_agent.os.version`  | Version of the operating system.  | keyword  |   |   |
| <a name="user_agent.os.major"></a>`user_agent.os.major`  | Major version of the operating system.  | long  |   |   |
| <a name="user_agent.os.minor"></a>`user_agent.os.minor`  | Minor version of the operating system.  | long  |   |   |
| <a name="user_agent.os.name"></a>`user_agent.os.name`  | Name of the operating system.  | keyword  |   |   |


## <a name="use-cases"></a>Use cases

ECS fields can be applied to common use cases.

 * [APM](https://github.com/elastic/ecs/blob/master/use-cases/apm.md)
 * [Auditbeat](https://github.com/elastic/ecs/blob/master/use-cases/auditbeat.md)
 * [Beats](https://github.com/elastic/ecs/blob/master/use-cases/beats.md)
 * [Filebeat Apache](https://github.com/elastic/ecs/blob/master/use-cases/filebeat-apache-access.md)
 * [Logging](https://github.com/elastic/ecs/blob/master/use-cases/logging.md)
 * [Metricbeat](https://github.com/elastic/ecs/blob/master/use-cases/metricbeat.md)


## <a name="implementing-ecs"></a>Implementing ECS

 **Guidelines**

 * The document MUST have the `@timestamp` field.
 * The [data type](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/mapping-types.html) defined for an ECS field MUST be used.
 * It SHOULD have the field `event.version` to define which version of ECS it uses.
 * As many fields as possible should be mapped to ECS.

 **Writing fields**

 * All fields must be lower case
 * No special characters except `_`
 * Use underscore to combine words

 **Naming Fields**

 * *Present tense.* Use present tense unless field describes historical information.
 * *Singular or plural.* Use singular and plural names properly to reflect the field content. For example, use `requests_per_sec` rather than `request_per_sec`.
 * *General to specific.* Organise the prefixes from general to specific to allow grouping fields into objects with a prefix like `host.*`.
 * *Avoid repetition.* Avoid stuttering of words. If part of the field name is already in the prefix, do not repeat it. Example: `host.host_ip` should be `host.ip`.
 * *Use prefixes.* Fields must be prefixed except for the base fields. For example all `host` fields are prefixed with `host.`. See `dot` notation in FAQ for more details.
 * Do not use abbreviations (few exceptions like `ip` exist)


## <a name="faq-ecs"></a>FAQ

### What are the benefits of using ECS?

The benefits for adopting ECS guidelines in your clusters are:

* **Data correlation.** Ability to easily correlate data from the same or different sources, including:
    * data from metrics, logs, and apm
    * data from the same machines/hosts
    * data from the same service

* **Ease of recall.** Improved ability to remember commonly used field names (because there is a single set, not a set per data source)
* **Ease of deduction.** Improved ability to deduce field names (because the field naming follows a small number of rules with few exceptions)
* **Reuse.** Ability to re-use analysis content (searches, visualizations, dashboards, alerts, reports, and ML jobs) across multiple data sources
* **Future proofing.** Ability to use any future Elastic-provided analysis content in your environment without modifications


### What if I have fields that conflict with ECS?

The [rename processor](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/rename-processor.html) can help you resolve field conflicts. For example, imagine that you already have a field called "user," but ECS employs `user` as an object. You can use the rename processor on ingest time to rename your field to the matching ECS field. If your field does not match ECS, you can rename your field to `user.value` instead.

### What if my events have additional fields?

Often events contain fields in addition to ECS fields. These fields can follow the ECS naming and writing rules, but this is not a requirement.

### Why does ECS use a dot notation instead of an underline notation?

There are two common key formats for ingesting data into Elasticsearch:

* Dot notation: `user.firstname: Nicolas`, `user.lastname: Ruflin`
* Underline notation: `user_firstname: Nicolas`, `user_lastname: Ruflin`

For ECS we decided to use the dot notation. Here's some background on this decision.

**What is the difference between the two notations?**

Ingesting `user.firstname` and `user.lastname` is identical to ingesting the following JSON:

```
"user": {
  "firstname": "Nicolas",
  "lastname": "Ruflin"
}
```

In Elasticsearch, `user` is represented as an [object datatype](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/object.html). In the case of the underline notation, both are just [string datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).

NOTE: ECS does not use [nested datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html), which are arrays of objects.

**Advantages of dot notation**

With dot notation, each prefix in Elasticsearch is an object. Each object can have [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html#object-params) that control how fields inside the object are treated. In the context of ECS, for example, these parameters would allow you to disable dynamic property creation for certain prefixes.

Individual objects give you more flexibility on both the ingest and the event sides.  In Elasticsearch, for example, you can use the remove processor to drop complete objects instead of selecting each key inside. You don't have to know ahead of time which keys will be in an object. 

In Beats, you can simplify the creation of events. For example, you can treat each object as an object (or struct in Golang), which makes constructing and modifying each part of the final event easier. 

**Disadvantage of dot notation**

In Elasticsearch, each key can only have one type. For example, if `user` is an `object`, you can't use it as a`keyword` type in the same index, like `{"user": "nicolas ruflin"}`. This restriction can be an issue in certain datasets. For the ECS data itself, this is not an issue because all fields are predefined.

**What if I already use the underline notation?**

Mixing the underline notation with the ECS dot notation is not a problem. As long as there are no conflicts, they can coexist in the same document.

