"""Test merging."""
import json
import pytest

from reasoner_util import (
    merge_categories,
    merge_ids,
    merge_qedges,
    merge_qnodes,
    merge_knodes,
    merge_kedges,
)

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


def test_merge_qedges_error():
    """Test merge_qedges"""
    with open("tests/test_jsons/test_merge_qedges1.json", "r") as file:
        qedges1 = json.load(file)
    with open("tests/test_jsons/test_merge_qedges2_w_error.json", "r") as file:
        qedges2 = json.load(file)

    with pytest.raises(ValueError):
        merge_qedges(qedges1, qedges2)


def test_merge_qnodes():
    """Test merge_qnodes"""
    with open("tests/test_jsons/test_merge_qnodes1.json", "r") as file:
        qnodes1 = json.load(file)
    with open("tests/test_jsons/test_merge_qnodes2.json", "r") as file:
        qnodes2 = json.load(file)

    merged_qnodes = merge_qnodes(qnodes1, qnodes2)

    with open("tests/test_jsons/test_merge_qnodes_success.json", "r") as file:
        correct_merged_qnodes = json.load(file)

    assert merged_qnodes == correct_merged_qnodes


def test_merge_qnodes_error():
    """Test merge_qnodes"""
    with open("tests/test_jsons/test_merge_qnodes1.json", "r") as file:
        qnodes1 = json.load(file)
    with open("tests/test_jsons/test_merge_qnodes2_w_error.json", "r") as file:
        qnodes2 = json.load(file)

    with pytest.raises(ValueError):
        merge_qnodes(qnodes1, qnodes2)


def test_merge_knodes():
    """Test merge_knodes"""
    with open("tests/test_jsons/test_merge_knodes1.json", "r") as file:
        knodes1 = json.load(file)
    with open("tests/test_jsons/test_merge_knodes2.json", "r") as file:
        knodes2 = json.load(file)

    merged_knodes = merge_knodes(knodes1, knodes2)

    with open("tests/test_jsons/test_merge_knodes_success.json", "r") as file:
        correct_merged_knodes = json.load(file)

    assert merged_knodes == correct_merged_knodes


def test_merge_kedges():
    """Test merge_kedges"""
    with open("tests/test_jsons/test_merge_kedges1.json", "r") as file:
        kedges1 = json.load(file)
    with open("tests/test_jsons/test_merge_kedges2.json", "r") as file:
        kedges2 = json.load(file)

    merged_kedges = merge_kedges(kedges1, kedges2)

    with open("tests/test_jsons/test_merge_kedges_success.json", "r") as file:
        correct_merged_kedges = json.load(file)

    assert merged_kedges == correct_merged_kedges
