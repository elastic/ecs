# 0027: Function as a Service Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-06-01** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Using APM agents in the context of serverless environments (e.g. AWS Lambda, Azure Functions, etc.) allows to capture function as a service (faas) specific context that can be of great value for the end users and provide correlation points with other sources of data.

Extending ECS with a dedicated fields group or embedding it into exsting `cloud` fields would allow to capture this data in a meaningful, semantically aligned way and correlate the data accross different use cases (e.g. correlating AWS Lambda traces with corresponding Lambda metrics and logs).

The existing specification in OpenTelemetry can serve as a good orientation: https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/faas.md#example

<!--
Initial proposal:

Field | Example | Description
 -- | -- | --
faas.trigger.type | "http" | one of `http`,`pubsub`,`datasource`, `timer`, `other`
faas.trigger.name | "POST /{proxy+}/Prod" | Human readable name of the trigger instance.
faas.trigger.id | `arn:aws:sqs:us-east-2:123456789012:my-queue` | The ID of the trigger instance (e.g. Api-ID, SQS-queue-ARN, etc.)
faas.trigger.request_id | e.g. `123456789` | The iD of the trigger request , message, event, etc.
faas.trigger.account.name | "SomeAccount" | The name of the account the trigger belongs to.
faas.trigger.account.id | `12345678912` | The ID of the account the trigger belongs to.
faas.trigger.region | `us-east-1` | The cloud region of the trigger.
faas.trigger.version | `2.1` | The version of the trigger.
faas.execution | "af9d5aa4-a685-4c5f-a22b-444f80b3cc28" | The execution ID of the current function execution.
faas.coldstart |  true | Boolean value indicating a cold start of a function
faas.name | "my-lambda-function" | the name of the function
faas.id | "arn:aws:lambda:us-west-2:123456789012:function:my-lambda-function" | The ID of the function
faas.version | "semver:2.0.0" | The version of the function
faas.instance | "my-lambda-function:instance-0001" | The instance of the function
-->

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

Discussing the initial proposal with Andrew Wilkins, we came up with an adapted proposal (compared to the proposal for stage 0) that would reuse as many as possible existing ECS fields:

### New Fields
Field | Type | Example | Description | Use case
 -- | -- | --  | --  |--
faas.coldstart | boolean | true | Boolean value indicating a cold start of a function | Can be used in the UI denote function coldstarts.
faas.execution | keyword | "af9d5aa4-a685-4c5f-a22b-444f80b3cc28" | The execution ID of the current function execution. | Allows correlation with CloudWatch logs and metrics
faas.trigger.type | keyword | "http" | one of `http`,`pubsub`,`datasource`, `timer`, `other` | Allows differentiating different function types
faas.trigger.request_id | keyword | e.g. `123456789` | The iD of the trigger request , message, event, etc. | Correlation of metrics and logs with the corresponding trigger request

### Reusing existing `service.*` fields
For the initially proposed fields `faas.name`, `faas.id`, `faas.version` and `faas.instance` we decided to reuse the existing fields `service.name`, `service.id`, `service.version` and `service.node.name`.

### Nesting `cloud.*` and `service.*` fields under `_.origin.*` and `_.target.*`
We identified a big overlap between the initially proposed `faas.trigger.*` fields with the already existing `cloud.*` and `service.` fields.
Allowing to **self-nest cloud and service fields** under `cloud.origin.*` / `cloud.target.*` and `service.origin.*` / `service.target.*`, respectively, would allow to cover most of the `faas.trigger.*` fields.

