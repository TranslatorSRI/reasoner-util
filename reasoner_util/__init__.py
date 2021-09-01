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
    results = message_dict["message"]["results"]
    for result in results:
        for rnode in result["node_bindings"]:
            for entry in result["node_bindings"][rnode]:
                all_curies.append(entry["id"])
    return all_curies


def map_ids(original_ids: List[str], normalized_ids: List[str]) -> dict:
    """Map normalized curies(ids) to the original curies
    from the trapi message"""
    return {
        original_id: normalized_id
        for original_id, normalized_id in zip(original_ids, normalized_ids)
    }


def apply_ids(id_map: dict, message_dict: dict):
    """Apply id map to message dictionary"""
    qgraph = message_dict["message"]["query_graph"]
    kgraph = message_dict["message"]["knowledge_graph"]

    for qnode in qgraph["nodes"]:
        if qgraph["nodes"][qnode]["ids"] is None:
            continue
        qgraph["nodes"][qnode]["ids"] = [
            id_map[item]
            for item in qgraph["nodes"][qnode]["ids"]
        ]
    for node in kgraph["nodes"]:
        kgraph["nodes"][
            id_map[node]
        ] = kgraph["nodes"].pop(node)
    for edge in kgraph["edges"]:
        e_subject = kgraph["edges"][edge]["subject"]
        e_object = kgraph["edges"][edge]["object"]
        kgraph["edges"][edge]["subject"] = id_map[e_subject]
        kgraph["edges"][edge]["object"] = id_map[e_object]
    for result in message_dict["message"]["results"]:
        for rnode in result["node_bindings"]:
            for entry in result["node_bindings"][rnode]:
                entry["id"] = id_map[entry["id"]]
    return message_dict
