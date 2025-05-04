from .TokenType import TokenType


class Token:
    def __init__(self, type_: TokenType, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)})"