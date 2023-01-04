from Grammar import Grammar
from GrammarToAutomaton import grammar_to_automaton


def main():
    g = Grammar()
    g.read_grammar("grammar.txt")  # gramatica de tipul 3

    m = None

    if g.verify_grammar() and g.is_idc():
        while True:
            print("1. Afisarea gramaticii")
            print("2. Generarea unui numar n de cuvinte in gramatica G")
            print("3. Obtinerea automatului echivalent cu G")
            print("4. Verificarea daca un cuvant este sau nu acceptat de automatul obtinut")
            print("5. Generarea unui cuvant in G + verificarea daca e acceptat de catre automat")
            print("6. Iesire")

            option = input("Introduceti optiunea: ")

            if option == "1":
                print(g)

            elif option == "2":
                n = int(input("Introduceti numarul de cuvinte: "))
                words = []
                while len(words) < n:
                    word = g.generate_word()
                    if word not in words:
                        words.append(word)
                    else:
                        print(f"Cuvantul \"{word}\" deja exista")
                print(words)

            elif option == "3":
                m = grammar_to_automaton(g)
                if m is not None:
                    m.print_automaton()

            elif option == "4":
                word = input("Introduceti cuvantul: ")
                if m is None:
                    print("Automatul nu a fost generat")
                else:
                    print(m.check_word(word))

            elif option == "5":
                word = g.generate_word()
                print(word)
                if m is None:
                    print("Automatul nu a fost generat")
                else:
                    print(m.check_word(word))

            elif option == "6":
                break
            else:
                print("Optiune invalida")
    else:
        print("Gramatica nu este valida")


if __name__ == "__main__":
    main()
