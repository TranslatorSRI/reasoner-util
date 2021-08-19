"""Build merging and normalizing functions."""
from typing import Hashable, Iterable, List, TypeVar
from typing_extensions import Literal
import httpx
from bmt import Toolkit
from pydantic import tools

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


def normalize_qcatagories(catagories: List[str]) -> List[str]:
    """Normalize a list of catagories by stripping all descendents"""
    normalized_catagories = strip_descendants(catagories)
    return normalized_catagories


def strip_descendants(item_list: List[str]) -> List[str]:
    """strip descendants of biolink catagories or predicates"""
    for x_item in item_list:
        descendants = Toolkit.get_descendants(x_item, reflexive=False)
        for y_item in item_list:
            if y_item in descendants:
                item_list.remove(y_item)
            else:
                pass
    return item_list
