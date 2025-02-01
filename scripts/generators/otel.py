import git
import os
import shutil
from typing import (
    Dict,
    List,
)
import yaml
from schema import visitor
from generators import ecs_helpers
from _types import (
    OTelModelFile,
    OTelMapping,
    OTelAttribute,
    FieldEntry,
    FieldNestedEntry,
    Field,
    OTelMappingSummary,
    OTelGroup,
)

OTEL_SEMCONV_GIT = "https://github.com/open-telemetry/semantic-conventions.git"
LOCAL_TARGET_DIR_OTEL_SEMCONV = "./build/otel-semconv/"


def get_model_files(
    git_repo: str,
    semconv_version: str,
) -> List[OTelModelFile]:
    """Loads OpenTelemetry Semantic Conventions model from GitHub"""
    target_dir = "model"
    tree: git.objects.tree.Tree = get_tree_by_url(git_repo, semconv_version)
    if ecs_helpers.path_exists_in_git_tree(tree, target_dir):
        return collectOTelModelFiles(tree[target_dir])
    else:
        raise KeyError(f"Target directory './{target_dir}' not present in git '{git_repo}'!")


def get_attributes(
    model_files: List[OTelModelFile]
) -> Dict[str, OTelAttribute]:
    """Retrieves (non-deprecated) OTel attributes from the model files"""

    attributes: Dict[str, OTelAttribute] = {}
    for model_file in model_files:
        for group in model_file['groups']:
            if 'type' in group and group['type'] == 'attribute_group' and 'deprecated' not in group and 'attributes' in group:
                for attribute in group['attributes']:
                    if 'id' in attribute and 'deprecated' not in attribute:
                        if 'prefix' in group:
                            attribute['id'] = group['prefix'] + "." + attribute['id']
                        attributes[attribute['id']] = attribute
                        if 'display_name' in group:
                            attribute['group_display_name'] = group['display_name']
    return attributes


def get_metrics(
    model_files: List[OTelModelFile]
) -> Dict[str, OTelAttribute]:
    """Retrieves (non-deprecated) OTel metrics from the model files"""

    metrics: Dict[str, OTelGroup] = {}
    for model_file in model_files:
        for group in model_file['groups']:
            if 'type' in group and group['type'] == 'metric' and 'metric_name' in group and 'deprecated' not in group:
                metrics[group['metric_name']] = group
    return metrics


def collectOTelModelFiles(
    tree: git.objects.tree.Tree,
    level=0
) -> List[OTelModelFile]:
    otel_model_files: List[OTelModelFile] = []
    for entry in tree:
        if entry.type == "tree":
            otel_model_files.extend(collectOTelModelFiles(entry, level + 1))
        elif entry.type == "blob" and (entry.name.endswith('.yml') or entry.name.endswith('.yaml')):
            content: str = entry.data_stream.read().decode('utf-8')
            model_file: OTelModelFile = yaml.safe_load(content)
            otel_model_files.append(model_file)
    return otel_model_files


def get_tree_by_url(
    url: str,
    git_ref: str,
) -> git.objects.tree.Tree:
    repo: git.repo.base.Repo
    clone_from_remote = False
    if os.path.exists(LOCAL_TARGET_DIR_OTEL_SEMCONV):
        repo = git.Repo(LOCAL_TARGET_DIR_OTEL_SEMCONV)

        if not git_ref in repo.tags and not git_ref in repo.branches:
            shutil.rmtree(LOCAL_TARGET_DIR_OTEL_SEMCONV)
            clone_from_remote = True
    else:
        clone_from_remote = True

    if clone_from_remote:
        print(f'Loading OpenTelemetry Semantic Conventions version "{git_ref}"')
        repo = git.Repo.clone_from(url, LOCAL_TARGET_DIR_OTEL_SEMCONV)

    repo.git.checkout(git_ref)
    return repo.head.commit.tree


