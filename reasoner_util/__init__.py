"""Build merging and normalizing functions."""
from typing import Hashable, Iterable, List, TypeVar
import httpx
from bmt import Toolkit

T = TypeVar("T", bound=Hashable)


def merge_iterables(cats1: Iterable[T], cats2: Iterable[T]) -> List[T]:
    """Merge iterables."""
    return list(set(cats1) | set(cats2))


merge_ids = merge_iterables
merge_categories = merge_iterables


def get_preferred_ids(curies: List[str]) -> List[str]:
    """Get list of preferred ids for a list of CURIES."""
    params = {"curie": curies}
    response = httpx.get(
        "https://nodenormalization-sri-dev.renci.org/1.1/get_normalized_nodes",
        params=params,
    )
    response_dict = response.json()
    preferred_ids = [
        response_dict[curie]["id"]["identifier"]
        for curie in curies
    ]
    return preferred_ids


def normalize_ids(curies: List[str]) -> List[str]:
    """Normalize a list of ids by finding the BioLink prefered list of ids
    and stripping out any descendants"""
    normalized_ids = get_preferred_ids(curies)
    # TODO perform function that strips descendents from the curies list.
    return normalized_ids


def normalize_qcategories(catagories: List[str]) -> List[str]:
    """Normalize a list of catagories by stripping all descendents"""
    normalized_catagories = strip_descendants(catagories)
    return normalized_catagories


def normalize_predicates(predicates: List[str]) -> List[str]:
    """Normalize a list of predicates by stripping all descendents"""
    normalized_predicates = strip_descendants(predicates)
    return normalized_predicates


tk = Toolkit()


def strip_descendants(items: List[str]) -> List[str]:
    """strip descendants of biolink catagories or predicates"""
    working_items = items.copy()
    for item in items:
        descendants = tk.get_descendants(
            item,
            reflexive=False,
            formatted=True,
        )
        for descendant in descendants:
            if descendant in working_items:
                working_items.remove(descendant)
    stripped_items = working_items
    return stripped_items
