from ast_nodes import *

class SyntaxError(Exception):
    def __init__(self, message, line, col):
        super().__init__(f"SyntaxError at line {line} column {col}:\n{message}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def consume(self, expected_type, expected_value=None):
        tok = self.current()
        if tok.type == expected_type and (expected_value is None or tok.value == expected_value):
            self.pos += 1
            return tok
        val_msg = f" '{expected_value}'" if expected_value else ""
        raise SyntaxError(f"Expected {expected_type}{val_msg}, got {tok.type} '{tok.value}'", tok.line, tok.col)

    def parse(self):
        statements = []
        while self.current().type != 'EOF':
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self):
        tok = self.current()
        if tok.type == 'KEYWORD':
            if tok.value == 'if': return self.parse_if()
            if tok.value == 'while': return self.parse_while()
            if tok.value == 'for': return self.parse_for()
            if tok.value == 'function': return self.parse_function()
            if tok.value == 'return': return self.parse_return()
        return self.parse_assignment()

    def parse_assignment(self):
        var_name = self.consume('ID').value
        self.consume('ASSIGN')
        expr = self.parse_expression()
        return AssignmentNode(var_name, expr)

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        condition = self.parse_expression()
        self.consume('KEYWORD', 'then')
        if_body = []
        while self.current().value not in ('else', 'end'):
            if_body.append(self.parse_statement())
        else_body = None
        if self.current().value == 'else':
            self.consume('KEYWORD', 'else')
            else_body = []
            while self.current().value != 'end':
                else_body.append(self.parse_statement())
        self.consume('KEYWORD', 'end')
        return IfNode(condition, if_body, else_body)

    def parse_while(self):
        self.consume('KEYWORD', 'while')
        condition = self.parse_expression()
        self.consume('KEYWORD', 'do')
        body = []
        while self.current().value != 'end':
            body.append(self.parse_statement())
        self.consume('KEYWORD', 'end')
        return WhileNode(condition, body)

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        var_name = self.consume('ID').value
        self.consume('ASSIGN')
        start_expr = self.parse_expression()
        self.consume('PUNCT', ',')
        end_expr = self.parse_expression()
        self.consume('KEYWORD', 'do')
        body = []
        while self.current().value != 'end':
            body.append(self.parse_statement())
        self.consume('KEYWORD', 'end')
        return ForNode(var_name, start_expr, end_expr, body)

    def parse_function(self):
        self.consume('KEYWORD', 'function')
        name = self.consume('ID').value
        self.consume('PUNCT', '(')
        params = []
        while self.current().type == 'ID':
            params.append(self.consume('ID').value)
            if self.current().value == ',':
                self.consume('PUNCT', ',')
        self.consume('PUNCT', ')')
        body = []
        while self.current().value != 'end':
            body.append(self.parse_statement())
        self.consume('KEYWORD', 'end')
        return FunctionNode(name, params, body)

    def parse_return(self):
        self.consume('KEYWORD', 'return')
        expr = self.parse_expression() if self.current().type not in ('KEYWORD', 'EOF') else None
        return ReturnNode(expr)

    def parse_expression(self):
        node = self.parse_arithmetic()
        while self.current().type == 'OP_COMP':
            op = self.consume('OP_COMP').value
            right = self.parse_arithmetic()
            node = BinaryOpNode(node, op, right)
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.current().type == 'OP_ARITH' and self.current().value in ('+', '-'):
            op = self.consume('OP_ARITH').value
            right = self.parse_term()
            node = BinaryOpNode(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current().type == 'OP_ARITH' and self.current().value in ('*', '/', '%'):
            op = self.consume('OP_ARITH').value
            right = self.parse_factor()
            node = BinaryOpNode(node, op, right)
        return node

    def parse_factor(self):
        tok = self.current()
        if tok.type == 'INTEGER':
            self.pos += 1
            return NumberNode(int(tok.value))
        elif tok.type == 'FLOAT':
            self.pos += 1
            return NumberNode(float(tok.value), True)
        elif tok.type == 'STRING':
            self.pos += 1
            return StringNode(tok.value)
        elif tok.type == 'KEYWORD' and tok.value in ('true', 'false'):
            self.pos += 1
            return BooleanNode(tok.value == 'true')
        elif tok.type == 'ID':
            self.pos += 1
            return VariableNode(tok.value)
        elif tok.type == 'PUNCT' and tok.value == '(':
            self.pos += 1
            node = self.parse_expression()
            self.consume('PUNCT', ')')
            return node
        raise SyntaxError(f"Unexpected factor: {tok.type} '{tok.value}'", tok.line, tok.col)
