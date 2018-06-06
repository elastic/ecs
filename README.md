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

## <a name="base"></a> Base fields

The base set contains all fields which are on the top level without a namespace.

These are fields which are common across all types of events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="@timestamp"></a>`@timestamp`  | Timestamp when the event was created.<br/>For log events this is expected to be when the event was generated and not when it was read.<br/>Timestamp is a required field and must exist in all events.  | date  |   | `2016-05-23T08:05:34.853Z`  |
| <a name="tags"></a>`tags`  | Tags is a list of keywords which are used to tag each event.  | keyword  |   | `["production", "env2"]`  |
| <a name="labels"></a>`labels`  | Labels is an object which contains key/value pairs.<br/>Labels can be used to add additional meta information to events. Label should not contain nested objects and all values are stored as keyword.<br/>An example usage is the docker and k8s labels.  | object  |   | `{key1: value1, key2: value2}`  |
| <a name="message"></a>`message`  | For log events the message field contains the log message.<br/>In other use cases the message field can be used to concatenate together different values which are then freely searchable. Or if multiple messages exist they can be combined here into one message.  | text  |   | `Hello World`  |


## <a name="agent"></a> Agent fields

The agent fields contains the data about the agent/client/shipper that created the event.

As an example in case of Beats for logs the `agent.name` is `filebeat`. In the case of APM it is the agent running in the app / service. The agent information does not change if data is sent through queuing system like Kafka, Redis, or processing systems like Logstash or APM Server.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="agent.version"></a>`agent.version`  | Agent version.  | keyword  |   | `6.0.0-rc2`  |
| <a name="agent.name"></a>`agent.name`  | Agent name.<br/>Name of the agent.  | keyword  |   | `filebeat`  |
| <a name="agent.id"></a>`agent.id`  | Unique identifier of this agent if one exists.<br/>In the case of Beats this would be beat.id.  | keyword  |   | `8a4f500d`  |
| <a name="agent.ephemeral_id"></a>`agent.ephemeral_id`  | Ephemeral identifier of this agent if one exists.<br/>This id compared to id normally changes across restarts.  | keyword  |   | `8a4f500f`  |


## <a name="cloud"></a> Cloud fields

All fields related to the cloud or infrastructure the events are coming from.

In case Metricbeat is running on an EC2 host and fetches data from its host, the cloud info is expected to contain the data about this machine. In the case Metricbeat runs outside the cloud on a remote machine and fetches data from a service running in the cloud it is expected to have the cloud data from the machine on which the service is running in.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="cloud.provider"></a>`cloud.provider`  | Name of the cloud provider. Example values are ec2, gce, or digitalocean.  | keyword  |   | `ec2`  |
| <a name="cloud.availability_zone"></a>`cloud.availability_zone`  | Availability zone in which this host is running.  | keyword  |   | `us-east-1c`  |
| <a name="cloud.region"></a>`cloud.region`  | Region in which this host is running.  | keyword  |   | `us-east-1`  |
| <a name="cloud.instance.id"></a>`cloud.instance.id`  | Instance ID of the host machine.  | keyword  |   | `i-1234567890abcdef0`  |
| <a name="cloud.instance.name"></a>`cloud.instance.name`  | Instance name of the host machine.  | keyword  |   |   |
| <a name="cloud.machine.type"></a>`cloud.machine.type`  | Machine type of the host machine.  | keyword  |   | `t2.medium`  |
| <a name="cloud.account.id"></a>`cloud.account.id`  | The cloud account or organization id<br/>This could be the AWS account id or Google Cloud ORG Id. This should be organizational.  | keyword  |   | `666777888999`  |


## <a name="container"></a> Container fields

Container fields are used for meta information about the specific container the information is coming from. This should help to correlate data based containers from any runtime.


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
| <a name="destination.ip"></a>`destination.ip`  | IP address of the destination.<br/>This can be on or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="destination.hostname"></a>`destination.hostname`  | Hostname of the destination.  | keyword  |   |   |
| <a name="destination.port"></a>`destination.port`  | Port of the destination.  | long  |   |   |
| <a name="destination.mac"></a>`destination.mac`  | MAC address of the destination.  | keyword  |   |   |
| <a name="destination.domain"></a>`destination.domain`  | Destination domain.  | keyword  |   |   |
| <a name="destination.subdomain"></a>`destination.subdomain`  | Destination subdomain.  | keyword  |   |   |


## <a name="device"></a> Device fields

Device fields are used to give additional information about the device that the information is coming from.

