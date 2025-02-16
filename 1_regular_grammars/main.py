from Grammar import Grammar


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

    fa = grammar.to_finite_automaton()
    # some simple test cases
    print('checking some simple strings belong to language')
    test_strings = ["aa", "abb", "aac", "baba", "bca"]
    for test in test_strings:
        print(f"'{test}' accepted: {fa.string_belongs_to_language(test)}")

    print('checking the previously generated words:')
    for word in generated_words:
        print(f"'{word}' accepted: {fa.string_belongs_to_language(word)}")


if __name__ == "__main__":
    main()
