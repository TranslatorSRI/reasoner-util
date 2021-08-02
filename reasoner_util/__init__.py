"""Build merging functions."""
from typing import Hashable, Iterable, List, TypeVar

T = TypeVar("T", bound=Hashable)

def merge_iterables(cats1: Iterable[T], cats2: Iterable[T]) -> List[T]:
    """Merge iterables."""
    return list(set(cats1) | set(cats2))


merge_ids = merge_iterables
merge_categories = merge_iterables
