import re
from DeterministicFiniteAutomaton import DeterministicFiniteAutomaton as DFA


def regex_to_finite_automaton(r: str) -> DFA:
	automat: DFA
	automat = DFA()

	# TODO : Obtinerea unui automat Mλ cu λ tranzitii corespunzator expresiei regulate

	# Obtinerea automatului Mλ: Pentru rezolvarea primei etape:

	# Se poate obtine relativ usor o forma poloneza postfixata pentru o expresie
	# aritmetica, in mod similar cu algoritmul prezentat la SD, la
	# capitolul "Stive si cozi". Se poate considera operatia de sau (|) echivalenta cu
	# operatia +, operatia de concatenare (.) echivalenta cu operatia de inmultire
	# aritmetica si operatia de stelare (*) similara cu ridicarea la putere, doar ca
	# spre deosebire de ridicarea la putere este o operatie unara.

	# exemplu
	# a.b.a.(a.a|b.b)*.c.(a.b)*

	# forma poloneza
	# ab.a.aa.bb.|*.c.ab.*.

	# Din forma poloneza obtinuta se poate obtine automatul cu λ tranzitii in mod
	# similar cu evaluarea unei expresii aritmetice pe baza formei poloneze postfixate,
	# in modul urmator, folosind o stiva de automate SA si un contor pentru
	# numarul de stari, contor, initial egal cu 0:

	# 1. se parcurge forma polonez element cu element cu un indice index

	# 2. daca fp[index] este un caracter "a" atunci se construieste automatul corespunzator.
	# Acest automat se pune pe stiva SA, se creste contorul cu 2.

	# 3. daca fp[index] este operatorul | (sau) atunci:
	# - se extrag din vârful stivei 2 automate B = SA.top(), SA.pop(),
	# A = SA.top(), SA.pop()

	# - cele doua automate se leaga ca în figura si se obtine un nou automat
	# C, care se pune pe stiva SA.
	# A
	# λ   # ---------------------- #   λ #
	# ----> #  # iA           # fA   # <---- #
	# |     # ---------------------- #     | #
	# |                                    | #
	# qcontor                                # qcontor+1
	# |                                    | #
	# |     # ---------------------- #     | #
	# ----> #  # iB           # fB   # <---- #
	# λ   # ---------------------- #   λ #
	# B

	# Acest lucru presupune ca starile initiale (iA, iB) si finale ale A si B
	# (fA, fB) isi pierd aceste calitati, devenind stari obisnuite. In plus
	# apare o noua stare initiala qcontor si o noua stare finala qcontor+1,
	# precum si 4 λ-tranzitii: de la noua stare initiala la fostele stari initiale
	# ale automatelor A si B, si de la fostele stari finale ale automatelor A
	# si B catre noua stare finala. Din nou creste contorul cu 2.

	# - automatul C se pune pe stiva SA

	# 4. daca fp[index] este operatorul . (concatenare) atunci:
	# - se extrag din varful stivei 2 automate B = SA.top(), SA.pop(),
	# A = SA.top(), SA.pop()

	# - cele 2 automate se leaga ca in figura si se obtine un nou automat
	# C, care se pune pe stiva SA.

	# iA | fA = fB | iB

	# Acest lucru presupune ca starea initiala a lui A (iA) va fi starea
	# initiala a lui C, starea finala a lui B (fB) va fi starea finala a lui
	# C, starea finala a lui A (fA) isi pierde calitatea de finala si starea
	# initiala lui B (iB) isi pierde calitatea de initiala, iar cele 2 stari
	# se contopesc. Aici trebuie avut grija la toate tranzitiile pe care le au
	# cele 2 stari.

	# - automatul C se pune pe stiva SA

	# 5. daca fp[index] este operatorul * (inchiderea kleene - "stelare") atunci:
	# - se extrage din varful stivei automatul A = SA.top(), SA.pop()

	# - se adauga o noua stare initiala qcontor, iar starea initiala veche (iA)
	# isi pierde calitatea de initiala, se adauga o noua stare finala qcontor+1,
	# iar vechea stare finala (fA) isi pierde calitatea de finala. Se adauga
	# 4 λ-tranzitii noi: de la noua stare initiala la vechea stare initiala, de
	# la vechea stare finala la noua stare finala, de la noua stare initiala la
	# noua stare finala si de la vechea stare finala la vechea stare initiala
	# (vezi figura). Contorul creste cu 2.

	# -------------------------------------------- #
	# |                                          | #
	# v     # λ                        # λ       v #
	# qcontor ------>  iA     A    fA  ------>  qcontor+1 #
	# ^            ^ #
	# |            | #
	# -------------- #

	# - automatul C se pune pe stiva SA

	# Dupa ce s-a parcurs toata forma poloneza, pe stiva trebuie sa fie un singur
	# automat = automatul final

	# Observaµie: Trebuie definite functii, care din 2 automate (respectiv unul la
	# operatia *) cu un operator construiesc un al treilea automat.

	fp = forma_poloneza(r)


	A = DFA()
	B = DFA()
	C = DFA()
	SA = []
	contor = 0

	# TODO : Obtinerea unui automat finit determinist M echivalent cu Mλ obtinut la punctul anterior

	return DFA()


def prec(c):
	if c == '|':
		return 1
	elif c == '.':
		return 2
	elif c == '*':
		return 3
	elif c == '(':
		return 0
	elif c == ')':
		return 0
	else:
		return 4


def forma_poloneza(sir):
	FP = []
	OP = []

	for E in sir:
		if E == ' ' or E == '\t':
			continue
		if 'a' <= E <= 'c':
			FP.append(E)
		elif E == '(':
			OP.append(E)
		elif E == ')':
			while OP[-1] != '(':
				FP.append(OP.pop())
			OP.pop()
			if len(OP) == 0:
				print("Parantezare incorecta")
				FP = []
				return FP
			OP.pop()
		elif E == '*' or E == '.' or E == '|':
			while not len(OP) == 0 and OP[-1] != '(' and prec(OP[-1]) >= prec(E):
				FP.append(OP.pop())
			OP.append(E)
		else:
			print("Caracter invalid")
			FP = []
			return FP
	while not len(OP) == 0:
		if OP[-1] == '(':
			print("Parantezare incorecta")
			FP = []
			return FP
		FP.append(OP.pop())
	return FP
