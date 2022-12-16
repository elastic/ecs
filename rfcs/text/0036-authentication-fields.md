# 0036: Authentication Fields RFC

Stage: 0
Date: 2022-12-16

This RFC will provide normalization for fields related to authentication fields to assure that they are retained primarily in ECS core and in any extended fieldset when needed. These fields are important to normalize into ECS fields in order to maximize effectiveness of cross log utilization. 

## Fields

#### Log
|Proposed Field Name|Type|Value|Description|
| --- | --- | --- | --- |
|authentication.scope|keyword|user_impersonation|azure.activitylogs.identity.claims.http://schemas_microsoft_com/identity/claims/scope|
|authentication.requirement|keyword|multiFactorAuthentication|azure.activitylogs.properties.authentication_requirement|
|authentication.additional.details|keyword|MFA requirement satisfied by claim in the token|azure.activitylogs.properties.status.additionalDetails|
|authentication.authorization|keyword|ROOTMANAGESHAREDACCESSKEY|azure.resource.authorization_rule|
|authentication.interactive|boolean|FALSE|azure.signinlogs.properties.interactive|
|authentication.risk|keyword|low|azure.signinlogs.properties.risk_level_aggregated|
|authentication.id|keyword||Unique ID given across primary authentication and additional (multi factor) authentication.|
|authentication.protocol|keyword||Authentication Protocol (authproto)|
|authentication.token|keyword||Unique token provided during the event|
|authentication.token.identifier|keyword||Login token identifier/value|

## Source data

The source data for the logn fields came from multiple data sources, such as Azure Eventhubs, Azure Blob Storage, or PanOS Authentication Logs.

