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
        return isinstance(o, Bouffe) and self.date == o.date

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
        for i in range(self.bouffes):
            if vieille_bouffe == self.bouffes[i]:
                self.bouffes.pop(i)
                return 0
        return 1

    def save(self):
        file_bouffes = open(self.filename, "w")
        file_bouffes.write("date;montant;participants\n")
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
    t = ligne.split(";")
    print(t)
    date, montant = t
    return Bouffe(date, int(montant))


def file_line_of_bouffe(bouffe: Bouffe) -> str:
    return bouffe.date + ";" + str(bouffe.montant) + ";" + str(bouffe.participants) + "\n"
