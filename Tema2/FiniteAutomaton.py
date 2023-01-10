# asta e un automat pushdown
class Production:
    def __init__(self, argumente, rezultate):
        self.argumente = argumente
        self.rezultate = rezultate

    def __str__(self):
        return str(self.argumente) + " -> " + str(self.rezultate)

class FiniteAutomaton:

    def __init__(self):
        self.Q = set()
        self.sigma = set()
        self.gama = set()
        self.q0 = str
        self.Z0 = str
        self.F = set()
        self.delta = list()

    def __str__(self):
        result = ""
        result += "Q: " + str(self.Q) + "\n"
        result += "sigma: " + str(self.sigma) + "\n"
        result += "gama: " + str(self.gama) + "\n"
        result += "q0: " + str(self.q0) + "\n"
        result += "Z0: " + str(self.Z0) + "\n"
        result += "F: " + str(self.F) + "\n"
        result += "delta:\n"
        for transition in self.delta:
            result += str(transition) + "\n"
        return result

    def verify_automaton(self):
        if len(self.Q) == 0:
            print("ERROR: Q e gol")
            return False

        if len(self.sigma) == 0:
            print("ERROR: sigma e gol")
            return False

        if len(self.gama) == 0:
            print("ERROR: gama e gol")
            return False

        if self.q0 not in self.Q:
            print("ERROR: q0 nu e in Q")
            return False

        if self.Z0 not in self.gama:
            print("ERROR: Z0 nu e in gama")
            return False

        if len(self.F) == 0:
            print("ERROR: F e gol")
            return False

        return True

    def check_word(self, word):
        if not self.verify_automaton():
            print("ERROR: Automatul nu e valid")
            return False

        word = word + " "

        state = self.q0
        stack = [self.Z0]

        for letter in word:
            for production in self.delta:
                if production.left[0] == state and production.left[1] == letter and production.left[2] == stack[-1]:
                    state = production.right[0]
                    stack.pop()
                    for element in reversed(production.right[1]):
                        if element != " ":
                            stack.append(element)
                    break
            else:
                return False

        return state in self.F and len(stack) == 1 and stack[0] == self.Z0

    def is_deterministic(self):
        for state in self.Q:
            for symbol in self.sigma:
                transitions = [transition for transition in self.delta if transition[0] == state and transition[1] == symbol]
                if len(transitions) > 1:
                    return False

        # pt fiecare q din Q si Z din gama, daca delta(q, lambda, Z) = multime vida atunci delta(q, a, Z) = multimea vida pt orice a din gama
        for state in self.Q:
            for symbol in self.gama:
                if len([transition for transition in self.delta if transition[0] == state and transition[1] == symbol]) == 0:
                    for symbol2 in self.gama:
                        if len([transition for transition in self.delta if transition[0] == state and transition[1] == symbol2]) != 0:
                            return False

        return True
