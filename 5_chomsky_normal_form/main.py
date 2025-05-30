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
    grammar.normalize_cnf()


if __name__ == "__main__":
    main()
