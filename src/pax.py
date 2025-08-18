class Pax:
    id: int
    nom = ""
    prenom = ""
    numero_tel = ""
    mail = ""
    solde = 0
    est_X = True

    def __init__(self, id, nom, prenom, est_X=True, numero_tel="", mail="", solde=0):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.est_X = est_X
        self.numero_tel = numero_tel
        self.mail = mail
        self.solde = solde

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Pax) and self.id == o.id

    def __lt__(self, o: object) -> bool:
        return self.id < o.id

    def __str__(self) -> str:
        string = "{prenom} {nom}, solde : {solde}, ".format(
            prenom=self.prenom, nom=self.nom, solde=self.solde
        )
        if self.est_X:
            string += "est X"
        else:
            string += "n'est pas X"
        if self.numero_tel:
            string += ", numero de telephone : {}".format(self.numero_tel)
        if self.numero_tel:
            string += ", email : {}".format(self.mail)
        return string


class Croyant:
    membres: list[Pax]
    filename: str

    def __init__(self) -> None:
        self.membres = []
        self.filename = "data/pax.csv"

    def import_from_database(self) -> None:
        file_pax = open(self.filename, "r")
        file_pax.readline()
        for ligne in file_pax:
            self.membres.append(parse_pax(ligne))
        file_pax.close()

    def add_pax(self, pax: Pax) -> None:
        self.membres.append(pax)

    def delete_pax(self, heretique):
        for i in range(len(self.membres)):
            if heretique == self.membres[i]:
                self.membres.pop(i)
                return 0
        return 1

    def save(self) -> None:
        file_pax = open(self.filename, "w")
        file_pax.write("id;nom;prenom;est_X;numero_tel;mail;solde\n")
        for pax in self.membres:
            file_pax.write(file_line_of_pax(pax))
        file_pax.close()

    def __len__(self) -> int:
        return len(self.membres)

    def __iter__(self):
        return self.membres.__iter__()

    def __getitem__(self, index: int) -> Pax:
        return self.membres[index]

    def find_pax(
        self,
        clees: list[str | bool | int] | str | bool | int,
        critere_clees: list[str] | str,
    ) -> list[Pax]:
        clees, critere_clees = self.clean_find_clees(clees, critere_clees)
        return self.find_pax_plusieurs_criteres(clees, critere_clees)

    def clean_find_clees(
        self,
        clees: list[str | bool | int] | str | bool | int,
        critere_clees: list[str] | str,
    ) -> tuple[list[str | bool | int], list[str]]:
        try:
            clees[0]
            return (
                [clee for clee in clees if clee != ""],
                [critere_clees[i] for i in range(len(critere_clees)) if clees[i] != ""],
            )
        except:
            return [clees], [critere_clees]

    def find_pax_plusieurs_criteres(
        self, clees: list[str | bool | int], critere_clees: list[str]
    ) -> list[Pax]:
        listes_trouves = []
        for i in range(len(clees)):
            listes_trouves.append(self.find_pax_1_critere(clees[i], critere_clees[i]))
        return self.find_pax_fusion(listes_trouves)

    def find_pax_1_critere(self, clee: str | bool | int, critere: str) -> list[int]:
        match critere:
            case "id":
                return self.find_pax_id(clee)
            case "nom":
                return self.find_pax_nom(clee)
            case "prenom":
                return self.find_pax_prenom(clee)
            case "est_X":
                return self.find_pax_est_X(clee)
            case "numero_tel":
                return self.find_pax_numero_tel(clee)
            case "mail":
                return self.find_pax_mail(clee)

    def find_pax_id(self, id: int) -> list[int]:
        for i in range(len(self.membres)):
            if self.membres[i].id == id:
                return [i]

    def find_pax_nom(self, nom: str) -> list[int]:
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].nom == nom:
                trouves.append(i)
        return trouves

    def find_pax_prenom(self, prenom: str) -> list[int]:
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].prenom == prenom:
                trouves.append(i)
        return trouves

    def find_pax_est_X(self, est_X: bool) -> list[int]:
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].est_X == est_X:
                trouves.append(i)
        return trouves

    def find_pax_numero_tel(self, numero_tel: str) -> list[int]:
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].numero_tel == numero_tel:
                trouves.append(i)
        return trouves

    def find_pax_mail(self, mail: str) -> list[int]:
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].mail == mail:
                trouves.append(i)
        return trouves

    def find_pax_fusion(self, listes_trouves: list[list[int]]) -> list[Pax]:
        trouves = []
        for idx_pax in listes_trouves[0]:
            verifie_autres_criteres = True
            for liste in listes_trouves[1:]:
                if idx_pax not in liste:
                    verifie_autres_criteres = False
                    break
            if verifie_autres_criteres:
                trouves.append(idx_pax)
        return [self.membres[i] for i in trouves]


def parse_pax(ligne: str) -> Pax:
    id, nom, prenom, est_X, numero_tel, mail, solde = ligne.split(";")
    return Pax(
        int(id),
        nom,
        prenom,
        bool_of_string_est_X(est_X),
        numero_tel,
        mail,
        int(solde),
    )


def bool_of_string_est_X(est_X: str) -> str | bool:
    if est_X == "":
        return ""
    return not est_X == "0"


def file_line_of_pax(pax: Pax) -> str:
    return (
        str(pax.id)
        + ";"
        + pax.nom
        + ";"
        + pax.prenom
        + ";"
        + string_of_bool_est_X(pax.est_X)
        + ";"
        + pax.numero_tel
        + ";"
        + pax.mail
        + ";"
        + str(pax.solde)
        + "\n"
    )


def string_of_bool_est_X(est_X: bool) -> str:
    if est_X:
        return "1"
    return "0"