This could be a firewall, network device, etc.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="device.mac"></a>`device.mac`  | MAC address of the device  | keyword  |   |   |
| <a name="device.ip"></a>`device.ip`  | IP address of the device.  | ip  |   |   |
| <a name="device.hostname"></a>`device.hostname`  | Hostname of the device.  | keyword  |   |   |
| <a name="device.vendor"></a>`device.vendor`  | Device vendor information.  | text  |   |   |
| <a name="device.version"></a>`device.version`  | Device version.  | keyword  |   |   |
| <a name="device.serial_number"></a>`device.serial_number`  | Device serial number.  | keyword  |   |   |
| <a name="device.timezone.offset.sec"></a>`device.timezone.offset.sec`  | Timezone offset of the host in seconds.<br/>Number of seconds relative to UTC. In case the offset is -01:30 the value will be -5400.  | long  |   | `-5400`  |
| <a name="device.type"></a>`device.type`  | The type of the device the data is coming from.<br/>There is no predefined list of device types. Some examples are `endpoint`, `firewall`, `ids`, `ips`, `proxy`.  | keyword  |   | `firewall`  |


## <a name="error"></a> Error fields

Error namespace

This can be used to represent all kinds of errors. It can be for errors that happen while fetching events or if the event itself contains an error.


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
| <a name="event.raw"></a>`event.raw`  | Raw text message of entire event to be used to demonstrate log integrity.  | keyword  |   | `Sep 19 08:26:10 host CEF:0&#124;Security&#124; threatmanager&#124;1.0&#124;100&#124; worm successfully stopped&#124;10&#124;src=10.0.0.1 dst=2.1.2.2spt=1232`  |
| <a name="event.hash"></a>`event.hash`  | Hash (perhaps logstash fingerprint) of raw field to be able to demonstrate log integrity.  | keyword  |   | `123456789012345678901234567890ABCD`  |
| <a name="event.version"></a>`event.version`  | The version field contains the version an event for ECS adheres to.<br/>This field should be provided as part of each event to make it possible to detect to which ECS version an event belongs.<br/>event.version is a required field and must exist in all events. It describes which ECS version the event adheres to.<br/>The current version is 0.1.0.  | keyword  |   | `0.1.0`  |
| <a name="event.duration"></a>`event.duration`  | Duration of the event in nanoseconds.  | long  |   |   |
| <a name="event.created"></a>`event.created`  | event.created contains the date when the event was created.<br/>This timestamp is distinct from @timestamp in that @timestamp contains the processed timestamp. For logs these two timestamps can be different as the timestamp in the log line and when the event is read for example by Filebeat are not identical. `@timestamp` must contain the timestamp extracted from the log line, event.created when the log line is read. The same could apply to package capturing where @timestamp contains the timestamp extracted from the network package and event.created when the event was created.<br/>In case the two timestamps are identical, @timestamp should be used.  | date  |   |   |
| <a name="event.risk_score"></a>`event.risk_score`  | Risk score value of the event.  | float  |   |   |


## <a name="file"></a> File fields

File attributes.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="file.path"></a>`file.path`  | The path to the file.  | text  |   |   |
| <a name="file.path.raw"></a>`file.path.raw`  | The path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.target_path"></a>`file.target_path`  | The target path for symlinks.  | text  |   |   |
| <a name="file.target_path.raw"></a>`file.target_path.raw`  | The path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.extension"></a>`file.extension`  | The file extension.<br/>This should allow easy filtering by file extensions.  | keyword  |   | `png`  |
| <a name="file.type"></a>`file.type`  | The file type (file, dir, or symlink).  | keyword  |   |   |
| <a name="file.device"></a>`file.device`  | The device.  | keyword  |   |   |
| <a name="file.inode"></a>`file.inode`  | The inode representing the file in the filesystem.  | keyword  |   |   |
| <a name="file.uid"></a>`file.uid`  | The user ID (UID) or security identifier (SID) of the file owner.  | keyword  |   |   |
| <a name="file.owner"></a>`file.owner`  | The file owner's username.  | keyword  |   |   |
| <a name="file.gid"></a>`file.gid`  | The primary group ID (GID) of the file.  | keyword  |   |   |
| <a name="file.group"></a>`file.group`  | The primary group name of the file.  | keyword  |   |   |
| <a name="file.mode"></a>`file.mode`  | The mode of the file in octal representation.  | keyword  |   | `416`  |
| <a name="file.size"></a>`file.size`  | The file size in bytes (field is only added when `type` is `file`).  | long  |   |   |
| <a name="file.mtime"></a>`file.mtime`  | The last modified time of the file (time when content was modified).  | date  |   |   |
| <a name="file.ctime"></a>`file.ctime`  | The last change time of the file (time when metadata was changed).  | date  |   |   |


