"""Test merging."""
import json

from reasoner_util import merge_categories, merge_ids
from reasoner_util import merge_qedges

from .util import unordered_lists_equal


def test_merge_ids():
    """Test merge_ids()."""
    cats1 = [
        "MONDO:0005737",
    ]
    cats2 = [
        "MONDO:0000001",
        "MONDO:0004979",
    ]
    assert unordered_lists_equal(
        merge_ids(cats1, cats2),
        [
            "MONDO:0005737",
            "MONDO:0000001",
            "MONDO:0004979",
        ],
    )


def test_merge_categories():
    """Test merge_categories()."""
    cats1 = [
        "biolink:Disease",
    ]
    cats2 = [
        "biolink:ChemicalSubstance",
        "biolink:DiseaseOrPhenotypicFeature",
    ]
    assert unordered_lists_equal(
        merge_categories(cats1, cats2),
        [
            "biolink:ChemicalSubstance",
            "biolink:Disease",
            "biolink:DiseaseOrPhenotypicFeature",
        ],
    )


def test_merge_qedges():
    """Test merge_qedges"""
    with open("tests/test_jsons/test_merge_qedges1.json", "r") as file:
        qedges1 = json.load(file)
    with open("tests/test_jsons/test_merge_qedges2.json", "r") as file:
        qedges2 = json.load(file)

    merged_qedges = merge_qedges(qedges1, qedges2)

    with open("tests/test_jsons/test_merge_qedges_success.json", "r") as file:
        correct_merged_qedges = json.load(file)

    assert merged_qedges == correct_merged_qedges
