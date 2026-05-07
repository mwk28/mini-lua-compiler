class ASTNode:
    def print_tree(self, indent=0):
        pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def print_tree(self, indent=0):
        res = "  " * indent + "Program\n"
        for stmt in self.statements:
            res += stmt.print_tree(indent + 1)
        return res

class NumberNode(ASTNode):
    def __init__(self, value, is_float=False):
        self.value = value
        self.is_float = is_float
    def print_tree(self, indent=0):
        return "  " * indent + f"Number({self.value})\n"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def print_tree(self, indent=0):
        return "  " * indent + f"String('{self.value}')\n"

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def print_tree(self, indent=0):
        return "  " * indent + f"Boolean({self.value})\n"

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def print_tree(self, indent=0):
        return "  " * indent + f"Variable({self.name})\n"

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def print_tree(self, indent=0):
        res = "  " * indent + f"BinaryOp({self.op})\n"
        res += self.left.print_tree(indent + 1)
        res += self.right.print_tree(indent + 1)
        return res

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def print_tree(self, indent=0):
        res = "  " * indent + f"Assignment({self.name})\n"
        res += self.value.print_tree(indent + 1)
        return res

class IfNode(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
    def print_tree(self, indent=0):
        res = "  " * indent + "If\n"
        res += "  " * (indent+1) + "Condition:\n" + self.condition.print_tree(indent + 2)
        res += "  " * (indent+1) + "Then:\n"
        for stmt in self.if_body: res += stmt.print_tree(indent + 2)
        if self.else_body:
            res += "  " * (indent+1) + "Else:\n"
            for stmt in self.else_body: res += stmt.print_tree(indent + 2)
        return res

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def print_tree(self, indent=0):
        res = "  " * indent + "While\n"
        res += "  " * (indent+1) + "Condition:\n" + self.condition.print_tree(indent + 2)
        res += "  " * (indent+1) + "Body:\n"
        for stmt in self.body: res += stmt.print_tree(indent + 2)
        return res

class ForNode(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, body):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body
    def print_tree(self, indent=0):
        res = "  " * indent + f"For({self.var_name})\n"
        res += "  " * (indent+1) + "Start:\n" + self.start_expr.print_tree(indent + 2)
        res += "  " * (indent+1) + "End:\n" + self.end_expr.print_tree(indent + 2)
        res += "  " * (indent+1) + "Body:\n"
        for stmt in self.body: res += stmt.print_tree(indent + 2)
        return res

class FunctionNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def print_tree(self, indent=0):
        res = "  " * indent + f"Function({self.name}, {self.params})\n"
        for stmt in self.body: res += stmt.print_tree(indent + 1)
        return res

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def print_tree(self, indent=0):
        res = "  " * indent + "Return\n"
        if self.value:
            res += self.value.print_tree(indent + 1)
        return res
