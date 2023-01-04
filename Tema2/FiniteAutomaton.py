class FiniteAutomaton:
    def __init__(self):
        self.Q = set()
        self.sigma = set()
        self.delta = set()
        self.q0 = str
        self.F = set()

    def __str__(self):
        result = ""
        result += "Q: " + str(self.Q) + "\n"
        result += "sigma: " + str(self.sigma) + "\n"
        result += "delta:\n"
        for rule in self.delta:
            result += "    delta(" + rule[0] + "," + rule[1] + ") = " + rule[2] + "\n"
        result += "q0: " + str(self.q0) + "\n"
        result += "F: " + str(self.F) + "\n"
        return result

    def verify_automaton(self):
        if len(self.Q) == 0:
            print("ERROR: Q e gol")
            return False

        if len(self.sigma) == 0:
            print("ERROR: sigma e gol")
            return False

        if self.q0 not in self.Q:
            print("ERROR: q0 nu exista in Q")
            return False

        for state in self.F:
            if state not in self.Q:
                print("ERROR: F nu e inclus in Q")
                return False

        for transition in self.delta:
            if transition[0] not in self.Q or transition[1] not in self.sigma or transition[2] not in self.Q:
                print("ERROR: delta nu e o functie din Q x sigma spre Q")
                return False

        return True

    def check_word(self, word):
        if not self.verify_automaton():
            print("ERROR: Automatul nu e valid")
            return False

        states = list(self.q0)
        for symbol in word:
            new_states = list()
            for state in states:
                for transition in self.delta:
                    if transition[0] == state and transition[1] == symbol:
                        new_states.append(transition[2])
            states = new_states

        for state in states:
            if state in self.F:
                return True

        return False

    def is_deterministic(self):
        for transition in self.delta:
            for transition2 in self.delta:
                if transition[0] == transition2[0] and \
                        transition[1] == transition2[1] and \
                        transition[2] != transition2[2]:
                    return False
        return True
