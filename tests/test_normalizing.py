"""Test normalizing."""
from reasoner_util import get_preferred_ids
from reasoner_util import normalize_qcategories
from reasoner_util import normalize_predicates


def test_get_preferred_ids():
    """Test get_preferred_ids"""
    curies = ["CHEBI:15377", "NCIT:C34373"]  # examples of non-preferred ids
    output = get_preferred_ids(curies)
    assert output == ["PUBCHEM.COMPOUND:962", "MONDO:0004976"]


def test_normalize_qcategories():
    """Test normalize_qcatagories to test strip_descendants with
    the input of a list of catagories. Note that this test assumes that the
    order of elements in the input does not change"""
    catagories = [
        "biolink:Disease",
        "biolink:DiseaseOrPhenotypicFeature",
        "biolink:ThingWithTaxon",
        "biolink:BiologicalEntity",
        "biolink:NamedThing",
        "biolink:Entity",
      ]
    output = normalize_qcategories(catagories)
    assert output == ["biolink:ThingWithTaxon", "biolink:Entity"]


def test_normalize_predicates():
    """Test normalize_predicates to test strip_descendants with
    the input of a list of predicates"""
    predicates = [
        "biolink:related_to",
        "biolink:interacts_with",
        "biolink:increases_abundance_of",
        "biolink:genetically_interacts_with",
        "biolink:affects_mutation_rate_of",
        "biolink:affects_folding_of",
      ]
    output = normalize_predicates(predicates)
    assert output == ["biolink:related_to"]
