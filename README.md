**WARNING: THIS IS WORK IN PROGRESS**

# Elastic Common Schema (ECS)

The Elastic Common Schema (ECS) is used to provide a common data model when
ingesting data into Elasticsearch. Having a common schema allows you correlate
data from sources like logs and metrics or IT operations
analytics and security analytics.

ECS is still under development and backward compatibility is not guaranteed. Any
feedback on the general structure, missing fields, or existing fields is appreciated.
For contributions please read the [Contributing Guide](CONTRIBUTING.md).

The current version of ECS is `0.1.0`.

* [Fields](#fields)
* [Use cases](#use-cases)
* [Implementing ECS](#implementing-ecs)
* [About ECS](#about-ecs)

# <a name="fields"></a>Fields

List of available ECS fields.
 * [Base fields](#base)
 * [Agent fields](#agent)
 * [Cloud fields](#cloud)
 * [Container fields](#container)
 * [Destination fields](#destination)
 * [Device fields](#device)
 * [Error fields](#error)
 * [Event fields](#event)
 * [File fields](#file)
 * [Geoip fields](#geoip)
 * [Host fields](#host)
 * [HTTP fields](#http)
 * [Kubernetes fields](#kubernetes)
 * [Log fields](#log)
 * [Network fields](#network)
 * [Organization fields](#organization)
 * [Operating System fields](#os)
 * [Process fields](#process)
 * [Service fields](#service)
 * [Source fields](#source)
 * [URL fields](#url)
 * [User fields](#user)
 * [User agent fields](#user_agent)

## <a name="base"></a> Base fields

The base set contains all fields which are on the top level. These fields are common across all types of events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="@timestamp"></a>`@timestamp`  | Date/time when the event originated.<br/>For log events this is the date/time when the event was generated, and not when it was read.<br/>Required field for all events.  | date  |   | `2016-05-23T08:05:34.853Z`  |
| <a name="tags"></a>`tags`  | List of keywords used to tag each event.  | keyword  |   | `["production", "env2"]`  |
| <a name="labels"></a>`labels`  | Key/value pairs.<br/>Can be used to add meta information to events. Should not contain nested objects. All values are stored as keyword.<br/>Example: `docker` and `k8s` labels.  | object  |   | `{key1: value1, key2: value2}`  |
| <a name="message"></a>`message`  | For log events the message field contains the log message.<br/>In other use cases the message field can be used to concatenate different values which are then freely searchable. If multiple messages exist, they can be combined into one message.  | text  |   | `Hello World`  |


## <a name="agent"></a> Agent fields

The agent fields contain the data about the agent/client/shipper that created the event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="agent.version"></a>`agent.version`  | Version of the agent.  | keyword  |   | `6.0.0-rc2`  |
| <a name="agent.name"></a>`agent.name`  | Name of the agent.  | keyword  |   | `filebeat`  |
| <a name="agent.id"></a>`agent.id`  | Unique identifier of this agent (if one exists).<br/>Example: For Beats this would be beat.id.  | keyword  |   | `8a4f500d`  |
| <a name="agent.ephemeral_id"></a>`agent.ephemeral_id`  | Ephemeral identifier of this agent (if one exists).<br/>This id normally changes across restarts, but `agent.id` does not.  | keyword  |   | `8a4f500f`  |


Examples: In the case of Beats for logs, the agent.name is filebeat. For APM, it is the agent running in the app/service. The agent information does not change if data is sent through queuing systems like Kafka, Redis, or processing systems such as Logstash or APM Server.


## <a name="cloud"></a> Cloud fields

Fields related to the cloud or infrastructure the events are coming from.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="cloud.provider"></a>`cloud.provider`  | Name of the cloud provider. Example values are ec2, gce, or digitalocean.  | keyword  |   | `ec2`  |
| <a name="cloud.availability_zone"></a>`cloud.availability_zone`  | Availability zone in which this host is running.  | keyword  |   | `us-east-1c`  |
| <a name="cloud.region"></a>`cloud.region`  | Region in which this host is running.  | keyword  |   | `us-east-1`  |
| <a name="cloud.instance.id"></a>`cloud.instance.id`  | Instance ID of the host machine.  | keyword  |   | `i-1234567890abcdef0`  |
| <a name="cloud.instance.name"></a>`cloud.instance.name`  | Instance name of the host machine.  | keyword  |   |   |
| <a name="cloud.machine.type"></a>`cloud.machine.type`  | Machine type of the host machine.  | keyword  |   | `t2.medium`  |
| <a name="cloud.account.id"></a>`cloud.account.id`  | The cloud account or organization id used to identify different entities in a multi-tenant environment.<br/>Examples: AWS account id, Google Cloud ORG Id, or other unique identifier.  | keyword  |   | `666777888999`  |


Examples: If Metricbeat is running on an EC2 host and fetches data from its host, the cloud info contains the data about this machine. If Metricbeat runs on a remote machine outside the cloud and fetches data from a service running in the cloud, the field contains cloud data from the machine the  service is running on.


## <a name="container"></a> Container fields

Container fields are used for meta information about the specific container that is the source of information. These fields help correlate data based containers from any runtime.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="container.runtime"></a>`container.runtime`  | Runtime managing this container.  | keyword  |   | `docker`  |
| <a name="container.id"></a>`container.id`  | Unique container id.  | keyword  |   |   |
| <a name="container.image.name"></a>`container.image.name`  | Name of the image the container was built on.  | keyword  |   |   |
| <a name="container.image.tag"></a>`container.image.tag`  | Container image tag.  | keyword  |   |   |
| <a name="container.name"></a>`container.name`  | Container name.  | keyword  |   |   |
| <a name="container.labels"></a>`container.labels`  | Image labels.  | object  |   |   |


## <a name="destination"></a> Destination fields

Destination fields describe details about the destination of a packet/event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="destination.ip"></a>`destination.ip`  | IP address of the destination.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="destination.hostname"></a>`destination.hostname`  | Hostname of the destination.  | keyword  |   |   |
| <a name="destination.port"></a>`destination.port`  | Port of the destination.  | long  |   |   |
| <a name="destination.mac"></a>`destination.mac`  | MAC address of the destination.  | keyword  |   |   |
| <a name="destination.domain"></a>`destination.domain`  | Destination domain.  | keyword  |   |   |
| <a name="destination.subdomain"></a>`destination.subdomain`  | Destination subdomain.  | keyword  |   |   |


## <a name="device"></a> Device fields

Device fields are used to provide additional information about the device that is the source of the information. This could be a firewall, network device, etc.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="device.mac"></a>`device.mac`  | MAC address of the device  | keyword  |   |   |
| <a name="device.ip"></a>`device.ip`  | IP address of the device.  | ip  |   |   |
| <a name="device.hostname"></a>`device.hostname`  | Hostname of the device.  | keyword  |   |   |
| <a name="device.vendor"></a>`device.vendor`  | Device vendor information.  | text  |   |   |
| <a name="device.version"></a>`device.version`  | Device version.  | keyword  |   |   |
| <a name="device.serial_number"></a>`device.serial_number`  | Device serial number.  | keyword  |   |   |
| <a name="device.timezone.offset.sec"></a>`device.timezone.offset.sec`  | Timezone offset of the host in seconds.<br/>Number of seconds relative to UTC. If the offset is -01:30 the value will be -5400.  | long  |   | `-5400`  |
| <a name="device.type"></a>`device.type`  | The type of the device the data is coming from.<br/>There is no predefined list of device types. Some examples are `endpoint`, `firewall`, `ids`, `ips`, `proxy`.  | keyword  |   | `firewall`  |


## <a name="error"></a> Error fields

These fields can represent errors of any kind. Use them for errors that happen while fetching events or in cases where the event itself contains an error.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="error.id"></a>`error.id`  | Unique identifier for the error.  | keyword  |   |   |
| <a name="error.message"></a>`error.message`  | Error message.  | text  |   |   |
| <a name="error.code"></a>`error.code`  | Error code describing the error.  | keyword  |   |   |


## <a name="event"></a> Event fields

The event fields are used for context information about the data itself.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="event.id"></a>`event.id`  | Unique ID to describe the event.  | keyword  |   | `8a4f500d`  |
| <a name="event.category"></a>`event.category`  | Event category.<br/>This can be a user defined category.  | keyword  |   | `metrics`  |
| <a name="event.type"></a>`event.type`  | A type given to this kind of event which can be used for grouping.<br/>This is normally defined by the user.  | keyword  |   | `nginx-stats-metrics`  |
| <a name="event.module"></a>`event.module`  | Name of the module this data is coming from.<br/>This information is coming from the modules used in Beats or Logstash.  | keyword  |   | `mysql`  |
| <a name="event.dataset"></a>`event.dataset`  | Name of the dataset.<br/>The concept of a `dataset` (fileset / metricset) is used in Beats as a subset of modules. It contains the information which is currently stored in metricset.name and metricset.module or fileset.name.  | keyword  |   | `stats`  |
| <a name="event.severity"></a>`event.severity`  | Severity describes the severity of the event. What the different severity values mean can very different between use cases. It's up to the implementer to make sure severities are consistent across events.  | long  |   | `7`  |
| <a name="event.raw"></a>`event.raw`  | Raw text message of entire event. Used to demonstrate log integrity.<br/>This field is not indexed and doc_values are disabled. It cannot be searched, but it can be retrieved from `_source`.  | keyword  |   | `Sep 19 08:26:10 host CEF:0&#124;Security&#124; threatmanager&#124;1.0&#124;100&#124; worm successfully stopped&#124;10&#124;src=10.0.0.1 dst=2.1.2.2spt=1232`  |
| <a name="event.hash"></a>`event.hash`  | Hash (perhaps logstash fingerprint) of raw field to be able to demonstrate log integrity.  | keyword  |   | `123456789012345678901234567890ABCD`  |
| <a name="event.version"></a>`event.version`  | The version field contains the version an event for ECS adheres to.<br/>This field should be provided as part of each event to make it possible to detect to which ECS version an event belongs.<br/>event.version is a required field and must exist in all events. It describes which ECS version the event adheres to.<br/>The current version is 0.1.0.  | keyword  |   | `0.1.0`  |
| <a name="event.duration"></a>`event.duration`  | Duration of the event in nanoseconds.  | long  |   |   |
| <a name="event.created"></a>`event.created`  | event.created contains the date when the event was created.<br/>This timestamp is distinct from @timestamp in that @timestamp contains the processed timestamp. For logs these two timestamps can be different as the timestamp in the log line and when the event is read for example by Filebeat are not identical. `@timestamp` must contain the timestamp extracted from the log line, event.created when the log line is read. The same could apply to package capturing where @timestamp contains the timestamp extracted from the network package and event.created when the event was created.<br/>In case the two timestamps are identical, @timestamp should be used.  | date  |   |   |
| <a name="event.risk_score"></a>`event.risk_score`  | Risk score value of the event.  | float  |   |   |


## <a name="file"></a> File fields

File fields provide details about each file.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="file.path"></a>`file.path`  | Path to the file.  | text  |   |   |
| <a name="file.path.raw"></a>`file.path.raw`  | Path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.target_path"></a>`file.target_path`  | Target path for symlinks.  | text  |   |   |
| <a name="file.target_path.raw"></a>`file.target_path.raw`  | Path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.extension"></a>`file.extension`  | File extension.<br/>This should allow easy filtering by file extensions.  | keyword  |   | `png`  |
| <a name="file.type"></a>`file.type`  | File type (file, dir, or symlink).  | keyword  |   |   |
| <a name="file.device"></a>`file.device`  | Device that is the source of the file.  | keyword  |   |   |
| <a name="file.inode"></a>`file.inode`  | Inode representing the file in the filesystem.  | keyword  |   |   |
| <a name="file.uid"></a>`file.uid`  | The user ID (UID) or security identifier (SID) of the file owner.  | keyword  |   |   |
| <a name="file.owner"></a>`file.owner`  | File owner's username.  | keyword  |   |   |
| <a name="file.gid"></a>`file.gid`  | Primary group ID (GID) of the file.  | keyword  |   |   |
| <a name="file.group"></a>`file.group`  | Primary group name of the file.  | keyword  |   |   |
| <a name="file.mode"></a>`file.mode`  | Mode of the file in octal representation.  | keyword  |   | `416`  |
| <a name="file.size"></a>`file.size`  | File size in bytes (field is only added when `type` is `file`).  | long  |   |   |
| <a name="file.mtime"></a>`file.mtime`  | Last time file content was modified.  | date  |   |   |
| <a name="file.ctime"></a>`file.ctime`  | Last time file metadata changed.  | date  |   |   |


## <a name="geoip"></a> Geoip fields

Geoip fields carry geo information for an ip address.  The Elasticsearch geoip plugin can do the conversion to geoip.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="geoip.continent_name"></a>`geoip.continent_name`  | Name of the continent.  | keyword  |   |   |
| <a name="geoip.country_iso_code"></a>`geoip.country_iso_code`  | Country ISO code.  | keyword  |   |   |
| <a name="geoip.location"></a>`geoip.location`  | Longitude and latitude.  | geo_point  |   |   |
| <a name="geoip.region_name"></a>`geoip.region_name`  | Region name.  | keyword  |   |   |
| <a name="geoip.city_name"></a>`geoip.city_name`  | City name.  | keyword  |   |   |


## <a name="host"></a> Host fields

Host fields provide information related to a host. A host can be a physical machine, a virtual machine, or a Docker container.

Normally the host information is related to the machine on which the event was generated/collected, but they can be used differently if needed.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="host.timezone.offset.sec"></a>`host.timezone.offset.sec`  | Timezone offset of the host in seconds.<br/>Number of seconds relative to UTC. If the offset is -01:30 the value will be -5400.  | long  |   | `-5400`  |
| <a name="host.name"></a>`host.name`  | host.name is the hostname of the host.<br/>It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use.  | keyword  |   |   |
| <a name="host.id"></a>`host.id`  | Unique host id.<br/>As hostname is not always unique, use values that are meaningful in your environment. <br/>Example: The current usage of `beat.name`.  | keyword  |   |   |
| <a name="host.ip"></a>`host.ip`  | Host ip address.  | ip  |   |   |
| <a name="host.mac"></a>`host.mac`  | Host mac address.  | keyword  |   |   |
| <a name="host.type"></a>`host.type`  | Type of host.<br/>For Cloud providers this can be the machine type like `t2.medium`. If vm, this could be the container, for example, or other information meaningful in your environment.  | keyword  |   |   |
| <a name="host.os.platform"></a>`host.os.platform`  | Operating system platform (centos, ubuntu, windows, etc.)  | keyword  |   | `darwin`  |
| <a name="host.os.name"></a>`host.os.name`  | Operating system name.  | keyword  |   | `Mac OS X`  |
| <a name="host.os.family"></a>`host.os.family`  | OS family (redhat, debian, freebsd, windows, etc.)  | keyword  |   | `debian`  |
| <a name="host.os.version"></a>`host.os.version`  | Operating system version.  | keyword  |   | `10.12.6`  |
| <a name="host.architecture"></a>`host.architecture`  | Operating system architecture.  | keyword  |   | `x86_64`  |


## <a name="http"></a> HTTP fields

Fields related to HTTP requests and responses.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="http.response.status_code"></a>`http.response.status_code`  | Http response status code.  | long  |   | `404`  |
| <a name="http.response.body"></a>`http.response.body`  | The full http response body.  | text  |   | `Hello world`  |


## <a name="kubernetes"></a> Kubernetes fields

Kubernetes fields are used for Kubernetes meta information. This information helps correlate data from Kubernetes setups.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="kubernetes.pod.name"></a>`kubernetes.pod.name`  | Kubernetes pod name  | keyword  |   |   |
| <a name="kubernetes.namespace"></a>`kubernetes.namespace`  | Kubernetes namespace  | keyword  |   |   |
| <a name="kubernetes.labels"></a>`kubernetes.labels`  | Kubernetes labels map  | object  |   |   |
| <a name="kubernetes.annotations"></a>`kubernetes.annotations`  | Kubernetes annotations map  | object  |   |   |
| <a name="kubernetes.container.name"></a>`kubernetes.container.name`  | Kubernetes container name. This name is unique within the pod only. It is different from the underlying `container.name` field.  | keyword  |   |   |


## <a name="log"></a> Log fields

Fields which are specific to log events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="log.level"></a>`log.level`  | Log level of the log event.<br/>Some examples are `WARN`, `ERR`, `INFO`.  | keyword  |   | `ERR`  |
| <a name="log.line"></a>`log.line`  | Line number the log event was collected from.  | long  |   | `18`  |
| <a name="log.offset"></a>`log.offset`  | Offset of the beginning of the log event.  | long  |   | `12`  |
| <a name="log.message"></a>`log.message`  | This is the log message and contains the full log message before splitting it up in multiple parts.<br/>In contrast to the `message` field which can contain an extracted part of the log message, this field contains the original, full log message. It can have already some modifications applied like encoding or new lines removed to clean up the log message.<br/>This field is not indexed and doc_values are disabled so it can't be queried but the value can be retrieved from `_source`.  | keyword  |   | `Sep 19 08:26:10 localhost My log`  |


## <a name="network"></a> Network fields

Fields related to network data.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="network.protocol"></a>`network.protocol`  | Network protocol name.  | keyword  |   | `http`  |
| <a name="network.direction"></a>`network.direction`  | Direction of the network traffic.<br/>Recommended values are:<br/>  * inbound<br/>  * outbound<br/>  * unknown  | keyword  |   | `inbound`  |
| <a name="network.forwarded_ip"></a>`network.forwarded_ip`  | Host IP address when the source IP address is the proxy.  | ip  |   | `192.1.1.2`  |
| <a name="network.inbound.bytes"></a>`network.inbound.bytes`  | Network inbound bytes.  | long  |   | `184`  |
| <a name="network.inbound.packets"></a>`network.inbound.packets`  | Network inbound packets.  | long  |   | `12`  |
| <a name="network.outbound.bytes"></a>`network.outbound.bytes`  | Network outbound bytes.  | long  |   | `184`  |
| <a name="network.outbound.packets"></a>`network.outbound.packets`  | Network outbound packets.  | long  |   | `12`  |


## <a name="organization"></a> Organization fields

The organization fields enrich data with information about the company or entity  the data is associated with. These fields help you arrange or filter data stored in an index by one or multiple organizations.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="organization.name"></a>`organization.name`  | Organization name.  | text  |   |   |
| <a name="organization.id"></a>`organization.id`  | Unique identifier for the organization.  | keyword  |   |   |


## <a name="os"></a> Operating System fields

The OS fields contain information about the operating system. These fields are often used inside other prefixes, such as `host.os.*` or `user_agent.os.*`.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="os.platform"></a>`os.platform`  | Operating system platform (such centos, ubuntu, windows).  | keyword  |   | `darwin`  |
| <a name="os.name"></a>`os.name`  | Operating system name.  | keyword  |   | `Mac OS X`  |
| <a name="os.family"></a>`os.family`  | OS family (such as redhat, debian, freebsd, windows).  | keyword  |   | `debian`  |
| <a name="os.version"></a>`os.version`  | Operating system version as a raw string.  | keyword  |   | `10.12.6-rc2`  |


## <a name="process"></a> Process fields

These fields contain information about a process. These fields can help you correlate metrics information with a process id/name from a log message.  The `process.pid` often stays in the metric itself and is copied to the global field for correlation.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="process.args"></a>`process.args`  | Process arguments.<br/>May be filtered to protect sensitive information.  | keyword  |   | `['-l', 'user', '10.0.0.16']`  |
| <a name="process.name"></a>`process.name`  | Process name.<br/>Sometimes called program name or similar.  | keyword  |   | `ssh`  |
| <a name="process.pid"></a>`process.pid`  | Process id.  | long  |   |   |
| <a name="process.ppid"></a>`process.ppid`  | Process parent id.  | long  |   |   |
| <a name="process.title"></a>`process.title`  | Process title.<br/>The proctitle, often the same as process name.  | keyword  |   |   |


## <a name="service"></a> Service fields

The service fields describe the service for or from which the data was collected. These fields help you find and correlate logs for a specific service and version.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="service.id"></a>`service.id`  | Unique identifier of the running service.<br/>This id should uniquely identify this service. This makes it possible to correlate logs and metrics for one specific service. <br/>Example: If you are experiencing issues with one redis instance, you can filter on that id to see metrics and logs for that single instance.  | keyword  |   | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6`  |
| <a name="service.name"></a>`service.name`  | Name of the service data is collected from.<br/>The name can be used to group and correlate logs and metrics from one service.<br/>Example: If logs or metrics are collected from Redis, `service.name` would be `redis`.  | keyword  |   | `elasticsearch`  |
| <a name="service.type"></a>`service.type`  | Service type.  | keyword  |   |   |
| <a name="service.state"></a>`service.state`  | Current state of the service.  | keyword  |   |   |
| <a name="service.version"></a>`service.version`  | Version of the service the data was collected from.<br/>This allows to look at a data set only for a specific version of a service.  | keyword  |   | `3.2.4`  |
| <a name="service.ephemeral_id"></a>`service.ephemeral_id`  | Ephemeral identifier of this service (if one exists).<br/>This id normally changes across restarts, but `service.id` does not.  | keyword  |   | `8a4f500f`  |


## <a name="source"></a> Source fields

Source fields describe details about the source of the event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="source.ip"></a>`source.ip`  | IP address of the source.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="source.hostname"></a>`source.hostname`  | Hostname of the source.  | keyword  |   |   |
| <a name="source.port"></a>`source.port`  | Port of the source.  | long  |   |   |
| <a name="source.mac"></a>`source.mac`  | MAC address of the source.  | keyword  |   |   |
| <a name="source.domain"></a>`source.domain`  | Source domain.  | keyword  |   |   |
| <a name="source.subdomain"></a>`source.subdomain`  | Source subdomain.  | keyword  |   |   |


## <a name="url"></a> URL fields

URL fields provide a complete URL, with scheme, host, and path. The URL object can be reused in other prefixes, such as `host.url.*` for example. Keep the structure consistent whenever you use URL fields.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="url.href"></a>`url.href`  | Full url. The field is stored as keyword.<br/>`url.href` is a [multi field](https://www.elastic.co/guide/en/ elasticsearch/reference/6.2/ multi-fields.html#_multi_fields_with_multiple_analyzers). The data is stored as keyword `url.href` and test `url.href.analyzed`. These fields enable you to run a query against part of the url still works splitting up the URL at ingest time.  <br/>`href` is an analyzed field so the parsed information can be accessed through `href.analyzed` in queries.  | text  |   | `https://elastic.co:443/search?q=elasticsearch#top`  |
| <a name="url.href.raw"></a>`url.href.raw`  | The full URL. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.scheme"></a>`url.scheme`  | Scheme of the request, such as "https".<br/>Note: The `:` is not part of the scheme.  | keyword  |   | `https`  |
| <a name="url.host.name"></a>`url.host.name`  | Hostname of the request, such as "example.com".<br/>For correlation the this field can be copied into the `host.name` field.  | keyword  |   | `elastic.co`  |
| <a name="url.port"></a>`url.port`  | Port of the request, such as 443.  | integer  |   | `443`  |
| <a name="url.path"></a>`url.path`  | Path of the request, such as "/search".  | text  |   |   |
| <a name="url.path.raw"></a>`url.path.raw`  | URL path. A non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.query"></a>`url.query`  | The query field describes the query string of the request, such as "q=elasticsearch".<br/>The `?` is excluded from the query string. If a URL contains no `?`, there is no query field. If there is a `?` but no query, the query field exists with an empty string. The `exists` query can be used to differentiate between the two cases.  | text  |   |   |
| <a name="url.query.raw"></a>`url.query.raw`  | URL query part. A non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.fragment"></a>`url.fragment`  | Portion of the url after the `#`, such as "top".<br/>The `#` is not part of the fragment.  | keyword  |   |   |
| <a name="url.username"></a>`url.username`  | Username of the request.  | keyword  |   |   |
| <a name="url.password"></a>`url.password`  | Password of the request.  | keyword  |   |   |


## <a name="user"></a> User fields

The user fields describe information about the user that is relevant to  the event. Fields can have one entry or multiple entries. If a user has more than one id, provide an array that includes all of them.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user.id"></a>`user.id`  | One or multiple unique identifiers of the user.  | keyword  |   |   |
| <a name="user.name"></a>`user.name`  | Name of the user.<br/>The field is a keyword, and will not be tokenized.  | keyword  |   |   |
| <a name="user.email"></a>`user.email`  | User email address.  | keyword  |   |   |
| <a name="user.hash"></a>`user.hash`  | Unique user hash to correlate information for a user in anonymized form.<br/>Useful if `user.id` or `user.name` contain confidential information and cannot be used.  | keyword  |   |   |


## <a name="user_agent"></a> User agent fields

The user_agent fields normally come from a browser request. They often show up in web service logs coming from the parsed user agent string.


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





# <a name="use-cases"></a>Use cases

Below are some examples that demonstrate how ECS fields can be applied to
specific use cases.

 * [APM](https://github.com/elastic/ecs/blob/master/use-cases/apm.md)
 * [Auditbeat](https://github.com/elastic/ecs/blob/master/use-cases/auditbeat.md)
 * [Beats](https://github.com/elastic/ecs/blob/master/use-cases/beats.md)
 * [Filebeat Apache](https://github.com/elastic/ecs/blob/master/use-cases/filebeat-apache-access.md)
 * [Logging](https://github.com/elastic/ecs/blob/master/use-cases/logging.md)
 * [Metricbeat](https://github.com/elastic/ecs/blob/master/use-cases/metricbeat.md)



# <a name="implementing-ecs"></a>Implementing ECS

## Adhere to ECS

The following rules apply if an event wants to adhere to ECS

* The document MUST have the `@timestamp` field.
* The [data type](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/mapping-types.html) defined for an ECS field MUST be used.
* It SHOULD have the field `event.version` to define which version of ECS it uses.

To make the most out of ECS as many fields as possible should be mapped to ECS.

## Rules

ECS follows the following writing and naming rules for the fields. The goal of
these rules is to make the fields easy to remember and have a guide when new
fields are added.

Often events will contain additional fields besides ECS. These can follow the
the same naming and writing rules but don't have to.

**Writing**

* All fields must be lower case
* No special characters except `_`
* Words are combined through underscore

**Naming**

* Use present tense unless field describes historical information.
* Use singular and plural names properly to reflect the field content. For example, use `requests_per_sec` rather than `request_per_sec`.
* Organise the prefixes from general to specific to allow grouping fields into objects with a prefix like `host.*`.
* Avoid stuttering of words. If part of the field name is already in the prefix, do not repeat it. Example: `host.host_ip` should be `host.ip`.
* Fields must be prefixed except for the base fields. For example all `host` fields are prefixed with `host.`. See `dot` notation in FAQ for more details.
* Do not use abbreviations (few exceptions like `ip` exist)

# <a name="about-ecs"></a>About ECS

## Scope

The Elastic Common Schema defines a common set of document fields (and their respective field names) to be used in event messages stored in Elasticsearch as part of any logging or metrics use case of the Elastic Stack, including IT operations analytics and security analytics.

## Goals

The ECS has the following goals:

* Correlate data between metrics, logs and APM
* Correlate data coming from the same machines / hosts
* Correlate data coming from the same service

Priority on which fields are added is based on these goals.


## Benefits

The benefits to a user adopting these fields and names in their clusters are:

- Ability to simply correlate data from different data sources
- Improved ability to remember commonly used field names (since there is only a single set, not a set per data source)
- Improved ability to deduce unremembered field names (since the field naming follows a small number of rules with few exceptions)
- Ability to re-use analysis content (searches, visualizations, dashboards, alerts, reports, and ML jobs) across multiple data sources
- Ability to use any future Elastic-provided analysis content in their environment without modifications


## FAQ

### Why is ECS using a dot nation instead of an underline notation?

There are two common formats on how keys are formatted when ingesting data into Elasticsearch:

* Dot notation: `user.firstname: Nicolas`, `user.lastname: Ruflin`
* Underline notation: `user_firstname: Nicolas`, `user_lastname: Ruflin`

In ECS the decision was made to use the dot notation and this entry is intended to share some background on this decision.

**What is the difference between the two notations?**

When ingesting `user.firstname` and `user.lastname` it is identical to ingesting the following JSON:

```
"user": {
  "firstname": "Nicolas",
  "lastname": "Ruflin"
}
```

This means internally in Elasticsearch `user` is represented as an [object datatype](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/object.html). In the case of the underline notation both are just [string datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).

NOTE: ECS does not used [nested datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html) which is an array of objects.

**Advantages of dot notation**

The advantage of the dot notation is that on the Elasticsearch side each prefix is an object. Each object can have [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html#object-params) on how fields inside the object should be treated, for example if they should be index or mappings should be extended. In the context of ECS this allows for example to disable dynamic property creation for certain prefixes.

On the ingest side of Elasticsearch it makes it simpler to for example drop complete objects with the remove processor instead of selecting each key inside it. It does not require prior knowledge which keys will end up in the object.

On the event producing side like in Beats it simplifies the creation of the events as on the code side each object can be treated as an object (or struct in Golang as an example) which makes constructing and modifying each part of the final event easier.

**Disadvantage of dot notation**

In Elasticsearch each key can only have one type. So if `user` is an object it's not possible to have in the same index `user` as type `keyword` like `{"user": "nicolas ruflin"}`. This can be an issue in certain datasets.

For the ECS data itself this is not an issue as all fields are predefined.

**What if I already use the underline notation?**

It's not a problem to mix the underline notation with the ECS do notation. They can coexist in the same document as long as there are not conflicts.

**I have conflicting fields with ECS?**

Assuming you already have a field user but ECS uses `user` as an object, you can use the [rename processor](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/rename-processor.html) on ingest time to rename your field to either the matching ECS field or rename it to `user.value` instead if your field does not match ECS.
