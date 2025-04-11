from fa import Grammar


def main():
    v_n = {"S", "A", "B", "C", "D", "X"}
    v_t = {"a", "b"}
    p = {
        "S": ["A"],
        "A": ["aX", "bX"],
        "X": ["", "BX", "b"],
        "B": ["AD"],
        "D": ["aD", "a"],
        "C": ["Ca"],
    }
    s = {"S"}

    grammar = Grammar(v_n, v_t, p, s)
    print(grammar)
    print()
    nullable_set = grammar.get_nullable()
    print(nullable_set)
    print()
    grammar.eliminate_epsilon_productions(nullable_set)
    print(grammar)
    grammar.eliminate_unit_productions()
    print()
    print(grammar)
    grammar.eliminate_nonproductive()
    print()
    print(grammar)


if __name__ == "__main__":
    main()