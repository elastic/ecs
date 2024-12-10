from typing import (
    List,
    TypedDict,
)


class OTelAttribute(TypedDict, total=False):
    id: str
    stability: str
    ref: str
    deprecated: str
    group_display_name: str


class OTelGroup(TypedDict, total=False):
    id: str
    type: str
    prefix: str
    display_name: str
    attributes: List[OTelAttribute]
    stability: str
    metric_name: str


class OTelModelFile(TypedDict, total=False):
    groups: List[OTelGroup]


class OTelMappingSummary(TypedDict, total=False):
    namespace: str
    title: str
    nr_plain_ecs_fields: int
    nr_all_ecs_fields: int
    nr_otel_fields: int
    nr_matching_fields: int
    nr_equivalent_fields: int
    nr_conflicting_fields: int
    nr_related_fields: int
    nr_metric_fields: int
