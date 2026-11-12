<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

#### Added

- Add `namespace` field to `service` schema. #2688
* Add `conversation.id` field to `gen_ai` schema. #2697
* Add `tool.source.name`, `tool.source.type`, `tool.source.address`, `usage.cache_read.input_tokens` and `usage.cache_write.input_tokens` fields to `gen_ai` schema from RFC 0060. #2711

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

* Update OTel semantic conventions to 1.44.0, support the `definition/2` model format and load GenAI conventions from `semantic-conventions-genai`. #2709
* Detect type conflicts when adding intermediate fields. #2671

#### Deprecated
