from finite_automaton import FiniteAutomaton as Fa

def regex_to_finite_automaton(r):
	fp = forma_poloneza(r)

	SA = []
	contor = 0

	for char in fp:
		if 'a' <= char <= 'z':
			C = Fa()

			C.q0 = "q" + str(contor)
			C.F.add("q" + str(contor+ 1))
			C.Q.add(C.q0)
			C.Q.add(list(C.F)[-1])
			C.sigma.add(char)
			C.delta.add((C.q0, char, list(C.F)[-1]))

			contor += 2
			SA.append(C)

		elif char == '|':
			B = SA.pop()
			A = SA.pop()
			C = Fa()

			C.q0 = "q" + str(contor)
			C.Q = A.Q | B.Q
			C.Q.add(C.q0)
			C.F.add("q" + str(contor + 1))
			C.Q.add(list(C.F)[-1])
			C.Q.update({A.q0, B.q0, list(A.F)[-1], list(B.F)[-1]})
			C.sigma = A.sigma | B.sigma
			C.sigma.add("λ")
			C.delta = A.delta | B.delta
			C.delta.add((C.q0, "λ", A.q0))
			C.delta.add((C.q0, "λ", B.q0))
			C.delta.add((list(A.F)[-1], "λ", list(C.F)[-1]))
			C.delta.add((list(B.F)[-1], "λ", list(C.F)[-1]))

			contor += 2
			SA.append(C)

		elif char == '.':
			B = SA.pop()
			A = SA.pop()

			for transition in A.delta:
				if transition[2] == list(A.F)[-1]:
					new_transition = (transition[0], transition[1], B.q0)
					A.delta.remove(transition)
					A.delta.add(new_transition)

			A.Q.remove(list(A.F)[-1])
			A.F = {B.q0}
			A.Q.add(list(A.F)[-1])

			C = Fa()
			C.q0 = A.q0
			C.F.add(list(B.F)[-1])
			C.Q = A.Q | B.Q
			C.sigma = A.sigma | B.sigma
			C.delta = A.delta | B.delta

			SA.append(C)

		elif char == '*':
			A = SA.pop()
			C = Fa()

			C.q0 = "q" + str(contor)
			C.Q = A.Q
			C.Q.add(C.q0)
			C.F.add("q" + str(contor + 1))
			C.Q.add(list(C.F)[-1])
			C.Q.update({A.q0, list(A.F)[-1]})
			C.sigma = A.sigma | {"λ"}
			C.delta = A.delta
			C.delta.add((C.q0, "λ", A.q0))
			C.delta.add((list(A.F)[-1], "λ", list(C.F)[-1]))
			C.delta.add((C.q0, "λ", list(C.F)[-1]))
			C.delta.add((list(A.F)[-1], "λ", A.q0))

			contor += 2
			SA.append(C)

	if len(SA) != 1:
		print("EROARE")
		exit(1)

	result = SA.pop()

	elemente = dict()
	elemente["q'0"] = lambda_inchidere(result, [result.q0])

	contor_elemente_din_dictionar = 0

	while elemente["q'" + str(contor_elemente_din_dictionar)].intersection(result.F) == set():
		for litera in result.sigma - {"λ"}:
			delta_prim_element = delta_prim(elemente["q'" + str(contor_elemente_din_dictionar)], result, litera)
			if delta_prim_element not in elemente.values():
				contor_elemente_din_dictionar += 1
				elemente["q'" + str(contor_elemente_din_dictionar)] = lambda_inchidere(result, delta_prim_element)

	print(elemente)

	# show me all the deltas from the elemente



	new_automaton = Fa()
	new_automaton.q0 = "q'0"
	new_automaton.Q = set(elemente.keys())
	new_automaton.F = list(elemente.keys())[-1]
	new_automaton.sigma = result.sigma

	for key in elemente.keys():
		for litera in result.sigma - {"λ"}:
			delta_prim_element = delta_prim(elemente[key], result, litera)
			print(key, litera, delta_prim_element)

	new_automaton.print_automaton()













	# elemente["q'1"] = lambda_inchidere(result, delta_prim(elemente["q'0"], result, "a"))
	# elemente["q'2"] = lambda_inchidere(result, delta_prim(elemente["q'0"], result, "b"))
	# elemente["q'3"] = lambda_inchidere(result, delta_prim(elemente["q'1"], result, "a"))
	# elemente["q'4"] = lambda_inchidere(result, delta_prim(elemente["q'2"], result, "b"))
	#
	# print(elemente["q'0"], "= q'0")
	# print("delta(q'0, a) = ", delta_prim(elemente["q'0"], result, "a"))
	# print(elemente["q'1"], "= q'1")
	# print("delta(q'0, b) = ", delta_prim(elemente["q'0"], result, "b"))
	# print(elemente["q'2"], "= q'2")
	# print("delta(q'1, a) = ", delta_prim(elemente["q'1"], result, "a"))
	# print(elemente["q'3"], "= q'3")
	# print("delta(q'1, b) = ", delta_prim(elemente["q'1"], result, "b"))
	# print("delta(q'2, a) = ", delta_prim(elemente["q'2"], result, "a"))
	# print("delta(q'2, b) = ", delta_prim(elemente["q'2"], result, "b"))
	# print(elemente["q'4"], "= q'4")
	# print("delta(q'3, a) = ", delta_prim(elemente["q'3"], result, "a"))
	# print("delta(q'3, b) = ", delta_prim(elemente["q'3"], result, "b"))
	# print("delta(q'4, a) = ", delta_prim(elemente["q'4"], result, "a"))
	# print("delta(q'4, b) = ", delta_prim(elemente["q'4"], result, "b"))


def lambda_inchidere(automat, stari):
	stari_lambda = set(stari)

	yes = True
	while yes:
		yes = False
		for tranzitie in automat.delta:
			if tranzitie[0] in stari_lambda and tranzitie[1] == "λ":
				if tranzitie[2] not in stari_lambda:
					stari_lambda.add(tranzitie[2])
					yes = True
	return set(sorted(stari_lambda))


def delta_prim(lambda_inchidere_set, automat, litera):
	delta_prim_set = set()
	for tranzitie in automat.delta:
		if tranzitie[0] in lambda_inchidere_set and tranzitie[1] == litera:
			delta_prim_set.add(tranzitie[2])
	return set(sorted(delta_prim_set))


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
