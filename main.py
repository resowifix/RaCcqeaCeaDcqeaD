from ccx import CCX
import pax as p
import os


def main():
    ccx = CCX()
    stop = False
    print("Tagazok à toi, mon frère !")
    while not stop:
        stop = ask_user(ccx)
        if stop:
            stop = stop_app(ccx)


def ask_user(ccx):
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
            ccx.save()
            return False
        case "aj_pax":
            add_pax(ccx, args)
            return False
        case "aj_bouffe":
            add_bouffe(ccx, args)
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


def add_pax(ccx, args):
    print("Nom ? ", end="")
    nom = input()
    if not nom:
        return
    print("Prenom ? ", end="")
    prenom = input()
    if not prenom:
        return
    print("C'est un X ? (0 pour non)", end="")
    est_X = p.bool_of_string_est_X(input())
    print("Numero de téléphone ? ", end="")
    numero_tel = input()
    print("Mail ? ", end="")
    mail = input()
    ccx.add_pax(nom, prenom, est_X, numero_tel, mail)


def add_bouffe(ccx, args):
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
    NotImplemented


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


def stop_app(ccx):
    print("Sûr (O/n) ?")
    if input() == "n":
        return False
    print("Sauver avant de quitter (O/n) ?")
    if input() != "n":
        ccx.save()
    print("Deo gracias !")
    return True


main()
