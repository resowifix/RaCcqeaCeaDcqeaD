from ccx import CCX
from dogmes import Dogmes
import pax as p
import os


def main() -> None:
    ccx = CCX()
    dogmes = Dogmes()
    stop = False
    print("Tagazok à toi, mon frère !")
    while not stop:
        stop = ask_user(ccx, dogmes)
        if stop:
            stop = stop_app(ccx, dogmes)


def ask_user(ccx: CCX, dogmes: Dogmes) -> bool:
    print("Qu'est ce que tu me veux, wesh ??!!? ", end="")
    message = input()
    action, args = parse_message(message)
    match action:
        case "q":
            return True
        case "h":
            display_help()
            return False
        case "save":
            save(ccx, dogmes)
            return False
        case "aj_pax":
            add_pax(ccx, dogmes, args)
            return False
        case "aj_bouffe":
            add_bouffe(ccx, dogmes, args)
            return False
        case "del_pax":
            del_pax(ccx, args)
            return False
        case "del_bouffe":
            del_bouffe(ccx, args)
            return False
        case "find_pax":
            find_pax(ccx, args)
            return False
        case "find_bouffe":
            find_bouffe(ccx, args)
            return False
        case "reinitialiser":
            reinitialize(ccx)
            return False
        case _:
            unknown_action()
            return False


def parse_message(message: str) -> tuple[str, list[str]]:
    parsed_message = message.split()
    return parsed_message[0], parsed_message[1:]


def display_help() -> None:
    print("T'es pas bien malin !")


def add_pax(ccx: CCX, dogmes: Dogmes, args: list[str]) -> None:
    nom, prenom, est_X, numero_tel, mail = ask_info_pax()
    if check_info_pax(nom, prenom, est_X, numero_tel, mail):
        create_new_pax(ccx, dogmes, nom, prenom, est_X != False, numero_tel, mail)


def check_info_pax(
    nom: str, prenom: str, est_X: bool, numero_tel: str, mail: str
) -> bool:
    return True


def ask_info_pax() -> tuple[str, str, bool, str, str]:
    print("Nom ? ", end="")
    nom = input()
    print("Prenom ? ", end="")
    prenom = input()
    print("C'est un X ? (0 pour non)", end="")
    est_X = p.bool_of_string_est_X(input())
    print("Numero de téléphone ? ", end="")
    numero_tel = input()
    print("Mail ? ", end="")
    mail = input()
    return nom, prenom, est_X, numero_tel, mail


def create_new_pax(
    ccx: CCX,
    dogmes: Dogmes,
    nom: str,
    prenom: str,
    est_X: bool,
    numero_tel: str,
    mail: str,
) -> None:
    id = int(dogmes.kt("id_pax"))
    dogmes.concile("id_pax", str(id + 1))
    ccx.add_pax(id, nom, prenom, est_X, numero_tel, mail)


def add_bouffe(ccx: CCX, dogmes: Dogmes, args: list[str]) -> None:
    date, montant, participants = ask_info_bouffe()
    create_new_bouffe(ccx, dogmes, date, montant, participants)


def ask_info_bouffe() -> tuple[str, str, list[str]]:
    print("Date ? (aaaammjj) ", end="")
    date = input()
    print("Montant ? ", end="")
    montant = input()
    print("Pax ? (prenom.nom)")
    pax = input()
    participants = []
    while pax:
        print("Suivant")
        participants.append(pax)
        pax = input()
    return date, montant, participants


def check_bouffe(date: str, montant: str, catholiques: list[int]) -> bool:
    if len(date) != 8:
        return
    if not montant.isdigit():
        return
    if len(catholiques) == 0:
        return
    return True


def check_participants(ccx: CCX, participants: list[str]) -> tuple[list[int], list[str], list[str]]:
    catholiques = []
    athes = []
    protestants = []

    for infos in participants:
        if "." in infos:
            prenom, nom = infos.split(".")
            ouvriers = ccx.find_pax([nom, prenom], ["nom", "prenom"])
            match len(ouvriers):
                case 0:
                    athes.append(infos)
                case 1:
                    catholiques.append(ouvriers[0].id)
                case _:
                    protestants.append(infos)
        else:
            athes.append(infos)
    return catholiques, athes, protestants


def list_infideles(athes: list[str], protestants: list[str]) -> None:
    for nom in athes + protestants:
        print(f"Cette personne n'a pu être ajoutée à la bouffe: {nom}")


def create_new_bouffe(ccx: CCX, dogmes: Dogmes, date: str, montant: str, participants: list[int]) -> None:
    id = int(dogmes.kt("id_bouffe"))
    dogmes.concile("id_bouffe", str(id + 1))
    catholiques, athes, protestants = check_participants(ccx, participants)
    list_infideles(athes, protestants)
    if check_bouffe(date, montant, catholiques):
        ccx.add_bouffe(id, date, int(montant), catholiques)


def del_pax(ccx: CCX, args: list[str]) -> None:
    NotImplemented


def del_bouffe(ccx: CCX, args: list[str]) -> None:
    NotImplemented


def find_pax(ccx: CCX, args: list[str]) -> None:
    nom, prenom, est_X, numero_tel, mail = ask_info_pax()
    find_pax_with_info(ccx, nom, prenom, est_X, numero_tel, mail)


def find_pax_with_info(
    ccx: CCX, nom: str, prenom: str, est_X: bool, numero_tel: str, mail: str
) -> None:
    print_find_results(
        ccx.find_pax(
            [nom, prenom, est_X, numero_tel, mail],
            ["nom", "prenom", "est_X", "numero_tel", "mail"],
        )
    )


def print_find_results(results: list[p.Pax]) -> None:
    match len(results):
        case 0:
            print("On est dans le désert depuis 40 jours, y'a plus grand monde :(")
        case 1:
            print("Voici l'élu :")
            print(results[0])
        case _:
            print("Va falloir plus que 5 pains et 2 poissons")
            for result in results:
                print(result)


def find_bouffe(ccx: CCX, args: list[str]) -> None:
    NotImplemented


def unknown_action() -> None:
    print("Je parle pas le sanscrit !")
    print("h pour l'aide.")


def reinitialize(ccx: CCX) -> None:
    print("Attention, tout va péter !")
    print("Sûr (o/N) ?")
    if input() == "o":
        os.system("./initialisation")
        ccx.__init__()


def save(ccx: CCX, dogmes: Dogmes) -> None:
    ccx.save()
    dogmes.save()


def stop_app(ccx: CCX, dogmes: Dogmes) -> bool:
    print("Sûr (O/n) ?")
    if input() == "n":
        return False
    print("Sauver avant de quitter (O/n) ?")
    if input() != "n":
        save(ccx, dogmes)
    print("Deo gracias !")
    return True


main()
