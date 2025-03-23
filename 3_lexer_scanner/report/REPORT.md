# The title of the work

### Course: Formal Languages & Finite Automata
### Author: Mihai Gurduza
### Academic Group: FAF-233 

----

## Theory
### Definitions: 
* **Lexer**: The lexical analyzer defines how the contents of a file are broken into tokens, which is the basis for supporting custom language features [[1]](#ref1). 
* **Token**: A lexical token is a string with an assigned and thus identified meaning. A lexical token consists of a token name and an optional token value.
* **Lexeme**: A lexeme is only a string of characters known to be of a certain kind (e.g., a string literal, a sequence of letters).

## Objectives:

* Understand what lexical analysis [[1]](#ref1) is;
* Get familiar with the inner workings of a lexer/scanner/tokenizer;
* Implement a sample lexer and show how it works.

## Implementation description

* The **Token** class is a fundamental building block of the lexer, representing individual tokens generated during the lexical analysis process. Each token holds a type (EVENT, INT, STRING...) and an optional value (e.g., the numeric value of an integer or the string content).

```python
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"
```

---
* The `go_next_char` method from the `Lexer` class is responsible for advancing the lexer to the next character in the input text. It increments the pos attribute to move the pointer forward and updates the current_char attribute to reflect the new character at the updated position. If the end of the input text is reached, current_char is set to None, signaling the lexer to stop processing. This method makes the lexer moves through the input text in a controlled and predictable manner, making it process one character at a time. 
```python
def go_next_char(self):
    self.pos += 1
    if self.pos < len(self.text):
        self.current_char = self.text[self.pos]
    else:
        self.current_char = None
```

---
* The `integer` method is made to extract numeric literals from the input text, which are represented as sequences of consecutive digits. It iteratively accumulates digits into a string while advancing the lexer's position, ensuring that all digits in the number are captured. Once the entire numeric sequence is collected, the method converts the resulting string into an integer and returns it as part of a Token object. 

```python
def integer(self):
    result = ""
    while self.current_char is not None and self.current_char.isdigit():
        result += self.current_char
        self.go_next_char()
    return int(result)
```

---
* Identifiers and reserved keywords are fundamental components of any programming language, and the `identifier` method is responsible for recognizing and differentiating between them. It processes sequences of alphanumeric characters and underscores, accumulating them into a string while advancing the lexer's position. Once the full identifier is collected, the method checks if it matches any of the predefined reserved keywords in a dictionary. If a match is found, the corresponding keyword token (e.g., EVENT, PERIOD) is returned; otherwise, the identifier is classified as a user-defined name (ID).

```python
def identifier(self):
    result = ""
    while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
        result += self.current_char
        self.go_next_char()

    keywords = {
        'event': 'EVENT',
        'period': 'PERIOD',
        # other keywords ...
    }

    return Token(keywords.get(result, 'ID'), result)
```

---
* String literals, enclosed in double quotes, are a common feature, and the `string` method is designed to handle their extraction and tokenization. It begins by skipping the opening quote and then iteratively collects characters until the closing quote is encountered. If the closing quote is missing, the method raises an error to indicate malformed input. Once the entire string content is captured, it is returned as part of a Token object with the type STRING.

```python
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
```

---
* The `get_next_token` method is the main part of the lexer, handling the identification and generation of tokens based on the input text. It uses a match statement to handle a different token types, including single-character tokens (e.g., +, -), multi-character operators (e.g., <=, ==), and special cases like strings and identifiers. For example, when encountering an equals sign (=), the method checks if it is followed by another equals sign to determine whether it represents an assignment (=) or an equality comparison (==). Similarly, it delegates the processing of integers, identifiers, and strings to dedicated helper methods presented above.

```python
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

            case '=':
                self.go_next_char()
                if self.current_char == '=':
                    self.go_next_char()
                    return Token('EQ_EQ', '==')
                return Token('EQ', '=')

            # other cases ...

        return Token('EOF', None)
```

## Results

Using the lexer for a sample program in the [input.dsl](../input.dsl) file gives the following list of tokens:

```
tokens:
Token(EVENT, 'event')
Token(ID, 'juliusCaesarBirth')
Token(LCURLY, '{')
Token(TITLE, 'title')
Token(EQ, '=')
Token(STRING, 'Birth of Julius Caesar')
Token(SEMI, ';')
Token(DATE, 'date')
Token(EQ, '=')
Token(INT, 12)
Token(DASH, '-')
Token(INT, 7)
Token(DASH, '-')
Token(INT, 100)
Token(BCE, 'BCE')
Token(SEMI, ';')
Token(IMPORTANCE, 'importance')
Token(EQ, '=')
Token(MEDIUM, 'medium')
Token(SEMI, ';')
Token(RCURLY, '}')
Token(EVENT, 'event')
Token(ID, 'juliusCaesarDeath')
Token(LCURLY, '{')
Token(TITLE, 'title')
Token(EQ, '=')
Token(STRING, 'Assassination of Julius Caesar')
Token(SEMI, ';')
Token(DATE, 'date')
Token(EQ, '=')
Token(INT, 15)
Token(DASH, '-')
Token(INT, 3)
Token(DASH, '-')
Token(INT, 44)
Token(BCE, 'BCE')
Token(SEMI, ';')
Token(IMPORTANCE, 'importance')
Token(EQ, '=')
Token(HIGH, 'high')
Token(SEMI, ';')
Token(RCURLY, '}')
Token(PERIOD, 'period')
Token(ID, 'romanRepublic')
Token(LCURLY, '{')
Token(TITLE, 'title')
Token(EQ, '=')
Token(STRING, ' Roman Republic ')
Token(SEMI, ';')
Token(START, 'start')
Token(EQ, '=')
Token(INT, 509)
Token(BCE, 'BCE')
Token(SEMI, ';')
Token(END, 'end')
Token(EQ, '=')
Token(INT, 27)
Token(BCE, 'BCE')
Token(SEMI, ';')
Token(IMPORTANCE, 'importance')
Token(EQ, '=')
Token(HIGH, 'high')
Token(SEMI, ';')
Token(RCURLY, '}')
Token(TIMELINE, 'timeline')
Token(ID, 'romanHistory')
Token(LCURLY, '{')
Token(TITLE, 'title')
Token(EQ, '=')
Token(STRING, 'Roman History')
Token(SEMI, ';')
Token(ID, 'juliusCaesarBirth')
Token(COMMA, ',')
Token(ID, 'juliusCaesarDeath')
Token(COMMA, ',')
Token(ID, 'romanRepublic')
Token(SEMI, ';')
Token(RCURLY, '}')
Token(MAIN, 'main')
Token(LCURLY, '{')
Token(FOR, 'for')
Token(ID, 'item')
Token(IN, 'in')
Token(ID, 'romanHistory')
Token(LCURLY, '{')
Token(IF, 'if')
Token(LPAREN, '(')
Token(ID, 'item')
Token(DOT, '.')
Token(YEAR, 'year')
Token(LE, '<=')
Token(INT, 0)
Token(RPAREN, ')')
Token(LCURLY, '{')
Token(MODIFY, 'modify')
Token(ID, 'item')
Token(LCURLY, '{')
Token(IMPORTANCE, 'importance')
Token(EQ, '=')
Token(HIGH, 'high')
Token(SEMI, ';')
Token(RCURLY, '}')
Token(RCURLY, '}')
Token(RCURLY, '}')
Token(EXPORT, 'export')
Token(ID, 'romanHistory')
Token(SEMI, ';')
Token(RCURLY, '}')
Token(EOF, None)
```

## Conclusion

The laboratory work successfully demonstrated the design and implementation of a lexer for a custom domain-specific language (DSL) for my team's PBL project, showing its ability to accurately tokenize input files into meaningful grouped components. The lexer processed a variety of token types, including keywords, identifiers, strings, integers, and operators, effectively capturing the structure of the DSL. The dedicated methods for handling whitespace, numeric literals, identifiers, and special symbols, ensured clarity. This exercise showed the role of lexical analysis as the first step in processing structured input, providing a good foundation for building more advanced tools such as parsers or interpreters.

## References
<a id="ref1"></a>[1] "Lexical analysis" https://en.wikipedia.org/wiki/Lexical_analysis

<a id="ref2"></a>[2] “Kaleidoscope: Kaleidoscope Introduction and the Lexer" https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html.
