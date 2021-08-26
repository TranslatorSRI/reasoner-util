"""Test normalizing."""
import json
from reasoner_util import get_preferred_ids
from reasoner_util import normalize_qcategories
from reasoner_util import normalize_predicates
from reasoner_util import get_all_curies


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


def test_get_all_curies():
    """"Test get_all_curies"""
    with open("tests/trapi_message.json", "r") as file:
        message_dict = json.load(file)
    output = get_all_curies(message_dict)
    correct_output = [
        "CHEBI:15377",
        "GO:0043508",
        "GO:1901222",
        "GO:0002480",
        "GO:0002485",
        "GO:0002486",
        "GO:0070433",
        "GO:2001198",
        "GO:0042277",
        "NCBIGene:60412",
        "NCBIGene:3106",
        "GO:0006955",
        "NCBIGene:3106",
        "GO:0002250",
        "NCBIGene:3106",
        "GO:0005515",
        "NCBIGene:3105",
        "GO:0006955",
        "NCBIGene:3105",
        "GO:0005515",
    ]
    assert output == correct_output
