## Auditbeat use case

ECS usage in Auditbeat.

### <a name="auditbeat"></a> Auditbeat fields


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| [event.module](https://github.com/elastic/ecs#event.module)  | Auditbeat module name.  |   |   |   |
| [file.*](https://github.com/elastic/ecs#file.*)  | File attributes.<br/>  |   |   |   |
| [file.path](https://github.com/elastic/ecs#file.path)  | The path to the file.  | text  |   |   |
| [file.path.raw](https://github.com/elastic/ecs#file.path.raw)  | The path to the file. This is a non-analyzed field that is useful for aggregations.  | keyword  | 1  |   |
| [file.target_path](https://github.com/elastic/ecs#file.target_path)  | The target path for symlinks.  | keyword  |   |   |
| [file.type](https://github.com/elastic/ecs#file.type)  | The file type (file, dir, or symlink).  | keyword  |   |   |
| [file.device](https://github.com/elastic/ecs#file.device)  | The device.  | keyword  |   |   |
| [file.inode](https://github.com/elastic/ecs#file.inode)  | The inode representing the file in the filesystem.  | keyword  |   |   |
| [file.uid](https://github.com/elastic/ecs#file.uid)  | The user ID (UID) or security identifier (SID) of the file owner.  | keyword  |   |   |
| [file.owner](https://github.com/elastic/ecs#file.owner)  | The file owner's username.  | keyword  |   |   |
| [file.gid](https://github.com/elastic/ecs#file.gid)  | The primary group ID (GID) of the file.  | keyword  |   |   |
| [file.group](https://github.com/elastic/ecs#file.group)  | The primary group name of the file.  | keyword  |   |   |
| [file.mode](https://github.com/elastic/ecs#file.mode)  | The mode of the file in octal representation.  | keyword  |   | `416`  |
| [file.size](https://github.com/elastic/ecs#file.size)  | The file size in bytes (field is only added when `type` is `file`).  | long  |   |   |
| [file.mtime](https://github.com/elastic/ecs#file.mtime)  | The last modified time of the file (time when content was modified).  | date  |   |   |
| [file.ctime](https://github.com/elastic/ecs#file.ctime)  | The last change time of the file (time when metadata was changed).  | date  |   |   |
| [hash.*](https://github.com/elastic/ecs#hash.*)  | Hash fields used in Auditbeat.<br/>The hash field contains cryptographic hashes of data associated with the event (such as a file). The keys are names of cryptographic algorithms. The values are encoded as hexidecimal (lower-case).<br/>All fields in user can have one or multiple entries.<br/>  |   |   |   |
| <a name="hash.md5"></a>*hash.md5*  | *MD5 hash.*  | keyword  |   |   |
| <a name="hash.sha1"></a>*hash.sha1*  | *SHA-1 hash.*  | keyword  |   |   |
| <a name="hash.sha224"></a>*hash.sha224*  | *SHA-224 hash (SHA-2 family).*  | keyword  |   |   |
| <a name="hash.sha256"></a>*hash.sha256*  | *SHA-256 hash (SHA-2 family).*  | keyword  |   |   |
| <a name="hash.sha384"></a>*hash.sha384*  | *SHA-384 hash (SHA-2 family).*  | keyword  |   |   |
| <a name="hash.sha512"></a>*hash.sha512*  | *SHA-512 hash (SHA-2 family).*  | keyword  |   |   |
| <a name="hash.sha512_224"></a>*hash.sha512_224*  | *SHA-512/224 hash (SHA-2 family).*  | keyword  |   |   |
| <a name="hash.sha512_256"></a>*hash.sha512_256*  | *SHA-512/256 hash (SHA-2 family).*  | keyword  |   |   |
| <a name="hash.sha3_224"></a>*hash.sha3_224*  | *SHA3-224 hash (SHA-3 family).*  | keyword  |   |   |
| <a name="hash.sha3_256"></a>*hash.sha3_256*  | *SHA3-256 hash (SHA-3 family).*  | keyword  |   |   |
| <a name="hash.sha3_384"></a>*hash.sha3_384*  | *SHA3-384 hash (SHA-3 family).*  | keyword  |   |   |
| <a name="hash.sha3_512"></a>*hash.sha3_512*  | *SHA3-512 hash (SHA-3 family).*  | keyword  |   |   |