## <a name="geoip"></a> Geoip fields

Geoip fields are for used for geo information for an ip address.

The conversion to geoip information can be done by the Elasticsearch geoip plugin.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="geoip.continent_name"></a>`geoip.continent_name`  | The name of the continent.  | keyword  |   |   |
| <a name="geoip.country_iso_code"></a>`geoip.country_iso_code`  | Country ISO code.  | keyword  |   |   |
| <a name="geoip.location"></a>`geoip.location`  | The longitude and latitude.  | geo_point  |   |   |
| <a name="geoip.region_name"></a>`geoip.region_name`  | The region name.  | keyword  |   |   |
| <a name="geoip.city_name"></a>`geoip.city_name`  | The city name.  | keyword  |   |   |


## <a name="host"></a> Host fields

All fields related to a host. A host can be a physical machine, a virtual machine, and also a Docker container.

Normally the host information is related to the machine on which the event was generated / collected but also can be used differently if needed.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="host.timezone.offset.sec"></a>`host.timezone.offset.sec`  | Timezone offset of the host in seconds.<br/>Number of seconds relative to UTC. In case the offset is -01:30 the value will be -5400.  | long  |   | `-5400`  |
| <a name="host.name"></a>`host.name`  | host.name is the hostname of the host.<br/>It can contain what `hostname` returns on Unix systems, the fully qualified domain name or also a name specified by the user. It is up to the sender to decide which value to use.  | keyword  |   |   |
| <a name="host.id"></a>`host.id`  | Unique host id.<br/>As hostname is not always unique, this often can be configured by the user. An example here is the current usage of `beat.name`.  | keyword  |   |   |
| <a name="host.ip"></a>`host.ip`  | Host ip address.  | ip  |   |   |
| <a name="host.mac"></a>`host.mac`  | Host mac address.  | keyword  |   |   |
| <a name="host.type"></a>`host.type`  | This is the type of the host.<br/>For Cloud providers this can be the machine type like `t2.medium`. Or it vm, container for example or something user defined.  | keyword  |   |   |
| <a name="host.os.platform"></a>`host.os.platform`  | Operating system platform (e.g. centos, ubuntu, windows).  | keyword  |   | `darwin`  |
| <a name="host.os.name"></a>`host.os.name`  | Operating system name.  | keyword  |   | `Mac OS X`  |
| <a name="host.os.family"></a>`host.os.family`  | OS family (e.g. redhat, debian, freebsd, windows).  | keyword  |   | `debian`  |
| <a name="host.os.version"></a>`host.os.version`  | Operating system version.  | keyword  |   | `10.12.6`  |
| <a name="host.architecture"></a>`host.architecture`  | Operating system architecture.  | keyword  |   | `x86_64`  |


## <a name="kubernetes"></a> Kubernetes fields

Kubernetes fields are used for meta information about k8s. This should help to correlate data coming out of k8s setups.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="kubernetes.pod.name"></a>`kubernetes.pod.name`  | Kubernetes pod name  | keyword  |   |   |
| <a name="kubernetes.namespace"></a>`kubernetes.namespace`  | Kubernetes namespace  | keyword  |   |   |
| <a name="kubernetes.labels"></a>`kubernetes.labels`  | Kubernetes labels map  | object  |   |   |
| <a name="kubernetes.annotations"></a>`kubernetes.annotations`  | Kubernetes annotations map  | object  |   |   |
| <a name="kubernetes.container.name"></a>`kubernetes.container.name`  | Kubernetes container name. This name is unique within the pod only, it's different from underlying container name (container.name in ECS)  | keyword  |   |   |


## <a name="log"></a> Log fields

Fields which are specific to log events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="log.level"></a>`log.level`  | Log level of the log event.<br/>Some examples are `WARN`, `ERR`, `INFO`.  | keyword  |   | `ERR`  |
| <a name="log.line"></a>`log.line`  | Line number the log event was collected from.  | long  |   | `18`  |
| <a name="log.offset"></a>`log.offset`  | Offset of the beginning of the log event.  | long  |   | `12`  |


## <a name="network"></a> Network fields

