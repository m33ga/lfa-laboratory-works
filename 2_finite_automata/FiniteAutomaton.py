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

    def __str__(self):
        transitions_str = "\n".join(
            [f"  {state} --{symbol}--> {next_states}"
             for (state, symbol), next_states in self.transitions.items()]
        )
        accept_states_str = ", ".join(self.accept_states)

        return (
            f"Finite Automaton:\n"
            f"States: {', '.join(self.states)}\n"
            f"Alphabet: {', '.join(self.alphabet)}\n"
            f"Start State: {self.start_state}\n"
            f"Accept States: {accept_states_str}\n"
            f"Transitions:\n{transitions_str}"
        )

    def __repr__(self):
        return (
            f"FiniteAutomaton(states={self.states}, "
            f"alphabet={self.alphabet}, transitions={self.transitions}, "
            f"start_state={self.start_state}, accept_states={self.accept_states})"
        )
