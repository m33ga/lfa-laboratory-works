from .Token import Token


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception(f"Invalid character: {self.current_char}")

    def go_next_char(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.go_next_char()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.go_next_char()
        return int(result)

    def identifier(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.go_next_char()

        # check if id is reserved keyword
        keywords = {
            'event': 'EVENT',
            'period': 'PERIOD',
            'timeline': 'TIMELINE',
            'relationship': 'RELATIONSHIP',
            'main': 'MAIN',
            'export': 'EXPORT',
            'if': 'IF',
            'else': 'ELSE',
            'for': 'FOR',
            'in': 'IN',
            'modify': 'MODIFY',
            'high': 'HIGH',
            'medium': 'MEDIUM',
            'low': 'LOW',
            'cause-effect': 'CAUSE_EFFECT',
            'contemporaneous': 'CONTEMPORANEOUS',
            'precedes': 'PRECEDES',
            'follows': 'FOLLOWS',
            'includes': 'INCLUDES',
            'excludes': 'EXCLUDES',
            'BCE': 'BCE',
            'CE': 'CE',
            'true': 'TRUE',
            'false': 'FALSE',
            'title': 'TITLE',
            'date': 'DATE',
            'start': 'START',
            'end': 'END',
            'importance': 'IMPORTANCE',
            'from': 'FROM',
            'to': 'TO',
            'type': 'TYPE',
            'year': 'YEAR',
            'month': 'MONTH',
            'day': 'DAY'
        }

        return Token(keywords.get(result, 'ID'), result)

    def string(self):
        result = ""
        self.go_next_char()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.go_next_char()
        if self.current_char == '"':
            self.go_next_char()
            return Token('STRING', result)
        else:
            self.error()

    def get_next_token(self):

        while self.current_char is not None:
            match self.current_char:
                case c if c.isspace():
                    self.skip_whitespace()
                    continue

                case c if c.isdigit():
                    return Token('INT', self.integer())

                case c if c.isalpha() or c == '_':
                    return self.identifier()

                case '"':
                    return self.string()

                case '=':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token('EQ_EQ', '==')
                    return Token('EQ', '=')

                case ',':
                    self.go_next_char()
                    return Token('COMMA', ',')

                case ';':
                    self.go_next_char()
                    return Token('SEMI', ';')

                case '.':
                    self.go_next_char()
                    return Token('DOT', '.')

                case '(':
                    self.go_next_char()
                    return Token('LPAREN', '(')

                case ')':
                    self.go_next_char()
                    return Token('RPAREN', ')')

                case '{':
                    self.go_next_char()
                    return Token('LCURLY', '{')

                case '}':
                    self.go_next_char()
                    return Token('RCURLY', '}')

                case '-':
                    self.go_next_char()
                    return Token('DASH', '-')

                case '+':
                    self.go_next_char()
                    return Token('ADD_OP', '+')

                case '<':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token('LE', '<=')
                    return Token('LT', '<')

                case '>':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token('GE', '>=')
                    return Token('GT', '>')

                case '!':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token('NEQ', '!=')
                    self.error()

                case _:
                    self.error()

        return Token('EOF', None)