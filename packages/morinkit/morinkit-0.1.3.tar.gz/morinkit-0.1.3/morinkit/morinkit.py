"""
morinkit.morinkit
~~~~~~~~~~~~~~~~~

This module acts as the entry point to the morinkit package.
"""

import sys
import logging
from .ui import parse_args
from .utils import config_logging
from . import convert, process, summarize
from .exceptions import NotUniqueError

MODULES = [convert, process, summarize]


def find_func(name, modules=MODULES):
    """Find function with a given name in a given set of modules.

    This is mainly used to find the relevant function for a given
    subcommand.

    Args:
        name (str): Function name.
        modules (list): List of modules.

    Returns:
        Function object or None.

    Raises:
        NotUniqueError: Found more than one function with the given name
    """
    assert isinstance(name, str), '`name` is not a string'
    assert isinstance(modules, list), '`modules` is not a list'
    funcs = []
    for m in modules:
        func = getattr(m, name, None)
        if func is not None:
            funcs.append(func)
    if len(funcs) == 0:
        return None
    if len(funcs) == 1:
        return funcs[0]
    elif len(funcs) > 1:
        raise NotUniqueError('Found more than one function named {}'.format(name))


def main():
    """Call relevant function based on command-line arguments."""
    config_logging()
    logging.info('Command: {}'.format(' '.join(sys.argv)))
    args = parse_args()
    subcommand = args.pop("subcommand")
    func = find_func(subcommand)
    func(**args)


if __name__ == '__main__':
    main()
