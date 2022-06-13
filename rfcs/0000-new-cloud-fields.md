# 0000: New cloud (or related) fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This RFC is to add several new cloud or cloud related fields to ECS.  As more cloud integrations/data sources are developed there are a variety of fields that don't have an ECS normalized field to put them. This would add the ability to normalize data related to cloud instance images, network/VPC information, S3/Object storage data....

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

Initial list of proposed fields:

* `cloud.edge_location`: The edge location, usually an airport IATA code (DFW), of a cloud service. Very common for DNS, CDN, or other cloud services
* `cloud.instance.image.id`: ID of the image used to create the virtual instance/machine
* `cloud.instance.image.name`: Name of the image used to create teh virtual instance/machine
* `cloud.vpc.name`: Name of the virtual network
* `cloud.vpc.id`: ID of the virtual network
* `cloud.subnet.name`: Name of the Subnet within the VPC/Virtual network
* `cloud.subnet.id`: ID of the Subnet within the VPC/Virtual network
* `cloud.instance.lifecycle`: Type of instance *normal* vs *spot*, see https://github.com/elastic/ecs/issues/323 for more discussion
* `cloud.object_store.name`: Name of S3/Compatible storage
* `cloud.object_store.id`: Name of S3/Compatible storage


Possible alternatives proposed in https://github.com/elastic/ecs/issues/1725
* `network.edge_location` instead of `cloud.edge_location`
* `cloud.image.id` instead of `cloud.instance.image.id`
* `cloud.image.name` instead of `cloud.instance.image.name`
* `network.name` (already exists) instead of  instead of `cloud.vpc.name`
* `network.id` instead of `cloud.vpc.id`
* `network.subnetwork.name` instead of  instead of `cloud.subnet.name`
* `network.subnetwork.id` instead of `cloud.subnet.id`

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage
This started with multiple new cloud integrations for the agent having edge location data fields to include Akamai, Cloudflare, AWS DNS, AWS Cloudfront...  Additionally AWS Guard Duty integration has numerous data points with regards to AWS network, S3/Object storage, instance information...

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data
### AWS Cloudfront Logs
2019-12-04	21:02:31	**LAX1**	392	89.160.20.112	GET	d111111abcdef8.cloudfront.net	/index.html	200	-	.......
### AWS Public ZOne DNS Logs
1.0 2017-12-13T08:16:02.130Z Z123412341234 example.com A NOERROR UDP **FRA6** 89.160.20.112 -
### Cloudflare HTTP Logs
{...**"EdgeColoCode":"AMS"**,"EdgeColoID":20,...}
### GCP Flow logs:
..."src_vpc":{"project_id":"my-sample-project",**"subnetwork_name":"default"**,**"vpc_name":"default"**}...
## GCP DNS logs
..."sourceIP":"10.154.0.3",**"sourceNetwork":"default"**,"vmInstanceId":8340998530665147,"vmInstanceIdString":"8340998530665147",...
### AWS Guard Duty Logs
  {
    "schemaVersion": "2.0",
    "accountId": "290443255379",
    "region": "us-east-2",
    "partition": "aws",
    "id": "02bf27df0ab318783b0a8f63569dfd68",
    "arn": "arn:aws:guardduty:us-east-2:290443255379:detector/c0bf27def0a899b467ad81c4a5681b78/finding/02bf27df0ab318783b0a8f63569dfd68",
    "type": "Impact:S3/MaliciousIPCaller",
    "resource": {
      "resourceType": "S3Bucket",
      "accessKeyDetails": {
        "accessKeyId": "GeneratedFindingAccessKeyId",
        "principalId": "GeneratedFindingPrincipalId",
        "userType": "IAMUser",
        "userName": "GeneratedFindingUserName"
      },
      "s3BucketDetails": [
        {
          "owner": {
            "id": "CanonicalId of Owner"
          },
          "createdAt": 1513612691.551,
          **"name": "bucketName",**
          "defaultServerSideEncryption": {
            "kmsMasterKeyArn": "arn:aws:kms:region:123456789012:key/key-id",
            "encryptionType": "SSEAlgorithm"
          },
          **"arn": "arn:aws:s3:::bucketName",**
          "type": "Destination",
        }
      ],
      "instanceDetails": {
        "instanceId": "i-99999999",
        "instanceType": "m3.xlarge",
        "outpostArn": "arn:aws:outposts:us-west-2:123456789000:outpost/op-0fbc006e9abbc73c3",
        "launchTime": "2016-08-02T02:05:06.000Z",
        "platform": null,
        "productCodes": [
          {
            "productCodeId": "GeneratedFindingProductCodeId",
            "productCodeType": "GeneratedFindingProductCodeType"
          }
        ],
        "iamInstanceProfile": {
          "arn": "arn:aws:iam::290443255379:example/instance/profile",
          "id": "GeneratedFindingInstanceProfileId"
        },
        "networkInterfaces": [
          {
            "networkInterfaceId": "eni-bfcffe88",
            "privateIpAddresses": [
              {
                "privateDnsName": "GeneratedFindingPrivateName",
                "privateIpAddress": "10.0.0.1"
              }
            ],
            "subnetId": "GeneratedFindingSubnetId",
            **"vpcId": "GeneratedFindingVPCId",**
            "privateDnsName": "GeneratedFindingPrivateDnsName",
            "securityGroups": [
              {
                "groupName": "GeneratedFindingSecurityGroupName",
                "groupId": "GeneratedFindingSecurityId"
              }
            ],
            "publicIp": "198.51.100.0",
            "ipv6Addresses": [],
            "publicDnsName": "GeneratedFindingPublicDNSName",
            "privateIpAddress": "10.0.0.1"
          }
        ],
        "instanceState": "running",
        "availabilityZone": "GeneratedFindingInstaceAvailabilityZone",
        **"imageId": "ami-99999999",**
        "imageDescription": "GeneratedFindingInstaceImageDescription"
      }
    }

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* TBD | author

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1953

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
