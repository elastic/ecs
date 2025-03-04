---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-geo.html
applies_to:
  stack: all
  serverless: all
---

# Geo fields [ecs-geo]

Geo fields can carry data about a specific location related to an event.

This geolocation information can be derived from techniques such as Geo IP, or be user-supplied.


## Geo field details [_geo_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-geo-city-name$$$[geo.city_name](#field-geo-city-name) | City name.<br><br>type: keyword<br><br>example: `Montreal`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [geo.locality.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-locality-name)<br> | core |
| $$$field-geo-continent-code$$$[geo.continent_code](#field-geo-continent-code) | Two-letter code representing continent’s name.<br><br>type: keyword<br><br>example: `NA`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [geo.continent.code](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-continent-code)<br> | core |
| $$$field-geo-continent-name$$$[geo.continent_name](#field-geo-continent-name) | Name of the continent.<br><br>type: keyword<br><br>example: `North America`<br> | core |
| $$$field-geo-country-iso-code$$$[geo.country_iso_code](#field-geo-country-iso-code) | Country ISO code.<br><br>type: keyword<br><br>example: `CA`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [geo.country.iso_code](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-country-iso-code)<br> | core |
| $$$field-geo-country-name$$$[geo.country_name](#field-geo-country-name) | Country name.<br><br>type: keyword<br><br>example: `Canada`<br> | core |
| $$$field-geo-location$$$[geo.location](#field-geo-location) | Longitude and latitude.<br><br>type: geo_point<br><br>example: `{ "lon": -73.614830, "lat": 45.505918 }`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/related-efc20d?style=flat "related") [geo.location.lat](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-location-lat)<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/related-efc20d?style=flat "related") [geo.location.lon](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-location-lon)<br> | core |
| $$$field-geo-name$$$[geo.name](#field-geo-name) | User-defined description of a location, at the level of granularity they care about.<br><br>Could be the name of their data centers, the floor number, if this describes a local physical entity, city names.<br><br>Not typically used in automated geolocation.<br><br>type: keyword<br><br>example: `boston-dc`<br> | extended |
| $$$field-geo-postal-code$$$[geo.postal_code](#field-geo-postal-code) | Postal code associated with the location.<br><br>Values appropriate for this field may also be known as a postcode or ZIP code and will vary widely from country to country.<br><br>type: keyword<br><br>example: `94040`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [geo.postal_code](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-postal-code)<br> | core |
| $$$field-geo-region-iso-code$$$[geo.region_iso_code](#field-geo-region-iso-code) | Region ISO code.<br><br>type: keyword<br><br>example: `CA-QC`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [geo.region.iso_code](https://opentelemetry.io/docs/specs/semconv/attributes-registry/geo/#geo-region-iso-code)<br> | core |
| $$$field-geo-region-name$$$[geo.region_name](#field-geo-region-name) | Region name.<br><br>type: keyword<br><br>example: `Quebec`<br> | core |
| $$$field-geo-timezone$$$[geo.timezone](#field-geo-timezone) | The time zone of the location, such as IANA time zone name.<br><br>type: keyword<br><br>example: `America/Argentina/Buenos_Aires`<br> | core |


## Field reuse [_field_reuse_10]

The `geo` fields are expected to be nested at:

* `client.geo`
* `destination.geo`
* `host.geo`
* `observer.geo`
* `server.geo`
* `source.geo`
* `threat.enrichments.indicator.geo`
* `threat.indicator.geo`

Note also that the `geo` fields are not expected to be used directly at the root of the events.

