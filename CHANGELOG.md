# Change Log
All notable changes to this project will be documented in this file based on the [Keep a Changelog](http://keepachangelog.com/) Standard. This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased](https://github.com/elastic/ecs/compare/0.1.0...master)

### Breaking changes
* Change structure of URL. #7
* Rename `url.href` `multi_field`. #18
* Rename `geoip.*` to `geo`. #58
* Rename log.message to log.original. #106
* Rename `event.raw` to `event.original`. #107
* Rename `user_agent.raw` to `user_agent.original` and make it a keyword. #107
* Rename `file.path.raw` to `file.path.keyword`, `file.target_path.raw` to `file.target_path.keyword`,
  `url.href.raw` to `url.href.keyword`, `url.path.raw` to `url.path.keyword`,
  `url.query.raw` to `url.query.keyword`, and `network.name.raw` to `network.name.keyword`. #103
* Remove `log.offset` and `log.line` as too specific for ECS. #131
* Remove top level objects `kubernetes` and `tls`. #132
* Remove `*.timezone.offset.sec` fields as too specific for ECS at the moment. #134

### Bugfixes

### Added
* Add `network.total.packets` and `network.total.bytes` field. PR#2
* Add `event.action` field. #21
* Add `network.name`, to track network names in the monitoring pipeline. #25
* Adds cloud.account.id for top level organizational level. #11
* Add `http.response.status_code` and `http.response.body` fields. #4
* Add fields for Operating System data. #5
* Add `log.message`. #3
* Add http.request.method and http.version
* Add `host.os.kernel` containing the OS kernel version. #60

### Deprecated
