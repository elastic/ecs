import collections
import json

from scripts.generators import bp_generator

Rule = collections.namedtuple('Rule', ['name', 'kql'])


def before_all(context):
    context.best_practices = []
    context.detection_rules = []


def after_all(context):
    if len(context.best_practices) > 0:
        write_best_practices(context.best_practices,
                             context.config.userdata.get("bp_output",
                                                         "docs/using-best-practices.asciidoc"))
    if len(context.detection_rules) > 0:
        write_detection_rules(context.detection_rules,
                              context.config.userdata.get("rules_output",
                                                          "generated/rules/best-practices-rules.ndjson"))


def before_feature(context, feature):
    context.feature_best_practices = []
    context.feature_detection_rules = []


def after_feature(context, feature):
    if len(context.feature_best_practices) > 0:
        context.best_practices.append({feature.name: context.feature_best_practices})
    if len(context.feature_detection_rules) > 0:
        context.detection_rules.extend(context.feature_detection_rules)


def before_scenario(context, scenario):
    context.givens = []
    context.thens = []
    context.skip_detection_rule = False


def after_scenario(context, scenario):
    context.feature_best_practices.append(scenario.name)
    if not context.skip_detection_rule:
        context.feature_detection_rules.append(Rule(name=scenario.name,
                                                    kql=" and ".join(context.givens + context.thens)))


def write_best_practices(best_practices, filename):
    bp_generator.save_asciidoc(filename,
                               "best_practices.j2",
                               {"best_practices": best_practices})


def write_detection_rules(detection_rules, filename):
    list_of_objs = []
    for rule in detection_rules:
        r = bp_generator.default_detection_rule()
        r['description'] = rule.name
        r['name'] = "ECS Check: {0}".format(rule.name)
        r['query'] = rule.kql
        list_of_objs.append(r)
    bp_generator.save_ndjson(filename, list_of_objs)
