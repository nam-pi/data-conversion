"""Module for the NoValue class.

Classes:
    NoValue
"""
from enum import Enum


class NoValue(Enum):
    """Enum-like that hides the actual enum value and enables replacing it with a custom value.

    See:
        https://docs.python.org/3/library/enum.html#omitting-values
    """

    def __repr__(self):
        """Modify the instance."""
        return "<%s.%s>" % (self.__class__.__name__, self.name)
