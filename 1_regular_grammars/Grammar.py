import random
from FiniteAutomaton import FiniteAutomaton


class Grammar:
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = S

    def generate_string(self, max_length=10):
        current_string = self.S

        for i in range(max_length):
            non_terminals = [c for c in current_string if c in self.V_n]
            if not non_terminals:
                break

            nt = random.choice(non_terminals)
            replacement = random.choice(self.P[nt])
            print(f"{current_string} ->")
            current_string = current_string.replace(nt, replacement, 1)

        return current_string

    def to_finite_automaton(self):
        states = self.V_n | {"q_accept"}
        alphabet = self.V_t
        transitions = {}
        start_state = self.S
        accept_states = {"q_accept"}

        for nt, productions in self.P.items():
            for production in productions:
                if len(production) == 1 and production in self.V_t:
                    transitions.setdefault((nt, production), set()).add("q_accept")
                elif len(production) > 1:
                    transitions.setdefault((nt, production[0]), set()).add(production[1:])

        return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)

