class ASTNode:
    pass


class EventDeclaration(ASTNode):
    def __init__(self, name, title, date, importance=None):
        self.name = name
        self.title = title
        self.date = date
        self.importance = importance

    def __repr__(self):
        return f"Event({self.name}, title={self.title}, date={self.date}, importance={self.importance})"


class PeriodDeclaration(ASTNode):
    def __init__(self, name, title, start_date, end_date, importance=None):
        self.name = name
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.importance = importance

    def __repr__(self):
        return f"Period({self.name}, title={self.title}, start={self.start_date}, end={self.end_date}, importance={self.importance})"


class TimelineDeclaration(ASTNode):
    def __init__(self, name, title, components):
        self.name = name
        self.title = title
        self.components = components  # list of IDs

    def __repr__(self):
        return f"Timeline({self.name}, title={self.title}, components={self.components})"


class RelationshipDeclaration(ASTNode):
    def __init__(self, name, from_id, to_id, rel_type):
        self.name = name
        self.from_id = from_id
        self.to_id = to_id
        self.rel_type = rel_type

    def __repr__(self):
        return f"Relationship({self.name}, from={self.from_id}, to={self.to_id}, type={self.rel_type})"


class DateLiteral(ASTNode):
    def __init__(self, year, month=None, day=None, era=None):
        self.year = year
        self.month = month
        self.day = day
        self.era = era

    def __repr__(self):
        return f"Date({self.year}-{self.month or ''}-{self.day or ''} {self.era or ''})".rstrip(" -")


class DateCalculation(ASTNode):
    def __init__(self, target_id, field, op, value):
        self.target_id = target_id
        self.field = field
        self.op = op
        self.value = value

    def __repr__(self):
        return f"{self.target_id}.{self.field} {self.op} {self.value}"


class Program(ASTNode):
    def __init__(self, declarations, main_block=None):
        self.declarations = declarations
        self.main_block = main_block

    def __repr__(self):
        return f"Program(declarations={self.declarations}, main_block={self.main_block})"


class MainBlock(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"MainBlock(statements={self.statements})"


class ExportStatement(ASTNode):
    def __init__(self, target_id):
        self.target_id = target_id

    def __repr__(self):
        return f"Export({self.target_id})"


class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"If({self.condition}) Then: {self.then_block} Else: {self.else_block}"


class ForStatement(ASTNode):
    def __init__(self, var_name, iterable_id, body):
        self.var_name = var_name
        self.iterable_id = iterable_id
        self.body = body

    def __repr__(self):
        return f"For({self.var_name} in {self.iterable_id}) Do: {self.body}"


class ModifyStatement(ASTNode):
    def __init__(self, target_id, assignments):
        self.target_id = target_id
        self.assignments = assignments

    def __repr__(self):
        return f"Modify({self.target_id}, {self.assignments})"


class PropertyAssignment(ASTNode):
    def __init__(self, property_name, value):
        self.property_name = property_name
        self.value = value

    def __repr__(self):
        return f"{self.property_name} = {self.value}"


def ast_to_dict(node):
    if isinstance(node, list):
        return [ast_to_dict(n) for n in node]
    if not isinstance(node, ASTNode):
        return node
    return {
        '__type__': node.__class__.__name__,
        **{k: ast_to_dict(v) for k, v in node.__dict__.items()}
    }