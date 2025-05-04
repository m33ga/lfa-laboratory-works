# Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata

### Author: Mihai Gurduza

---

## Theory

Parsing is the process of analyzing a sequence of tokens to determine its grammatical structure with respect to a given formal grammar. It is a fundamental step in the compilation process, where the source code is converted into an intermediate representation [1]. Abstract Syntax Trees (ASTs) are tree representations of the abstract syntactic structure of source code. Each node in the tree denotes a construct occurring in the source code. ASTs are widely used in compilers and interpreters to represent the structure of programs and facilitate further processing, such as optimization and code generation [2].

## Objectives:

1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type **_TokenType_** (like an enum) that can be used in the lexical analysis to categorize the tokens.
      2. Use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation description

### Parser Implementation

The `Parser` class is responsible for analyzing the tokenized input and constructing an AST. It uses methods like `parse_program`, `parse_declaration`, and `parse_statement` to handle different parts of the input. The `parse_program` method is the entry point for parsing the entire program. It iterates through the tokens, identifying and parsing declarations until it encounters the `MAIN` token or the end of the file. If a `MAIN` block is present, it is parsed separately. The result is a `Program` node that encapsulates all declarations and the main block.

```python
class Parser:
    def parse_program(self):
        declarations = []
        while self.current_token.type not in (TokenType.MAIN, TokenType.EOF):
            decl = self.parse_declaration()
            declarations.append(decl)
        main_block = None
        if self.current_token.type == TokenType.MAIN:
            main_block = self.parse_main_block()
        return Program(declarations, main_block)
```

### ASTNode Implementation

The `ASTNode` class and its subclasses represent the nodes of the AST. For example, the `EventDeclaration` class is a specialized node that represents an event declaration in the DSL. It contains attributes such as `name`, `title`, `date`, and `importance`, which correspond to the properties of an event. The `__repr__` method provides a string representation of the node, making it easier to debug and visualize the AST.

```python
class EventDeclaration(ASTNode):
    def __init__(self, name, title, date, importance=None):
        self.name = name
        self.title = title
        self.date = date
        self.importance = importance

    def __repr__(self):
        return f"Event({self.name}, title={self.title}, date={self.date}, importance={self.importance})"
```

### Example of Parsing a Declaration

The `parse_event_decl` method in the `Parser` class is specifically designed to parse event declarations. It begins by consuming the `EVENT` token and extracting the event's name. The method then enters a loop to parse the event's properties, such as `title`, `date`, and `importance`. Each property is identified by its corresponding token type, and the method ensures that the syntax is correct by consuming the expected tokens in sequence. Once all properties are parsed, the method constructs and returns an `EventDeclaration` node.

```python
class Parser:
    def parse_event_decl(self):
        self.eat(TokenType.EVENT)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LCURLY)

        title = None
        date = None
        importance = None

        while self.current_token.type != TokenType.RCURLY:
            match self.current_token.type:
                case TokenType.TITLE:
                    self.eat(TokenType.TITLE)
                    self.eat(TokenType.EQ)
                    title = self.current_token.value.strip('"')
                    self.eat(TokenType.STRING)
                    self.eat(TokenType.SEMI)
                case TokenType.DATE:
                    self.eat(TokenType.DATE)
                    self.eat(TokenType.EQ)
                    date = self.parse_date_expr()
                    self.eat(TokenType.SEMI)
                case TokenType.IMPORTANCE:
                    self.eat(TokenType.IMPORTANCE)
                    self.eat(TokenType.EQ)
                    importance = self.current_token.value
                    self.eat(self.current_token.type)
                    self.eat(TokenType.SEMI)
                case _:
                    raise Exception(f"Unexpected token in event declaration: {self.current_token.type.name}")

        self.eat(TokenType.RCURLY)
        return EventDeclaration(name, title, date, importance)
```

## Results

Testing the parser for input from [input.dsl](/6_parser_ast_build/input.dsl) file, the following JSON is created:

```
Abstract Syntax Tree (AST):

{
  "__type__": "Program",
  "declarations": [
    {
      "__type__": "EventDeclaration",
      "name": "juliusCaesarBirth",
      "title": "Birth of Julius Caesar",
      "date": {
        "__type__": "DateLiteral",
        "year": 12,
        "month": 7,
        "day": 100,
        "era": "BCE"
      },
      "importance": "medium"
    },
    {
      "__type__": "EventDeclaration",
      "name": "juliusCaesarDeath",
      "title": "Assassination of Julius Caesar",
      "date": {
        "__type__": "DateLiteral",
        "year": 15,
        "month": 3,
        "day": 44,
        "era": "BCE"
      },
      "importance": "high"
    },
    {
      "__type__": "PeriodDeclaration",
      "name": "romanRepublic",
      "title": " Roman Republic ",
      "start_date": {
        "__type__": "DateLiteral",
        "year": 509,
        "month": null,
        "day": null,
        "era": "BCE"
      },
      "end_date": {
        "__type__": "DateLiteral",
        "year": 27,
        "month": null,
        "day": null,
        "era": "BCE"
      },
      "importance": "high"
    },
    {
      "__type__": "TimelineDeclaration",
      "name": "romanHistory",
      "title": "Roman History",
      "components": [
        "juliusCaesarBirth",
        "juliusCaesarDeath",
        "romanRepublic"
      ]
    }
  ],
  "main_block": {
    "__type__": "MainBlock",
    "statements": [
      {
        "__type__": "ForStatement",
        "var_name": "item",
        "iterable_id": "romanHistory",
        "body": [
          {
            "__type__": "IfStatement",
            "condition": {
              "left": "item.year",
              "op": "LE",
              "right": 0
            },
            "then_block": [
              {
                "__type__": "ModifyStatement",
                "target_id": "item",
                "assignments": [
                  {
                    "__type__": "PropertyAssignment",
                    "property_name": "IMPORTANCE",
                    "value": "high"
                  }
                ]
              }
            ],
            "else_block": []
          }
        ]
      },
      {
        "__type__": "ExportStatement",
        "target_id": "romanHistory"
      }
    ]
  }
}
```

In order to make the representation easier to read, it was fed into a JSON visualizer to create a graphical representation of it.

![JSON Output](/6_parser_ast_build/report/images/ast1.png)

## Conclusions

This lab was a great way to learn about parsing and ASTs. I saw how to break down a language into smaller parts and represent it in a structured way. The parser handled different declarations and statements, making sure the input was correct. The AST made the program's structure clear and easy to work with. Each method in the parser had a specific job, which made the code easier to understand. The AST classes kept the data organized and reusable. This project helped me understand how parsing works and why ASTs are important in programming languages. It also showed how these concepts are used in real tools like compilers and interpreters.

## References

[1] [Parsing Wiki](https://en.wikipedia.org/wiki/Parsing)

[2] [Abstract Syntax Tree Wiki](https://en.wikipedia.org/wiki/Abstract_syntax_tree)

[3] [JSON Viewer](https://jsoncrack.com/editor)