Here is a copy and example of a rawLog that came from Azure EventHubs.
```json
[
    {
        "@timestamp": "2019-10-24T00:13:46.355Z",
        "azure.activitylogs.category": "Action",
        "azure.activitylogs.event_category": "Administrative",
        "azure.activitylogs.identity.authorization.action": "Microsoft.EventHub/namespaces/authorizationRules/listKeys/action",
        "azure.activitylogs.identity.authorization.evidence.principal_id": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.authorization.evidence.principal_type": "ServicePrincipal",
        "azure.activitylogs.identity.authorization.evidence.role": "Azure EventGrid Service BuiltIn Role",
        "azure.activitylogs.identity.authorization.evidence.role_assignment_id": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.authorization.evidence.role_assignment_scope": "/subscriptions/8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.authorization.evidence.role_definition_id": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.authorization.scope": "/subscriptions/8a4de8b5-095c-47d0-a96f-a75130c61d53/resourceGroups/sa-hem/providers/Microsoft.EventHub/namespaces/azurelsevents/authorizationRules/RootManageSharedAccessKey",
        "azure.activitylogs.identity.claims.aio": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.claims.appid": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.claims.appidacr": "2",
        "azure.activitylogs.identity.claims.aud": "https://management.core.windows.net/",
        "azure.activitylogs.identity.claims.exp": "1571904826",
        "azure.activitylogs.identity.claims.http://schemas_microsoft_com/identity/claims/identityprovider": "https://sts.windows.net/8a4de8b5-095c-47d0-a96f-a75130c61d53/",
        "azure.activitylogs.identity.claims.http://schemas_microsoft_com/identity/claims/objectidentifier": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.claims.http://schemas_microsoft_com/identity/claims/tenantid": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.claims.http://schemas_xmlsoap_org/ws/2005/05/identity/claims/nameidentifier": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.claims.iat": "1571875726",
        "azure.activitylogs.identity.claims.iss": "https://sts.windows.net/8a4de8b5-095c-47d0-a96f-a75130c61d53/",
        "azure.activitylogs.identity.claims.nbf": "1571875726",
        "azure.activitylogs.identity.claims.uti": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.activitylogs.identity.claims.ver": "1.0",
        "azure.activitylogs.operation_name": "MICROSOFT.EVENTHUB/NAMESPACES/AUTHORIZATIONRULES/LISTKEYS/ACTION",
        "azure.activitylogs.result_signature": "Started.",
        "azure.activitylogs.result_type": "Start",
        "azure.correlation_id": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "azure.resource.authorization_rule": "ROOTMANAGESHAREDACCESSKEY",
        "azure.resource.group": "SA-HEMA",
        "azure.resource.id": "/SUBSCRIPTIONS/8a4de8b5-095c-47d0-a96f-a75130c61d53/RESOURCEGROUPS/SA-HEMA/PROVIDERS/MICROSOFT.EVENTHUB/NAMESPACES/AZURELSEVENTS/AUTHORIZATIONRULES/ROOTMANAGESHAREDACCESSKEY",
        "azure.resource.namespace": "AZURELSEVENTS",
        "azure.resource.provider": "MICROSOFT.EVENTHUB",
        "azure.subscription_id": "8a4de8b5-095c-47d0-a96f-a75130c61d53",
        "client.ip": "216.160.83.61",
        "cloud.provider": "azure",
        "event.action": "MICROSOFT.EVENTHUB/NAMESPACES/AUTHORIZATIONRULES/LISTKEYS/ACTION",
        "event.dataset": "azure.activitylogs",
        "event.duration": 0,
        "event.kind": "event",
        "event.module": "azure",
        "event.original": "{\"callerIpAddress\":\"216.160.83.61\",\"category\":\"Action\",\"correlationId\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"durationMs\":0,\"identity\":{\"authorization\":{\"action\":\"Microsoft.EventHub/namespaces/authorizationRules/listKeys/action\",\"evidence\":{\"principalId\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"principalType\":\"ServicePrincipal\",\"role\":\"Azure EventGrid Service BuiltIn Role\",\"roleAssignmentId\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"roleAssignmentScope\":\"/subscriptions/8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"roleDefinitionId\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\"},\"scope\":\"/subscriptions/8a4de8b5-095c-47d0-a96f-a75130c61d53/resourceGroups/sa-hem/providers/Microsoft.EventHub/namespaces/azurelsevents/authorizationRules/RootManageSharedAccessKey\"},\"claims\":{\"aio\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"appid\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"appidacr\":\"2\",\"aud\":\"https://management.core.windows.net/\",\"exp\":\"1571904826\",\"http://schemas.microsoft.com/identity/claims/identityprovider\":\"https://sts.windows.net/8a4de8b5-095c-47d0-a96f-a75130c61d53/\",\"http://schemas.microsoft.com/identity/claims/objectidentifier\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"http://schemas.microsoft.com/identity/claims/tenantid\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"iat\":\"1571875726\",\"iss\":\"https://sts.windows.net/8a4de8b5-095c-47d0-a96f-a75130c61d53/\",\"nbf\":\"1571875726\",\"uti\":\"8a4de8b5-095c-47d0-a96f-a75130c61d53\",\"ver\":\"1.0\"}},\"level\":\"Information\",\"location\":\"global\",\"operationName\":\"MICROSOFT.EVENTHUB/NAMESPACES/AUTHORIZATIONRULES/LISTKEYS/ACTION\",\"resourceId\":\"/SUBSCRIPTIONS/8a4de8b5-095c-47d0-a96f-a75130c61d53/RESOURCEGROUPS/SA-HEMA/PROVIDERS/MICROSOFT.EVENTHUB/NAMESPACES/AZURELSEVENTS/AUTHORIZATIONRULES/ROOTMANAGESHAREDACCESSKEY\",\"resultSignature\":\"Started.\",\"resultType\":\"Start\",\"time\":\"2019-10-24T00:13:46.3554259Z\"}",
        "event.type": [
            "change"
        ],
        "fileset.name": "activitylogs",
        "geo.city_name": "Milton",
        "geo.continent_name": "North America",
        "geo.country_iso_code": "US",
        "geo.country_name": "United States",
        "geo.location.lat": 47.2513,
        "geo.location.lon": -122.3149,
        "geo.region_iso_code": "US-WA",
        "geo.region_name": "Washington",
        "input.type": "log",
        "log.level": "Information",
        "log.offset": 0,
        "related.ip": [
            "216.160.83.61"
        ],
        "service.type": "azure",
        "source.as.number": 209,
        "source.geo.city_name": "Milton",
        "source.geo.continent_name": "North America",
        "source.geo.country_iso_code": "US",
        "source.geo.country_name": "United States",
        "source.geo.location.lat": 47.2513,
        "source.geo.location.lon": -122.3149,
        "source.geo.region_iso_code": "US-WA",
        "source.geo.region_name": "Washington",
        "source.ip": "216.160.83.61",
        "tags": [
            "forwarded"
        ]
    }
]
```
Palo Alto Authentication Logs:
FUTURE_USE, Receive Time, Serial Number, Type, Threat/Content Type, FUTURE_USE, Generated Time, Virtual System, Source IP, User, Normalize User, Object, Authentication Policy, Repeat Count, Authentication ID, Vendor, Log Action, Server Profile, Description, Client Type, Event Type, Factor Number, Sequence Number, Action Flags, Device Group Hierarchy 1, Device Group Hierarchy 2, Device Group Hierarchy 3, Device Group Hierarchy 4, Virtual System Name, Device Name, Virtual System ID, Authentication Protocol, UUID for rule, High Resolution Timestamp, Source Device Category, Source Device Profile, Source Device Model, Source Device Vendor, Source Device OS Family, Source Device OS Version, Source Hostname, Source Mac Address, Region, FUTURE_USE, User Agent, Session ID


## Scope of impact

No impact expected as login fieldsets are not impacting any existing fields, as these proposed fields are new. Moreover, these fields allow logs to be in a greater alignment with the ECS base fields and allow for expanded utilization and wider adoption.

## Concerns

The concerns that might arise relate to how the nested fields could be broken out into separate fields or that fields that are arrays are numbered. There are additional potential fields that could be implemented, but until they are seen in other vendor information, it makes sense to wait to add them to ECS.

## People

The following are the people that consulted on the contents of this RFC.

•	@mr1716 | author

## References

## RFC Pull Requests
•	Stage 0: https://github.com/elastic/ecs/pull/2023


## RFC References:
ecs/0027-faas-fields.md at main · elastic/ecs (github.com)
ecs/0011-sip-fields.md at main · elastic/ecs (github.com)
ecs/0025-container-metric-fields.md at main · elastic/ecs (github.com)
