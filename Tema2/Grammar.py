import random


class Grammar:
    def __init__(self):
        self.VN = set()
        self.VT = set()
        self.S = None
        self.P = []

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
        for symbol_n in self.VN:
            for symbol_t in self.VT:
                if symbol_n == symbol_t:
                    return False

        # S nu se afla in VN
        if self.S not in self.VN:
            return False

        # pt fiecare productie, partea stanga contine cel putin un element din VN
        for rule in self.P:
            if rule[0] not in self.VN:
                return False

        # exista cel putin o productie care sa-l aiba pe S in stanga
        rule_containing_S = len([rule for rule in self.P if rule[0] == self.S]) > 0
        if not rule_containing_S:
            return False

        # toate productiile au cel putin un element din VN si VT
        for rule in self.P:
            for symbol in rule[1]:
                if symbol not in self.VT and symbol not in self.VN:
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
        # verificam daca toate productiile sunt de forma A -> aB
        for rule in self.P:
            if len(rule[1]) != 2:
                return False
            if rule[1][0] not in self.VT:
                return False
            if rule[1][1] not in self.VN:
                return False

        # verificam daca exista cel putin o productie care sa aiba S in stanga
        rule_containing_S = len([rule for rule in self.P if rule[0] == self.S]) > 0
        if not rule_containing_S:
            return False

        # verificam daca toate productiile au cel putin un element din VN si VT
        for rule in self.P:
            for symbol in rule[1]:
                if symbol not in self.VT and symbol not in self.VN:
                    return False

        return True

    def simplify(self):
        # daca nu este IDC, nu se poate simplifica
        if not self.is_idc():
            return False

        # daca nu exista nicio productie care sa aiba S in stanga, nu se poate simplifica
        rule_containing_S = len([rule for rule in self.P if rule[0] == self.S]) > 0
        if not rule_containing_S:
            return False

        # daca exista cel putin o productie care sa aiba S in dreapta, nu se poate simplifica
        rule_containing_S = len([rule for rule in self.P if rule[1] == self.S]) > 0
        if rule_containing_S:
            return False

        return True

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