from regex import RegexGenerator


if __name__ == '__main__':
    # variant 4
    examples = [
        "(S|T)(U|V)W*Y+24",
        "L(M|N)O{3}P*Q(2|3)",
        "R*(S|T|U|V)W(X|Y|Z){2}"
    ]

    for example in examples:
        print(f"\nexample : {example}")
        generator = RegexGenerator(example)
        generator.parse()
        combinations = generator.get_combinations()
        print("strings:", combinations)
        generator.show_processing_sequence()
