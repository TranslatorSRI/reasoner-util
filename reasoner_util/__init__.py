"""Build merging functions."""
from typing import Hashable, Iterable, List, TypeVar
import httpx

T = TypeVar("T", bound=Hashable)


def merge_iterables(cats1: Iterable[T], cats2: Iterable[T]) -> List[T]:
    """Merge iterables."""
    return list(set(cats1) | set(cats2))


merge_ids = merge_iterables
merge_categories = merge_iterables


def get_preferred_ids(curies: List[str]):
    """Get list of preferred ids for a list of CURIES."""
    params = {"curie": curies}
    r = httpx.get(
        "https://nodenormalization-sri-dev.renci.org/1.1/get_normalized_nodes", 
        params=params,
    )
    r_dict = r.json()
    preferred_ids = [r_dict[curie]['id']['identifier'] for curie in curies]
    return preferred_ids


def normalize_ids(curies: List[str]):
    """Normalize a list of ids by finding the BioLink prefered list of ids
    and stripping out any descendants"""
    normalized_ids = get_preferred_ids(curies)
    # normalized_ids = strip_descendants(normalized_ids)
    return normalized_ids
