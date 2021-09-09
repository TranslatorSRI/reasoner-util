"""Test normalizing."""
import json
from reasoner_util import get_preferred_ids
from reasoner_util import normalize_qcategories
from reasoner_util import normalize_qpredicates
from reasoner_util import get_all_ids
from reasoner_util import map_ids
from reasoner_util import apply_ids
from reasoner_util import strip_descendants


def test_get_preferred_ids():
    """Test get_preferred_ids"""
    curies = ["CHEBI:15377", "NCIT:C34373"]  # examples of non-preferred ids
    output = get_preferred_ids(curies)
    assert output == ["PUBCHEM.COMPOUND:962", "MONDO:0004976"]


def test_strip_descendants():
    """Test strip_descendants"""
    items = [
         "biolink:Disease",
         "biolink:DiseaseOrPhenotypicFeature",
         "biolink:BiologicalEntity",
         "biolink:NamedThing",
         "biolink:Entity",
     ]
    output = strip_descendants(items)
    correct_output = ["biolink:Entity"]
    assert output == correct_output


def test_normalize_qcategories():
    """Test normalize_qcatagories"""
    with open("tests/test_get_qpredicates_qcategories.json", "r") as file:
        message_dict = json.load(file)
    normalize_qcategories(message_dict)

    with open("tests/test_apply_qcategories_success.json") as file:
        correct_output = json.load(file)

    assert message_dict == correct_output


def test_normalize_qpredicates():
    """Test normalize_predicates"""
    with open("tests/test_get_qpredicates_qcategories.json", "r") as file:
        message_dict = json.load(file)
    normalize_qpredicates(message_dict)

    with open("tests/test_apply_qpredicates_success.json") as file:
        correct_output = json.load(file)

    assert message_dict == correct_output


def test_get_all_ids():
    """"Test get_all_ids"""
    with open("tests/test_apply_ids.json", "r") as file:
        message_dict = json.load(file)
    output = get_all_ids(message_dict)
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


def test_map_ids():
    """Test map_ids"""
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
    apply_ids(id_map, message_dict)
    with open("tests/test_apply_ids_success.json", "r") as file:
        correct_output = json.load(file)
    assert message_dict == correct_output
