"""
morinkit.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains exceptions for morinkit.
"""


class Error(Exception):
    """Base error"""


class NotUniqueError(Error):
    """More than one items found when only one is expected."""
