<!--

WARNING: README.md is generated based on the files under docs/
and the field descriptions in the YAML files under schemas/.

Therefore if you want to modify anything in this readme, please perform
your changes in these other locations, then run `make`.

See CONTRIBUTING.md for more details on setting up.

-->

**WARNING: THIS IS WORK IN PROGRESS**

# Elastic Common Schema (ECS)

The Elastic Common Schema (ECS) defines a common set of fields for
ingesting data into Elasticsearch. A common schema helps you correlate
data from sources like logs and metrics or IT operations
analytics and security analytics.

ECS is still under development and backward compatibility is not guaranteed. Any
feedback on the general structure, missing fields, or existing fields is appreciated.
For contributions please read the [Contributing Guide](CONTRIBUTING.md).

<a name="ecs-version"></a>The current version of ECS is `0.1.0`.

# In this readme

* [Fields](#fields)
* [Use cases](#use-cases)
* [Implementing ECS](#implementing-ecs)
* [FAQ](#faq-ecs)

# <a name="fields"></a>Fields

ECS defines these fields.
 * [Base fields](#base)
 * [Agent fields](#agent)
 * [Cloud fields](#cloud)
 * [Container fields](#container)
 * [Destination fields](#destination)
 * [Device fields](#device)
 * [Error fields](#error)
 * [Event fields](#event)
 * [File fields](#file)
 * [Geo fields](#geo)
 * [Host fields](#host)
 * [HTTP fields](#http)
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
| <a name="@timestamp"></a>@timestamp  | Date/time when the event originated.<br/>For log events this is the date/time when the event was generated, and not when it was read.<br/>Required field for all events.  | date  |   | `2016-05-23T08:05:34.853Z`  |
| <a name="tags"></a>tags  | List of keywords used to tag each event.  | keyword  |   | `["production", "env2"]`  |
| <a name="labels"></a>labels  | Key/value pairs.<br/>Can be used to add meta information to events. Should not contain nested objects. All values are stored as keyword.<br/>Example: `docker` and `k8s` labels.  | object  |   | `{'application': 'foo-bar', 'env': 'production'}`  |
| <a name="message"></a>message  | For log events the message field contains the log message.<br/>In other use cases the message field can be used to concatenate different values which are then freely searchable. If multiple messages exist, they can be combined into one message.  | text  |   | `Hello World`  |


## <a name="agent"></a> Agent fields

The agent fields contain the data about the agent/client/shipper that created the event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="agent.version"></a>agent.version  | Version of the agent.  | keyword  |   | `6.0.0-rc2`  |
| <a name="agent.name"></a>agent.name  | Name of the agent.  | keyword  |   | `filebeat`  |
| <a name="agent.id"></a>agent.id  | Unique identifier of this agent (if one exists).<br/>Example: For Beats this would be beat.id.  | keyword  |   | `8a4f500d`  |
| <a name="agent.ephemeral_id"></a>agent.ephemeral_id  | Ephemeral identifier of this agent (if one exists).<br/>This id normally changes across restarts, but `agent.id` does not.  | keyword  |   | `8a4f500f`  |


Examples: In the case of Beats for logs, the agent.name is filebeat. For APM, it is the agent running in the app/service. The agent information does not change if data is sent through queuing systems like Kafka, Redis, or processing systems such as Logstash or APM Server.


## <a name="cloud"></a> Cloud fields

Fields related to the cloud or infrastructure the events are coming from.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="cloud.provider"></a>cloud.provider  | Name of the cloud provider. Example values are ec2, gce, or digitalocean.  | keyword  |   | `ec2`  |
| <a name="cloud.availability_zone"></a>cloud.availability_zone  | Availability zone in which this host is running.  | keyword  |   | `us-east-1c`  |
| <a name="cloud.region"></a>cloud.region  | Region in which this host is running.  | keyword  |   | `us-east-1`  |
| <a name="cloud.instance.id"></a>cloud.instance.id  | Instance ID of the host machine.  | keyword  |   | `i-1234567890abcdef0`  |
| <a name="cloud.instance.name"></a>cloud.instance.name  | Instance name of the host machine.  | keyword  |   |   |
| <a name="cloud.machine.type"></a>cloud.machine.type  | Machine type of the host machine.  | keyword  |   | `t2.medium`  |
| <a name="cloud.account.id"></a>cloud.account.id  | The cloud account or organization id used to identify different entities in a multi-tenant environment.<br/>Examples: AWS account id, Google Cloud ORG Id, or other unique identifier.  | keyword  |   | `666777888999`  |


Examples: If Metricbeat is running on an EC2 host and fetches data from its host, the cloud info contains the data about this machine. If Metricbeat runs on a remote machine outside the cloud and fetches data from a service running in the cloud, the field contains cloud data from the machine the service is running on.


## <a name="container"></a> Container fields

Container fields are used for meta information about the specific container that is the source of information. These fields help correlate data based containers from any runtime.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="container.runtime"></a>container.runtime  | Runtime managing this container.  | keyword  |   | `docker`  |
| <a name="container.id"></a>container.id  | Unique container id.  | keyword  |   |   |
| <a name="container.image.name"></a>container.image.name  | Name of the image the container was built on.  | keyword  |   |   |
| <a name="container.image.tag"></a>container.image.tag  | Container image tag.  | keyword  |   |   |
| <a name="container.name"></a>container.name  | Container name.  | keyword  |   |   |
| <a name="container.labels"></a>container.labels  | Image labels.  | object  |   |   |


## <a name="destination"></a> Destination fields

Destination fields describe details about the destination of a packet/event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="destination.ip"></a>destination.ip  | IP address of the destination.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="destination.hostname"></a>destination.hostname  | Hostname of the destination.  | keyword  |   |   |
| <a name="destination.port"></a>destination.port  | Port of the destination.  | long  |   |   |
| <a name="destination.mac"></a>destination.mac  | MAC address of the destination.  | keyword  |   |   |
| <a name="destination.domain"></a>destination.domain  | Destination domain.  | keyword  |   |   |
| <a name="destination.subdomain"></a>destination.subdomain  | Destination subdomain.  | keyword  |   |   |


## <a name="device"></a> Device fields

Device fields are used to provide additional information about the device that is the source of the information. This could be a firewall, network device, etc.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="device.mac"></a>device.mac  | MAC address of the device  | keyword  |   |   |
| <a name="device.ip"></a>device.ip  | IP address of the device.  | ip  |   |   |
| <a name="device.hostname"></a>device.hostname  | Hostname of the device.  | keyword  |   |   |
| <a name="device.vendor"></a>device.vendor  | Device vendor information.  | text  |   |   |
| <a name="device.version"></a>device.version  | Device version.  | keyword  |   |   |
| <a name="device.serial_number"></a>device.serial_number  | Device serial number.  | keyword  |   |   |
| <a name="device.type"></a>device.type  | The type of the device the data is coming from.<br/>There is no predefined list of device types. Some examples are `endpoint`, `firewall`, `ids`, `ips`, `proxy`.  | keyword  |   | `firewall`  |


## <a name="error"></a> Error fields

These fields can represent errors of any kind. Use them for errors that happen while fetching events or in cases where the event itself contains an error.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="error.id"></a>error.id  | Unique identifier for the error.  | keyword  |   |   |
| <a name="error.message"></a>error.message  | Error message.  | text  |   |   |
| <a name="error.code"></a>error.code  | Error code describing the error.  | keyword  |   |   |


## <a name="event"></a> Event fields

The event fields are used for context information about the data itself.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="event.id"></a>event.id  | Unique ID to describe the event.  | keyword  |   | `8a4f500d`  |
| <a name="event.category"></a>event.category  | Event category.<br/>This can be a user defined category.  | keyword  |   | `metrics`  |
| <a name="event.type"></a>event.type  | A type given to this kind of event which can be used for grouping.<br/>This is normally defined by the user.  | keyword  |   | `nginx-stats-metrics`  |
| <a name="event.action"></a>event.action  | The action captured by the event. The type of action will vary from system to system but is likely to include actions by security services, such as blocking or quarantining; as well as more generic actions such as login events, file i/o or proxy forwarding events.<br/>The value is normally defined by the user.  | keyword  |   | `reject`  |
| <a name="event.module"></a>event.module  | Name of the module this data is coming from.<br/>This information is coming from the modules used in Beats or Logstash.  | keyword  |   | `mysql`  |
| <a name="event.dataset"></a>event.dataset  | Name of the dataset.<br/>The concept of a `dataset` (fileset / metricset) is used in Beats as a subset of modules. It contains the information which is currently stored in metricset.name and metricset.module or fileset.name.  | keyword  |   | `stats`  |
| <a name="event.severity"></a>event.severity  | Severity describes the severity of the event. What the different severity values mean can very different between use cases. It's up to the implementer to make sure severities are consistent across events.  | long  |   | `7`  |
| <a name="event.original"></a>event.original  | Raw text message of entire event. Used to demonstrate log integrity.<br/>This field is not indexed and doc_values are disabled. It cannot be searched, but it can be retrieved from `_source`.  | keyword  |   | `Sep 19 08:26:10 host CEF:0&#124;Security&#124; threatmanager&#124;1.0&#124;100&#124; worm successfully stopped&#124;10&#124;src=10.0.0.1 dst=2.1.2.2spt=1232`  |
| <a name="event.hash"></a>event.hash  | Hash (perhaps logstash fingerprint) of raw field to be able to demonstrate log integrity.  | keyword  |   | `123456789012345678901234567890ABCD`  |
| <a name="event.version"></a>event.version  | The version field contains the version an event for ECS adheres to.<br/>This field should be provided as part of each event to make it possible to detect to which ECS version an event belongs.<br/>event.version is a required field and must exist in all events. It describes which ECS version the event adheres to.<br/>The current version is 0.1.0.  | keyword  |   | `0.1.0`  |
| <a name="event.duration"></a>event.duration  | Duration of the event in nanoseconds.  | long  |   |   |
| <a name="event.created"></a>event.created  | event.created contains the date when the event was created.<br/>This timestamp is distinct from @timestamp in that @timestamp contains the processed timestamp. For logs these two timestamps can be different as the timestamp in the log line and when the event is read for example by Filebeat are not identical. `@timestamp` must contain the timestamp extracted from the log line, event.created when the log line is read. The same could apply to package capturing where @timestamp contains the timestamp extracted from the network package and event.created when the event was created.<br/>In case the two timestamps are identical, @timestamp should be used.  | date  |   |   |
| <a name="event.risk_score"></a>event.risk_score  | Risk score or priority of the event (e.g. security solutions). Use your system's original value here.  | float  |   |   |
| <a name="event.risk_score_norm"></a>event.risk_score_norm  | Normalized risk score or priority of the event, on a scale of 0 to 100.<br/>This is mainly useful if you use more than one system that assigns risk scores, and you want to see a normalized value across all systems.  | float  |   |   |


## <a name="file"></a> File fields

File fields provide details about each file.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="file.path"></a>file.path  | Path to the file.  | text  |   |   |
| <a name="file.path.keyword"></a>file.path.keyword  | Path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.target_path"></a>file.target_path  | Target path for symlinks.  | text  |   |   |
| <a name="file.target_path.keyword"></a>file.target_path.keyword  | Path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="file.extension"></a>file.extension  | File extension.<br/>This should allow easy filtering by file extensions.  | keyword  |   | `png`  |
| <a name="file.type"></a>file.type  | File type (file, dir, or symlink).  | keyword  |   |   |
| <a name="file.device"></a>file.device  | Device that is the source of the file.  | keyword  |   |   |
| <a name="file.inode"></a>file.inode  | Inode representing the file in the filesystem.  | keyword  |   |   |
| <a name="file.uid"></a>file.uid  | The user ID (UID) or security identifier (SID) of the file owner.  | keyword  |   |   |
| <a name="file.owner"></a>file.owner  | File owner's username.  | keyword  |   |   |
| <a name="file.gid"></a>file.gid  | Primary group ID (GID) of the file.  | keyword  |   |   |
| <a name="file.group"></a>file.group  | Primary group name of the file.  | keyword  |   |   |
| <a name="file.mode"></a>file.mode  | Mode of the file in octal representation.  | keyword  |   | `416`  |
| <a name="file.size"></a>file.size  | File size in bytes (field is only added when `type` is `file`).  | long  |   |   |
| <a name="file.mtime"></a>file.mtime  | Last time file content was modified.  | date  |   |   |
| <a name="file.ctime"></a>file.ctime  | Last time file metadata changed.  | date  |   |   |


## <a name="geo"></a> Geo fields

Geo fields can carry data about a specific location related to an event or geo information for an IP field.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="geo.continent_name"></a>geo.continent_name  | Name of the continent.  | keyword  |   |   |
| <a name="geo.country_iso_code"></a>geo.country_iso_code  | Country ISO code.  | keyword  |   |   |
| <a name="geo.location"></a>geo.location  | Longitude and latitude.  | geo_point  |   |   |
| <a name="geo.region_name"></a>geo.region_name  | Region name.  | keyword  |   |   |
| <a name="geo.city_name"></a>geo.city_name  | City name.  | keyword  |   |   |


## <a name="host"></a> Host fields

Host fields provide information related to a host. A host can be a physical machine, a virtual machine, or a Docker container.

Normally the host information is related to the machine on which the event was generated/collected, but they can be used differently if needed.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="host.name"></a>host.name  | host.name is the hostname of the host.<br/>It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use.  | keyword  |   |   |
| <a name="host.id"></a>host.id  | Unique host id.<br/>As hostname is not always unique, use values that are meaningful in your environment.<br/>Example: The current usage of `beat.name`.  | keyword  |   |   |
| <a name="host.ip"></a>host.ip  | Host ip address.  | ip  |   |   |
| <a name="host.mac"></a>host.mac  | Host mac address.  | keyword  |   |   |
| <a name="host.type"></a>host.type  | Type of host.<br/>For Cloud providers this can be the machine type like `t2.medium`. If vm, this could be the container, for example, or other information meaningful in your environment.  | keyword  |   |   |
| <a name="host.os.platform"></a>host.os.platform  | Operating system platform (centos, ubuntu, windows, etc.)  | keyword  |   | `darwin`  |
| <a name="host.os.name"></a>host.os.name  | Operating system name.  | keyword  |   | `Mac OS X`  |
| <a name="host.os.family"></a>host.os.family  | OS family (redhat, debian, freebsd, windows, etc.)  | keyword  |   | `debian`  |
| <a name="host.os.version"></a>host.os.version  | Operating system version.  | keyword  |   | `10.12.6`  |
| <a name="host.architecture"></a>host.architecture  | Operating system architecture.  | keyword  |   | `x86_64`  |


## <a name="http"></a> HTTP fields

Fields related to HTTP requests and responses.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="http.request.method"></a>http.request.method  | Http request method.  | keyword  |   | `GET, POST, PUT`  |
| <a name="http.response.status_code"></a>http.response.status_code  | Http response status code.  | long  |   | `404`  |
| <a name="http.response.body"></a>http.response.body  | The full http response body.  | text  |   | `Hello world`  |
| <a name="http.version"></a>http.version  | Http version.  | keyword  |   | `1.1`  |


## <a name="log"></a> Log fields

Fields which are specific to log events.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="log.level"></a>log.level  | Log level of the log event.<br/>Some examples are `WARN`, `ERR`, `INFO`.  | keyword  |   | `ERR`  |
| <a name="log.original"></a>log.original  | This is the original log message and contains the full log message before splitting it up in multiple parts.<br/>In contrast to the `message` field which can contain an extracted part of the log message, this field contains the original, full log message. It can have already some modifications applied like encoding or new lines removed to clean up the log message.<br/>This field is not indexed and doc_values are disabled so it can't be queried but the value can be retrieved from `_source`.  | keyword  |   | `Sep 19 08:26:10 localhost My log`  |


## <a name="network"></a> Network fields

Fields related to network data.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="network.name"></a>network.name  | Name given by operators to sections of their network.  | text  |   | `Guest Wifi`  |
| <a name="network.name.keyword"></a>network.name.keyword  | Name given by operators to sections of their network.  | keyword  | 1  |   |
| <a name="network.protocol"></a>network.protocol  | Network protocol name.  | keyword  |   | `http`  |
| <a name="network.direction"></a>network.direction  | Direction of the network traffic.<br/>Recommended values are:<br/>  * inbound<br/>  * outbound<br/>  * unknown  | keyword  |   | `inbound`  |
| <a name="network.forwarded_ip"></a>network.forwarded_ip  | Host IP address when the source IP address is the proxy.  | ip  |   | `192.1.1.2`  |
| <a name="network.inbound.bytes"></a>network.inbound.bytes  | Network inbound bytes.  | long  |   | `184`  |
| <a name="network.inbound.packets"></a>network.inbound.packets  | Network inbound packets.  | long  |   | `12`  |
| <a name="network.outbound.bytes"></a>network.outbound.bytes  | Network outbound bytes.  | long  |   | `184`  |
| <a name="network.outbound.packets"></a>network.outbound.packets  | Network outbound packets.  | long  |   | `12`  |
| <a name="network.total.bytes"></a>network.total.bytes  | Network total bytes. The sum of inbound.bytes + outbound.bytes.  | long  |   | `368`  |
| <a name="network.total.packets"></a>network.total.packets  | Network outbound packets. The sum of inbound.packets + outbound.packets  | long  |   | `24`  |


## <a name="organization"></a> Organization fields

The organization fields enrich data with information about the company or entity the data is associated with. These fields help you arrange or filter data stored in an index by one or multiple organizations.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="organization.name"></a>organization.name  | Organization name.  | text  |   |   |
| <a name="organization.id"></a>organization.id  | Unique identifier for the organization.  | keyword  |   |   |


## <a name="os"></a> Operating System fields

The OS fields contain information about the operating system. These fields are often used inside other prefixes, such as `host.os.*` or `user_agent.os.*`.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="os.platform"></a>os.platform  | Operating system platform (such centos, ubuntu, windows).  | keyword  |   | `darwin`  |
| <a name="os.name"></a>os.name  | Operating system name.  | keyword  |   | `Mac OS X`  |
| <a name="os.family"></a>os.family  | OS family (such as redhat, debian, freebsd, windows).  | keyword  |   | `debian`  |
| <a name="os.version"></a>os.version  | Operating system version as a raw string.  | keyword  |   | `10.12.6-rc2`  |
| <a name="os.kernel"></a>os.kernel  | Operating system kernel version as a raw string.  | keyword  |   | `4.4.0-112-generic`  |


## <a name="process"></a> Process fields

These fields contain information about a process. These fields can help you correlate metrics information with a process id/name from a log message.  The `process.pid` often stays in the metric itself and is copied to the global field for correlation.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="process.args"></a>process.args  | Process arguments.<br/>May be filtered to protect sensitive information.  | keyword  |   | `['-l', 'user', '10.0.0.16']`  |
| <a name="process.name"></a>process.name  | Process name.<br/>Sometimes called program name or similar.  | keyword  |   | `ssh`  |
| <a name="process.pid"></a>process.pid  | Process id.  | long  |   |   |
| <a name="process.ppid"></a>process.ppid  | Process parent id.  | long  |   |   |
| <a name="process.title"></a>process.title  | Process title.<br/>The proctitle, some times the same as process name. Can also be different: for example a browser setting its title to the web page currently opened.  | keyword  |   |   |


## <a name="service"></a> Service fields

The service fields describe the service for or from which the data was collected. These fields help you find and correlate logs for a specific service and version.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="service.id"></a>service.id  | Unique identifier of the running service.<br/>This id should uniquely identify this service. This makes it possible to correlate logs and metrics for one specific service.<br/>Example: If you are experiencing issues with one redis instance, you can filter on that id to see metrics and logs for that single instance.  | keyword  |   | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6`  |
| <a name="service.name"></a>service.name  | Name of the service data is collected from.<br/>The name can be used to group and correlate logs and metrics from one service.<br/>Example: If logs or metrics are collected from Redis, `service.name` would be `redis`.  | keyword  |   | `elasticsearch`  |
| <a name="service.type"></a>service.type  | Service type.  | keyword  |   |   |
| <a name="service.state"></a>service.state  | Current state of the service.  | keyword  |   |   |
| <a name="service.version"></a>service.version  | Version of the service the data was collected from.<br/>This allows to look at a data set only for a specific version of a service.  | keyword  |   | `3.2.4`  |
| <a name="service.ephemeral_id"></a>service.ephemeral_id  | Ephemeral identifier of this service (if one exists).<br/>This id normally changes across restarts, but `service.id` does not.  | keyword  |   | `8a4f500f`  |


## <a name="source"></a> Source fields

Source fields describe details about the source of the event.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="source.ip"></a>source.ip  | IP address of the source.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   |   |
| <a name="source.hostname"></a>source.hostname  | Hostname of the source.  | keyword  |   |   |
| <a name="source.port"></a>source.port  | Port of the source.  | long  |   |   |
| <a name="source.mac"></a>source.mac  | MAC address of the source.  | keyword  |   |   |
| <a name="source.domain"></a>source.domain  | Source domain.  | keyword  |   |   |
| <a name="source.subdomain"></a>source.subdomain  | Source subdomain.  | keyword  |   |   |


## <a name="url"></a> URL fields

URL fields provide a complete URL, with scheme, host, and path. The URL object can be reused in other prefixes, such as `host.url.*` for example. Keep the structure consistent whenever you use URL fields.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="url.href"></a>url.href  | Full url. The field is stored as keyword.<br/>`url.href` is a [multi field](https://www.elastic.co/guide/en/ elasticsearch/reference/6.2/ multi-fields.html#_multi_fields_with_multiple_analyzers). The data is stored as keyword `url.href` and test `url.href.analyzed`. These fields enable you to run a query against part of the url still works splitting up the URL at ingest time.<br/>`href` is an analyzed field so the parsed information can be accessed through `href.analyzed` in queries.  | text  |   | `https://elastic.co:443/search?q=elasticsearch#top`  |
| <a name="url.href.keyword"></a>url.href.keyword  | The full URL. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.scheme"></a>url.scheme  | Scheme of the request, such as "https".<br/>Note: The `:` is not part of the scheme.  | keyword  |   | `https`  |
| <a name="url.host.name"></a>url.host.name  | Hostname of the request, such as "example.com".<br/>For correlation the this field can be copied into the `host.name` field.  | keyword  |   | `elastic.co`  |
| <a name="url.port"></a>url.port  | Port of the request, such as 443.  | integer  |   | `443`  |
| <a name="url.path"></a>url.path  | Path of the request, such as "/search".  | text  |   |   |
| <a name="url.path.keyword"></a>url.path.keyword  | URL path. A non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.query"></a>url.query  | The query field describes the query string of the request, such as "q=elasticsearch".<br/>The `?` is excluded from the query string. If a URL contains no `?`, there is no query field. If there is a `?` but no query, the query field exists with an empty string. The `exists` query can be used to differentiate between the two cases.  | text  |   |   |
| <a name="url.query.keyword"></a>url.query.keyword  | URL query part. A non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| <a name="url.fragment"></a>url.fragment  | Portion of the url after the `#`, such as "top".<br/>The `#` is not part of the fragment.  | keyword  |   |   |
| <a name="url.username"></a>url.username  | Username of the request.  | keyword  |   |   |
| <a name="url.password"></a>url.password  | Password of the request.  | keyword  |   |   |


## <a name="user"></a> User fields

The user fields describe information about the user that is relevant to  the event. Fields can have one entry or multiple entries. If a user has more than one id, provide an array that includes all of them.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user.id"></a>user.id  | One or multiple unique identifiers of the user.  | keyword  |   |   |
| <a name="user.name"></a>user.name  | Name of the user.<br/>The field is a keyword, and will not be tokenized.  | keyword  |   |   |
| <a name="user.email"></a>user.email  | User email address.  | keyword  |   |   |
| <a name="user.hash"></a>user.hash  | Unique user hash to correlate information for a user in anonymized form.<br/>Useful if `user.id` or `user.name` contain confidential information and cannot be used.  | keyword  |   |   |


## <a name="user_agent"></a> User agent fields

The user_agent fields normally come from a browser request. They often show up in web service logs coming from the parsed user agent string.


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="user_agent.original"></a>user_agent.original  | Unparsed version of the user_agent.  | text  |   |   |
| <a name="user_agent.device"></a>user_agent.device  | Name of the physical device.  | keyword  |   |   |
| <a name="user_agent.version"></a>user_agent.version  | Version of the physical device.  | keyword  |   |   |
| <a name="user_agent.major"></a>user_agent.major  | Major version of the user agent.  | long  |   |   |
| <a name="user_agent.minor"></a>user_agent.minor  | Minor version of the user agent.  | long  |   |   |
| <a name="user_agent.patch"></a>user_agent.patch  | Patch version of the user agent.  | keyword  |   |   |
| <a name="user_agent.name"></a>user_agent.name  | Name of the user agent.  | keyword  |   | `Chrome`  |
| <a name="user_agent.os.name"></a>user_agent.os.name  | Name of the operating system.  | keyword  |   |   |
| <a name="user_agent.os.version"></a>user_agent.os.version  | Version of the operating system.  | keyword  |   |   |
| <a name="user_agent.os.major"></a>user_agent.os.major  | Major version of the operating system.  | long  |   |   |
| <a name="user_agent.os.minor"></a>user_agent.os.minor  | Minor version of the operating system.  | long  |   |   |





# <a name="use-cases"></a>Use cases

These are example on how ECS fields can be used in different use cases. Most use
cases not only contain ECS fields but additional fields which are not in ECS to
describe the full use case. The fields which are not in ECS are in italic.

Contributions of additional uses cases on top of ECS are welcome.

 * [APM](https://github.com/elastic/ecs/blob/master/use-cases/apm.md)
 * [Auditbeat](https://github.com/elastic/ecs/blob/master/use-cases/auditbeat.md)
 * [Beats](https://github.com/elastic/ecs/blob/master/use-cases/beats.md)
 * [Filebeat Apache](https://github.com/elastic/ecs/blob/master/use-cases/filebeat-apache-access.md)
 * [Kubernetes](https://github.com/elastic/ecs/blob/master/use-cases/kubernetes.md)
 * [Logging](https://github.com/elastic/ecs/blob/master/use-cases/logging.md)
 * [Metricbeat](https://github.com/elastic/ecs/blob/master/use-cases/metricbeat.md)
 * [TLS](https://github.com/elastic/ecs/blob/master/use-cases/tls.md)



# <a name="implementing-ecs"></a>Implementing ECS

## Guidelines

* The document MUST have the `@timestamp` field.
* The [data type](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/mapping-types.html) defined for an ECS field MUST be used.
* It SHOULD have the field `event.version` to define which version of ECS it uses.
* As many fields as possible should be mapped to ECS.

**Writing fields**

* All fields must be lower case
* Combine words using underscore
* No special characters except `_`

**Naming fields**

* *Present tense.* Use present tense unless field describes historical information.
* *Singular or plural.* Use singular and plural names properly to reflect the field content. For example, use `requests_per_sec` rather than `request_per_sec`.
* *General to specific.* Organise the prefixes from general to specific to allow grouping fields into objects with a prefix like `host.*`.
* *Avoid repetition.* Avoid stuttering of words. If part of the field name is already in the prefix, do not repeat it. Example: `host.host_ip` should be `host.ip`.
* *Use prefixes.* Fields must be prefixed except for the base fields. For example all `host` fields are prefixed with `host.`. See `dot` notation in FAQ for more details.
* Do not use abbreviations. (A few exceptions like `ip` exist.)

## Understanding ECS conventions

### Multi-fields text indexing

ElasticSearch can index text multiple ways:

* [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) indexing allows for full text search, or searching arbitrary words that
  are part of the field.
* [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) indexing allows for much faster
  [exact match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)
  and [prefix search](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html),
  and allows for [aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
  (what Kibana visualizations are built on).

In some cases, only one type of indexing makes sense for a field.

However there are cases where both types of indexing can be useful, and we want
to index both ways.
As an example, log messages can sometimes be short enough that it makes sense
to sort them by frequency (that's an aggregation). They can also be long and
varied enough that full text search can be useful on them.

Whenever both types of indexing are helpful, we use multi-fields indexing. The
convention used is the following:

* `foo`: `text` indexing.
  The top level of the field (its plain name) is used for full text search.
* `foo.raw`: `keyword` indexing.
  The nested field has suffix `.raw` and is what you will use for aggregations.
  * Performance tip: when filtering your stream in Kibana (or elsewhere), if you
    are filtering for an exact match or doing a prefix search,
    both `text` and `keyword` field can be used, but doing so on the `keyword`
    field (named `.raw`) will be much faster and less memory intensive.

**Keyword only fields**

The fields that only make sense as type `keyword` are not named `foo.raw`, the
plain field (`foo`) will be of type `keyword`, with no nested field.

### IDs are keywords not integers

Despite the fact that IDs are often integers in various systems, this is not
always the case. Since we want to make it possible to map as many data sources
to ECS as possible, we default to using the `keyword` type for IDs.

# <a name="about-ecs"></a>FAQ

## What are the benefits of using ECS?

The benefits to a user adopting these fields and names in their clusters are:

* **Data correlation.** Ability to easily correlate data from the same or different sources, including:
    * data from metrics, logs, and apm
    * data from the same machines/hosts
    * data from the same service
* **Ease of recall.** Improved ability to remember commonly used field names (because there is a single set, not a set per data source)
* **Ease of deduction.** Improved ability to deduce field names (because the field naming follows a small number of rules with few exceptions)
* **Reuse.** Ability to re-use analysis content (searches, visualizations, dashboards, alerts, reports, and ML jobs) across multiple data sources
* **Future proofing.** Ability to use any future Elastic-provided analysis content in your environment without modifications

## What if I have fields that conflict with ECS?

The [rename processor](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/rename-processor.html) can help you resolve field conflicts. For example, imagine that you already have a field called "user," but ECS employs `user` as an object. You can use the rename processor on ingest time to rename your field to the matching ECS field. If your field does not match ECS, you can rename your field to `user.value` instead.

## What if my events have additional fields?

Events may contain fields in addition to ECS fields. These fields can follow the ECS naming and writing rules, but this is not a requirement.

## Why does ECS use a dot notation instead of an underline notation?

There are two common key formats for ingesting data into Elasticsearch:

* Dot notation: `user.firstname: Nicolas`, `user.lastname: Ruflin`
* Underline notation: `user_firstname: Nicolas`, `user_lastname: Ruflin`

For ECS we decided to use the dot notation. Here's some background on this decision.

### What is the difference between the two notations?

Ingesting `user.firstname: Nicolas` and `user.lastname: Ruflin` is identical to ingesting the following JSON:

```
"user": {
  "firstname": "Nicolas",
  "lastname": "Ruflin"
}
```

In Elasticsearch, `user` is represented as an [object datatype](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/object.html). In the case of the underline notation, both are just [string datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).

NOTE: ECS does not use [nested datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html), which are arrays of objects.

### Advantages of dot notation

With dot notation, each prefix in Elasticsearch is an object. Each object can have [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html#object-params) that control how fields inside the object are treated. In the context of ECS, for example, these parameters would allow you to disable dynamic property creation for certain prefixes.

Individual objects give you more flexibility on both the ingest and the event sides.  In Elasticsearch, for example, you can use the remove processor to drop complete objects instead of selecting each key inside. You don't have to know ahead of time which keys will be in an object.

In Beats, you can simplify the creation of events. For example, you can treat each object as an object (or struct in Golang), which makes constructing and modifying each part of the final event easier.

### Disadvantage of dot notation

In Elasticsearch, each key can only have one type. For example, if `user` is an `object`, you can't use it as a `keyword` type in the same index, like `{"user": "nicolas ruflin"}`. This restriction can be an issue in certain datasets. For the ECS data itself, this is not an issue because all fields are predefined.

### What if I already use the underline notation?

Mixing the underline notation with the ECS dot notation is not a problem. As long as there are no conflicts, they can coexist in the same document.
