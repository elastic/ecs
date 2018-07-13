# Change Log
All notable changes to this project will be documented in this file based on the [Keep a Changelog](http://keepachangelog.com/) Standard. This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased](https://github.com/elastic/ecs/compare/0.1.0...master)

### Breaking changes
* Change structure of URL. #7
* Rename `url.href` `multi_field`. #18

### Bugfixes

### Added
* Add `network.total.packets` and `network.total.bytes` field. PR#2
* Add `event.action` field. #21
* Adds cloud.account.id for top level organizational level. #11
* Add `http.response.status_code` and `http.response.body` fields. #4
* Add fields for Operating System data. #5
* Add `log.message`. #3
* Add http.request.method and http.version

### Deprecated
