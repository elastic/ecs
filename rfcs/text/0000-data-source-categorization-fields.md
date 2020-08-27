# 0000: Data Source Categorization Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **August 26 2020** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Elastic currently supports ingestion of data from 180+ sources, and growing. However, we do not have a coherent way to categorise these sources. This has resulted in a disconnect in how we categorize these sources from the Elastic website, in-product experiences and ECS.

The fieldset we use to describe the data source is up for discussion, data_stream.category is a possibility. Here are proposed allowed values:

- apm
- application
- audit
- CASB
- cloud
- collaboration
- Config Management
- containers
- CRM
- EDR
- email
- firewall
- Identity and access management
- IDS/IPS
- Operating System
- productivity
- proxy
- queue/message queue
- security
- storage
- threat intelligence
- ticketing
- VPN
- vulnerability scanner
- Web server

## Usage
Categorization fields in ECS can govern how we categorize these data source, but only a limited set of event.category values are supported by the schema today. The event categorisation fields are catered to individual events, but don't categorise the data source.  Expanding the values we support, allows us to align the user experience from ECS, Ingest Manager and the Elastic Website (elastic.co/integrations). Some additional context here: #845 (comment).

These categories could also be used to categorise detection rules, to map data sources to corresponding rules. This would improve our onboarding experience by suggesting detection rules to users based on the sources they are ingesting data from.


## People

The following are the people that consulted on the contents of this RFC.

* @jamiehynds | author
* @exekias | sponsor

## References

* https://github.com/elastic/ecs/issues/901
* https://github.com/elastic/ecs/pull/845

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/958

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
