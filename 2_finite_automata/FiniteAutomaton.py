class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # dict {frozenset: dict{symbol: set(next states)}
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        current_states = {self.start_state}

        for char in input_string:
            if char not in self.alphabet:
                return False

            next_states = set()
            for state in current_states:
                if state in self.transitions and char in self.transitions[state]:
                    next_states.update(self.transitions[state][char])
            current_states = next_states

            if not current_states:
                return False

        return bool(current_states.intersection(self.accept_states))

    def to_grammar(self):
        from Grammar import Grammar
        V_n = self.states
        V_t = self.alphabet
        P = {}

        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    if state not in P:
                        P[state] = []
                    if next_state in self.accept_states:
                        P[state].append(symbol)  # A -> a
                    else:
                        P[state].append(f"{symbol}{next_state}")  # A -> aB

        S = self.start_state
        return Grammar(V_n, V_t, P, S)

    def is_nfa(self):
        for transitions in self.transitions.values():
            for next_states in transitions.values():
                if len(next_states) > 1 and next_states not in self.states:
                    return True
        return False

    def nfa_to_dfa(self):

        if not self.is_nfa():

            return self

        dfa_states = []
        dfa_transitions = {}
        unprocessed_states = [self.start_state.copy()]
        processed_states = set()

        while unprocessed_states:
            current_state = unprocessed_states.pop(0)
            processed_states.add(frozenset(current_state))
            dfa_states.append(current_state)

            for symbol in self.alphabet:
                next_state = set()
                for s in current_state:
                    if s in self.transitions and symbol in self.transitions[s]:
                        next_state.update(self.transitions[s][symbol])

                if next_state:
                    next_state_frozen = frozenset(next_state)
                    if next_state_frozen not in processed_states and next_state not in unprocessed_states:
                        unprocessed_states.append(next_state.copy())

                    dfa_transitions[frozenset(current_state)] = dfa_transitions.get(frozenset(current_state), {})
                    dfa_transitions[frozenset(current_state)][symbol] = next_state.copy()

        dfa_accept_states = [
            state for state in dfa_states if any(s in self.accept_states for s in state)
        ]

        return FiniteAutomaton(
            dfa_states,
            self.alphabet,
            {frozenset(k): v for k, v in dfa_transitions.items()},
            self.start_state,
            dfa_accept_states
        )

    def draw_graph(self, name):
        from graphviz import Digraph
        import os

        dot = Digraph(name=name, format="png")

        def format_state(state):
            sorted_states = sorted(state)
            return "{{{}}}".format(", ".join(sorted_states)) if sorted_states else "∅"

        for state in self.states:

            formatted_state = format_state(state)
            if any(state == accept for accept in self.accept_states):
                dot.node(formatted_state, shape="doublecircle")
            else:
                dot.node(formatted_state, shape="circle")

        dot.node("", shape="plaintext")
        formatted_start = format_state(self.start_state)
        dot.edge("", formatted_start, label="start")

        for from_state, transitions in self.transitions.items():
            formatted_from = format_state(from_state)
            for symbol, to_states in transitions.items():
                if to_states in self.states:
                    formatted_to = format_state(to_states)
                    dot.edge(formatted_from, formatted_to, label=symbol)
                else:
                    for inner_state in to_states:
                        formatted_to = format_state(inner_state)
                        dot.edge(formatted_from, formatted_to, label=symbol)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "\graph_drawings\\")
        dot.render(path + name, view=True)

    def __str__(self):
        transitions_str = "\n".join(
            f"{set(state)} --({symbol})--> {next_states}"
            for state, transitions in self.transitions.items()
            for symbol, next_states in transitions.items()
        )
        return (
            f"States: {self.states}\n"
            f"Alphabet: {self.alphabet}\n"
            f"Start State: {self.start_state}\n"
            f"Accept States: {self.accept_states}\n"
            f"Transitions:\n{transitions_str}"
        )
