import pytest
import sys
import os
sys.path.append("src/")
import pax


paxPierre = pax.Pax(0, "Pierre", "Simon", False, "0101010101", "pierre@simon.jd")
paxVaneau = pax.Pax(1, "Vaneau", "Louis", True, "0612121212", "louis.vaneau@polytechnique.edu")
paxJudas = pax.Pax(2, "Le Radin", "Judas", False, "0000000000", "judas@iscariote@gmail.com")


def create_croyants_and_add_pax_list(paxList: list[pax.Pax]) -> pax.Croyant:
    cr = pax.Croyant()
    for p in paxList:
        cr.add_pax(p)
    return cr


@pytest.mark.parametrize("paxList, membreResult", [
    ([paxPierre], [paxPierre]),
    ([paxPierre, paxVaneau, paxJudas], [paxPierre, paxVaneau, paxJudas])
])
def test_add_pax(paxList: list[pax.Pax], membreResult: list[pax.Pax]) -> None:
    croyants = create_croyants_and_add_pax_list(paxList)
    assert croyants.membres == membreResult


@pytest.mark.parametrize("heretique, membreResult", [
    (paxPierre, [paxVaneau])
])
def test_delete_pax(heretique: pax.Pax, membreResult: list[pax.Pax]) -> None:
    paxList = [paxPierre, paxVaneau]
    croyants = create_croyants_and_add_pax_list(paxList)
    croyants.delete_pax(heretique)
    assert croyants.membres == membreResult


@pytest.mark.parametrize("saveFile", [
    (['id;nom;prenom;est_X;numero_tel;mail;solde\n', '0;Pierre;Simon;0;0101010101;pierre@simon.jd;0\n', '1;Vaneau;Louis;1;0612121212;louis.vaneau@polytechnique.edu;0\n', '2;Le Radin;Judas;0;0000000000;judas@iscariote@gmail.com;0\n'])
])
def test_save(saveFile: str) -> None:
    paxList = [paxPierre, paxVaneau, paxJudas]
    croyants = create_croyants_and_add_pax_list(paxList)
    croyants.filename = "test_save.csv"
    croyants.save()
    file = open(croyants.filename, "r")
    content = file.readlines()
    assert content == saveFile
    file.close()
    os.system(f"rm {croyants.filename}")


@pytest.mark.parametrize("paxList, lenght", [
    ([paxPierre], 1),
    ([paxJudas, paxPierre, paxVaneau], 3)
])
def test_len(paxList: list[pax.Pax], lenght: int) -> None:
    croyants = create_croyants_and_add_pax_list(paxList)
    assert len(croyants) == lenght


@pytest.mark.parametrize("paxList, item_number, item", [
    ([paxJudas], 0, paxJudas),
    ([paxPierre, paxVaneau], 1, paxVaneau)
])
def test_get_item(paxList: list[pax.Pax], item_number: int, item: pax.Pax) -> None:
    croyants = create_croyants_and_add_pax_list(paxList)
    assert croyants[item_number] == item


@pytest.mark.parametrize("clee, critere_clee, result", [
    (0, "id", [paxPierre]),
    ([0, "Judas"], ["id", "prenom"], []),
    ("Judas", "prenom", [paxJudas]),
    ("Le Radin", "nom", [paxJudas]),
    (True, "est_X", [paxVaneau]),
    (False, "est_X", [paxPierre, paxJudas]),
    ("0101010101", "numero_tel", [paxPierre]),
    ("louis.vaneau@polytechnique.edu", "mail", [paxVaneau]),
    (["Pierre", "N'importe"], ["prenom", "nom"], []),
    (["Louis", "Vaneau"], ["prenom", "nom"], [paxVaneau])
])
def test_find_pax(clee: list[str | bool | int] | str | bool | int, critere_clee: list[str] | str, result: list[pax.Pax]) -> None:
    paxList = [paxPierre, paxJudas, paxVaneau]
    croyants = create_croyants_and_add_pax_list(paxList)
    assert croyants.find_pax(clee, critere_clee) == result


@pytest.mark.parametrize("ligne, result", [
    ("0;Pierre;Simon;0;0101010101;pierre@simon.jd;0", paxPierre),
    ("1;Vaneau;Louis;1;0612121212;louis.vaneau@polytechnique.edu;0", paxVaneau),
    ("2;Le Radin;Judas;0;0000000000;judas@iscariote@gmail.com;0", paxJudas)
])
def test_parse_pax(ligne: str, result: pax.Pax) -> None:
    assert pax.parse_pax(ligne) == result


@pytest.mark.parametrize("input, output", [
    ("", ""),
    ("0", False),
    ("dsfjkl", True)
])
def test_bool_of_string_est_X(input: str, output: str | bool) -> None:
    assert pax.bool_of_string_est_X(input) == output


@pytest.mark.parametrize("paxObj, ligne", [
    (paxPierre, "0;Pierre;Simon;0;0101010101;pierre@simon.jd;0\n"),
    (paxVaneau, "1;Vaneau;Louis;1;0612121212;louis.vaneau@polytechnique.edu;0\n"),
    (paxJudas, "2;Le Radin;Judas;0;0000000000;judas@iscariote@gmail.com;0\n")
])
def test_file_line_of_pax(paxObj: pax.Pax, ligne: str) -> None:
    assert pax.file_line_of_pax(paxObj) == ligne


@pytest.mark.parametrize("est_X, string", [
    (True, "1"),
    (False, "0")
])
def test_string_of_bool_est_X(est_X: bool, string: str) -> None:
    assert pax.string_of_bool_est_X(est_X) == string
