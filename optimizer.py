from ast_nodes import *

class Optimizer:
    def optimize(self, node):
        if isinstance(node, ProgramNode):
            node.statements = [self.optimize(stmt) for stmt in node.statements]
            return node
            
        elif isinstance(node, AssignmentNode):
            node.value = self.optimize(node.value)
            return node
            
        elif isinstance(node, BinaryOpNode):
            node.left = self.optimize(node.left)
            node.right = self.optimize(node.right)
            
            # Constant Folding for Arithmetic and Comparisons
            if isinstance(node.left, NumberNode) and isinstance(node.right, NumberNode):
                return self._fold_constant(node.left, node.op, node.right)
            return node
            
        elif isinstance(node, IfNode):
            node.condition = self.optimize(node.condition)
            node.if_body = [self.optimize(stmt) for stmt in node.if_body]
            if node.else_body:
                node.else_body = [self.optimize(stmt) for stmt in node.else_body]
            return node
            
        elif isinstance(node, WhileNode):
            node.condition = self.optimize(node.condition)
            node.body = [self.optimize(stmt) for stmt in node.body]
            return node
            
        elif isinstance(node, ForNode):
            node.start_expr = self.optimize(node.start_expr)
            node.end_expr = self.optimize(node.end_expr)
            node.body = [self.optimize(stmt) for stmt in node.body]
            return node
            
        elif isinstance(node, FunctionNode):
            node.body = [self.optimize(stmt) for stmt in node.body]
            return node
            
        elif isinstance(node, ReturnNode):
            if node.value:
                node.value = self.optimize(node.value)
            return node
            
        # Leaf nodes return themselves
        return node

    def _fold_constant(self, left, op, right):
        lval = left.value
        rval = right.value
        try:
            # Arithmetic
            if op == '+': res = lval + rval
            elif op == '-': res = lval - rval
            elif op == '*': res = lval * rval
            elif op == '/': res = lval / rval
            elif op == '%': res = lval % rval
            # Comparisons
            elif op == '==': return BooleanNode(lval == rval)
            elif op == '!=': return BooleanNode(lval != rval)
            elif op == '<':  return BooleanNode(lval < rval)
            elif op == '>':  return BooleanNode(lval > rval)
            elif op == '<=': return BooleanNode(lval <= rval)
            elif op == '>=': return BooleanNode(lval >= rval)
            else: return BinaryOpNode(left, op, right)
            
            is_float = isinstance(res, float)
            return NumberNode(res, is_float)
        except ZeroDivisionError:
            return BinaryOpNode(left, op, right) # Don't fold division by zero