def get_otel_attribute_name(
    field: Field,
    otel: OTelMapping
) -> str:
    if otel['relation'] == 'match':
        return field['flat_name']
    elif 'attribute' in otel:
        return otel['attribute']
    elif 'metric' in otel:
        raise KeyError("Passed OTel mapping is of type 'metric', expected 'attribute' here!")
    else:
        raise KeyError(
            f"On field '{field['flat_name']}': Cannot retrieve attribute name for an OTel mapping with relation '{otel['relation']}'!")


def must_have(ecs_field_name, otel, relation_type, property):
    if property not in otel:
        raise ValueError(
            f"On field '{ecs_field_name}': An OTel mapping with relation type '{relation_type}' must specify the property '{property}'!")


def must_not_have(ecs_field_name, otel, relation_type, property):
    if property in otel:
        raise ValueError(
            f"On field '{ecs_field_name}': An OTel mapping with relation type '{relation_type}' must not have the property '{property}'!")


class OTelGenerator:

    def __init__(self, semconv_version: str):
        model_files = get_model_files(OTEL_SEMCONV_GIT, semconv_version)

        self.attributes: Dict[str, OTelAttribute] = get_attributes(model_files)
        self.otel_attribute_names = list(self.attributes.keys())

        self.metrics: Dict[str, OTelGroup] = get_metrics(model_files)
        self.otel_metric_names = list(self.metrics.keys())

        self.semconv_version = semconv_version

    def __set_stability(self, details):
        field_details = details['field_details']
        if 'flat_name' in field_details and 'otel' in field_details:
            for otel in field_details['otel']:
                if otel['relation'] == 'metric':
                    otel['stability'] = self.metrics[otel['metric']]['stability']
                elif otel['relation'] == 'match' or 'attribute' in otel:
                    otel['stability'] = self.attributes[get_otel_attribute_name(field_details, otel)]['stability']

    def __check_metric_name(self, field_name, metric_name):
        if not metric_name in self.otel_metric_names:
            raise ValueError(
                f"On field '{field_name}': Metric '{metric_name}' does not exist in Semantic Conventions version {self.semconv_version}!")

    def __check_attribute_name(self, field_details, otel):
        otel_attr_name = get_otel_attribute_name(field_details, otel)
        if not otel_attr_name in self.otel_attribute_names:
            raise ValueError(
                f"On field '{field_details['flat_name']}': Attribute '{otel_attr_name}' does not exist in Semantic Conventions version {self.semconv_version}!")

    def __check_mapping(self, details):
        field_details = details['field_details']
        if 'flat_name' in field_details and (not 'intermediate' in field_details or not field_details['intermediate']):
            ecs_field_name = field_details['flat_name']
            if 'otel' in field_details:
                for otel in field_details['otel']:
                    if not 'relation' in otel:
                        raise ValueError(
                            f"On field '{field_details['flat_name']}': OTel mapping must specify the 'relation' property!")

                    if otel['relation'] == 'metric':
                        must_have(ecs_field_name, otel, otel['relation'], 'metric')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'attribute')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'otlp_field')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'stability')
                        self.__check_metric_name(ecs_field_name, otel['metric'])
                    elif otel['relation'] == 'otlp':
                        must_have(ecs_field_name, otel, otel['relation'], 'otlp_field')
                        must_have(ecs_field_name, otel, otel['relation'], 'stability')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'attribute')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'metric')
                    elif otel['relation'] == 'na':
                        must_not_have(ecs_field_name, otel, otel['relation'], 'otlp_field')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'attribute')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'metric')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'stability')
                    elif otel['relation'] == 'match':
                        must_not_have(ecs_field_name, otel, otel['relation'], 'otlp_field')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'attribute')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'metric')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'stability')
                    elif otel['relation'] == 'equivalent' or otel['relation'] == 'related' or otel['relation'] == 'conflict':
                        must_have(ecs_field_name, otel, otel['relation'], 'attribute')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'otlp_field')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'metric')
                        must_not_have(ecs_field_name, otel, otel['relation'], 'stability')
                        self.__check_attribute_name(field_details, otel)
                    else:
                        raise ValueError(
                            f"On field '{field_details['flat_name']}': Invalid relation type '{otel['relation']}'")

            elif ecs_field_name in self.otel_attribute_names:
                print(
                    f'WARNING: Field "{ecs_field_name}" exists in OTel Semantic Conventions with exactly the same name but is not mapped in ECS!')

    def validate_otel_mapping(
        self,
        field_entries: Dict[str, FieldEntry]
    ) -> None:
        visitor.visit_fields(field_entries, None, self.__check_mapping)
        visitor.visit_fields(field_entries, None, self.__set_stability)

    def get_mapping_summaries(
        self,
        fieldsets: List[FieldNestedEntry],
    ) -> List[OTelMappingSummary]:
        summaries: List[OTelMappingSummary] = []

        otel_namespaces = set([attr.split('.')[0] for attr in self.attributes.keys()])

        for fieldset in fieldsets:
            summary: OTelMappingSummary = {}

            summary['namespace'] = fieldset['name']
            if fieldset['name'] in otel_namespaces:
                otel_namespaces.remove(fieldset['name'])

            summary['title'] = fieldset['title']
            summary['nr_all_ecs_fields'] = 0
            summary['nr_plain_ecs_fields'] = 0
            summary['nr_otel_fields'] = 0
            summary['nr_matching_fields'] = 0
            summary['nr_equivalent_fields'] = 0
            summary['nr_related_fields'] = 0
            summary['nr_metric_fields'] = 0
            summary['nr_conflicting_fields'] = 0
            summary['nr_not_applicable_fields'] = 0
            summary['nr_otlp_fields'] = 0

            for field in fieldset['fields'].values():
                summary['nr_all_ecs_fields'] += 1
                if 'original_fieldset' not in field:
                    summary['nr_plain_ecs_fields'] += 1

                if 'otel' in field:
                    for otel in field['otel']:
                        if otel['relation'] == "match":
                            summary['nr_matching_fields'] += 1
                        elif otel['relation'] == "equivalent":
                            summary['nr_equivalent_fields'] += 1
                        elif otel['relation'] == "related":
                            summary['nr_related_fields'] += 1
                        elif otel['relation'] == "metric":
                            summary['nr_metric_fields'] += 1
                        elif otel['relation'] == "conflict":
                            summary['nr_conflicting_fields'] += 1
                        elif otel['relation'] == "na":
                            summary['nr_not_applicable_fields'] += 1
                        elif otel['relation'] == "otlp":
                            summary['nr_otlp_fields'] += 1

            summary['nr_otel_fields'] += len([attr for attr in list(self.attributes.keys())
                                             if attr.startswith(summary['namespace'] + ".")])
            summaries.append(summary)

        for otel_ns in otel_namespaces:
            summary: OTelMappingSummary = {}
            summary['namespace'] = otel_ns
            summary['title'] = otel_ns
            ex_attr = next(attr for attr in list(self.attributes.values()) if attr['id'].startswith(otel_ns + "."))
            if 'group_display_name' in ex_attr:
                disp_name = ex_attr['group_display_name']
                if disp_name.endswith(" Attributes"):
                    disp_name = disp_name[:-11]
                summary['title'] = disp_name
            summary['nr_otel_fields'] = len([attr for attr in list(
                self.attributes.keys()) if attr.startswith(otel_ns + ".")])
            summary['nr_all_ecs_fields'] = 0
            summary['nr_plain_ecs_fields'] = 0
            summary['nr_matching_fields'] = 0
            summary['nr_equivalent_fields'] = 0
            summary['nr_related_fields'] = 0
            summary['nr_conflicting_fields'] = 0
            summary['nr_metric_fields'] = 0
            summary['nr_otlp_fields'] = 0
            summaries.append(summary)

        return sorted(summaries, key=lambda s: s['namespace'])