All fields related to network data.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="network.protocol"></a>`network.protocol`  | Network protocol name.  | keyword  |   | `http`  |
| <a name="network.direction"></a>`network.direction`  | Direction of the network traffic.<br/>The recommended values are:<br/>  * inbound<br/>  * outbound<br/>  * unknown  | keyword  |   | `inbound`  |
| <a name="network.forwarded_ip"></a>`network.forwarded_ip`  | forwarded_ip indicates the host IP address when the source IP address is the proxy.  | ip  |   | `192.1.1.2`  |
| <a name="network.inbound.bytes"></a>`network.inbound.bytes`  | Network inbound bytes.  | long  |   | `184`  |
| <a name="network.inbound.packets"></a>`network.inbound.packets`  | Network inbound packets.  | long  |   | `12`  |
| <a name="network.outbound.bytes"></a>`network.outbound.bytes`  | Network outbound bytes.  | long  |   | `184`  |
| <a name="network.outbound.packets"></a>`network.outbound.packets`  | Network outbound packets.  | long  |   | `12`  |


## <a name="organization"></a> Organization fields

The organization namespace can be used to enrich data with information from which organization the data belongs.

This can be useful if data should stored in the same index should be sometimes filtered or organized by one or multiple organizations.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="organization.name"></a>`organization.name`  | Organization name.  | text  |   |   |
| <a name="organization.id"></a>`organization.id`  | Unique identifier for the organization.  | keyword  |   |   |


## <a name="process"></a> Process fields

These fields contain information about a process.

If metrics information is collected for a process and a process id / name shows up in a log message, these fields should help to correlated the two. It is expected that the `process.pid` will often also stay in the metric itself and only copied to the global field for correlation.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="process.args"></a>`process.args`  | Process arguments.<br/>May be filtered to protect sensitive information.  | keyword  |   | `['-l', 'user', '10.0.0.16']`  |
| <a name="process.name"></a>`process.name`  | Process name.<br/>This is sometimes also known as program name or similar.  | keyword  |   | `ssh`  |
| <a name="process.pid"></a>`process.pid`  | Process id.  | long  |   |   |
| <a name="process.ppid"></a>`process.ppid`  | Process parent id.  | long  |   |   |
| <a name="process.title"></a>`process.title`  | Process title.<br/>The proctitle, often the same as process name.  | keyword  |   |   |


## <a name="service"></a> Service fields

The service fields describe the service for / from which the data was collected.

If logs or metrics are collected from Redis, `service.name` would be `redis`. This allows to find and correlate logs for a specific service and even version with `service.version`.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="service.id"></a>`service.id`  | Unique identifier of the running service.<br/>This id should uniquely identify this service. This makes it possible to correlate logs and metrics for one specific service. For example in case of issues with one redis instance, it's possible to filter on the id to see metrics and logs for this single instance.  | keyword  |   | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6`  |
| <a name="service.name"></a>`service.name`  | Name of the service data is collected from.<br/>The name can be used to group logs and metrics together from one service and correlate them.  | keyword  |   | `elasticsearch`  |
| <a name="service.type"></a>`service.type`  | Service type.  | keyword  |   |   |
| <a name="service.state"></a>`service.state`  | Current state of the service.  | keyword  |   |   |
| <a name="service.version"></a>`service.version`  | Version of the service the data was collected from.<br/>This allows to look at a data set only for a specific version of a service.  | keyword  |   | `3.2.4`  |
| <a name="service.ephemeral_id"></a>`service.ephemeral_id`  | Ephemeral identifier of this service if one exists.<br/>This id compared to id normally changes across restarts.  | keyword  |   | `8a4f500f`  |


## <a name="source"></a> Source fields

Source fields describe details about the source of where the event is coming from.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="source.ip"></a>`source.ip`  | IP address of the source.<br/>This can be on or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="source.hostname"></a>`source.hostname`  | Hostname of the source.  | keyword  |   |   |
| <a name="source.port"></a>`source.port`  | Port of the source.  | long  |   |   |
| <a name="source.mac"></a>`source.mac`  | MAC address of the source.  | keyword  |   |   |
| <a name="source.domain"></a>`source.domain`  | Source domain.  | keyword  |   |   |
| <a name="source.subdomain"></a>`source.subdomain`  | Source subdomain.  | keyword  |   |   |


## <a name="url"></a> URL fields

A complete URL, with scheme, host, and path.

The URL object can be reused in other prefixes like `host.url.*` for example. It is important that whenever URL is used that the same structure is used.

