from ast_nodes import *

class TACGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.generate(stmt)
        
        elif isinstance(node, NumberNode) or isinstance(node, StringNode) or isinstance(node, BooleanNode):
            val = f"'{node.value}'" if isinstance(node, StringNode) else str(node.value)
            return val
            
        elif isinstance(node, VariableNode):
            return node.name
            
        elif isinstance(node, BinaryOpNode):
            left_val = self.generate(node.left)
            right_val = self.generate(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left_val} {node.op} {right_val}")
            return temp
            
        elif isinstance(node, AssignmentNode):
            expr_val = self.generate(node.value)
            self.code.append(f"{node.name} = {expr_val}")
            
        elif isinstance(node, IfNode):
            cond_val = self.generate(node.condition)
            l_else = self.new_label()
            l_end = self.new_label()
            
            self.code.append(f"ifFalse {cond_val} goto {l_else if node.else_body else l_end}")
            for stmt in node.if_body:
                self.generate(stmt)
                
            if node.else_body:
                self.code.append(f"goto {l_end}")
                self.code.append(f"{l_else}:")
                for stmt in node.else_body:
                    self.generate(stmt)
                    
            self.code.append(f"{l_end}:")
            
        elif isinstance(node, WhileNode):
            l_start = self.new_label()
            l_end = self.new_label()
            
            self.code.append(f"{l_start}:")
            cond_val = self.generate(node.condition)
            self.code.append(f"ifFalse {cond_val} goto {l_end}")
            
            for stmt in node.body:
                self.generate(stmt)
            self.code.append(f"goto {l_start}")
            self.code.append(f"{l_end}:")
            
        elif isinstance(node, ForNode):
            # for var = start, end do ... end
            start_val = self.generate(node.start_expr)
            self.code.append(f"{node.var_name} = {start_val}")
            
            l_start = self.new_label()
            l_end = self.new_label()
            
            self.code.append(f"{l_start}:")
            end_val = self.generate(node.end_expr)
            
            temp_cond = self.new_temp()
            self.code.append(f"{temp_cond} = {node.var_name} <= {end_val}")
            self.code.append(f"ifFalse {temp_cond} goto {l_end}")
            
            for stmt in node.body:
                self.generate(stmt)
                
            # Increment
            self.code.append(f"{node.var_name} = {node.var_name} + 1")
            self.code.append(f"goto {l_start}")
            self.code.append(f"{l_end}:")
            
        elif isinstance(node, FunctionNode):
            self.code.append(f"func {node.name}():")
            for stmt in node.body:
                self.generate(stmt)
            self.code.append(f"endfunc")
            
        elif isinstance(node, ReturnNode):
            if node.value:
                val = self.generate(node.value)
                self.code.append(f"return {val}")
            else:
                self.code.append("return")
                
        return None
