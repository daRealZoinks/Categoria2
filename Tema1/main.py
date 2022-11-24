import re
from regex_to_finite_automaton import regex_to_finite_automaton as R2FA
from DeterministicFiniteAutomaton import DeterministicFiniteAutomaton as DFA
def main():

    file = open("DepresieRegulata.txt", 'r')
    r = file.readline()

    try:
        re.compile(r)

    except re.error:
        print("Non valid regex pattern")
        exit()

    M = R2FA(r)

    if not M.is_deterministic():
        print("M is not deterministic!")
        return

    Tries = 1
    while True:
        print("Option 1: Afisarea automatului M")
        print("Option 2: Afisara inteligibila a expresiei regulate r din fisier")
        print("Option 3: Verificarea unui cuvant in automat")
        print("Option 4: Exit menu")

        option = input("Enter option: ")

        if Tries == 10 :
            print("TOO MANY TRIES!!!")
            return
        if option == '1':
            Tries = 1
            M.print_automaton()
            pass
        elif option == '2':
            Tries = 1
            print(r)
            pass
        elif option == '3':
            Tries = 1
            cuv = input("Enter word: ")
            if M.check_word(cuv):
                print("Word is valid")
            else:
                print("Word is not valid")
            pass
        elif option == '4':
            Tries = 1
            return
        else:
            print("Option not valid!\n")
            Tries+=1


if __name__ == '__main__':
    main()
