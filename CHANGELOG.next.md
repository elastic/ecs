<!-- When adding an entry to the Changelog:
- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
Thanks, you're awesome :-) -->

## Unreleased

### Breaking changes

### Bugfixes

### Added
* Add support for installed software packages. #532

* Added fields in `log.*` to allow for full Syslog mapping. #525
* Added `top_level_domain` field to `url`, `dns.question`,
    `source`, `destination`, `client`, and `server`. #562, #572
* Add group.domain field #547
* Added `url.extension` #551, #573
* Added `observer.name` and `observer.product` #557, #571
* Added `error.stack_trace` field. #562
* Added `log.origin.file.name`, `log.origin.function` and `log.origin.file.line` fields. #563
* Added `service.node.name` to allow distinction between different nodes of the same service running on the same host. #565
* Added `error.type` field. #566

* Added Threat fields #505

### Improvements

### Deprecated


<!-- All empty sections:

## Unreleased

### Breaking changes

### Bugfixes

### Added

### Improvements

### Deprecated

-->