`url.href` is a [multi field](https://www.elastic.co/guide/en/ elasticsearch/reference/6.2/ multi-fields.html#_multi_fields_with_multiple_analyzers) which means the data is stored as keyword `url.href` and test `url.href.analyzed`. The advantage of this is that for running a query against only a part of the url still works without having to split up the URL in all its part on ingest time.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="url.href"></a>`url.href`  | href contains the full url. The field is stored as keyword.<br/>`href` is an analyzed field so the parsed information can be accessed through `href.analyzed` in quries.  | keyword  |   | `https://elastic.co:443/search?q=elasticsearch#top`  |
| <a name="url.href.analyzed"></a>`url.href.analyzed`  |   | text  | 1  |   |
| <a name="url.scheme"></a>`url.scheme`  | The scheme of the request, e.g. "https".<br/>Note: The `:` is not part of the scheme.  | keyword  |   | `https`  |
| <a name="url.host.name"></a>`url.host.name`  | The hostname of the request, e.g. "example.com".<br/>For correlation the this field can be copied into the `host.name` field.  | keyword  |   | `elastic.co`  |
| <a name="url.port"></a>`url.port`  | The port of the request, e.g. 443.  | integer  |   | `443`  |
| <a name="url.path"></a>`url.path`  | The path of the request, e.g. "/search".  | text  |   |   |
| <a name="url.path.raw"></a>`url.path.raw`  | The url path. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.query"></a>`url.query`  | The query field describes the query string of the request, e.g. "q=elasticsearch".<br/>The `?` is excluded from the query string. In case an URL contains no `?` it is expected that the query field is left out. In case there is a `?` but no query, the query field is expected to exist with an empty string. Like this the `exists` query can be used to differentiate between the two cases.  | text  |   |   |
| <a name="url.query.raw"></a>`url.query.raw`  | The url query part. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.fragment"></a>`url.fragment`  | The part of the url after the `#`, e.g. "top".<br/>The `#` is not part of the fragment.  | keyword  |   |   |
| <a name="url.username"></a>`url.username`  | The username of the request.  | keyword  |   |   |
| <a name="url.password"></a>`url.password`  | The password of the request.  | keyword  |   |   |


## <a name="user"></a> User fields

The user fields are used to describe user information as part of the event.

All fields in user can have one or multiple entries. If a user has more then one id, an array with the ids must be provided.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user.id"></a>`user.id`  | One or multiple unique identifiers of the user.  | keyword  |   |   |
| <a name="user.name"></a>`user.name`  | Name of the user.<br/>As the field is a keyword, the field will not be tokenized.  | keyword  |   |   |
| <a name="user.email"></a>`user.email`  | User email address.  | keyword  |   |   |
| <a name="user.hash"></a>`user.hash`  | Unique user hash to correlate information for a user in anonymized form.<br/>This is useful in case `user.id` or `user.name` cannot be used because it contains confidential information.  | keyword  |   |   |


## <a name="user_agent"></a> User agent fields

The user_agent fields are normally coming from a browser request.

These are common to show up in web service logs coming from the parsed user agent string.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user_agent.raw"></a>`user_agent.raw`  | Unparsed version of the user_agent.  | text  |   |   |
| <a name="user_agent.device"></a>`user_agent.device`  | The name of the physical device.  | keyword  |   |   |
| <a name="user_agent.version"></a>`user_agent.version`  | Version of the physical device.  | keyword  |   |   |
| <a name="user_agent.major"></a>`user_agent.major`  | The major version of the user agent.  | long  |   |   |
| <a name="user_agent.minor"></a>`user_agent.minor`  | The minor version of the user agent.  | long  |   |   |
| <a name="user_agent.patch"></a>`user_agent.patch`  | The patch version of the user agent.  | keyword  |   |   |
| <a name="user_agent.name"></a>`user_agent.name`  | The name of the user agent.  | keyword  |   | `Chrome`  |
| <a name="user_agent.os.name"></a>`user_agent.os.name`  | The name of the operating system.  | keyword  |   |   |
| <a name="user_agent.os.version"></a>`user_agent.os.version`  | Version of the operating system.  | keyword  |   |   |
| <a name="user_agent.os.major"></a>`user_agent.os.major`  | The major version of the operating system.  | long  |   |   |
| <a name="user_agent.os.minor"></a>`user_agent.os.minor`  | The minor version of the operating system.  | long  |   |   |
| <a name="user_agent.os.name"></a>`user_agent.os.name`  | The name of the operating system.  | keyword  |   |   |





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
