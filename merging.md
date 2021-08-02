# Merging messages

The following assumes that we are merging exactly two messages together. To merge more than two, successively merge pairs. The merge operation should be associative and commutative.

After pre-processing, the `query_graph`, `knowledge_graph`, and `results` from the messages should be merged independently.

## Pre-processing

* Each knowledge graph node key, knowledge graph edge endpoint, query graph node id, and node binding should be normalized to use a shared set of preferred identifiers.
* Any superfluous predicates, categories, and ids should be removed (those whose ancestor is also present)
* All `name` properties should be removed.

## Query graph

The query graph `nodes` and `edges` should be merged independently.

Query graph nodes should be merged if and only if their keys are identical and their values are equivalent.
* qnode.ids lists are equivalent when the (unordered) lists are identical _after_ removing any ids whose ancestors are present and accounting for equivalence per node-norm
* qnode.categories lists are equivalent when the (unordered) lists are identical _after_ removing any categories whose ancestors are presentthey are equivalent.
* Identical keys with inconsistent values should result in an error.

Query graph edges should be merged if and only if their keys are identical and their values are equivalent.
* qedge.predicates are equivalent when the (unordered) lists are identical _after_ removing any predicates whose ancestors are presentthey are equivalent.
* Identical keys with inconsistent values should result in an error.

## Knowledge graph

The normalized knowledge graph `nodes` and `edges` should be merged independently.

Knowledge graph nodes should be merged if and only if their keys are equivalent per node-norm.

Knowledge graph edges should be merged if and only if when their subjects, predicates, objects, and original_knowledge_source are identical (any edge without original_knowledge_source is never equivalent).

### Knowledge graph nodes

Knowledge graph node values should be merged by:

* finding the union of their `categories` lists
* finding the union of their `attributes` lists

### Knowledge graph edges

Knowledge graph edge values should be merged by:

* finding the union of their `attributes` lists

## Results

Results should be merged if and only if their node bindings and edge bindings are identical, after accounting for knowledge graph element equivalence.

Two equivalent results should be merged by:

* extracting all key-value pairs aside from node_bindings and edge_bindings into separate objects
* using these objects as values in a `metadata` field, keyed by the corresponding source

For example,
```json
{
    "node_bindings": {"n0": [{"id": "MONDO:xxx"}]},
    "edge_bindings": {},
    "score": 1.0
}
```
and
```json
{
    "node_bindings": {"n0": [{"id": "MONDO:xxx"}]},
    "edge_bindings": {},
    "score": 0.5,
    "description": "This is interesting!"
}
```
will be merged into
```json
{
    "node_bindings": {"n0": [{"id": "MONDO:xxx"}]},
    "edge_bindings": {},
    "metadata": {
        "a": {
            "score": 1.0
        },
        "b": {
            "score": 0.5,
            "description": "This is interesting!"
        }
    }
}
```
