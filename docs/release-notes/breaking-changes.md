---
navigation_title: "Breaking changes"
---

# ECS breaking changes [ecs-breaking-changes]
Breaking changes can impact your Elastic applications, potentially disrupting normal operations.
Before you upgrade, carefully review the ECS breaking changes and take the necessary steps to mitigate any issues.

% ## Next version [ecs-nextversion-breaking-changes]

% ::::{dropdown} Title of breaking change
% Description of the breaking change.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of the breaking change.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.0.0 [ecs-900-breaking-changes]


:::::{dropdown} Remove previously deprecated fields
:name: remove-deprecated-fields-9.0.0

We've removed fields that were marked as deprecated in the previous major version of ECS.

The removed fields are: `process.parent.pgid`, `process.pgid`, `service.node.role`,
`service.origin.node.role`, `service.target.node.role`.

For more information, check [#2410](https://github.com/elastic/ecs/pull/2410).
::::
