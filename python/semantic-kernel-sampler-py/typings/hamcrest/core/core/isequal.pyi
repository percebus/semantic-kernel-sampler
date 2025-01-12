"""
This type stub file was generated by pyright.
"""

from typing import Any
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

__author__ = ...
__copyright__ = ...
__license__ = ...
class IsEqual(BaseMatcher[Any]):
    def __init__(self, equals: Any) -> None:
        ...
    
    def describe_to(self, description: Description) -> None:
        ...
    


def equal_to(obj: Any) -> Matcher[Any]:
    """Matches if object is equal to a given object.

    :param obj: The object to compare against as the expected value.

    This matcher compares the evaluated object to ``obj`` for equality."""
    ...

