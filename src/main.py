from ccx import CCX
from dogmes import Dogmes
import pax as p
import os


def main():
    ccx = CCX()
    dogmes = Dogmes()
    stop = False
    print("Tagazok à toi, mon frère !")
    while not stop:
        stop = ask_user(ccx, dogmes)
        if stop:
            stop = stop_app(ccx, dogmes)


def ask_user(ccx, dogmes):
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


def parse_message(message: str):
    parsed_message = message.split()
    return parsed_message[0], parsed_message[1:]


def display_help():
    print("T'es pas bien malin !")


def add_pax(ccx, dogmes, args):
    nom, prenom, est_X, numero_tel, mail = ask_info_pax()
    if check_info_pax(nom, prenom, est_X, numero_tel, mail):
        create_new_pax(ccx, dogmes, nom, prenom, est_X != False, numero_tel, mail)


def check_info_pax(nom, prenom, est_X, numero_tel, mail):
    return True


def ask_info_pax():
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


def create_new_pax(ccx, dogmes, nom, prenom, est_X, numero_tel, mail):
    id = int(dogmes.kt("id_pax"))
    dogmes.concile("id_pax", str(id + 1))
    ccx.add_pax(id, nom, prenom, est_X, numero_tel, mail)


def add_bouffe(ccx, dogmes, args):
    print("Date ? (aaaammjj) ", end="")
    date = input()
    if not date.isdigit() or len(date) != 8:
        return
    print("Montant ? ", end="")
    montant = int(input())
    if not montant:
        return
    print("Pax ? (prenom.nom)")
    pax = input()
    participants = []
    while pax:
        print("Suivant")
        participants.append(pax.split("."))
        pax = input()
    ccx.add_bouffe(date, montant, participants)


def del_pax(ccx, args):
    NotImplemented


def del_bouffe(ccx, args):
    NotImplemented


def find_pax(ccx, args):
    nom, prenom, est_X, numero_tel, mail = ask_info_pax()
    find_pax_with_info(ccx, nom, prenom, est_X, numero_tel, mail)


def find_pax_with_info(ccx, nom, prenom, est_X, numero_tel, mail):
    print_find_results(
        ccx.find_pax(
            [nom, prenom, est_X, numero_tel, mail],
            ["nom", "prenom", "est_X", "numero_tel", "mail"],
        )
    )


def print_find_results(results):
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


def find_bouffe(ccx, args):
    NotImplemented


def unknown_action():
    print("Je parle pas le sanscrit !")
    print("h pour l'aide.")


def reinitialize(ccx):
    print("Attention, tout va péter !")
    print("Sûr (o/N) ?")
    if input() == "o":
        os.system("./initialisation")
        ccx.__init__()


def save(ccx, dogmes):
    ccx.save()
    dogmes.save()


def stop_app(ccx, dogmes):
    print("Sûr (O/n) ?")
    if input() == "n":
        return False
    print("Sauver avant de quitter (O/n) ?")
    if input() != "n":
        save(ccx, dogmes)
    print("Deo gracias !")
    return True


main()
