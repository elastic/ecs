import json
import os.path
import sys


from generators import ecs_helpers
from generators import bp_generator


def generate(ecs_flat, version, out_dir):
    rules = []
    rules.extend(gen_required_rules(ecs_flat))
    rules.extend(gen_allowed_values_rules(ecs_flat))
    rules.extend(gen_category_expected_types_rules(ecs_flat))
    if len(rules) > 0:
        ecs_helpers.make_dirs(os.path.join(out_dir, 'rules'))
        bp_generator.save_ndjson(os.path.join(out_dir, 'rules/ecs-rules.ndjson'), rules)


def gen_required_rules(ecs_flat):
    rules = []
    required_fields = dict(filter(lambda elem: 'required' in elem[1], ecs_flat.items()))
    for field_name, field_properties in required_fields.items():
        if field_properties['required'] == False:
            next
        rule = bp_generator.default_detection_rule()
        rule['name'] = "ECS Check: {0} required field".format(field_name)
        rule['description'] = "This rule checks to make sure the required field `{0}` is present.".format(field_name)
        rule['query'] = "not {0}:*".format(field_name)
        rules.append(rule)
    return rules


def gen_allowed_values_rules(ecs_flat):
    rules = []
    allowed_values = dict(filter(lambda elem: 'allowed_values' in elem[1], ecs_flat.items()))
    for field_name, field_properties in allowed_values.items():
        rule = bp_generator.default_detection_rule()
        rule['name'] = "ECS Check: {0} allowed values".format(field_name)
        rule['description'] = "This rule checks to make sure the `{0}` field only contains allowed values.".format(
            field_name)
        rule['query'] = "{0}:*".format(field_name)
        for x in field_properties['allowed_values']:
            rule['query'] = "{0} and not {1}:{2}".format(rule['query'], field_name, x['name'])
        rules.append(rule)
    return rules


def gen_category_expected_types_rules(ecs_flat):
    rules = []
    for allowed_value in ecs_flat['event.category']['allowed_values']:
        if not 'expected_event_types' in allowed_value:
            next
        event_types = ["not event.type:{0}".format(x) for x in allowed_value['expected_event_types']]
        rule = bp_generator.default_detection_rule()
        rule['name'] = "ECS Check: expected `event.type` for `event.category` {0}".format(allowed_value['name'])
        rule['description'] = "This rule checks to make sure that `event.type` contains expected values when `event.category` is {0}.".format(
            allowed_value['name'])
        rule['query'] = "event.category:{0} and event.type:* and {1}".format(
            allowed_value['name'], " and ".join(event_types))
        rules.append(rule)
    return rules
