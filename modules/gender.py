"""The module for the Gender class.

Classes:
    Gender
"""
from enum import Enum, auto


class Gender(Enum):
    """A persons gender."""

    FEMALE = auto()
    MALE = auto()
