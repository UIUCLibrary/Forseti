from behave import *

import speedwagon.models
import speedwagon.tools
import speedwagon.tools.options

use_step_matcher("re")


@when("we provide data to generate a Qt model options model 3")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    context.data_model = speedwagon.models.ToolOptionsModel3(context.data)


@then("we get a ToolOptionsModel3 object")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    assert isinstance(context.data_model, speedwagon.models.ToolOptionsModel3)


@given("I have an options model with ToolOptions 3 with a single my_option")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    my_option =speedwagon.tools.options.UserOptionPythonDataType2("my_option", str)
    my_option.data = ""
    data = [my_option]
    # data = [speedwagon.tools.options.ToolOptionDataType(name="my_option")]
    context.data_model = speedwagon.models.ToolOptionsModel3(data)
