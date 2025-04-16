import random
from itertools import product

class Grammar:
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = set(S)

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
        states = set(self.V_n)
        alphabet = set(self.V_t)
        transitions = {}
        start_state = self.S
        accept_states = set()

        for lhs, rhs_list in self.P.items():
            if lhs not in transitions:
                transitions[lhs] = {}

            for rhs in rhs_list:
                if len(rhs) == 1 and rhs in self.V_t:  # A -> a (terminal)
                    if rhs not in transitions[lhs]:
                        transitions[lhs][rhs] = set()
                    transitions[lhs][rhs].add("X")
                    accept_states.add("X")

                elif len(rhs) == 2 and rhs[0] in self.V_t and rhs[1] in self.V_n:  # A -> aB
                    symbol, next_state = rhs[0], rhs[1]
                    if symbol not in transitions[lhs]:
                        transitions[lhs][symbol] = set()
                    transitions[lhs][symbol].add(next_state)

                elif len(rhs) == 2 and rhs[1] in self.V_t and rhs[0] in self.V_n:  # A -> Ba
                    symbol, next_state = rhs[1], rhs[0]
                    if symbol not in transitions[lhs]:
                        transitions[lhs][symbol] = set()
                    transitions[lhs][symbol].add(next_state)

        states.add("X")

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
                    return 3, "Type 3 - Left Linear Regular Grammar"
                elif is_right_linear:
                    return 3, "Type 3 - Right Linear Regular Grammar"

            elif is_type_2:
                return 2, "Type 2 - Context-Free Grammar"

            elif is_type_1:
                return 1, "Type 1 - Context-Sensitive Grammar"

            elif is_type_0:
                return 0, "Type 0 - Unrestricted Grammar"
        else:
            return -1, "Invalid"

    # task lab 5:
    # Get familiar with the approaches of normalizing a grammar.
    # Implement a method for normalizing an input grammar by the rules of CNF.
    # The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    # The implemented functionality needs executed and tested.
    # Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

    # def normalize_cnf(self):
        # steps:
        # 1. eliminate epsilon productions
        # 2. eliminate renaming productions (X -> Y)
        # 3. eliminate inaccessible states
        # 4. eliminate non-productive symbols (not leading to terminal)
        # 5. get CNF by adding new states

        # variant 12:
        # V_n = {S, A, B, C, D, X}
        # V_t = {a, b}
        # P = {
        #     "S": ["A"],
        #     "A": ["aX", "bX"],
        #     "X": ["", "BX", "b"],
        #     "B": ["AD"],
        #     "D": ["aD", "a"],
        #     "C": ["Ca"],
        # }

    def normalize_cnf(self):
        normalization_steps = {}
        normalization_steps["Original Grammar:"] = str(self)

        # Step 1: Remove epsilon productions
        nullable = self.get_nullable()
        self.eliminate_epsilon_productions(nullable)
        normalization_steps["Step 1: Remove Epsilon Productions"] = str(self)
        print(self)

        # Step 2: Remove unit productions
        self.eliminate_unit_productions()
        normalization_steps["Step 2: Remove Unit Productions"] = str(self)
        print(self)

        # Step 3: Remove non-productive symbols
        self.eliminate_nonproductive()
        normalization_steps["Step 3: Remove Non-Productive Symbols"] = str(self)
        print(self)

        # Step 4: Remove inaccessible symbols
        self.eliminate_inaccessible()
        normalization_steps["Step 4: Remove Inaccessible Symbols"] = str(self)
        print(self)

        # Step 5: Convert to CNF
        self.replace_terminals()
        self.replace_long_productions()
        normalization_steps["Result: Bring to Chomsky Normal Form (CNF)"] = str(self)
        print(self)

        return normalization_steps

    def get_nullable(self):
        nullable = set()
        for lhs, rhs_list in self.P.items():
            for prod in rhs_list:
                if (prod == "" or prod in nullable) and lhs not in nullable:
                    nullable.add(lhs)
                    rhs_list.remove("")
        found = True
        while found:
            found = False
            for lhs, rhs_list in self.P.items():
                for prod in rhs_list:
                    if prod in nullable and lhs not in nullable:
                        nullable.add(lhs)
                        found = True

        return nullable

    def _get_combinations_replacing_epsilon(self, state_string, separator_list):
        parts = []
        current_string = ''
        for char in state_string:
            if char in separator_list and char in self.V_n:
                if len(current_string) > 0:
                    parts.append(current_string)
                    current_string = ''
                parts.append([char, ''])
            else:
                current_string += char
        if len(current_string) > 0:
            parts.append(current_string)
        iterables = [x if isinstance(x, list) else [x] for x in parts]
        result = [''.join(p) for p in product(*iterables)]

        return result

    def eliminate_epsilon_productions(self, nullable):
        for lhs, rhs_list in self.P.items():
            for idx, rhs in enumerate(rhs_list):
                if any(c in rhs for c in nullable):
                    rhs_list[idx:idx+1] = self._get_combinations_replacing_epsilon(rhs, nullable)

    def eliminate_unit_productions(self):
        for lhs, rhs_list in self.P.items():
            reachable_states = set()
            additional_transitions = set()
            analyzed_states = set()
            found = False
            for rhs in rhs_list:
                if rhs in self.V_n:
                    reachable_states.add(rhs)
                    found = True

            while found:
                found = False
                for state in reachable_states.copy():
                    if state not in analyzed_states:
                        for production in self.P[state]:
                            if production in self.V_n and production not in analyzed_states and production not in reachable_states:
                                found = True
                                reachable_states.add(production)
                            elif production not in additional_transitions:
                                additional_transitions.add(production)
                        analyzed_states.add(state)

            if len(additional_transitions) > 0:
                additional_transitions -= set(rhs_list)
                for element in additional_transitions:
                    if element not in rhs_list:
                        rhs_list.append(element)
                for element in reachable_states:
                    if element in rhs_list:
                        rhs_list.remove(element)

    def eliminate_nonproductive(self):
        # remove production which don't result terminals
        productive = set()
        change_detected = True
        while change_detected:
            change_detected = False
            for lhs, rhs_list in self.P.items():
                for rhs in rhs_list:
                    for symbol in rhs:
                        if ((symbol in self.V_t and len(rhs) == 1) or (symbol in productive)) and lhs not in productive:
                            productive.add(lhs)
                            change_detected = True

        unproductive = set(self.V_n) - productive
        for state in unproductive:
            del self.P[state]
            self.V_n.remove(state)
            if state in self.S:
                self.S.remove(state)

    def eliminate_inaccessible(self):
        accessible = self.S.copy()
        change_detected = True
        while change_detected:
            change_detected = False
            for state in accessible.copy():
                for production in self.P[state]:
                    for symbol in production:
                        if symbol in self.V_n and symbol not in accessible:
                            accessible.add(symbol)
                            change_detected = True

        inaccessible = set(self.V_n) - accessible
        for state in inaccessible:
            if state in self.P:
                del self.P[state]
            if state in self.V_n:
                self.V_n.remove(state)

    def replace_terminals(self):
        terminal_dict = {}
        if not self.V_n == set():
            for terminal in self.V_t:
                new_state = f"T_{terminal}"
                self.V_n.add(new_state)
                self.P[new_state] = list(terminal)
                terminal_dict[terminal] = new_state

            for lhs, rhs_list in self.P.items():
                new_rhs = []
                for rhs in rhs_list:
                    if len(rhs) > 1:
                        new_rhs.append([terminal_dict.get(symbol, symbol) for symbol in rhs])
                    else:
                        new_rhs.append(rhs)
                self.P[lhs] = new_rhs

    def replace_long_productions(self):
        additional_productions = {}
        additional_productions_number = 0
        change_detected = True
        while change_detected:
            change_detected = False
            new_transitions = {}
            for lhs, rhs_list in self.P.items():
                for rhs in rhs_list:
                    if len(rhs) > 2:
                        end_part_list = rhs[1:]
                        end_part = "".join(end_part_list)
                        if end_part in additional_productions:
                            new_state = additional_productions[end_part]
                        else:
                            new_state = f"X{additional_productions_number}"
                            additional_productions_number += 1
                            additional_productions[end_part] = new_state
                            new_transitions[new_state] = [end_part_list]
                            change_detected = True
                            self.V_n.add(new_state)
                        new_rhs = [rhs[0], new_state]
                        rhs_list.remove(rhs)
                        rhs_list.append(new_rhs)

            for lhs, rhs_list in new_transitions.items():
                self.P[lhs] = rhs_list


    def __str__(self):
        p_rules = ";\n".join(f"{{{key}}} -> {prod}" for key, prod in self.P.items())
        return (
            f"Non-terminals: {self.V_n}\n"
            f"Terminals: {self.V_t}\n"
            f"Start symbol: {self.S}\n"
            f"Production Rules:\n{p_rules}"
        )
