## Kubernetes use case

You can monitor containers running in a Kubernetes cluster by adding Kubernetes-specific information under `kubernetes.`


### <a name="kubernetes"></a> Kubernetes fields


| Field  | Level  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| [container.id](https://github.com/elastic/ecs#container.id)  | core | Unique container id. | keyword |  |
| [container.name](https://github.com/elastic/ecs#container.name)  | extended | Container name. | keyword |  |
| [host.hostname](https://github.com/elastic/ecs#host.hostname)  | core | Hostname of the host.<br/>It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use. | keyword |  |
| <a name="kubernetes.pod.name"></a>*kubernetes.pod.name* | (use case) | *Kubernetes pod name* | keyword |  |
| <a name="kubernetes.namespace"></a>*kubernetes.namespace* | (use case) | *Kubernetes namespace* | keyword |  |
| <a name="kubernetes.labels"></a>*kubernetes.labels* | (use case) | *Kubernetes labels map* | object |  |
| <a name="kubernetes.annotations"></a>*kubernetes.annotations* | (use case) | *Kubernetes annotations map* | object |  |
| <a name="kubernetes.container.name"></a>*kubernetes.container.name* | (use case) | *Kubernetes container name. This name is unique within the pod only. It is different from the `container.name` field.* | keyword |  |



