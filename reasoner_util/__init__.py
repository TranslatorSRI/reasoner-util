"""Build merging and normalizing functions."""
from typing import Hashable, Iterable, List, TypeVar
import copy
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


def normalize_qcategories(message_dict: dict) -> None:
    """Normalize categories for each node in the query graph by stripping
    all descendants. Modify the message in place."""
    q_nodes = message_dict["message"]["query_graph"]["nodes"]
    for q_node in q_nodes.values():
        q_node["categories"] = strip_descendants(q_node["categories"])


def normalize_qpredicates(message_dict: dict) -> None:
    """Normalize predicates for each edge in the query graph by stripping
    all descendants. Modify the message in place."""
    q_edges = message_dict["message"]["query_graph"]["edges"]
    for q_edge in q_edges.values():
        q_edge["predicates"] = strip_descendants(q_edge["predicates"])


def normalize_kcategories(message_dict: dict) -> None:
    """Normalize categories for each node in the knowledge graph by stripping
    all ancestors. Modify the message in place."""
    k_nodes = message_dict["message"]["knowledge_graph"]["nodes"]
    for k_node in k_nodes.values():
        k_node["categories"] = strip_ancestors(k_node["categories"])


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


def strip_ancestors(items: List[str]) -> List[str]:
    """strip ancestors of biolink categories or predicates"""
    ancestors = {
        ancestor
        for item in items
        for ancestor in tk.get_ancestors(
            item,
            reflexive=False,
            formatted=True,
        )
    }
    return [
        item
        for item in items
        if item not in ancestors
    ]


def get_all_ids(message_dict: dict) -> List[str]:
    """Grab all ids from the trapi message. The output will
    be a list of lists"""
    all_ids = []
    query_nodes = message_dict["message"]["query_graph"]["nodes"]
    for qnode in query_nodes:
        ids = message_dict["message"]["query_graph"]["nodes"][qnode]["ids"]
        if ids is not None:
            all_ids += ids
        else:
            all_ids += []
    kgraph_ids = list(
        message_dict["message"]["knowledge_graph"]["nodes"].keys()
    )
    all_ids += kgraph_ids
    results = message_dict["message"]["results"]
    for result in results:
        for rnode in result["node_bindings"]:
            for entry in result["node_bindings"][rnode]:
                all_ids.append(entry["id"])
    return all_ids


def map_ids(original_ids: List[str], normalized_ids: List[str]) -> dict:
    """Map normalized curies(ids) to the original curies
    from the trapi message"""
    return {
        original_id: normalized_id
        for original_id, normalized_id in zip(original_ids, normalized_ids)
    }


def apply_ids(id_map: dict, message_dict: dict) -> None:
    """Apply id map to message dictionary. Modify the message in place."""
    qgraph = message_dict["message"]["query_graph"]
    kgraph = message_dict["message"]["knowledge_graph"]

    for qnode in qgraph["nodes"].values():
        if qnode["ids"] is None:
            continue
        qnode["ids"] = [
            id_map[item]
            for item in qnode["ids"]
        ]
    kgraph["nodes"] = {
        id_map[knode_id]: knode
        for knode_id, knode in kgraph["nodes"].items()
    }
    for edge in kgraph["edges"].values():
        edge["subject"] = id_map[edge["subject"]]
        edge["object"] = id_map[edge["object"]]
    for result in message_dict["message"]["results"]:
        for rnode in result["node_bindings"].values():
            for entry in rnode:
                entry["id"] = id_map[entry["id"]]


def merge_qedges(
        message_dict1: dict,
        message_dict2: dict,
        merged_message_dict: dict = None
        ) -> dict:
    """Merge qedges: the keys must be the same and the values must be the same.
    If a key is unique to one message, then the edge will be concatinated to
    the new edges dictionary. If a particular key exists in both messages but
    the values do not match, this will result in an error. """
    if merged_message_dict is None:
        merged_message_dict = copy.deepcopy(message_dict1)

    qedges1 = message_dict1["message"]["query_graph"]["edges"]
    qedges2 = message_dict2["message"]["query_graph"]["edges"]

    new_qedges = {}
    for qedge in qedges1:
        if qedge in qedges2.keys():
            if qedges1[qedge] == qedges2[qedge]:
                new_qedges[qedge] = qedges1[qedge]
            else:
                raise ValueError(
                    "Key exists in both messages but values do not match."
                )
        else:
            new_qedges[qedge] = qedges1[qedge]

    for qedge in qedges2:
        if qedge not in new_qedges.keys():
            new_qedges[qedge] = qedges2[qedge]

    merged_message_dict["message"]["query_graph"]["edges"] = new_qedges
    return merged_message_dict
