import random


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
            result += "    " + rule[0] + " -> " + rule[1] + "\n"
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
            if rule[0] not in self.VN:
                return False

        # exista cel putin o productie care sa-l aiba pe S in stanga
        if len([rule for rule in self.P if rule[0] == self.S]) == 0:
            return False

        # toate productiile au cel putin un element din VN si VT
        for rule in self.P:
            for symbol in rule[1]:
                if symbol not in self.VN.union(self.VT):
                    return False

        return True

    def is_regular(self):
        for rule in self.P:
            if len(rule[1]) > 2:
                return False

        for rule in self.P:
            if rule[1][0] not in self.VT:
                return False
            if len(rule[1]) == 2:
                if rule[1][1] not in self.VN:
                    return False

        return True

    def generate_word(self):
        word = self.S
        print(self.S, end=" ")
        while True:
            applicable_rules = [rule for rule in self.P if rule[0] in word]
            if len(applicable_rules) == 0:
                print()
                return word
            chosen_rule = random.choice(applicable_rules)
            if chosen_rule[0] in word:
                word = word.replace(chosen_rule[0], chosen_rule[1], 1)
                print(" -> ", word, end=" ")

    def read_grammar(self, file_name):
        file = open(file_name, "r")

        self.VN = set(file.readline().split())
        self.VT = set(file.readline().split())
        self.S = file.readline().strip()
        file.readline()

        for line in file:
            self.P.append(tuple(line.strip().split(" -> ")))

        file.close()

    def is_idc(self):
        for rule in self.P:
            if rule[0] not in self.VN:
                return False
            for symbol in rule[1]:
                if symbol not in self.VN and symbol not in self.VT:
                    return False

        return True

    def simplify(self):

        g = None

        # daca nu este IDC, nu se poate simplifica
        if not self.is_idc():
            return g

        # daca nu exista nicio productie care sa aiba S in stanga, nu se poate simplifica
        if not len([rule for rule in self.P if rule[0] == self.S]) > 0:
            return g

        g = Grammar()
        g.VN = self.VN.copy()
        g.VT = self.VT.copy()
        g.S = self.S
        g.P = self.P.copy()

        g.VN = set()

        # TODO : elimina simbolurile neutilizabile

        V = []

        i = 0
        V0 = set()
        V.append(V0)

        while True:
            i = i + 1

            valid_symbols = set()
            for tpl in g.P:
                if tpl[1] in V[i-1].union(g.VT):
                    valid_symbols.add(tpl[0])

            Vi = V[i - 1].union(valid_symbols)
            V.append(Vi)

            if V[i] == V[i-1]:
                g.VN = Vi
                break

        newP = []
        for tpl in g.P:
            if tpl[0] in g.VN:
                newP.append(tpl)

        g.P = newP

        # TODO : elimina simbolurile inaccesibile

        V = []

        i = 0
        V0 = set()
        V0.add(g.S)
        V.append(V0)

        while True:
            i = i+1

            valid_symbols = set()
            for tpl in g.P:
                if tpl[0] in V[i-1]:
                    for A in g.VN:
                        if A in tpl[1]:
                            valid_symbols.add(A)

            Vi = V[i-1].union(valid_symbols)
            V.append(Vi)

            if V[i] == V[i-1]:
                g.VN = Vi
                break

        newP = []
        for tpl in g.P:
            if tpl[0] in g.VN:
                newP.append(tpl)

        g.P = newP

        # TODO : elimina redenumirile

        return g

    def to_fng(self):
        # daca nu este IDC, nu se poate transforma in FNG
        if not self.is_idc():
            return False

        # daca nu exista nicio productie care sa aiba S in stanga, nu se poate transforma in FNG
        rule_containing_S = len([rule for rule in self.P if rule[0] == self.S]) > 0
        if not rule_containing_S:
            return False

        # daca exista cel putin o productie care sa aiba S in dreapta, nu se poate transforma in FNG
        rule_containing_S = len([rule for rule in self.P if rule[1] == self.S]) > 0
        if rule_containing_S:
            return False

        return True
