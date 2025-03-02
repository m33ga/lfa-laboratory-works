class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        current_states = {self.start_state}

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            if not next_states:
                return False
            current_states = next_states

        return any(state in self.accept_states for state in current_states)

    def to_grammar(self):
        from Grammar import Grammar
        V_n = {state for state in self.states}
        V_t = self.alphabet
        P = {}
        start_symbol = self.start_state

        # transitions -> production rules
        for (state, symbol), next_states in self.transitions.items():

            if state not in P:
                P[state] = []

            for next_state in next_states:
                P[state].append(f"{symbol}{next_state}")

        for accept_state in self.accept_states:
            if accept_state not in P:
                P[accept_state] = []
            P[accept_state].append("")

        return Grammar(V_n, V_t, P, start_symbol)

    def is_nfa(self):
        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) > 1:
                return True
        return False

    def nfa_to_dfa(self):

        if not self.is_nfa():

            return self

        dfa_states = []
        dfa_transitions = {}
        dfa_accept_states = set()
        dfa_start_state = frozenset([self.start_state])
        dfa_states.append(dfa_start_state)

        # queue
        unprocessed_states = [dfa_start_state]

        while unprocessed_states:
            current_dfa_state = unprocessed_states.pop()
            for symbol in self.alphabet:
                next_dfa_state = set()
                for nfa_state in current_dfa_state:
                    if (nfa_state, symbol) in self.transitions:
                        next_dfa_state.update(self.transitions[(nfa_state, symbol)])

                if next_dfa_state:
                    next_dfa_state = frozenset(next_dfa_state)
                    if next_dfa_state not in dfa_states:
                        dfa_states.append(next_dfa_state)
                        unprocessed_states.append(next_dfa_state)

                    dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state

                    if any(state in self.accept_states for state in next_dfa_state):
                        dfa_accept_states.add(next_dfa_state)

        return FiniteAutomaton(
            states=set(dfa_states),
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            start_state=dfa_start_state,
            accept_states=dfa_accept_states
        )

    def __str__(self):
        def format_state(state):
            return f"{{{', '.join(state)}}}" if isinstance(state, frozenset) else str(state)

        transitions_str = "\n".join(
            [f"  {format_state(state)} --{symbol}--> {format_state(next_states)}"
             for (state, symbol), next_states in self.transitions.items()]
        )
        accept_states_str = ", ".join(format_state(state) for state in self.accept_states)
        states_str = ", ".join(format_state(state) for state in self.states)

        return (
            f"Finite Automaton:\n"
            f"States: {states_str}\n"
            f"Alphabet: {', '.join(self.alphabet)}\n"
            f"Start State: {format_state(self.start_state)}\n"
            f"Accept States: {accept_states_str}\n"
            f"Transitions:\n{transitions_str}"
        )
