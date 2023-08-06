"""."""

import os
import sys


# Things we consider to be False in a boolean variable
_FALSE_SET = (0, '0', '')


def _get_var_or_exit(var: str) -> str:
    value = os.getenv(var)
    if value is None:
        sys.exit('{} was not supplied in the environment.'.format(var))
    return value


def requiredvar(var: str) -> str:
    """Return the value of the required environment variable, `var`.

    If `var` is not available in the environment, `sys.exit()` is called with a
    message detailing that the variable was not supplied.
    """
    return _get_var_or_exit(var)


def requiredbool(var: str) -> bool:
    """Return the value of the required boolean environment variable, `var`.

    If `var` is present and non-zero, `True` will be returned. Otherwise,
    `False` is returned.

    If `var` is not present in the environment, `sys.exit()` is called with a
    message detailing that the variable was not supplied.
    """
    return _get_var_or_exit(var) not in _FALSE_SET


def optionalvar(var: str, default: bool) -> str:
    """Return the value of the optional environment variable, `var`.

    If `var` is present in the environment, its value will be returned. If it
    is not present in the environment, `default` will be returned.
    """
    value = os.getenv(var)
    return value if value else default


def optionalbool(var: str, default: bool) -> bool:
    """Return the value of the optional boolean environment variable, `var`.

    If `var` is present in the environment, its value will be returned. If it
    is not present in the environment, `default` will be returned.
    """
    value = os.getenv(var)
    if value is None:
        return default
    return True if value not in _FALSE_SET else False
