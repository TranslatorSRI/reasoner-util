"""Build merging and normalizing functions."""
from typing import Hashable, Iterable, List, TypeVar
import httpx
from bmt import Toolkit
import json

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
    descendants = {
        descendant
        for item in items
        for descendant in tk.get_descendants(
            item,
            reflexive=False,
            formatted=True,
        )
    }
    return [
        item
        for item in items
        if item not in descendants
    ]


def get_all_curies(message_dict: dict) -> List[str]:
    """Grab all curies from the trapi message. The output will
    be a list of lists"""
    all_curies = []
    query_nodes = message_dict["message"]["query_graph"]["nodes"]
    for qnode in query_nodes:
        ids = message_dict["message"]["query_graph"]["nodes"][qnode]["ids"]
        if ids is not None:
            all_curies += ids
        else:
            all_curies += []
    kgraph_ids = list(
        message_dict["message"]["knowledge_graph"]["nodes"].keys()
    )
    all_curies += kgraph_ids
    return all_curies


def map_normalized_node_ids(message_dict: dict):
    """Create a query node mapping to the original ids and
    the new normalized ids. Output includes the node, input ids,
    and the ids after normalization"""
    nodes = message_dict["message"]["query_graph"]["nodes"]
    nodes_map = {}
    for node in nodes:
        ids = message_dict["message"]["query_graph"]["nodes"][node]["ids"]
        if ids is not None:
            nodes_map[node] = ids
        else:
            nodes_map[node] = []
    output = {
        node: {"input_ids": ids, "normalized_ids": normalize_ids(ids)}
        for (node, ids) in nodes_map.items()
    }
    return output
