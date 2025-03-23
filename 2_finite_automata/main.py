from fa import Grammar, FiniteAutomaton


# variant 12

# previous grammar:

# VN={S, F, D},
# VT={a, b, c},
# P={
#     S → aF
#     F → bF
#     F → cD
#     S → bS
#     D → cS
#     D → a
#     F → a
# }

# current automaton:

# Q = {q0,q1,q2,q3},
# ∑ = {a,b,c},
# F = {q2},
# δ(q0,b) = q0,
# δ(q0,a) = q1,
# δ(q1,c) = q1,
# δ(q1,a) = q2,
# δ(q3,a) = q1,
# δ(q3,a) = q3,
# δ(q2,a) = q3.

def main():

    # grammar from lab 1, variant 12
    print("Variant 12")
    print("Previous grammar:")
    vn = {"S", "F", "D"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["aF", "bS"],
        "F": ["bF", "cD", "a"],
        "D": ["cS", "a"]
    }
    # create grammar
    grammar = Grammar(vn, vt, p, "S")
    print(grammar)
    # print grammar type
    print(grammar.get_grammar_type()[1])

    # create finite automaton
    fa = grammar.to_finite_automaton()
    print("\nFinite Automaton:")
    print(fa)
    print(f"FA is NFA: {fa.is_nfa()}")
    fa.draw_graph("FA1")

    # convert to dfa if nfa
    dfa = fa.nfa_to_dfa()
    print("\nConverted to DFA")
    print(dfa)
    print(f"FA is NFA: {dfa.is_nfa()}")

    new_grammar = dfa.to_grammar()
    print("\nGrammar converted from DFA")
    print(new_grammar)

    print("\nChecking some grammar types")
    # type 0
    vn = {"S", "A", "B", "C"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["AB", "aS"],
        "A": ["aA", "bB"],
        "B": ["bB", "cC"],
        "AB": ["bAB", "c"],
        "C": ["cA", "a"]
    }
    # Create grammar
    grammar = Grammar(vn, vt, p, "S")
    print(grammar)
    # Print grammar type
    print(grammar.get_grammar_type()[1])
    print()

    # type 1
    vn = {"S", "A", "B", "C"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["aAB", "bS"],
        "A": ["bAB", "bC"],
        "B": ["cB", "aC"],
        "BC": ["cB", "aC"],
        "C": ["cA", "a"]
    }
    # Create grammar
    grammar = Grammar(vn, vt, p, "S")
    print(grammar)
    # Print grammar type
    print(grammar.get_grammar_type()[1])
    print()

    # type 2
    vn = {"S", "F", "D"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["aFaa", "bS"],
        "F": ["bF", "bD", "a"],
        "D": ["cS", "a"]
    }
    # create grammar
    grammar = Grammar(vn, vt, p, "S")
    print(grammar)
    # print grammar type
    print(grammar.get_grammar_type()[1])
    print()

    # type 3 left linear
    vn = {"S", "F", "D"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["Fa", "Sb"],
        "F": ["Fb", "Dc", "a"],
        "D": ["Sc", "a"]
    }
    # create grammar
    grammar = Grammar(vn, vt, p, "S")
    print(grammar)
    # print grammar type
    print(grammar.get_grammar_type()[1])

    # task 12 from lab 2
    print("\nTask from Lab 2")
    states = {"A", "B", "C", "D"}
    alphabet = {"a", "b", "c"}
    final = {"C"}
    initial = {"A"}

    transitions = {
        "A": {"a": {"B"}, "b": {"A"}},
        "B": {"a": {"C"}, "c": {"B"}},
        "C": {"a": {"D"}},
        "D": {"a": {"B", "D"}}
    }

    nfa = FiniteAutomaton(states, alphabet, transitions, initial, final)
    print(nfa)
    print(f"FA is NFA: {nfa.is_nfa()}")
    dfa = nfa.nfa_to_dfa()
    nfa.draw_graph("NFA")
    print("\nConverted to DFA")
    print(dfa)
    print(f"FA is NFA: {dfa.is_nfa()}")
    dfa.draw_graph("DFA")


if __name__ == "__main__":
    main()

