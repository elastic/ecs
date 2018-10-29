## Kubernetes use case

You can monitor containers running in a Kubernetes cluster by adding Kubernetes-specific information under `kubernetes.`


### <a name="kubernetes"></a> Kubernetes fields


| Field  | Description  | Level  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| [container.id](https://github.com/elastic/ecs#container.id)  | Unique container id. | core | keyword |  | `fdbef803fa2b` |
| [container.name](https://github.com/elastic/ecs#container.name)  | Container name. | extended | keyword |  |  |
| [host.hostname](https://github.com/elastic/ecs#host.hostname)  | Hostname of the host.<br/>It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use. | core | keyword |  | `kube-high-cpu-42` |
| <a name="kubernetes.pod.name"></a>*kubernetes.pod.name* | *Kubernetes pod name* | (use case) | keyword |  | `foo-webserver` |
| <a name="kubernetes.namespace"></a>*kubernetes.namespace* | *Kubernetes namespace* | (use case) | keyword |  | `foo-team` |
| <a name="kubernetes.labels"></a>*kubernetes.labels* | *Kubernetes labels map* | (use case) | object |  |  |
| <a name="kubernetes.annotations"></a>*kubernetes.annotations* | *Kubernetes annotations map* | (use case) | object |  |  |
| <a name="kubernetes.container.name"></a>*kubernetes.container.name* | *Kubernetes container name. This name is unique within the pod only. It is different from the `container.name` field.* | (use case) | keyword |  |  |



