from ast_nodes import *

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(f"SemanticError:\n{message}")

class SemanticAnalyzer:
    def __init__(self):
        self.scopes = [{}] # Stack of scopes (dictionaries)
        self.functions = {} # Global functions

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare_var(self, name):
        self.scopes[-1][name] = True

    def check_var(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False

    def analyze(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.analyze(stmt)
                
        elif isinstance(node, AssignmentNode):
            self.analyze(node.value)
            if not self.check_var(node.name):
                self.declare_var(node.name) # auto-declare on first assignment
                
        elif isinstance(node, VariableNode):
            if not self.check_var(node.name):
                raise SemanticError(f"Undeclared variable '{node.name}'")
                
        elif isinstance(node, BinaryOpNode):
            self.analyze(node.left)
            self.analyze(node.right)
            
        elif isinstance(node, IfNode):
            self.analyze(node.condition)
            self.enter_scope()
            for stmt in node.if_body: self.analyze(stmt)
            self.exit_scope()
            if node.else_body:
                self.enter_scope()
                for stmt in node.else_body: self.analyze(stmt)
                self.exit_scope()
                
        elif isinstance(node, WhileNode):
            self.analyze(node.condition)
            self.enter_scope()
            for stmt in node.body: self.analyze(stmt)
            self.exit_scope()
            
        elif isinstance(node, ForNode):
            self.analyze(node.start_expr)
            self.analyze(node.end_expr)
            self.enter_scope()
            self.declare_var(node.var_name)
            for stmt in node.body: self.analyze(stmt)
            self.exit_scope()
            
        elif isinstance(node, FunctionNode):
            if node.name in self.functions:
                raise SemanticError(f"Function '{node.name}' already declared")
            self.functions[node.name] = len(node.params)
            self.enter_scope()
            for param in node.params:
                self.declare_var(param)
            for stmt in node.body:
                self.analyze(stmt)
            self.exit_scope()
            
        elif isinstance(node, ReturnNode):
            if node.value:
                self.analyze(node.value)
                
        elif isinstance(node, (NumberNode, StringNode, BooleanNode)):
            pass # Primitives are always semantically valid
            
        else:
            raise Exception(f"Unknown node type during semantic analysis: {type(node)}")
