## Auditbeat use case

ECS usage in Auditbeat.

### <a name="auditbeat"></a> Auditbeat fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| [event.module](../README.md#event.module)  | Auditbeat module name. | core | keyword | `apache` |
| <a name="file.&ast;"></a>*file.&ast;* | *File attributes.<br/>* |  |  |  |
| [file.path](../README.md#file.path)  | The path to the file. | extended | keyword |  |
| [file.target_path](../README.md#file.target_path)  | The target path for symlinks. | extended | keyword |  |
| [file.type](../README.md#file.type)  | The file type (file, dir, or symlink). | extended | keyword |  |
| [file.device](../README.md#file.device)  | The device. | extended | keyword |  |
| [file.inode](../README.md#file.inode)  | The inode representing the file in the filesystem. | extended | keyword |  |
| [file.uid](../README.md#file.uid)  | The user ID (UID) or security identifier (SID) of the file owner. | extended | keyword |  |
| [file.owner](../README.md#file.owner)  | The file owner's username. | extended | keyword |  |
| [file.gid](../README.md#file.gid)  | The primary group ID (GID) of the file. | extended | keyword |  |
| [file.group](../README.md#file.group)  | The primary group name of the file. | extended | keyword |  |
| [file.mode](../README.md#file.mode)  | The mode of the file in octal representation. | extended | keyword | `416` |
| [file.size](../README.md#file.size)  | The file size in bytes (field is only added when `type` is `file`). | extended | long |  |
| [file.mtime](../README.md#file.mtime)  | The last modified time of the file (time when content was modified). | extended | date |  |
| [file.ctime](../README.md#file.ctime)  | The last change time of the file (time when metadata was changed). | extended | date |  |
| <a name="hash.&ast;"></a>*hash.&ast;* | *Hash fields used in Auditbeat.<br/>The hash field contains cryptographic hashes of data associated with the event (such as a file). The keys are names of cryptographic algorithms. The values are encoded as hexidecimal (lower-case).<br/>All fields in user can have one or multiple entries.<br/>* |  |  |  |
| <a name="hash.blake2b_256"></a>*hash.blake2b_256* | *BLAKE2b-256 hash of the file.* | (use case) | keyword |  |
| <a name="hash.blake2b_384"></a>*hash.blake2b_384* | *BLAKE2b-384 hash of the file.* | (use case) | keyword |  |
| <a name="hash.blake2b_512"></a>*hash.blake2b_512* | *BLAKE2b-512 hash of the file.* | (use case) | keyword |  |
| <a name="hash.md5"></a>*hash.md5* | *MD5 hash.* | (use case) | keyword |  |
| <a name="hash.sha1"></a>*hash.sha1* | *SHA-1 hash.* | (use case) | keyword |  |
| <a name="hash.sha224"></a>*hash.sha224* | *SHA-224 hash (SHA-2 family).* | (use case) | keyword |  |
| <a name="hash.sha256"></a>*hash.sha256* | *SHA-256 hash (SHA-2 family).* | (use case) | keyword |  |
| <a name="hash.sha384"></a>*hash.sha384* | *SHA-384 hash (SHA-2 family).* | (use case) | keyword |  |
| <a name="hash.sha512"></a>*hash.sha512* | *SHA-512 hash (SHA-2 family).* | (use case) | keyword |  |
| <a name="hash.sha512_224"></a>*hash.sha512_224* | *SHA-512/224 hash (SHA-2 family).* | (use case) | keyword |  |
| <a name="hash.sha512_256"></a>*hash.sha512_256* | *SHA-512/256 hash (SHA-2 family).* | (use case) | keyword |  |
| <a name="hash.sha3_224"></a>*hash.sha3_224* | *SHA3-224 hash (SHA-3 family).* | (use case) | keyword |  |
| <a name="hash.sha3_256"></a>*hash.sha3_256* | *SHA3-256 hash (SHA-3 family).* | (use case) | keyword |  |
| <a name="hash.sha3_384"></a>*hash.sha3_384* | *SHA3-384 hash (SHA-3 family).* | (use case) | keyword |  |
| <a name="hash.sha3_512"></a>*hash.sha3_512* | *SHA3-512 hash (SHA-3 family).* | (use case) | keyword |  |
| <a name="hash.xxh64"></a>*hash.xxh64* | *XX64 hash of the file.* | (use case) | keyword |  |



