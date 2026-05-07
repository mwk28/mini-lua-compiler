class TACSimulator:
    def __init__(self, debug=False):
        self.debug = debug
        self.env = {}

    def simulate(self, tac_instructions):
        """Simulate TAC instructions. Returns number of instructions executed."""
        ip = 0
        instructions_executed = 0
        
        # Build label map
        labels = {}
        for i, instr in enumerate(tac_instructions):
            if instr.endswith(':'):
                labels[instr[:-1]] = i
                
        while ip < len(tac_instructions):
            instr = tac_instructions[ip]
            instructions_executed += 1
            ip += 1
            
            if instr.endswith(':') or instr.startswith('func ') or instr == 'endfunc':
                continue # Labels and function markers are no-ops
                
            if self.debug:
                print(f"[TAC] {instr}")
                
            parts = instr.split()
            
            if len(parts) == 0:
                continue
                
            if parts[0] == 'goto':
                ip = labels[parts[1]]
                continue
                
            if parts[0] == 'ifFalse':
                cond_var = parts[1]
                target = parts[3]
                val = self.env.get(cond_var, False)
                if not val:
                    ip = labels[target]
                continue
                
            if parts[0] == 'return':
                break # Halt simulation on return
                
            # Assignment: x = y op z OR x = y
            if len(parts) >= 3 and parts[1] == '=':
                dest = parts[0]
                left = self._eval_val(parts[2])
                
                if len(parts) == 3:
                    self.env[dest] = left
                elif len(parts) == 5:
                    op = parts[3]
                    right = self._eval_val(parts[4])
                    if op == '+': self.env[dest] = left + right
                    elif op == '-': self.env[dest] = left - right
                    elif op == '*': self.env[dest] = left * right
                    elif op == '/': self.env[dest] = left / right
                    elif op == '<': self.env[dest] = left < right
                    elif op == '>': self.env[dest] = left > right
                    elif op == '<=': self.env[dest] = left <= right
                    elif op == '>=': self.env[dest] = left >= right
                    elif op == '==': self.env[dest] = left == right
                    elif op == '!=': self.env[dest] = left != right

        return instructions_executed

    def _eval_val(self, val):
        if val == 'True': return True
        if val == 'False': return False
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return self.env.get(val, 0) # variable lookup
