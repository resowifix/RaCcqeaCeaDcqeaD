import pytest
import sys
import os
sys.path.append("src/")
import pax


paxPierre = pax.Pax(0, "Pierre", "Simon", False, "0101010101", "pierre@simon.jd")
paxVaneau = pax.Pax(1, "Vaneau", "Louis", True, "0612121212", "louis.vaneau@polytechnique.edu")
paxJudas = pax.Pax(2, "Le Radin", "Judas", False, "0000000000", "judas@iscariote@gmail.com")


@pytest.mark.parametrize("paxList, membreResult", [
    ([paxPierre], [paxPierre]),
    ([paxPierre, paxVaneau, paxJudas], [paxPierre, paxVaneau, paxJudas])
])
def test_add_pax(paxList: list[pax.Pax], membreResult: list[pax.Pax]) -> None:
    croyants = pax.Croyant()
    for p in paxList:
        croyants.add_pax(p)
    assert croyants.membres == membreResult


@pytest.mark.parametrize("heretique, membreResult", [
    (paxPierre, [paxVaneau])
])
def test_delete_pax(heretique: pax.Pax, membreResult: list[pax.Pax]) -> None:
    croyants = pax.Croyant()
    croyants.add_pax(paxPierre)
    croyants.add_pax(paxVaneau)
    croyants.delete_pax(heretique)
    assert croyants.membres == membreResult


@pytest.mark.parametrize("saveFile", [
    (['id;nom;prenom;est_X;numero_tel;mail;solde\n', '0;Pierre;Simon;0;0101010101;pierre@simon.jd;0\n', '1;Vaneau;Louis;1;0612121212;louis.vaneau@polytechnique.edu;0\n', '2;Le Radin;Judas;0;0000000000;judas@iscariote@gmail.com;0\n'])
])
def test_save(saveFile: str) -> None:
    croyants = pax.Croyant()
    croyants.filename = "test_save.csv"
    croyants.add_pax(paxPierre)
    croyants.add_pax(paxVaneau)
    croyants.add_pax(paxJudas)
    croyants.save()
    file = open(croyants.filename, "r")
    content = file.readlines()
    assert content == saveFile
    file.close()
    os.system(f"rm {croyants.filename}")
