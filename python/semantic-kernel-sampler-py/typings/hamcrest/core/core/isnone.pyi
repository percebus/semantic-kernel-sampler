"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

__author__ = ...
__copyright__ = ...
__license__ = ...
class IsNone(BaseMatcher[Optional[Any]]):
    def describe_to(self, description: Description) -> None:
        ...
    


def none() -> Matcher[Optional[Any]]:
    """Matches if object is ``None``."""
    ...

def not_none() -> Matcher[Optional[Any]]:
    """Matches if object is not ``None``."""
    ...
