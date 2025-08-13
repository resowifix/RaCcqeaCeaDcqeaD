import bouffe as lib_bouffe
import pax as lib_pax
import utilitaire as util


class CCX:
    bouffes = lib_bouffe.Ensemble_bouffes()
    pax = lib_pax.Croyant()
    presence: list[list[bool]]

    def __init__(self):
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
        NotImplemented

    def add_bouffe(self, date, montant, participants):
        NotImplemented

    def add_pax(self, nom, prenom, est_X, numero_tel, mail):
        NotImplemented
