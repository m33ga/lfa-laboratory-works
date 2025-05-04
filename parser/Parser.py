from .ASTNode import *
from lexer import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(
                f"Syntax error: Expected token {token_type.name} got {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}"
            )

    def parse_program(self):
        declarations = []
        while self.current_token.type not in (TokenType.MAIN, TokenType.EOF):
            decl = self.parse_declaration()
            declarations.append(decl)
        main_block = None
        if self.current_token.type == TokenType.MAIN:
            main_block = self.parse_main_block()
        return Program(declarations, main_block)

    def parse_declaration(self):
        match self.current_token.type:
            case TokenType.EVENT:
                return self.parse_event_decl()
            case TokenType.PERIOD:
                return self.parse_period_decl()
            case TokenType.TIMELINE:
                return self.parse_timeline_decl()
            case TokenType.RELATIONSHIP:
                return self.parse_relationship_decl()
            case _:
                raise Exception(f"Unknown declaration: {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}")

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
                    raise Exception(f"Unexpected token in event declaration: {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}")

        self.eat(TokenType.RCURLY)
        return EventDeclaration(name, title, date, importance)

    def parse_period_decl(self):
        self.eat(TokenType.PERIOD)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LCURLY)

        title = None
        start_date = None
        end_date = None
        importance = None

        while self.current_token.type != TokenType.RCURLY:
            match self.current_token.type:
                case TokenType.TITLE:
                    self.eat(TokenType.TITLE)
                    self.eat(TokenType.EQ)
                    title = self.current_token.value.strip('"')
                    self.eat(TokenType.STRING)
                    self.eat(TokenType.SEMI)
                case TokenType.START:
                    self.eat(TokenType.START)
                    self.eat(TokenType.EQ)
                    start_date = self.parse_date_expr()
                    self.eat(TokenType.SEMI)
                case TokenType.END:
                    self.eat(TokenType.END)
                    self.eat(TokenType.EQ)
                    end_date = self.parse_date_expr()
                    self.eat(TokenType.SEMI)
                case TokenType.IMPORTANCE:
                    self.eat(TokenType.IMPORTANCE)
                    self.eat(TokenType.EQ)
                    importance = self.current_token.value
                    self.eat(self.current_token.type)
                    self.eat(TokenType.SEMI)
                case _:
                    raise Exception(f"Unexpected token in period declaration: {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}")

        self.eat(TokenType.RCURLY)
        return PeriodDeclaration(name, title, start_date, end_date, importance)

    def parse_timeline_decl(self):
        self.eat(TokenType.TIMELINE)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LCURLY)

        title = None
        components = []

        while self.current_token.type != TokenType.RCURLY:
            match self.current_token.type:
                case TokenType.TITLE:
                    self.eat(TokenType.TITLE)
                    self.eat(TokenType.EQ)
                    title = self.current_token.value.strip('"')
                    self.eat(TokenType.STRING)
                    self.eat(TokenType.SEMI)
                case TokenType.ID:
                    components.append(self.current_token.value)
                    self.eat(TokenType.ID)
                    if self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                    elif self.current_token.type == TokenType.SEMI:
                        self.eat(TokenType.SEMI)
                    else:
                        raise Exception(f"Expected ',' or ';' after component  at {self.current_token.line}:{self.current_token.column}")
                case _:
                    raise Exception(f"Unexpected token in timeline declaration: {self.current_token.type.name}  at {self.current_token.line}:{self.current_token.column}")

        self.eat(TokenType.RCURLY)
        return TimelineDeclaration(name, title, components)

    def parse_relationship_decl(self):
        self.eat(TokenType.RELATIONSHIP)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LCURLY)

        from_id = None
        to_id = None
        rel_type = None

        while self.current_token.type != TokenType.RCURLY:
            match self.current_token.type:
                case TokenType.FROM:
                    self.eat(TokenType.FROM)
                    self.eat(TokenType.EQ)
                    from_id = self.current_token.value
                    self.eat(TokenType.ID)
                    self.eat(TokenType.SEMI)
                case TokenType.TO:
                    self.eat(TokenType.TO)
                    self.eat(TokenType.EQ)
                    to_id = self.current_token.value
                    self.eat(TokenType.ID)
                    self.eat(TokenType.SEMI)
                case TokenType.TYPE:
                    self.eat(TokenType.TYPE)
                    self.eat(TokenType.EQ)
                    rel_type = self.current_token.value
                    self.eat(self.current_token.type)
                    self.eat(TokenType.SEMI)
                case _:
                    raise Exception(f"Unexpected token in relationship declaration: {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}")

        self.eat(TokenType.RCURLY)

        return RelationshipDeclaration(name, from_id, to_id, rel_type)

    def parse_date_expr(self):
        year = self.current_token.value
        self.eat(TokenType.INT)
        era = None
        if self.current_token.type in (TokenType.BCE, TokenType.CE):
            era = self.current_token.type
            self.eat(self.current_token.type)
            return DateLiteral(year, None, None, era.name if era else None)

        month = None
        day = None
        if self.current_token.type == TokenType.DASH:
            self.eat(TokenType.DASH)
            month = self.current_token.value
            self.eat(TokenType.INT)
            if self.current_token.type == TokenType.DASH:
                self.eat(TokenType.DASH)
                day = self.current_token.value
                self.eat(TokenType.INT)
                if self.current_token.type in (TokenType.BCE, TokenType.CE):
                    era = self.current_token.type
                    self.eat(self.current_token.type)
        elif self.current_token.type in (TokenType.BCE, TokenType.CE):
            era = self.current_token.type
            self.eat(self.current_token.type)

        return DateLiteral(year, month, day, era.name if era else None)

    def parse_main_block(self):
        self.eat(TokenType.MAIN)
        self.eat(TokenType.LCURLY)
        statements = []
        while self.current_token.type != TokenType.RCURLY:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.eat(TokenType.RCURLY)

        return MainBlock(statements)

    def parse_statement(self):
        match self.current_token.type:
            case TokenType.EXPORT:
                return self.parse_export_stmt()
            case TokenType.FOR:
                return self.parse_for_stmt()
            case TokenType.IF:
                return self.parse_if_stmt()
            case TokenType.MODIFY:
                return self.parse_modify_stmt()
            case TokenType.SEMI:
                self.eat(TokenType.SEMI)
                return None
            case _:
                raise Exception(f"Unexpected statement: {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}")

    def parse_export_stmt(self):
        self.eat(TokenType.EXPORT)
        target_id = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.SEMI)
        return ExportStatement(target_id)

    def parse_for_stmt(self):
        self.eat(TokenType.FOR)
        var_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.IN)
        iterable_id = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LCURLY)
        body = []
        while self.current_token.type != TokenType.RCURLY:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.eat(TokenType.RCURLY)

        return ForStatement(var_name, iterable_id, body)

    def parse_if_stmt(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.parse_condition()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LCURLY)
        then_block = []
        while self.current_token.type != TokenType.RCURLY:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
        self.eat(TokenType.RCURLY)
        else_block = []
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LCURLY)
            while self.current_token.type != TokenType.RCURLY:
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
            self.eat(TokenType.RCURLY)
        return IfStatement(condition, then_block, else_block)

    def parse_condition(self):
        left = self.parse_expr()
        if self.current_token.type in (
                TokenType.EQ_EQ,
                TokenType.NEQ,
                TokenType.LT,
                TokenType.GT,
                TokenType.LE,
                TokenType.GE
        ):
            op = self.current_token.type
            self.eat(op)
            right = self.parse_expr()
            return {'left': left, 'op': op.name, 'right': right}
        else:
            raise Exception(
                f"Expected comparison operator, got {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}"
            )

    def parse_expr(self):
        if self.current_token.type in (TokenType.INT, TokenType.STRING):
            value = self.current_token.value
            self.eat(self.current_token.type)
            return value

        elif self.current_token.type in (TokenType.TRUE, TokenType.FALSE):
            value = self.current_token.value
            self.eat(self.current_token.type)
            return value

        elif self.current_token.type in (TokenType.HIGH, TokenType.MEDIUM, TokenType.LOW):
            value = self.current_token.value
            self.eat(self.current_token.type)
            return value

        elif self.current_token.type == TokenType.ID:
            id_value = self.current_token.value
            self.eat(TokenType.ID)

            if self.current_token.type == TokenType.DOT:
                self.eat(TokenType.DOT)
                if self.current_token.type in (TokenType.YEAR, TokenType.MONTH, TokenType.DAY,
                                               TokenType.TITLE, TokenType.DATE, TokenType.IMPORTANCE):
                    prop = self.current_token.type
                    self.eat(prop)
                    return f"{id_value}.{prop.name.lower()}"
                else:
                    raise Exception(f"Expected a valid property after '.', got {self.current_token.type.name}")

            else:
                return id_value

        else:
            raise Exception(f"Unexpected token in expression: {self.current_token.type.name}")

    def parse_modify_stmt(self):
        self.eat(TokenType.MODIFY)
        target_id = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LCURLY)
        assignments = []
        while self.current_token.type != TokenType.RCURLY:
            prop = self.current_token.type
            self.eat(prop)
            self.eat(TokenType.EQ)
            value = self.current_token.value
            self.eat(self.current_token.type)
            self.eat(TokenType.SEMI)
            assignments.append(PropertyAssignment(prop.name, value))
        self.eat(TokenType.RCURLY)

        return ModifyStatement(target_id, assignments)

