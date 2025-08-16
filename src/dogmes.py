class Dogmes:
    dogmes: dict
    file_name: str

    def __init__(self) -> None:
        self.file_name = "data/dogmes.csv"
        self.dogmes = {"id_pax": 0, "id_bouffe": 0}
        self.import_from_file()

    def import_from_file(self) -> None:
        file = open(self.file_name, "r")
        file.readline()
        for ligne in file:
            if ligne != "\n":
                nom, valeur = self.parse_dogme(ligne)
                self.dogmes[nom] = valeur
        file.close()

    def parse_dogme(self, ligne: str) -> tuple[str, str]:
        nom, valeur = ligne.split(";")
        return nom, valeur

    def __str__(self) -> None:
        print(self.dogmes)

    def concile(self, nom: str, reforme: str) -> None:
        self.dogmes[nom] = reforme

    def kt(self, nom: str) -> str:
        return self.dogmes[nom]

    def save(self) -> None:
        file = open(self.file_name, "w")
        lettre = "nom;valeur\n"
        for dogme in self.dogmes:
            lettre += f"{dogme};{self.dogmes[dogme]}\n"
        file.write(lettre)
        file.close()
