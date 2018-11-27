## Kubernetes use case

You can monitor containers running in a Kubernetes cluster by adding Kubernetes-specific information under `kubernetes.`


### <a name="kubernetes"></a> Kubernetes fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| [container.id](../README.md#container.id)  | Unique container id. | core | keyword | `fdbef803fa2b` |
| [container.name](../README.md#container.name)  | Container name. | extended | keyword |  |
| [host.hostname](../README.md#host.hostname)  | Hostname of the host.<br/>It normally contains what the `hostname` command returns on the host machine. | core | keyword | `kube-high-cpu-42` |
| <a name="kubernetes.pod.name"></a>*kubernetes.pod.name* | *Kubernetes pod name* | (use case) | keyword | `foo-webserver` |
| <a name="kubernetes.namespace"></a>*kubernetes.namespace* | *Kubernetes namespace* | (use case) | keyword | `foo-team` |
| <a name="kubernetes.labels"></a>*kubernetes.labels* | *Kubernetes labels map* | (use case) | object |  |
| <a name="kubernetes.annotations"></a>*kubernetes.annotations* | *Kubernetes annotations map* | (use case) | object |  |
| <a name="kubernetes.container.name"></a>*kubernetes.container.name* | *Kubernetes container name. This name is unique within the pod only. It is different from the `container.name` field.* | (use case) | keyword |  |



