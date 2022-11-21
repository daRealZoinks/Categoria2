class FiniteAutomaton:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = []
        self.initial_state = None
        self.final_states = []

    def print(self):
        print("States: ", self.states)
        print("Alphabet: ", self.alphabet)
        print("Transitions: ", self.transitions)
        print("Initial state: ", self.initial_state)
        print("Final states: ", self.final_states)