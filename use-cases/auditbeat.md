## Auditbeat use case

ECS usage in Auditbeat.

### <a name="auditbeat"></a> Auditbeat fields


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| [`event.module`](https://github.com/elastic/ecs#event.module)  | Auditbeat module name.  |   |   |   |
| [`file.*`](https://github.com/elastic/ecs#file.*)  | File attributes.<br/>  |   |   |   |
| [`file.path`](https://github.com/elastic/ecs#file.path)  | The path to the file.  | text  |   |   |
| [`file.path.raw`](https://github.com/elastic/ecs#file.path.raw)  | The path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| [`file.target_path`](https://github.com/elastic/ecs#file.target_path)  | The target path for symlinks.  | keyword  |   |   |
| [`file.type`](https://github.com/elastic/ecs#file.type)  | The file type (file, dir, or symlink).  | keyword  |   |   |
| [`file.device`](https://github.com/elastic/ecs#file.device)  | The device.  | keyword  |   |   |
| [`file.inode`](https://github.com/elastic/ecs#file.inode)  | The inode representing the file in the filesystem.  | keyword  |   |   |
| [`file.uid`](https://github.com/elastic/ecs#file.uid)  | The user ID (UID) or security identifier (SID) of the file owner.  | keyword  |   |   |
| [`file.owner`](https://github.com/elastic/ecs#file.owner)  | The file owner's username.  | keyword  |   |   |
| [`file.gid`](https://github.com/elastic/ecs#file.gid)  | The primary group ID (GID) of the file.  | keyword  |   |   |
| [`file.group`](https://github.com/elastic/ecs#file.group)  | The primary group name of the file.  | keyword  |   |   |
| [`file.mode`](https://github.com/elastic/ecs#file.mode)  | The mode of the file in octal representation.  | keyword  |   | `416`  |
| [`file.size`](https://github.com/elastic/ecs#file.size)  | The file size in bytes (field is only added when `type` is `file`).  | long  |   |   |
| [`file.mtime`](https://github.com/elastic/ecs#file.mtime)  | The last modified time of the file (time when content was modified).  | date  |   |   |
| [`file.ctime`](https://github.com/elastic/ecs#file.ctime)  | The last change time of the file (time when metadata was changed).  | date  |   |   |



