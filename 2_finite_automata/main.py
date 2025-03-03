from Grammar import Grammar
import os
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

# TODO: find consistent way of representing FAs
#       accept both right and left linear type 3 grammars
#       be able to differentiate NFA and DFA
#       check is_nfa
#       convert NFA to DFA
#       draw graph for FA
#       convert grammar to FA and FA to grammar

def main():

    # lab 1, variant 12
    vn = {"S", "F", "D"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["aF", "bS"],
        "F": ["bF", "bD", "a"],
        "D": ["cS", "a"]
    }
    # create grammar
    grammar = Grammar(vn, vt, p, "S")
    print(grammar)
    # print grammar type
    print(grammar.get_grammar_type()[1])

    # create finite automaton
    fa = grammar.to_finite_automaton()
    print(f"FA is NFA: {fa.is_nfa()}")
    print(fa)
    fa.draw_graph("fa1")

    # convert to dfa if nfa
    dfa = fa.nfa_to_dfa()
    print(f"FA is NFA: {dfa.is_nfa()}")
    print("Converted to DFA")
    print(dfa)

    dfa.draw_graph("dfa1")

    new_grammar = fa.to_grammar()
    print()
    print(new_grammar)

    new_grammar = dfa.to_grammar()
    print()
    print(new_grammar)


if __name__ == "__main__":
    main()
