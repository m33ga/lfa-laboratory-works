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
        "F": ["bF", "cD", "a"],
        "D": ["cS", "a"]
    }

    print("Non-terminals:", vn)
    print("Terminals:", vt)
    print("Rules:")
    for key in p:
        print(f"{key} -> {p[key]}")

    grammar = Grammar(vn, vt, p, "S")
    generated_words = []
    print("generating words:")
    for i in range(5):
        generated_words.append(grammar.generate_string())
        print(generated_words[i])
        print()

    print("generated words:")
    for word in generated_words:
        print(word)
    print()

    print(grammar.get_grammar_type())

    fa = grammar.to_finite_automaton()
    # some simple test cases
    print('checking some simple strings belong to language')
    test_strings = ["aa", "abb", "aac", "baba", "bca"]
    for test in test_strings:
        print(f"'{test}' accepted: {fa.string_belongs_to_language(test)}")

    print('checking the previously generated words:')
    for word in generated_words:
        print(f"'{word}' accepted: {fa.string_belongs_to_language(word)}")

    new_grammar = fa.to_grammar()
    print()
    print("new grammar")
    print(new_grammar)


if __name__ == "__main__":
    main()