Moreover, the proposal for nesting cloud fields would resolve other use cases as well (e.g. https://github.com/elastic/ecs/issues/1282).

Initially proposed | New proposed nested cloud or service field
-- | --
faas.trigger.name |  `service.origin.name`
faas.trigger.id | `service.origin.id`
faas.trigger.version | `service.origin.version`
faas.trigger.account.name | `cloud.origin.account.name`
faas.trigger.account.id | `cloud.origin.account.id`
faas.trigger.region | `cloud.origin.region`


<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->
Done.

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

### `faas.coldstart`
Will be used in the APM UI to mark function invocations that resultet from a coldstart. This is a useful information for the end users to differentiate coldstart behaviour from warmstart function invocations.

### `faas.execution` & `faas.trigger.request_id`
These IDs will be used to correlate APM data (traces / transactions), logs and metrics of the faas function (e.g. from CloudWatch) as well as logs and metrics from the corresponding trigger for individual invocations.

### `faas.trigger.type`
Indicates the type of the function trigger. Allows to group different function types.

### `service.origin.*` & `cloud.origin.*`
Provides meta information on the origin service that triggered the faas function. End users can use this information to better understand the context, dependencies and causalities when analyzing and troubleshooting faas-related observability scenarios.
For example, this information could provide insights on analysis questions like this: "Do function invocations that are triggered from cloud region us-east-1 behave similar to invocations from region eu-west-1?", etc.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->
Faas functions provide meta-information in their execution environment. APM agents use instrumentation techniques to read this information. For instance, AWS Lambda provides an `event` and a `context` object with each function invocation: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->
The above fields will be derived by the APM agents from the AWS Lambda `context object` and the `event object` that are passed with an invocation of a Lambda function. Below is an example for the context and event object.
The mapping to the proposed fields for this example is layed out in the following table

target ECS field | source field
--- | ---
faas.coldstart | No source field. Determined by the APM agent on the first Lambda function invocation.
faas.execution | `context.awsRequestId`
faas.trigger.type | No source field. Determined by the APM agent based on the `event object` type. Would be `http` in this example.
faas.trigger.request_id | `event.requestContext.requestId`
service.origin.name | `${event.requestContext.httpMethod} ${event.requestContext.resourcePath}/${event.requestContext.stage}` -> `GET /fetch_all/dev`
service.origin.id | `event.requestContext.apiId`
service.origin.version | No source field. Determined by the APM agent based on the `event object` type whether it's API version `1.0` or `2.0`.
cloud.origin.service.name | `api gateway`
cloud.origin.account.id | `event.requestContext.accountId`

### AWS Lambda context object 
Description [available here](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html).

**context:**
```json 
{
    "callbackWaitsForEmptyEventLoop": true,
    "functionVersion": "$LATEST",
    "functionName": "the-function-name",
    "memoryLimitInMB": "128",
    "logGroupName": "/aws/lambda/the-function-name",
    "logStreamName": "2021/08/13/[$LATEST]08834acf4e4f463b95b7b99aa8b34aff",
    "invokedFunctionArn": "arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:the-function-name",
    "awsRequestId": "649bf7d0-c6ae-432d-899d-da44ccd7ee95"
}
```
### AWS Lambda event object 
Description [available here](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html).

**event:**
```json
{
    "resource": "/fetch_all",
    "path": "/fetch_all",
    "httpMethod": "GET",
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-Country": "US",
        "Host": "02plqthge2.execute-api.us-east-1.amazonaws.com",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Via": "2.0 969f35f01b6eddd92239a3e818fc1e0d.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "eDbpfDwO-CRYymEFLkW6CBCsU_H_PS8R93_us53QWvXWLS45v3NvQw==",
        "X-Amzn-Trace-Id": "Root=1-5e502af4-fd0c1c6fdc164e1d6361183b",
        "X-Forwarded-For": "76.76.241.57, 52.46.47.139",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
    },
    "multiValueHeaders": {
        "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ],
        "Accept-Encoding": [
            "gzip, deflate, br"
        ],
        "Accept-Language": [
            "en-US,en;q=0.5"
        ],
        "CloudFront-Forwarded-Proto": [
            "https"
        ],
        "CloudFront-Is-Desktop-Viewer": [
            "true"
        ],
        "CloudFront-Is-Mobile-Viewer": [
            "false"
        ],
        "CloudFront-Is-SmartTV-Viewer": [
            "false"
        ],
        "CloudFront-Is-Tablet-Viewer": [
            "false"
        ],
        "CloudFront-Viewer-Country": [
            "US"
        ],
        "Host": [
            "02plqthge2.execute-api.us-east-1.amazonaws.com"
        ],
        "upgrade-insecure-requests": [
            "1"
        ],
        "User-Agent": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0"
        ],
        "Via": [
            "2.0 969f35f01b6eddd92239a3e818fc1e0d.cloudfront.net (CloudFront)"
        ],
        "X-Amz-Cf-Id": [
            "eDbpfDwO-CRYymEFLkW6CBCsU_H_PS8R93_us53QWvXWLS45v3NvQw=="
        ],
        "X-Amzn-Trace-Id": [
            "Root=1-5e502af4-fd0c1c6fdc164e1d6361183b"
        ],
        "X-Forwarded-For": [
            "76.76.241.57, 52.46.47.139"
        ],
        "X-Forwarded-Port": [
            "443"
        ],
        "X-Forwarded-Proto": [
            "https"
        ]
    },
    "queryStringParameters": null,
    "multiValueQueryStringParameters": null,
    "pathParameters": null,
    "stageVariables": null,
    "requestContext": {
        "resourceId": "y3tkf7",
        "resourcePath": "/fetch_all",
        "httpMethod": "GET",
        "extendedRequestId": "IQumRELJIAMF6fQ=",
        "requestTime": "21/Feb/2020:19:09:40 +0000",
        "path": "/dev/fetch_all",
        "accountId": "571481734049",
        "protocol": "HTTP/1.1",
        "stage": "dev",
        "domainPrefix": "02plqthge2",
        "requestTimeEpoch": 1582312180890,
        "requestId": "6f3dffca-46f8-4c8b-800b-6bc1ea2554ec",
        "identity": {
            "cognitoIdentityPoolId": null,
            "accountId": null,
            "cognitoIdentityId": null,
            "caller": null,
            "sourceIp": "76.76.241.57",
            "principalOrgId": null,
            "accessKey": null,
            "cognitoAuthenticationType": null,
            "cognitoAuthenticationProvider": null,
            "userArn": null,
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0",
            "user": null
        },
        "domainName": "02plqthge2.execute-api.us-east-1.amazonaws.com",
        "apiId": "02plqthge2"
    },
    "body": null,
    "isBase64Encoded": false
}
```

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
- Ingestion mechanisms:
  - APM server will extend the intake V2 API to accept the new fields and store them with the transaction documents
  - APM server will extend OpenTelemetry field mapping to account for these new fields
- Usage mechanisms:
  - APM UI may utilize the new fields to provide Lambda / serverless specific visualizations (e.g. indicating cold starts on transactions in the waterfall view, showing meta information on lambda service views)
- ECS project
  - the concept of self-nesting service and cloud fields under *origin* and *target* needs clear documentation that avoids confusion around when to use which of the fields. Tried to address this with the description in the schema for those fields in this PR.

## Concerns

### Nesting origin field to identify 3rd party
During stage 1 review @ebeahan identied the potential confusion over an established ECS pattern
where the root entity defines the `do'er` and `*.target.*` the affected entity.

This proposal extends this pattern as there are 3 active parties involved.
This puts the onus on ECS documentation being extremely clear on which field a user needs to
query to get their intended results.

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

- extended descriptio / footnote for service and cloud fields in this PR to avoid confusion about *origin* and *target* nesting of service and cloud fields

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @AlexanderWert | author, sponsor
* @axw | subject matter expert
* @Mpdreamz | subject matter expert

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
* [OpenTelemetry Faas Specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/faas.md#example)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1518
* Stage 1: https://github.com/elastic/ecs/pull/1542
