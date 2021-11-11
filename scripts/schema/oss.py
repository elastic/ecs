# This script performs a best effort fallback of basic data types to equivalent
# OSS data types.
# Note however that not all basic data types have an OSS replacement.
#
# The way this script is currently written, it has to be run on the fields *before*
# the cleaner script applies defaults, as there's no concept of defaults here.
# But since it navigates using the visitor script, it can easily be moved around
# in the chain, provided we add support for defaults as well.
#
# For now, no warning is output on basic fields that don't have a fallback.
# This could be improved if ECS starts using such types.

from schema import visitor

TYPE_FALLBACKS = {
    'constant_keyword': 'keyword',
    'wildcard': 'keyword',
    'version': 'keyword',
    'match_only_text': 'text',
    'flattened': 'object'
}


def fallback(fields):
    """Verify all fields for basic data type usage, and fallback to an OSS equivalent if appropriate."""
    visitor.visit_fields(fields, field_func=perform_fallback)


def perform_fallback(field):
    """Performs a best effort fallback of basic data types to equivalent OSS data types."""
    fallback_type = TYPE_FALLBACKS.get(field['field_details']['type'])
    if fallback_type:
        field['field_details']['type'] = fallback_type
