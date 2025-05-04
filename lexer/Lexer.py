from .Token import Token
from .TokenType import TokenType


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if self.text else None

    def go_next_char(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def error(self, message="Invalid character"):
        raise Exception(f"{message} at line {self.line}, column {self.column}: '{self.current_char}'")

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
        col = self.column
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
        return Token(keywords.get(result, TokenType.ID), result, self.line, col)

    def string(self):
        result = ""
        col = self.column
        self.go_next_char()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.go_next_char()
        if self.current_char == '"':
            self.go_next_char()
            return Token(TokenType.STRING, result, self.line, col)
        else:
            self.error()

    def get_next_token(self):

        while self.current_char is not None:
            match self.current_char:
                case c if c.isspace():
                    self.skip_whitespace()
                    continue

                case c if c.isdigit():
                    return Token(TokenType.INT, self.integer(), self.line, self.column)

                case c if c.isalpha() or c == '_':
                    return self.identifier()

                case '"':
                    return self.string()

                case '=':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.EQ_EQ, '==', self.line, self.column-2)
                    return Token(TokenType.EQ, '=', self.line, self.column-1)

                case ',':
                    self.go_next_char()
                    return Token(TokenType.COMMA, ',', self.line, self.column-1)

                case ';':
                    self.go_next_char()
                    return Token(TokenType.SEMI, ';', self.line, self.column-1)

                case '.':
                    self.go_next_char()
                    return Token(TokenType.DOT, '.', self.line, self.column-1)

                case '(':
                    self.go_next_char()
                    return Token(TokenType.LPAREN, '(', self.line, self.column-1)

                case ')':
                    self.go_next_char()
                    return Token(TokenType.RPAREN, ')', self.line, self.column-1)

                case '{':
                    self.go_next_char()
                    return Token(TokenType.LCURLY, '{', self.line, self.column-1)

                case '}':
                    self.go_next_char()
                    return Token(TokenType.RCURLY, '}', self.line, self.column-1)

                case '-':
                    self.go_next_char()
                    return Token(TokenType.DASH, '-', self.line, self.column-1)

                case '+':
                    self.go_next_char()
                    return Token(TokenType.ADD_OP, '+', self.line, self.column-1)

                case '<':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.LE, '<=', self.line, self.column-2)
                    return Token(TokenType.LT, '<', self.line, self.column-1)

                case '>':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.GE, '>=', self.line, self.column-2)
                    return Token(TokenType.GT, '>', self.line, self.column-1)

                case '!':
                    self.go_next_char()
                    if self.current_char == '=':
                        self.go_next_char()
                        return Token(TokenType.NEQ, '!=', self.line, self.column-2)
                    self.error()

                case _:
                    self.error()

        return Token(TokenType.EOF, None, self.line, self.column-1)
