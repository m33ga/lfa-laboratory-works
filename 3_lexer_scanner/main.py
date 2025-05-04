import sys
from lexer import Lexer, TokenType


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read file '{file_path}'.")
        sys.exit(1)


def main():
    # file path is passed as arg
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        text = read_file(file_path)
    else:
        print("enter DSL input (Ctrl+D to end):")
        text = sys.stdin.read()

    lexer = Lexer(text)
    print("tokens:")
    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type == TokenType.EOF:
            break


if __name__ == "__main__":
    main()
