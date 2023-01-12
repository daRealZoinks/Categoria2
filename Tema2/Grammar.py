import random

class Production:
    def __init__(self):
        self.left = list()
        self.right = list()

    def __str__(self):
        return str(self.left) + " -> " + str(self.right)

class Grammar:
    def __init__(self):
        self.VN = set()
        self.VT = set()
        self.S = str()
        self.P = list()

    def __str__(self):
        result = ""
        result += "VN: " + str(self.VN) + "\n"
        result += "VT: " + str(self.VT) + "\n"
        result += "S: " + str(self.S) + "\n"
        result += "P:\n"
        for rule in self.P:
            result += str(rule) + "\n"
        return result

    def verify_grammar(self):
        # elementele din VN nu apartin lui VT
        if self.VN.intersection(self.VT) != set():
            return False

        # S nu se afla in VN
        if self.S not in self.VN:
            return False

        # pt fiecare productie, partea stanga contine cel putin un element din VN
        for rule in self.P:
            if rule.left not in self.VN:
                return False

        # exista cel putin o productie care sa-l aiba pe S in stanga
        if len([rule for rule in self.P if rule.left == self.S]) == 0:
            return False

        # toate productiile au cel putin un element din VN si VT
        for rule in self.P:
            for symbol in rule.right:
                if symbol not in self.VN.union(self.VT):
                    return False

        return True

    def is_regular(self):
        for rule in self.P:
            if len(rule.right) > 2:
                return False

        for rule in self.P:
            if rule.right[0] not in self.VT:
                return False
            if len(rule.right) == 2:
                if rule.right[1] not in self.VN:
                    return False

        return True

    def generate_word(self):
        word = self.S
        print(self.S, end=" ")
        while True:
            applicable_rules = [rule for rule in self.P if rule.left in word]
            if len(applicable_rules) == 0:
                print()
                return word
            chosen_rule = random.choice(applicable_rules)
            if chosen_rule.left in word:
                word = word.replace(chosen_rule.left, "".join(chosen_rule.right), 1)
                print(" -> ", word, end=" ")

    def read_grammar(self, file_name):
        file = open(file_name, "r")

        self.VN = set(file.readline().split())
        self.VT = set(file.readline().split())
        self.S = file.readline().strip()
        file.readline()

        for line in file:
            stanga = line.split("->")[0].strip()
            dreapta = list(line.split("->")[1].strip())
            rule = Production()
            rule.left = stanga
            rule.right = dreapta
            self.P.append(rule)

        file.close()

    def is_idc(self):
        for rule in self.P:
            if rule.left not in self.VN:
                return False
            for symbol in rule.right:
                if symbol not in self.VN and symbol not in self.VT:
                    return False

        return True
    def simplify(self):
        """to fnc"""

        # daca nu este IDC, nu se poate simplifica
        if not self.is_idc():
            return None

        # daca nu exista nicio productie care sa aiba S in stanga, nu se poate simplifica
        if not len([rule for rule in self.P if rule.left == self.S]) > 0:
            return None

        g = Grammar()
        g.VN = self.VN.copy()
        g.VT = self.VT.copy()
        g.S = self.S
        g.P = self.P.copy()

        g.VN = set()

        # pasul 1

        V = []

        i = 0
        V0 = set()
        V.append(V0)

        while True:
            i = i + 1

            valid_symbols = set()
            for rule in g.P:
                valid = True
                for letter in rule.right:
                    if letter not in V[i - 1].union(g.VT):
                        valid = False
                if valid:
                    valid_symbols.add(rule.left)

            Vi = V[i - 1].union(valid_symbols)
            V.append(Vi)

            if V[i] == V[i-1]:
                g.VN = Vi
                break

        newP = []
        for rule in g.P:
            if rule.left in g.VN:
                valid = True
                for letter in rule.right:
                    if letter not in g.VN.union(g.VT):
                        valid = False
                if valid:
                    newP.append(rule)

        g.P = newP

        # pasul 2

        V = []

        i = 0
        V0 = set()
        V0.add(g.S)
        V.append(V0)

        while True:
            i = i+1

            valid_symbols = set()
            for rule in g.P:
                if rule.left in V[i - 1]:
                    for A in g.VN:
                        if A in rule.right:
                            valid_symbols.add(A)

            Vi = V[i-1].union(valid_symbols)
            V.append(Vi)

            if V[i] == V[i-1]:
                g.VN = Vi
                break

        newP = []
        for rule in g.P:
            if rule.left in g.VN:
                newP.append(rule)

        g.P = newP

        # TODO : elimina redenumirile

        def has_derivation(A):
            for rule in g.P:
                if A in rule.right:
                    return True
            return False
        def is_rename(rule):
            return len(rule.right) == 1 and rule.right[0] in g.VN

        P = []
        R = set() # set that keeps all the renames

        i = 0
        P0 = set()

        for rule in g.P:
            if not is_rename(rule):
                P0.add(rule)
            else:
                R.add(rule)

        P.append(P0)
        while True:
            i = i + 1
            Pi = P[i - 1].copy()

            for rename in R:
                for symbol in rename.right:
                    for rule in P[i-1]:
                        if rule.left == symbol:
                            new_rule = Production()
                            new_rule.left = rename.left
                            new_rule.right = rule.right
                            Pi.add(new_rule)

            if Pi == P[i - 1]:
                g.P = Pi
                break
            P.append(Pi)

        return g

    def to_fng(self):
            # daca nu este IDC, nu se poate transforma
            if not self.is_idc():
                return None

            # daca nu exista nicio productie care sa aiba S in stanga, nu se poate transforma
            if not len([rule for rule in self.P if rule.stanga == self.S]) > 0:
                return None

            g = Grammar()
            g.VN = self.VN.copy()
            g.VT = self.VT.copy()
            g.S = self.S
            g.P = self.P.copy()

            # TODO : FA mizeria asta ordinara

            # Case 1
            # G1 = {S → aAB | aB, A → aA | a, B → bB | b}
            # The production rules of G1 satisfy the rules specified for GNF, then the grammar G1 is in GNF.

            # Case 2
            # G2 = {S → aAB | aB, A → aA | ε, B → bB | ε}
            # The production rule of G2 is not satisfying the rules specified for GNF as
            # A → ε and B → ε contain ε(only the start symbol can generate ε).
            # So, the grammar G2 is not in GNF.

            # Steps for converting CFG into GNF
            # Step 1 − Convert the grammar into CNF. If the given grammar is not in CNF,
            # convert it into CNF.

            # Step 2 − If the grammar consists of left recursion, eliminate it. If the context
            # free grammar contains any left recursion, eliminate it.

            # Step 3 − In the grammar, convert the given production rule into GNF form. If
            # any production rule in the grammar is not in GNF form, convert it.

            # Step 1


            return g