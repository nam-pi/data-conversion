"""The module for the Source_type class.

Classes:
    Source_type
"""
from enum import Enum, auto


class Source_type(Enum):
    """The type of a source."""

    MANUSCRIPT = auto()
    ONLINE_RESOURCE = auto()
