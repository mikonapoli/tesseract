from behave import *

@given(u'everything has been done correctly')
def step_impl(context):
    pass

@when(u'acceptance tests are run')
def step_impl(context):
    assert True is not False

@then(u'Behave works as expected')
def step_impl(context):
    assert context.failed is False
