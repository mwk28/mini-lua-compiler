import re

class LexicalError(Exception):
    def __init__(self, message, line, col):
        super().__init__(f"LexicalError at line {line} column {col}:\n{message}")

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
        
    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.col})"

class Lexer:
    # Token specifications
    KEYWORDS = {'if', 'else', 'while', 'for', 'function', 'return', 'end', 'true', 'false', 'do', 'then'}
    
    TOKEN_SPEC = [
        ('M_COMMENT', r'--\[\[.*?\]\]'),   # Multiline comment
        ('S_COMMENT', r'--[^\n]*'),        # Single line comment
        ('FLOAT', r'\d+\.\d+'),            # Float literal
        ('INTEGER', r'\d+'),               # Integer literal
        ('STRING', r'"[^"\n]*"|\'[^\'\n]*\''), # String literal
        ('OP_COMP', r'==|!=|<=|>=|<|>'),   # Comparison operators
        ('OP_ARITH', r'[+\-*/%]'),         # Arithmetic operators
        ('ASSIGN', r'='),                  # Assignment
        ('PUNCT', r'[(),]'),               # Punctuation
        ('ID', r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
        ('WS', r'[ \t]+'),                 # Whitespace
        ('NEWLINE', r'\n'),                # Newline
        ('MISMATCH', r'.'),                # Any other character
    ]

    def __init__(self, code):
        self.code = code
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.TOKEN_SPEC)
        self.regex = re.compile(tok_regex, re.DOTALL)
        self.tokens = []

    def tokenize(self):
        line_num = 1
        line_start = 0
        
        for mo in self.regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            col = mo.start() - line_start + 1
            
            if kind in ('M_COMMENT', 'S_COMMENT'):
                if '\n' in value:
                    newlines = value.count('\n')
                    line_num += newlines
                    line_start = mo.end() - len(value) + value.rfind('\n') + 1
                continue
            elif kind == 'WS':
                continue
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'ID' and value in self.KEYWORDS:
                kind = 'KEYWORD'
            elif kind == 'STRING':
                value = value[1:-1] # Strip quotes
            elif kind == 'MISMATCH':
                raise LexicalError(f"Invalid token '{value}'", line_num, col)
            
            self.tokens.append(Token(kind, value, line_num, col))
            
        self.tokens.append(Token('EOF', '', line_num, len(self.code) - line_start + 1))
        return self.tokens
