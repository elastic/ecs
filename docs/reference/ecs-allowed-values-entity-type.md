---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-allowed-values-entity-type.html
applies_to:
  stack: all
  serverless: all
navigation_title: entity.type
---

# ECS categorization field: entity.type [ecs-allowed-values-entity-type]

A standardized high-level classification of the entity. This provides a normalized way to group similar entities across different providers or systems.

`entity.type` represents a categorization that enables filtering and grouping of entities regardless of their specific implementation or provider. For example, filtering on `entity.type:host` yields all host-related entities whether they are physical machines, virtual machines, or cloud instances.

This field is an array. This allows proper categorization of entities that may fall into multiple types.

**Allowed values**

* [application](#ecs-entity-type-application)
* [bucket](#ecs-entity-type-bucket)
* [container](#ecs-entity-type-container)
* [database](#ecs-entity-type-database)
* [function](#ecs-entity-type-function)
* [host](#ecs-entity-type-host)
* [queue](#ecs-entity-type-queue)
* [service](#ecs-entity-type-service)
* [session](#ecs-entity-type-session)
* [user](#ecs-entity-type-user)


## application [ecs-entity-type-application]

Represents a software application or service. This includes web applications, mobile applications, desktop applications, and other software components that provide functionality to users or other systems. Applications may run on various infrastructure components and can span multiple hosts or containers.


## bucket [ecs-entity-type-bucket]

Represents a storage container or bucket, typically used for object storage. Common examples include AWS S3 buckets, Google Cloud Storage buckets, Azure Blob containers, and other cloud storage services. Buckets are used to organize and store files, objects, or data in cloud environments.


## container [ecs-entity-type-container]

Represents a containerized application or process. This includes Docker containers, Kubernetes pods, and other containerization technologies. Containers encapsulate applications and their dependencies, providing isolation and portability across different environments.


## database [ecs-entity-type-database]

Represents a database system or database instance. This includes relational databases (MySQL, PostgreSQL, Oracle), NoSQL databases (MongoDB, Cassandra, DynamoDB), time-series databases, and other data storage systems. The entity may represent the entire database system or a specific database instance.


## function [ecs-entity-type-function]

Represents a serverless function or Function-as-a-Service (FaaS) component. This includes AWS Lambda functions, Azure Functions, Google Cloud Functions, and other serverless computing resources. Functions are typically event-driven and execute code without managing the underlying infrastructure.


## host [ecs-entity-type-host]

Represents a computing host or machine. This includes physical servers, virtual machines, cloud instances, and other computing resources that can run applications or services. Hosts provide the fundamental computing infrastructure for other entity types.


## queue [ecs-entity-type-queue]

Represents a message queue or messaging system. This includes message brokers, event queues, and other messaging infrastructure components such as Amazon SQS, RabbitMQ, Apache Kafka, and Azure Service Bus. Queues facilitate asynchronous communication between applications and services.


## service [ecs-entity-type-service]

Represents a service or microservice component. This includes web services, APIs, background services, and other service-oriented architecture components. Services provide specific functionality and may communicate with other services to fulfill business requirements.


## session [ecs-entity-type-session]

Represents a user session or connection session. This includes user login sessions, database connections, network sessions, and other temporary interactive or persistent connections between users, applications, or systems.


## user [ecs-entity-type-user]

Represents a user account or identity. This includes human users, service accounts, system accounts, and other identity entities that can interact with systems, applications, or services. Users may have various roles, permissions, and attributes associated with their identity.

