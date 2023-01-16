from GrammarIDC import Grammar
from GrammarToAutomaton import grammar_to_automaton


def main():
	g = Grammar()
	g.read_grammar("grammar.txt")

	m = grammar_to_automaton(g)

	if g.verify_grammar() and g.is_idc():
		while True:
			print("1. Afisarea gramaticii")
			print("2. Generarea unui cuvant in gramatica G")
			print("3. Afisara rezultatului gramaticii simplificate")
			print("4. Afisarea gramaticii in FNG")
			print("5. Generarea unui cuvant in G + verificarea daca e acceptat de catre automat")
			print("6. Verificarea daca un cuvant citit de la tastatura e acceptat de automat")
			print("7. Iesire")

			option = input("Introduceti optiunea: ")

			if option == "1":
				print(g)

			elif option == "2":
				word = g.generate_word()
				print(word)

			elif option == "3":
				print(g.simplify())

			elif option == "4":
				print(g.to_fng())

			elif option == "5":
				word = g.generate_word()
				if m.check_word(word):
					print("Cuvantul este acceptat de automat")
				else:
					print("Cuvantul nu este acceptat de automat")

			elif option == "6":
				word = input("Introduceti cuvantul: ")
				if m.check_word(word):
					print("Cuvantul este acceptat de automat")
				else:
					print("Cuvantul nu este acceptat de automat")

			elif option == "7":
				break

			else:
				print("Optiune invalida")

		print()
		print()
	else:
		print("Gramatica nu este valida")


if __name__ == "__main__":
	main()
