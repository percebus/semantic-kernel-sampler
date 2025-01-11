"""
This type stub file was generated by pyright.
"""

from typing import Pattern, Union
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

__author__ = ...
__copyright__ = ...
__license__ = ...
class StringMatchesPattern(BaseMatcher[str]):
    def __init__(self, pattern) -> None:
        ...
    
    def describe_to(self, description: Description) -> None:
        ...
    


def matches_regexp(pattern: Union[str, Pattern[str]]) -> Matcher[str]:
    """Matches if object is a string containing a match for a given regular
    expression.

    :param pattern: The regular expression to search for.

    This matcher first checks whether the evaluated object is a string. If so,
    it checks if the regular expression ``pattern`` matches anywhere within the
    evaluated object.

    """
    ...

