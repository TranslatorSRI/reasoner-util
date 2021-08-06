"""Testing utilities."""
from typing import Iterable, TypeVar
from reasoner_util import get_preferred_ids

T = TypeVar("T")


def unordered_lists_equal(list1: Iterable[T], list2: Iterable[T]) -> bool:
    """Evaluate equality of two lists, assuming they are unordered."""
    return sorted(list1) == sorted(list2)


def test_get_preferred_ids():
    """Test get_preferred_ids"""
    curies = ["CHEBI:15377", "NCIT:C34373"]  # examples of non-preffered ids
    output = get_preferred_ids(curies)
    assert output == ["PUBCHEM.COMPOUND:962", "MONDO:0004976"]
