## Auditbeat use case

ECS usage in Auditbeat.

### <a name="auditbeat"></a> Auditbeat fields


| Field  | Level  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| [event.module](https://github.com/elastic/ecs#event.module)  | core | Auditbeat module name. | keyword |  |
| <a name="file.&ast;"></a>*file.&ast;* |  | *File attributes.<br/>* |  |  |
| [file.path](https://github.com/elastic/ecs#file.path)  | extended | The path to the file. | keyword |  |
| [file.target_path](https://github.com/elastic/ecs#file.target_path)  | extended | The target path for symlinks. | keyword |  |
| [file.type](https://github.com/elastic/ecs#file.type)  | extended | The file type (file, dir, or symlink). | keyword |  |
| [file.device](https://github.com/elastic/ecs#file.device)  | extended | The device. | keyword |  |
| [file.inode](https://github.com/elastic/ecs#file.inode)  | extended | The inode representing the file in the filesystem. | keyword |  |
| [file.uid](https://github.com/elastic/ecs#file.uid)  | extended | The user ID (UID) or security identifier (SID) of the file owner. | keyword |  |
| [file.owner](https://github.com/elastic/ecs#file.owner)  | extended | The file owner's username. | keyword |  |
| [file.gid](https://github.com/elastic/ecs#file.gid)  | extended | The primary group ID (GID) of the file. | keyword |  |
| [file.group](https://github.com/elastic/ecs#file.group)  | extended | The primary group name of the file. | keyword |  |
| [file.mode](https://github.com/elastic/ecs#file.mode)  | extended | The mode of the file in octal representation. | keyword |  |
| [file.size](https://github.com/elastic/ecs#file.size)  | extended | The file size in bytes (field is only added when `type` is `file`). | long |  |
| [file.mtime](https://github.com/elastic/ecs#file.mtime)  | extended | The last modified time of the file (time when content was modified). | date |  |
| [file.ctime](https://github.com/elastic/ecs#file.ctime)  | extended | The last change time of the file (time when metadata was changed). | date |  |
| <a name="hash.&ast;"></a>*hash.&ast;* |  | *Hash fields used in Auditbeat.<br/>The hash field contains cryptographic hashes of data associated with the event (such as a file). The keys are names of cryptographic algorithms. The values are encoded as hexidecimal (lower-case).<br/>All fields in user can have one or multiple entries.<br/>* |  |  |
| <a name="hash.blake2b_256"></a>*hash.blake2b_256* | (use case) | *BLAKE2b-256 hash of the file.* | keyword |  |
| <a name="hash.blake2b_384"></a>*hash.blake2b_384* | (use case) | *BLAKE2b-384 hash of the file.* | keyword |  |
| <a name="hash.blake2b_512"></a>*hash.blake2b_512* | (use case) | *BLAKE2b-512 hash of the file.* | keyword |  |
| <a name="hash.md5"></a>*hash.md5* | (use case) | *MD5 hash.* | keyword |  |
| <a name="hash.sha1"></a>*hash.sha1* | (use case) | *SHA-1 hash.* | keyword |  |
| <a name="hash.sha224"></a>*hash.sha224* | (use case) | *SHA-224 hash (SHA-2 family).* | keyword |  |
| <a name="hash.sha256"></a>*hash.sha256* | (use case) | *SHA-256 hash (SHA-2 family).* | keyword |  |
| <a name="hash.sha384"></a>*hash.sha384* | (use case) | *SHA-384 hash (SHA-2 family).* | keyword |  |
| <a name="hash.sha512"></a>*hash.sha512* | (use case) | *SHA-512 hash (SHA-2 family).* | keyword |  |
| <a name="hash.sha512_224"></a>*hash.sha512_224* | (use case) | *SHA-512/224 hash (SHA-2 family).* | keyword |  |
| <a name="hash.sha512_256"></a>*hash.sha512_256* | (use case) | *SHA-512/256 hash (SHA-2 family).* | keyword |  |
| <a name="hash.sha3_224"></a>*hash.sha3_224* | (use case) | *SHA3-224 hash (SHA-3 family).* | keyword |  |
| <a name="hash.sha3_256"></a>*hash.sha3_256* | (use case) | *SHA3-256 hash (SHA-3 family).* | keyword |  |
| <a name="hash.sha3_384"></a>*hash.sha3_384* | (use case) | *SHA3-384 hash (SHA-3 family).* | keyword |  |
| <a name="hash.sha3_512"></a>*hash.sha3_512* | (use case) | *SHA3-512 hash (SHA-3 family).* | keyword |  |
| <a name="hash.xxh64"></a>*hash.xxh64* | (use case) | *XX64 hash of the file.* | keyword |  |



