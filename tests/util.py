"""Testing utilities."""
from typing import Iterable, TypeVar

T = TypeVar("T")


def unordered_lists_equal(list1: Iterable[T], list2: Iterable[T]) -> bool:
    """Evaluate equality of two lists, assuming they are unordered."""
    return sorted(list1) == sorted(list2)
