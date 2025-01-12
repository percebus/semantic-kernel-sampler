"""
This type stub file was generated by pyright.
"""

from decimal import Decimal
from typing import Any, Union, overload
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

__author__ = ...
__copyright__ = ...
__license__ = ...
Number = Union[float, Decimal]
def isnumeric(value: Any) -> bool:
    """Confirm that 'value' can be treated numerically; duck-test accordingly"""
    ...

class IsCloseTo(BaseMatcher[Number]):
    def __init__(self, value: Number, delta: Number) -> None:
        ...
    
    def describe_mismatch(self, item: Number, mismatch_description: Description) -> None:
        ...
    
    def describe_to(self, description: Description) -> None:
        ...
    


@overload
def close_to(value: float, delta: float) -> Matcher[float]:
    ...

@overload
def close_to(value: Decimal, delta: Decimal) -> Matcher[Decimal]:
    ...

def close_to(value, delta): # -> IsCloseTo:
    """Matches if object is a number close to a given value, within a given
    delta.

    :param value: The value to compare against as the expected value.
    :param delta: The maximum delta between the values for which the numbers
        are considered close.

    This matcher compares the evaluated object against ``value`` to see if the
    difference is within a positive ``delta``.

    Example::

        close_to(3.0, 0.25)

    """
    ...

