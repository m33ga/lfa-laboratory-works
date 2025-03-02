from Grammar import Grammar

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
    # variant 12
    vn = {"S", "F", "D"}
    vt = {"a", "b", "c"}
    p = {
        "S": ["aF", "bS"],
        "F": ["bF", "bD", "a"],
        "D": ["cS", "aF"]
    }

    grammar = Grammar(vn, vt, p, "S")
    print(grammar)

    print(grammar.get_grammar_type())

    fa = grammar.to_finite_automaton()
    print()
    print(fa)
    print(fa.is_nfa())

    fa1 = fa.nfa_to_dfa()
    print(fa1)
    # new_grammar = fa.to_grammar()
    # print()
    # print(new_grammar)


if __name__ == "__main__":
    main()
