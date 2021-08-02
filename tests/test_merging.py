"""Test merging."""
from reasoner_util import merge_categories, merge_ids

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
