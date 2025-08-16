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
        self.est_X = True
        self.numero_tel = numero_tel
        self.mail = mail
        self.solde = solde

    def __eq__(self, o):
        return isinstance(o, Pax) and self.id == o.id

    def __lt__(self, o):
        return self.id < o.id

    def __str__(self):
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
    membres: list[Pax] = []
    filename: str

    def __init__(self):
        self.filename = "data/pax.csv"

    def import_from_database(self):
        file_pax = open(self.filename, "r")
        file_pax.readline()
        for ligne in file_pax:
            self.membres.append(parse_pax(ligne))
        file_pax.close()

    def add_pax(self, pax):
        self.membres.append(pax)

    def delete_pax(self, heretique):
        for i in range(self.membres):
            if heretique == self.pax[i]:
                self.membres.pop(i)
                return 0
        return 1

    def save(self):
        file_pax = open(self.filename, "w")
        file_pax.write("id;nom;prenom;est_X;numero_tel;mail;solde\n")  
        for pax in self.membres:
            file_pax.write(file_line_of_pax(pax))
        file_pax.close()

    def __len__(self):
        return len(self.membres)

    def __iter__(self):
        return self.membres.__iter__()

    def __getitem__(self, index):
        return self.membres[index]

    def find_pax(self, clees, critere_clees):
        try:
            clees[0]
            return self.find_pax_plusieurs_criteres(clees, critere_clees)
        except:
            return self.find_pax_1_critere(clees, critere_clees)

    def find_pax_plusieurs_criteres(self, clees, critere_clees):
        listes_trouves = []
        for i in range(len(clees)):
            listes_trouves.append(self.find_pax_1_critere(clees[i], critere_clees[i]))
        return self.find_pax_fusion(listes_trouves)

    def find_pax_1_critere(self, clee, critere):
        match critere:
            case "id":
                return self.find_pax_id(id)
            case "nom":
                return self.find_pax_nom(id)
            case "prenom":
                return self.find_pax_prenom(id)
            case "numero_tel":
                return self.find_pax_numero_tel(id)
            case "mail":
                return self.find_pax_mail(id)

    def find_pax_id(self, id):
        for i in range(len(self.membres)):
            if self.membres[i].id == id:
                return [i]

    def find_pax_nom(self, nom):
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].nom == nom:
                trouves.append(i)
        return trouves

    def find_pax_prenom(self, prenom):
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].prenom == prenom:
                trouves.append(i)
        return trouves

    def find_pax_numero_tel(self, numero_tel):
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].numero_tel == numero_tel:
                trouves.append(i)
        return trouves

    def find_pax_mail(self, mail):
        trouves = []
        for i in range(len(self.membres)):
            if self.membres[i].mail == mail:
                trouves.append(i)
        return trouves

    def find_pax_fusion(self, listes_trouves):
        trouves = []
        for idx_pax in listes_trouves[0]:
            verifie_autres_criteres = True
            for liste in listes_trouves[1:]:
                if idx_pax not in liste:
                    verifie_autres_criteres = False
                    break
            if verifie_autres_criteres:
                trouves.append(idx_pax)
        return trouves


def parse_pax(ligne: str) -> Pax:
    id, nom, prenom, est_X, numero_tel, mail, solde = ligne.split(ligne, ";")
    return Pax(
        int(id),
        nom,
        prenom,
        bool_of_string_est_X(est_X),
        numero_tel,
        mail,
        int(solde),
    )


def bool_of_string_est_X(est_X: str) -> bool:
    return not est_X == "0"


def file_line_of_pax(pax: Pax) -> str:
    return (
        str(pax.id)
        + ";"
        + pax.nom
        + ";"
        + pax.prenom
        + ";"
        + sring_of_bool_est_X(pax.est_X)
        + ";"
        + pax.numero_tel
        + ";"
        + pax.mail
        + ";"
        + str(pax.solde)
        + "\n"
    )


def sring_of_bool_est_X(est_X: bool) -> str:
    if est_X:
        return "1"
    return "0"
