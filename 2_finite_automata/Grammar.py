import random


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

            # check for rules with multiple non-terminals on lhs
            for lhs, rhs_list in self.P.items():

                if all(symbol in current_string for symbol in lhs):
                    replacement = random.choice(rhs_list)
                    print(f"{current_string} ->")
                    current_string = current_string.replace(lhs, replacement, 1)
                    break
            else:
                # no rule found
                break

        return current_string

    def to_finite_automaton(self):
        from FiniteAutomaton import FiniteAutomaton
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

    def get_grammar_type(self):
        # assume all types are satisfied, and then eliminate incorrect ones
        is_type_3 = True
        is_type_2 = True
        is_type_1 = True
        is_type_0 = True

        is_left_linear = True
        is_right_linear = True
        is_invalid = False

        for lhs, rhs_list in self.P.items():

            if not all(symbol in self.V_n or symbol in self.V_t for symbol in lhs):
                is_invalid = True
                break

            if len(lhs) > 1:  # type 2 and 3 have only 1 non-terminal on lhs
                is_type_3 = False
                is_type_2 = False

            for rhs in rhs_list:

                if not all(symbol in self.V_n or symbol in self.V_t for symbol in rhs):
                    is_invalid = True
                    break

                if len(rhs) < len(lhs):  # type 1 needs |rhs| >= |lhs|
                    is_type_1 = False

                if lhs not in self.V_n:  # type 2 and 3 lhs must: len = 1 (prev checked); be a non-terminal
                    is_type_2 = False
                    is_type_3 = False

                # check for type 3
                if len(rhs) == 1 and rhs[0] in self.V_t:
                    continue  # skip simple production: A → a

                elif len(rhs) == 2:
                    if rhs[0] in self.V_t and rhs[1] in self.V_n:
                        is_left_linear = False  # then all rules should be right linear
                    elif rhs[0] in self.V_n and rhs[1] in self.V_t:
                        is_right_linear = False  # then all rules should be left linear
                    else:
                        is_type_3 = False  # not regular grammar form (2 non terminals)
                else:
                    is_type_3 = False  # more than 2 symbols in rhs or non-terminal in rhs

        if not is_invalid:
            if is_type_3:
                if is_left_linear:
                    return "Type 3 - Left Linear Regular Grammar"
                elif is_right_linear:
                    return "Type 3 - Right Linear Regular Grammar"

            elif is_type_2:
                return "Type 2 - Context-Free Grammar"

            elif is_type_1:
                return "Type 1 - Context-Sensitive Grammar"

            elif is_type_0:
                return "Type 0 - Unrestricted Grammar"
        else:
            return "Invalid"

    def __str__(self):
        p_rules = "".join(f"{key} -> {prod}\n" for key, prod in self.P.items())
        return (
                f"Non-terminals: {self.V_n}\n"
                f"Terminals: {self.V_t}\n"
                f"Start symbol: {self.S}\n"
                f"Production Rules:\n{p_rules}"
        )


