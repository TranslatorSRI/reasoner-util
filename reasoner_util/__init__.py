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


def merge_qedges(qedges1: dict, qedges2: dict) -> dict:
    """Merge qedges: the keys must be the same and the values must be the same.
    If a key is unique to one edges dict, then the edge will be concatenated to
    the new edges dictionary. If a particular key exists in both messages but
    the values do not match, this will result in an error. """
    new_edges = copy.deepcopy(qedges1)
    for qedge_key, qedge_value in qedges2.items():
        if qedge_key not in new_edges:
            new_edges[qedge_key] = copy.deepcopy(qedge_value)
        elif qedge_value != new_edges[qedge_key]:
            raise ValueError("Key exists in both messages but values do not match.")
    return new_edges


def merge_qnodes(qnodes1: dict, qnodes2: dict) -> dict:
    """Merge qnodes: the keys must be the same and the values must be the same.
    If a key is unique to one nodes dict, then the node will be concatenated to
    the new nodes dictionary. If a particular key exists in both messages but
    the values do not match, this will result in an error. """
    new_nodes = copy.deepcopy(qnodes1)
    for qnode_key, qnode_value in qnodes2.items():
        if qnode_key not in new_nodes:
            new_nodes[qnode_key] = copy.deepcopy(qnode_value)
        elif qnode_value != new_nodes[qnode_key]:
            raise ValueError("Key exists in both messages but values do not match.")
    return new_nodes


def merge_attributes(
    knode1_attributes: List[dict],
    knode2_attributes: List[dict],
    in_place: bool = False
) -> List[dict]:
    """Find the union of the attributes lists in knowledge graph nodes that
    require merging. Note: in_place=True option is to merge the second
    knode attributes list into the first, rather than providing a third
    receptacle; the default is False."""
    if in_place is False:
        new_node_attributes = copy.deepcopy(knode1_attributes)
    else:
        new_node_attributes = knode1_attributes

    for attribute2 in knode2_attributes:
        if attribute2 not in new_node_attributes:
            new_node_attributes += [copy.deepcopy(attribute2)]
    return new_node_attributes


def merge_knodes(knodes1: dict, knodes2: dict) -> dict:
    """To merge knodes the keys must be the same. The knode values are merged
    by finding the union of their categories list and the union of their
    attributes list."""
    new_nodes = copy.deepcopy(knodes1)
    for knode_key, knode_value in knodes2.items():
        if knode_key not in new_nodes:
            new_nodes[knode_key] = copy.deepcopy(knode_value)
            continue
        new_nodes[knode_key]["attributes"] = merge_attributes(
            new_nodes[knode_key]["attributes"],
            knode_value["attributes"],
            in_place=True
        )
        new_nodes[knode_key]["categories"] = merge_iterables(
            new_nodes[knode_key]["categories"],
            knode_value["categories"]
        )
        new_nodes[knode_key]["categories"].sort()
    return new_nodes
