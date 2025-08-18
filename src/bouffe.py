class Bouffe:
    id: int
    date: str
    montant: int
    participants: list[int]

    def __init__(self, id: int, date: str, montant: int, participants: list[int]) -> None:
        self.id = id
        self.date = date
        self.montant = montant
        self.participants = participants

    def __eq__(self, o):
        return isinstance(o, Bouffe) and self.id == o.id

    def __lt__(self, o):
        return self.date < o.date


class Ensemble_bouffes:
    bouffes: list[Bouffe]
    filename: str

    def __init__(self):
        self.bouffes = []
        self.filename = "data/bouffes.csv"

    def import_from_database(self):
        file_bouffes = open(self.filename, "r")
        file_bouffes.readline()
        for ligne in file_bouffes:
            self.bouffes.append(parse_bouffe(ligne))
        file_bouffes.close()

    def add_bouffe(self, bouffe):
        self.bouffes.append(bouffe)

    def delete_bouffe(self, vieille_bouffe) -> int:
        for i in range(len(self.bouffes)):
            if vieille_bouffe == self.bouffes[i]:
                self.bouffes.pop(i)
                return 0
        return 1

    def save(self):
        file_bouffes = open(self.filename, "w")
        file_bouffes.write("id;date;montant;participants\n")
        for bouffe in self.bouffes:
            file_bouffes.write(file_line_of_bouffe(bouffe))
        file_bouffes.close()

    def __len__(self):
        return len(self.bouffes)

    def __iter__(self):
        return self.bouffes.__iter__()

    def __getitem__(self, index):
        return self.bouffes[index]

    def find_bouffe(self, date):
        for i in range(len(self.bouffes)):
            if self.bouffes[i].date == date:
                return i


def parse_bouffe(ligne: str) -> Bouffe:
    ligne = ligne[:-1]
    t = ligne.split(";")
    id, date, montant, participants = t
    return Bouffe(int(id), date, int(montant), str_to_list(participants))


def str_to_list(chaine: str) -> list[int]:
    if chaine == "[]":
        return []
    chaine = chaine[1:-1]
    print(chaine)
    print(chaine.split(","))
    return [int(i) for i in chaine.split(",")]


def file_line_of_bouffe(bouffe: Bouffe) -> str:
    return str(bouffe.id) + ";" + bouffe.date + ";" + str(bouffe.montant) + ";" + str(bouffe.participants) + "\n"
