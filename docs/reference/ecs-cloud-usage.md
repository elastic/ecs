---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-cloud-usage.html
applies_to:
  stack: all
  serverless: all
---

# Cloud fields usage and examples [ecs-cloud-usage]

Here are the subjects covered in this page.

* [Field reuse](#ecs-cloud-usage-field-reuse)

    * [Cloud fields at the root of an event](#ecs-cloud-usage-cloud-at-root)
    * [Describing external cloud resources in an invocation relationship](#ecs-cloud-usage-origin-target)



## Field reuse [ecs-cloud-usage-field-reuse]

The cloud fields can be used to * [describe the cloud resource an event comes from](#ecs-cloud-usage-cloud-at-root) * or to [describe the context of an external cloud resource](#ecs-cloud-usage-origin-target) that has a direct invocation relationship to the observed service or resource


### Cloud fields at the root of an event [ecs-cloud-usage-cloud-at-root]

Use the cloud fields at the root of an event to describe the cloud resource the event primarily relates to. An example for this use case is a log entry being recorded for a service that is deployed in a cloud environment:

```json
{
  "cloud": {
    "provider": "aws",
    "region": "us-east-1",
    "service": { "name": "ec2" }
  }
}
```


### Describing external cloud resources in an invocation relationship [ecs-cloud-usage-origin-target]

Managed cloud services can be in an invocation relationship to the observed service (i.e. service for which the corresponding event is captured). For instance, an observed service running on AWS Lambda can be invoked through an AWS API Gateway. Another example is an observed service that invokes an external cloud service (e.g. AWS Simple Email Service). In the context of an invocation relationship, cloud fields can be nested under `cloud.origin.*` and `cloud.target.*`, respectively, to capture the cloud context on origin or target cloud services from the perspective of an observed service. This concept is similar to [nesting of service fields](/reference/ecs-service-usage.md#ecs-service-usage-origin-target) under `service.origin.*` and `service.target.*`.

Let’s consider an exemplary event that represents an inbound AWS Lambda invocation coming from an AWS API Gateway. Use the following `cloud.origin.*` nesting to describe the API Gateway service from the perspective of the AWS Lambda service:

```json
{
  "service": { <1>
    "name": "MyLambdaFunction",
    "version": "1.0.0",
    "origin": { <2>
      "name": "MyGateway",
      "version" "2.0",
    }
  },
  "cloud": { <3>
    "provider": "aws",
    "region": "us-east-1",
    "service": { "name": "lambda" },
    "origin": { <4>
      "provider": "aws",
      "region": "eu-west-1",
      "service": { "name": "apigateway" }
    }
  }
}
```

1. Describes the observed AWS Lambda function
2. Describes the API Gateway service where the inbound request comes from
3. Describes the cloud context of the observed AWS Lambda function
4. Describes the cloud context of the API Gateway service where the inbound request comes from


Note that `cloud.origin.*` and `cloud.target.*` fields should only be used on events that represent an invocation relationship.

