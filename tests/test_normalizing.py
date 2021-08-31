"""Test normalizing."""
import json
from reasoner_util import get_preferred_ids
from reasoner_util import normalize_qcategories
from reasoner_util import normalize_predicates
from reasoner_util import get_all_curies
from reasoner_util import map_ids
from reasoner_util import apply_ids


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
    with open("tests/test_apply_ids.json", "r") as file:
        message_dict = json.load(file)
    output = get_all_curies(message_dict)
    print(output)
    correct_output = [
        "MESH:D003837",
        "EFO:0001645",
        "NCIT:C34424",
        "UMLS:C0003469",
        "UMLS:C0003469",
        "NCIT:C34424",
        "MESH:D003837",
        "CHEBI:15377",
    ]
    assert output == correct_output


def test_map_curies():
    """Test map_curies"""
    original_ids = [
        "CHEBI:15377",
        "MESH:D003837",
        "EFO:0001645",
        "NCIT:C34424",
        "UMLS:C0003469",
        "EFO:1001454",
    ]
    normalized_ids = [
        "PUBCHEM.COMPOUND:962",
        "CHEBI:23639",
        "MONDO:0005010",
        "MONDO:0024613",
        "MONDO:0005618",
        "EFO:1001454",
    ]
    output = map_ids(original_ids, normalized_ids)
    correct_output = {
        "CHEBI:15377": "PUBCHEM.COMPOUND:962",
        "MESH:D003837": "CHEBI:23639",
        "EFO:0001645": "MONDO:0005010",
        "NCIT:C34424": "MONDO:0024613",
        "UMLS:C0003469": "MONDO:0005618",
        "EFO:1001454": "EFO:1001454",
    }
    assert output == correct_output


def test_apply_ids():
    """Test apply_ids"""
    with open("tests/test_apply_ids.json", "r") as file:
        message_dict = json.load(file)
    id_map = {
        "CHEBI:15377": "PUBCHEM.COMPOUND:962",
        "MESH:D003837": "CHEBI:23639",
        "EFO:0001645": "MONDO:0005010",
        "NCIT:C34424": "MONDO:0024613",
        "UMLS:C0003469": "MONDO:0005618"
    }
    output = apply_ids(id_map, message_dict)
    with open("tests/data_file.json", "w") as write_file:
        json.dump(output, write_file)
    with open("tests/test_apply_ids_success.json", "r") as file:
        correct_output = json.load(file)
    assert output == correct_output
