from behave import *


@given('the {field} field is present')
def step_impl(context, field):
    context.givens.append("{0}:*".format(field))


@given('an event')
def step_imp(context):
    pass


@then('the {field} field is present')
def step_impl(context, field):
    context.thens.append("not {0}:*".format(field))


@then('the {field} field is not present')
def step_impl(context, field):
    context.thens.append("{0}:*".format(field))


@then('the {field1} field should not equal the {field2} field')
def step_imp(context, field1, field2):
    """don't know how to express field not equal field in KQL"""
    context.skip_detection_rule = True
