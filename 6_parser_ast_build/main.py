import sys
import json
from lexer import Lexer
from parser import Parser, ast_to_dict


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read file '{file_path}'.")
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        text = read_file(file_path)
    else:
        print("Enter DSL input (Ctrl+D to end):")
        text = sys.stdin.read()

    lexer = Lexer(text)
    parser = Parser(lexer)

    try:
        ast = parser.parse_program()

        print("\nAbstract Syntax Tree (AST):\n")
        ast_dict = ast_to_dict(ast)
        print(json.dumps(ast_dict, indent=2))

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
