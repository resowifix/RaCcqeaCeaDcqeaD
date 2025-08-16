def parse_line_1_presence(ligne: str) -> list[str]:
    bouffes = ligne.split(";")[3:]
    delete_last_cr(bouffes)
    return bouffes


def delete_last_cr(bouffes):
    if bouffes:
        bouffes[-1] = bouffes[-1][:-1]


def parse_presence(ligne: str) -> tuple[int, list[bool]]:
    _ligne = ligne.split(";")
    return (int(_ligne[0]), map(bool, map(int, _ligne[3:])))
