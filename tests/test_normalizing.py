"""Test normalizing."""
from reasoner_util import get_preferred_ids
from reasoner_util import strip_descendants


def test_get_preferred_ids():
    """Test get_preferred_ids"""
    curies = ["CHEBI:15377", "NCIT:C34373"]  # examples of non-preferred ids
    output = get_preferred_ids(curies)
    assert output == ["PUBCHEM.COMPOUND:962", "MONDO:0004976"]


def test_strip_descendants():
    """Test normalize_qcatagories to test strip_descendants with
    the input of a list of catagories"""
    catagories = [
        "biolink:Disease",
        "biolink:DiseaseOrPhenotypicFeature",
        "biolink:ThingWithTaxon",
        "biolink:BiologicalEntity",
        "biolink:NamedThing",
        "biolink:Entity"
      ]
    output = strip_descendants(catagories)
    assert output == ["biolink:ThingWithTaxon", "biolink:Entity"]
