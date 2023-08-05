# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import inspect

from botocore.docs.params import RequestParamsDocumenter
from botocore.docs.params import ResponseParamsDocumenter
from botocore.docs.example import ResponseExampleDocumenter
from botocore.docs.example import RequestExampleDocumenter


def get_instance_public_methods(instance):
    """Retrieves an objects public methods

    :param instance: The instance of the class to inspect
    :rtype: dict
    :returns: A dictionary that represents an instance's methods where
        the keys are the name of the methods and the
        values are the handler to the method.
    """
    instance_members = inspect.getmembers(instance)
    instance_methods = {}
    for name, member in instance_members:
        if not name.startswith('_'):
            if inspect.ismethod(member):
                instance_methods[name] = member
    return instance_methods


def document_model_driven_signature(section, name, operation_model,
                                    include=None, exclude=None):
    """Documents the signature of a model-driven method

    :param section: The section to write the documentation to.

    :param name: The name of the method

    :param operation_model: The operation model for the method

    :type include: Dictionary where keys are parameter names and
        values are the shapes of the parameter names.
    :param include: The parameter shapes to include in the documentation.

    :type exclude: List of the names of the parameters to exclude.
    :param exclude: The names of the parameters to exclude from
        documentation.
    """
    params = {}
    if operation_model.input_shape:
        params = operation_model.input_shape.members

    parameter_names = list(params.keys())

    if include is not None:
        for member in include:
            parameter_names.append(member.name)

    if exclude is not None:
        for member in exclude:
            if member in parameter_names:
                parameter_names.remove(member)

    signature_params = ''
    if parameter_names:
        signature_params = '**kwargs'
    section.style.start_sphinx_py_method(name, signature_params)


def document_custom_signature(section, name, method,
                              include=None, exclude=None):
    """Documents the signature of a custom method

    :param section: The section to write the documentation to.

    :param name: The name of the method

    :param method: The handle to the method being documented

    :type include: Dictionary where keys are parameter names and
        values are the shapes of the parameter names.
    :param include: The parameter shapes to include in the documentation.

    :type exclude: List of the names of the parameters to exclude.
    :param exclude: The names of the parameters to exclude from
        documentation.
    """
    args, varargs, keywords, defaults = inspect.getargspec(method)
    args = args[1:]
    signature_params = inspect.formatargspec(
        args, varargs, keywords, defaults)
    signature_params = signature_params.lstrip('(')
    signature_params = signature_params.rstrip(')')
    section.style.start_sphinx_py_method(name, signature_params)


def document_custom_method(section, method_name, method):
    """Documents a non-data driven method

    :param section: The section to write the documentation to.

    :param method_name: The name of the method

    :param method: The handle to the method being documented
    """
    document_custom_signature(
        section, method_name, method)
    method_intro_section = section.add_new_section('method-intro')
    method_intro_section.writeln('')
    doc_string = inspect.getdoc(method)
    if doc_string is not None:
        method_intro_section.style.write_py_doc_string(doc_string)


def document_model_driven_method(section, method_name, operation_model,
                                 event_emitter, method_description=None,
                                 example_prefix=None, include_input=None,
                                 include_output=None, exclude_input=None,
                                 exclude_output=None, document_output=True,
                                 include_signature=True):
    """Documents an individual method

    :param section: The section to write to

    :param method_name: The name of the method

    :param operation_model: The model of the operation

    :param event_emitter: The event emitter to use to emit events

    :param example_prefix: The prefix to use in the method example.

    :type include_input: Dictionary where keys are parameter names and
        values are the shapes of the parameter names.
    :param include_input: The parameter shapes to include in the
        input documentation.

    :type include_output: Dictionary where keys are parameter names and
        values are the shapes of the parameter names.
    :param include_input: The parameter shapes to include in the
        output documentation.

    :type exclude_input: List of the names of the parameters to exclude.
    :param exclude_input: The names of the parameters to exclude from
        input documentation.

    :type exclude_output: List of the names of the parameters to exclude.
    :param exclude_input: The names of the parameters to exclude from
        output documentation.

    :param document_output: A boolean flag to indicate whether to
        document the output.

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    # Add the signature if specified.
    if include_signature:
        document_model_driven_signature(
            section, method_name, operation_model, include=include_input,
            exclude=exclude_input)

    # Add the description for the method.
    method_intro_section = section.add_new_section('method-intro')
    method_intro_section.include_doc_string(method_description)

    # Add the example section.
    example_section = section.add_new_section('example')
    example_section.style.new_paragraph()
    example_section.style.bold('Request Syntax')

    context = {
        'special_shape_types': {
            'streaming_input_shape': operation_model.get_streaming_input(),
            'streaming_output_shape': operation_model.get_streaming_output()
        }
    }

    if operation_model.input_shape:
        RequestExampleDocumenter(
            service_name=operation_model.service_model.service_name,
            operation_name=operation_model.name,
            event_emitter=event_emitter, context=context).document_example(
                example_section, operation_model.input_shape,
                prefix=example_prefix, include=include_input,
                exclude=exclude_input)
    else:
        example_section.style.new_paragraph()
        example_section.style.start_codeblock()
        example_section.write(example_prefix + '()')

    # Add the request parameter documentation.
    request_params_section = section.add_new_section('request-params')
    if operation_model.input_shape:
        RequestParamsDocumenter(
            service_name=operation_model.service_model.service_name,
            operation_name=operation_model.name,
            event_emitter=event_emitter, context=context).document_params(
                request_params_section, operation_model.input_shape,
                include=include_input, exclude=exclude_input)

    # Add the return value documentation
    return_section = section.add_new_section('return')
    return_section.style.new_line()
    if operation_model.output_shape is not None and document_output:
        return_section.write(':rtype: dict')
        return_section.style.new_line()
        return_section.write(':returns: ')
        return_section.style.indent()
        return_section.style.new_line()

        # Add an example return value
        return_example_section = return_section.add_new_section('example')
        return_example_section.style.new_line()
        return_example_section.style.bold('Response Syntax')
        return_example_section.style.new_paragraph()
        ResponseExampleDocumenter(
            service_name=operation_model.service_model.service_name,
            operation_name=operation_model.name,
            event_emitter=event_emitter,
            context=context).document_example(
                return_example_section, operation_model.output_shape,
                include=include_output, exclude=exclude_output)

        # Add a description for the return value
        return_description_section = return_section.add_new_section(
            'description')
        return_description_section.style.new_line()
        return_description_section.style.bold('Response Structure')
        return_description_section.style.new_paragraph()
        ResponseParamsDocumenter(
            service_name=operation_model.service_model.service_name,
            operation_name=operation_model.name,
            event_emitter=event_emitter,
            context=context).document_params(
                return_description_section, operation_model.output_shape,
                include=include_output, exclude=exclude_output)
    else:
        return_section.write(':returns: None')
