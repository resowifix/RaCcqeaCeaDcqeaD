import pytest
import sys
import os
sys.path.append("src/")
import bouffe


bouffe1 = bouffe.Bouffe(0, "20250815", 100, [0, 1, 4])
bouffe_vide = bouffe.Bouffe(1, "20250423", 20, [])
bouffe_gratos = bouffe.Bouffe(2, "20250909", 0, [1, 0, 5])
bouffe_fausse_date = bouffe.Bouffe(3, "20253854", 12, [1])


# === Tests sur Bouffe ===
@pytest.mark.parametrize("bouffe1, bouffe2, equal", [
    (bouffe1, bouffe.Bouffe(0, "20250815", 100, [0, 1, 4]), True),  # mêmes dates => égalité
    (bouffe1, bouffe_vide, False),
    (bouffe1, bouffe.Bouffe(1, "20250815", 100, [0, 1, 4]), False)
])
def test_bouffe_eq(bouffe1: bouffe.Bouffe, bouffe2: bouffe.Bouffe, equal: bool) -> None:
    assert (bouffe1 == bouffe2) == equal


@pytest.mark.parametrize("bouffe1, bouffe2, result", [
    (bouffe_vide, bouffe1, True),   # date b1 < date b2
    (bouffe_gratos, bouffe1, False),
])
def test_bouffe_lt(bouffe1: bouffe.Bouffe, bouffe2: bouffe.Bouffe, result: bool) -> None:
    assert (bouffe1 < bouffe2) == result


@pytest.mark.parametrize("bouffeObj, expected", [
    (bouffe1, "0;20250815;100;[0, 1, 4]\n"),
    (bouffe_vide, "1;20250423;20;[]\n"),
])
def test_file_line_of_bouffe(bouffeObj: bouffe.Bouffe, expected: str) -> None:
    assert bouffe.file_line_of_bouffe(bouffeObj) == expected


@pytest.mark.parametrize("ligne, result", [
    ("0;20250815;100;[0, 1, 4]\n", bouffe1),
    ("1;20250423;20;[]\n", bouffe_vide),
])
def test_parse_bouffe(ligne: str, result: bouffe.Bouffe) -> None:
    assert bouffe.parse_bouffe(ligne) == result


@pytest.mark.parametrize("string, list_result", [
    ("[]", []),
    ("[1, 3, 4]", [1, 3, 4])
])
def test_str_to_list(string: str, list_result: list[int]) -> None:
    assert bouffe.str_to_list(string) == list_result


# === Tests sur Ensemble_bouffes ===
@pytest.mark.parametrize("bouffeList, expected_length", [
    ([bouffe1], 1),
    ([bouffe1, bouffe_vide, bouffe_gratos], 3),
])
def test_len(bouffeList: bouffe.Bouffe, expected_length: int) -> None:
    ens = bouffe.Ensemble_bouffes()
    for b in bouffeList:
        ens.add_bouffe(b)
    assert len(ens) == expected_length


@pytest.mark.parametrize("bouffeList, index, expected", [
    ([bouffe1, bouffe_gratos], 0, bouffe1),
    ([bouffe1, bouffe_gratos], 1, bouffe_gratos),
])
def test_get_item(bouffeList: bouffe.Bouffe, index: int, expected: bouffe.Bouffe):
    ens = bouffe.Ensemble_bouffes()
    for b in bouffeList:
        ens.add_bouffe(b)
    assert ens[index] == expected


def test_delete_bouffe():
    ens = bouffe.Ensemble_bouffes()
    ens.add_bouffe(bouffe1)
    ens.add_bouffe(bouffe_vide)

    # Suppression existante
    res = ens.delete_bouffe(bouffe1)
    assert res == 0
    assert len(ens) == 1 and ens[0] == bouffe_vide

    # Suppression inexistante
    res = ens.delete_bouffe(bouffe_gratos)
    assert res == 1


def test_find_bouffe():
    ens = bouffe.Ensemble_bouffes()
    ens.add_bouffe(bouffe1)
    ens.add_bouffe(bouffe_vide)

    assert ens.find_bouffe("20250815") == 0
    assert ens.find_bouffe("20250423") == 1
    assert ens.find_bouffe("20250505") is None


def test_save_and_import():
    ens = bouffe.Ensemble_bouffes()
    ens.filename = "bouffes.csv"
    ens.add_bouffe(bouffe1)
    ens.add_bouffe(bouffe_vide)

    # Test sauvegarde
    ens.save()
    file = open(ens.filename, "r")
    content = file.readlines()

    # Première ligne = header
    assert content[0] == "id;date;montant;participants\n"
    # Reste correspond à file_line_of_bouffe
    assert content[1] == "0;20250815;100;[0, 1, 4]\n"
    assert content[2] == "1;20250423;20;[]\n"

    # Import => plante car parse_bouffe est incomplet
    new_ens = bouffe.Ensemble_bouffes()
    new_ens.filename = ens.filename
    new_ens.import_from_database()
    assert new_ens.bouffes == [bouffe1, bouffe_vide]
    os.system(f"rm {ens.filename}")
