from .Token import Token
from .TokenType import TokenType


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
            'event': TokenType.EVENT,
            'period': TokenType.PERIOD,
            'timeline': TokenType.TIMELINE,
            'relationship': TokenType.RELATIONSHIP,
            'main': TokenType.MAIN,
            'export': TokenType.EXPORT,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'modify': TokenType.MODIFY,
            'high': TokenType.HIGH,
            'medium': TokenType.MEDIUM,
            'low': TokenType.LOW,
            'cause-effect': TokenType.CAUSE_EFFECT,
            'contemporaneous': TokenType.CONTEMPORANEOUS,
            'precedes': TokenType.PRECEDES,
            'follows': TokenType.FOLLOWS,
            'includes': TokenType.INCLUDES,
            'excludes': TokenType.EXCLUDES,
            'BCE': TokenType.BCE,
            'CE': TokenType.CE,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'title': TokenType.TITLE,
            'date': TokenType.DATE,
            'start': TokenType.START,
            'end': TokenType.END,
            'importance': TokenType.IMPORTANCE,
            'from': TokenType.FROM,
            'to': TokenType.TO,
            'type': TokenType.TYPE,
            'year': TokenType.YEAR,
            'month': TokenType.MONTH,
            'day': TokenType.DAY
        }
        return Token(keywords.get(result, TokenType.ID), result)

    def string(self):
        result = ""
        self.go_next_char()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.go_next_char()
        if self.current_char == '"':
            self.go_next_char()
            return Token(TokenType.STRING, result)
        else:
            self.error()

    def get_next_token(self):

        while self.current_char is not None:
            match self.current_char:
                case c if c.isspace():
                    self.skip_whitespace()
                    continue

                case c if c.isdigit():
                    return Token(TokenType.INT, self.integer())

                case c if c.isalpha() or c == '_':
                    return self.identifier()

                case '"':
                    return self.string()

                case '=':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.EQ_EQ, '==')
                    return Token(TokenType.EQ, '=')

                case ',':
                    self.go_next_char()
                    return Token(TokenType.COMMA, ',')

                case ';':
                    self.go_next_char()
                    return Token(TokenType.SEMI, ';')

                case '.':
                    self.go_next_char()
                    return Token(TokenType.DOT, '.')

                case '(':
                    self.go_next_char()
                    return Token(TokenType.LPAREN, '(')

                case ')':
                    self.go_next_char()
                    return Token(TokenType.RPAREN, ')')

                case '{':
                    self.go_next_char()
                    return Token(TokenType.LCURLY, '{')

                case '}':
                    self.go_next_char()
                    return Token(TokenType.RCURLY, '}')

                case '-':
                    self.go_next_char()
                    return Token(TokenType.DASH, '-')

                case '+':
                    self.go_next_char()
                    return Token(TokenType.ADD_OP, '+')

                case '<':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.LE, '<=')
                    return Token(TokenType.LT, '<')

                case '>':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.GE, '>=')
                    return Token(TokenType.GT, '>')

                case '!':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.NEQ, '!=')
                    self.error()

                case _:
                    self.error()

        return Token(TokenType.EOF, None)