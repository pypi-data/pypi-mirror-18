#    Copyright 2016 Alexey Stepanov aka penguinolog

#    Copyright 2016 Mirantis, Inc.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""func_helpers module

This is no reason to import this submodule directly, all required methods is
available from the main module.
"""

from __future__ import absolute_import

import collections
import inspect
import sys

# pylint: disable=no-member
# pylint: disable=ungrouped-imports, no-name-in-module
if sys.version_info[0:2] > (3, 0):
    from inspect import Parameter
    from inspect import signature
else:
    # noinspection PyUnresolvedReferences
    from funcsigs import Parameter
    # noinspection PyUnresolvedReferences
    from funcsigs import signature
# pylint: enable=ungrouped-imports, no-name-in-module


def get_arg_names(func):
    """get argument names for function

    :param func: Function to extract arguments from
    :type func: callable
    :return: list of function argument names
    :rtype: list

    >>> def tst_1():
    ...     pass

    >>> get_arg_names(tst_1)
    []

    >>> def tst_2(arg):
    ...     pass

    >>> get_arg_names(tst_2)
    ['arg']
    """
    return list(signature(obj=func).parameters.keys())


def get_call_args(func, *positional, **named):
    """get real function call arguments without calling function

    :param func: Function to bind arguments
    :type func: callable
    :type positional: iterable
    :type named: dict
    :rtype: collections.OrderedDict

    >>> def tst(arg, darg=2, *args, **kwargs):
    ...     pass

    >>> get_call_args(tst, *(1, ))
    OrderedDict([('arg', 1), ('darg', 2), ('args', ()), ('kwargs', {})])
    """
    # noinspection PyUnresolvedReferences
    if sys.version_info[0:2] < (3, 5):  # apply_defaults is py35 feature
        # pylint: disable=deprecated-method
        orig_args = inspect.getcallargs(func, *positional, **named)
        # pylint: enable=deprecated-method
        # Construct OrderedDict as Py3
        arguments = collections.OrderedDict(
            [(key, orig_args[key]) for key in get_arg_names(func)]
        )
        return arguments
    sig = inspect.signature(func).bind(*positional, **named)
    sig.apply_defaults()  # after bind we doesn't have defaults
    return sig.arguments


def prepare_repr(func):
    """Get arguments lists with defaults

    :type func: union(types.FunctionType, types.MethodType)
    :rtype: generator
    """
    isfunction = inspect.isfunction(func)
    real_func = func if isfunction else func.__func__

    parameters = list(signature(real_func).parameters.values())

    params = iter(parameters)
    if not isfunction and func.__self__ is not None:
        yield next(params).name, func.__self__
    for arg in params:
        if arg.default != Parameter.empty:
            yield arg.name, arg.default
        elif arg.kind == Parameter.VAR_POSITIONAL:
            yield '*' + arg.name
        elif arg.kind == Parameter.VAR_KEYWORD:
            yield '**' + arg.name
        else:
            yield arg.name

# pylint: enable=no-member

__all__ = [
    'get_arg_names',
    'get_call_args',
]
