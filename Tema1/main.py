import re
from regex_to_finite_automaton import regex_to_finite_automaton as r2fa


def main():
    file = open("DepresieRegulata.txt", 'r')
    r = file.readline()

    try:
        re.compile(r)

    except re.error:
        print("Regex invalid 🤡")
        exit()

    M = r2fa(r)

    if not M.is_deterministic():
        print("M nu e determinist 🤓")
        return

    Tries = 1
    while True:
        print()
        print("Option 1: Afisarea automatului M")
        print("Option 2: Afisara inteligibila a expresiei regulate r din fisier")
        print("Option 3: Verificarea unui cuvant in automat")
        print("Option 4: Iesire")

        option = input("Introdu optiunea: ")

        if Tries == 10:
            print("PREA MULTE INCERCARI!!! 🤬🤬🤬")
            return
        if option == '1':
            Tries = 1
            print(M)
            pass
        elif option == '2':
            Tries = 1
            regex = r.replace('.', '')
            print(regex)
            pass
        elif option == '3':
            Tries = 1
            cuv = input("Introdu cuvantul: ")
            if M.check_word(cuv):
                print("Cuvantul e valid 😜")
            else:
                print("Cuvantul nu e valid 💩")
            pass
        elif option == '4':
            Tries = 1
            print("Nu-i asa doamna ca suntem inteligenti si muncitori?? 😎")
            return
        else:
            print("Optiune invalida! 😡")
            Tries += 1


if __name__ == '__main__':
    main()
