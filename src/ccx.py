import bouffe as lib_bouffe
import pax as lib_pax
import utilitaire as util


class CCX:
    bouffes: lib_bouffe.Ensemble_bouffes
    pax: lib_pax.Croyant
    presence: list[list[bool]]

    def __init__(self):
        self.bouffes = lib_bouffe.Ensemble_bouffes()
        self.pax = lib_pax.Croyant()
        self.bouffes.import_from_database()
        self.pax.import_from_database()
        self.presence = [[42] * len(self.bouffes) for i in range(len(self.pax))]
        self.set_up_presence()

    def set_up_presence(self):
        presence_file = open("data/presence.csv", "r")
        bouffes = util.parse_line_1_presence(presence_file.readline())
        idx = 0
        for ligne in presence_file:
            id_pax, presenc_bouffes = util.parse_presence(ligne)
            if self.pax[idx] == id_pax:
                for i in range(len(self.bouffes)):
                    if self.bouffes[i] == bouffes[i]:
                        self.presence[idx][i] = presenc_bouffes[i]

    def save(self):
        self.pax.save()
        self.bouffes.save()

    def add_bouffe(self, id: int, date: str, montant: int, participants: list[int]) -> None:
        cene = lib_bouffe.Bouffe(id, date, montant, participants)
        self.bouffes.add_bouffe(cene)

    def add_pax(
        self, id: int, nom: str, prenom: str, est_X: bool, numero_tel: str, mail: str
    ) -> None:
        converti = lib_pax.Pax(id, nom, prenom, est_X, numero_tel, mail)
        self.pax.add_pax(converti)

    def find_pax(
        self,
        clees: list[str | int | bool] | str | int | bool,
        critere_clees: list[str] | str,
    ) -> list[lib_pax.Pax]:
        return self.pax.find_pax(clees, critere_clees)
