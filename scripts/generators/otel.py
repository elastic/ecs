# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""OpenTelemetry Semantic Conventions Integration Module.

This module handles the integration between ECS (Elastic Common Schema) and 
OpenTelemetry Semantic Conventions. It provides functionality to:
- Load OTel semantic conventions from GitHub
- Validate ECS field mappings against OTel attributes and metrics
- Generate alignment summaries for documentation

The module supports the ECS donation to OpenTelemetry initiative by maintaining
mappings between the two standards.

Key Components:
    - OTelGenerator: Main class for validation and summary generation
    - Model loading functions: Fetch OTel definitions from git
    - Validation functions: Ensure mapping integrity

See also: scripts/docs/otel-integration.md for detailed documentation
"""

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
from ecs_types import (
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
    """Load OpenTelemetry Semantic Conventions model files from a GitHub repository.
    
    This function clones or uses a cached version of the OTel semantic conventions
    repository and extracts all model files (YAML) from the 'model' directory.
    
    Args:
        git_repo: URL of the git repository containing semantic conventions
        semconv_version: Git tag or branch name to checkout (e.g., 'v1.24.0')
    
    Returns:
        List of OTel model files, each containing groups of attributes/metrics
    
    Raises:
        KeyError: If the 'model' directory doesn't exist in the repository
    
    Example:
        >>> files = get_model_files(OTEL_SEMCONV_GIT, 'v1.24.0')
        >>> len(files)  # Number of YAML files found
        150
    """
    target_dir = "model"
    tree: git.objects.tree.Tree = get_tree_by_url(git_repo, semconv_version)
    if ecs_helpers.path_exists_in_git_tree(tree, target_dir):
        return collectOTelModelFiles(tree[target_dir])
    else:
        raise KeyError(f"Target directory './{target_dir}' not present in git '{git_repo}'!")


def get_attributes(
    model_files: List[OTelModelFile]
) -> Dict[str, OTelAttribute]:
    """Extract all non-deprecated OTel attributes from model files.
    
    Iterates through all model files and extracts attributes from attribute_groups,
    filtering out deprecated entries. Prefixes are applied to attribute IDs when
    specified in the group definition.
    
    Args:
        model_files: List of OTel model files loaded from the repository
    
    Returns:
        Dictionary mapping attribute IDs (e.g., 'http.request.method') to their
        full attribute definitions including stability, type, and metadata
    
    Note:
        - Only processes groups with type='attribute_group'
        - Skips deprecated groups and attributes
        - Preserves group display names for documentation purposes
    """

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
    """Extract all non-deprecated OTel metrics from model files.
    
    Iterates through all model files and extracts metric definitions,
    filtering out deprecated entries.
    
    Args:
        model_files: List of OTel model files loaded from the repository
    
    Returns:
        Dictionary mapping metric names (e.g., 'http.server.request.duration')
        to their full metric group definitions including stability and metadata
    
    Note:
        - Only processes groups with type='metric'
        - Skips deprecated metrics
        - Metric names are used as dictionary keys
    """

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
    """Recursively collect all YAML model files from a git tree.
    
    Traverses the directory tree structure and parses all YAML files found,
    returning them as OTel model file objects.
    
    Args:
        tree: Git tree object representing a directory
        level: Current recursion depth (used for tracking)
    
    Returns:
        List of parsed OTel model files from all YAML files in the tree
    
    Note:
        - Recursively processes subdirectories
        - Only processes files with .yml or .yaml extensions
        - Files are parsed using yaml.safe_load for security
    """
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
    """Clone or update a git repository and return the tree for a specific reference.
    
    This function manages a local cache of the OTel semantic conventions repository.
    If the repository is already cloned and contains the requested ref, it reuses
    the cached version. Otherwise, it clones fresh from the remote.
    
    Args:
        url: Git repository URL to clone from
        git_ref: Git reference (tag or branch) to checkout (e.g., 'v1.24.0')
    
    Returns:
        Git tree object representing the repository contents at the specified ref
    
    Note:
        - Caches the repository in LOCAL_TARGET_DIR_OTEL_SEMCONV (./build/otel-semconv/)
        - If cached repo doesn't have the requested ref, re-clones from remote
        - Prints status message when downloading from remote
    
    Example:
        >>> tree = get_tree_by_url(OTEL_SEMCONV_GIT, 'v1.24.0')
        Loading OpenTelemetry Semantic Conventions version "v1.24.0"
    """
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
    """Extract the OTel attribute name from a mapping.
    
    Determines the appropriate OTel attribute name based on the mapping relation type:
    - 'match': Use the ECS field's flat_name (names are identical)
    - Other relations: Use the explicitly specified 'attribute' property
    
    Args:
        field: ECS field definition containing flat_name
        otel: OTel mapping configuration with relation type
    
    Returns:
        The OTel attribute name to use for lookups
    
    Raises:
        KeyError: If mapping is for a metric (not attribute) or if the relation
                 type doesn't support attribute name extraction
    
    Example:
        >>> field = {'flat_name': 'http.request.method'}
        >>> otel = {'relation': 'match'}
        >>> get_otel_attribute_name(field, otel)
        'http.request.method'
    """
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
    """Validate that a required property exists in an OTel mapping.
    
    Args:
        ecs_field_name: Name of the ECS field being validated
        otel: OTel mapping configuration dictionary
        relation_type: The relation type requiring this property
        property: Name of the required property
    
    Raises:
        ValueError: If the required property is missing
    """
    if property not in otel:
        raise ValueError(
            f"On field '{ecs_field_name}': An OTel mapping with relation type '{relation_type}' must specify the property '{property}'!")


def must_not_have(ecs_field_name, otel, relation_type, property):
    """Validate that a forbidden property does not exist in an OTel mapping.
    
    Args:
        ecs_field_name: Name of the ECS field being validated
        otel: OTel mapping configuration dictionary
        relation_type: The relation type forbidding this property
        property: Name of the forbidden property
    
    Raises:
        ValueError: If the forbidden property is present
    """
    if property in otel:
        raise ValueError(
            f"On field '{ecs_field_name}': An OTel mapping with relation type '{relation_type}' must not have the property '{property}'!")


class OTelGenerator:
    """Main class for OTel Semantic Conventions integration with ECS.
    
    This class handles the complete workflow of:
    1. Loading OTel semantic conventions from GitHub
    2. Validating ECS field mappings against OTel definitions
    3. Generating alignment summaries for documentation
    
    The generator is initialized with a specific OTel semantic conventions version
    and maintains in-memory caches of all attributes and metrics for validation.
    
    Attributes:
        attributes: Dictionary of all OTel attributes (keyed by attribute ID)
        otel_attribute_names: List of all attribute IDs for quick lookup
        metrics: Dictionary of all OTel metrics (keyed by metric name)
        otel_metric_names: List of all metric names for quick lookup
        semconv_version: Version of OTel semantic conventions being used
    
    Example:
        >>> generator = OTelGenerator('v1.24.0')
        >>> generator.validate_otel_mapping(ecs_fields)
        >>> summaries = generator.get_mapping_summaries(fieldsets)
    """

    def __init__(self, semconv_version: str):
        """Initialize the OTel generator with a specific semantic conventions version.
        
        Loads all model files from the OTel semantic conventions repository and
        extracts attributes and metrics for validation and reference.
        
        Args:
            semconv_version: Git tag or branch of semantic conventions to use
                           (e.g., 'v1.24.0')
        
        Note:
            This operation may take time on first run as it clones the repository.
            Subsequent runs with the same version use a cached clone.
        """
        model_files = get_model_files(OTEL_SEMCONV_GIT, semconv_version)

        self.attributes: Dict[str, OTelAttribute] = get_attributes(model_files)
        self.otel_attribute_names = list(self.attributes.keys())

        self.metrics: Dict[str, OTelGroup] = get_metrics(model_files)
        self.otel_metric_names = list(self.metrics.keys())

        self.semconv_version = semconv_version

    def __set_stability(self, details):
        """Set stability level on OTel mappings from their corresponding OTel definitions.
        
        Called by the visitor pattern during field traversal. Enriches each mapping
        with the stability level (experimental, stable, deprecated) from the OTel
        semantic conventions.
        
        Args:
            details: Field details dictionary containing 'field_details' with
                    optional 'otel' mappings
        
        Note:
            - For metrics: Uses the metric group's stability
            - For attributes: Uses the attribute's stability
            - Modifies the otel mapping in place
            - Private method used internally during validation
        """
        field_details = details['field_details']
        if 'flat_name' in field_details and 'otel' in field_details:
            for otel in field_details['otel']:
                if otel['relation'] == 'metric':
                    otel['stability'] = self.metrics[otel['metric']]['stability']
                elif otel['relation'] == 'match' or 'attribute' in otel:
                    otel['stability'] = self.attributes[get_otel_attribute_name(field_details, otel)]['stability']

    def __check_metric_name(self, field_name, metric_name):
        """Validate that a referenced metric exists in OTel semantic conventions.
        
        Args:
            field_name: Name of the ECS field being validated
            metric_name: OTel metric name to verify
        
        Raises:
            ValueError: If the metric doesn't exist in the loaded conventions
        """
        if not metric_name in self.otel_metric_names:
            raise ValueError(
                f"On field '{field_name}': Metric '{metric_name}' does not exist in Semantic Conventions version {self.semconv_version}!")

    def __check_attribute_name(self, field_details, otel):
        """Validate that a referenced attribute exists in OTel semantic conventions.
        
        Args:
            field_details: ECS field definition
            otel: OTel mapping configuration
        
        Raises:
            ValueError: If the attribute doesn't exist in the loaded conventions
        """
        otel_attr_name = get_otel_attribute_name(field_details, otel)
        if not otel_attr_name in self.otel_attribute_names:
            raise ValueError(
                f"On field '{field_details['flat_name']}': Attribute '{otel_attr_name}' does not exist in Semantic Conventions version {self.semconv_version}!")

    def __check_mapping(self, details):
        """Validate an ECS field's OTel mapping configuration.
        
        Performs comprehensive validation of OTel mappings including:
        - Required and forbidden properties for each relation type
        - Existence of referenced attributes/metrics
        - Proper structure and consistency
        
        Called by the visitor pattern during field traversal.
        
        Args:
            details: Field details dictionary containing 'field_details'
        
        Raises:
            ValueError: If mapping configuration is invalid
        
        Note:
            Relation types and their requirements:
            - 'match': Names are identical, no extra properties
            - 'equivalent': Requires 'attribute', semantically equivalent
            - 'related': Requires 'attribute', related but different
            - 'conflict': Requires 'attribute', conflicting definitions
            - 'metric': Requires 'metric', maps to OTel metric
            - 'otlp': Requires 'otlp_field' and 'stability', protocol-specific
            - 'na': Not applicable, no extra properties
        """
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
        """Validate all OTel mappings in ECS field definitions.
        
        This is the main validation entry point. It performs two passes over
        all fields:
        1. Validate mapping structure and referenced attributes/metrics exist
        2. Enrich mappings with stability information from OTel definitions
        
        Args:
            field_entries: Dictionary of all ECS field entries to validate
        
        Raises:
            ValueError: If any mapping is invalid or references non-existent
                       OTel attributes/metrics
        
        Note:
            Uses the visitor pattern to traverse nested field structures.
            Prints warnings for unmapped fields that match OTel attribute names.
        
        Example:
            >>> generator = OTelGenerator('v1.24.0')
            >>> fields = loader.load_schemas()
            >>> generator.validate_otel_mapping(fields)
        """
        visitor.visit_fields(field_entries, None, self.__check_mapping)
        visitor.visit_fields(field_entries, None, self.__set_stability)

    def get_mapping_summaries(
        self,
        fieldsets: List[FieldNestedEntry],
    ) -> List[OTelMappingSummary]:
        """Generate alignment summaries between ECS fieldsets and OTel namespaces.
        
        Creates summary statistics for each ECS fieldset and each OTel namespace,
        showing the degree of alignment between the two standards. This is used
        for generating documentation.
        
        Args:
            fieldsets: List of ECS fieldsets (nested field groups)
        
        Returns:
            List of summary objects containing:
            - namespace: The fieldset/namespace name
            - title: Display title
            - nr_all_ecs_fields: Total ECS fields in this namespace
            - nr_plain_ecs_fields: ECS-only fields (not reused from other sets)
            - nr_otel_fields: Total OTel attributes in this namespace
            - nr_matching_fields: Fields with 'match' relation
            - nr_equivalent_fields: Fields with 'equivalent' relation
            - nr_related_fields: Fields with 'related' relation
            - nr_conflicting_fields: Fields with 'conflict' relation
            - nr_metric_fields: Fields mapped to metrics
            - nr_otlp_fields: Fields mapped to OTLP protocol fields
            - nr_not_applicable_fields: Fields marked as not applicable
        
        Note:
            - Summaries are sorted alphabetically by namespace
            - Includes summaries for OTel namespaces that have no ECS equivalent
            - Used by markdown_fields.py to generate documentation
        
        Example:
            >>> summaries = generator.get_mapping_summaries(nested_fieldsets)
            >>> for s in summaries:
            ...     print(f"{s['namespace']}: {s['nr_matching_fields']} matches")
        """
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
