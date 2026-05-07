import sys
import time
import tracemalloc
import copy
import os
from lexer import Lexer, LexicalError
from parser import Parser, SyntaxError
from semantic import SemanticAnalyzer, SemanticError
from optimizer import Optimizer
from tac import TACGenerator
from benchmark import TACSimulator

def print_benchmark_table(metrics_before, metrics_after):
    table = f"\n{'+' + '-'*22 + '+' + '-'*13 + '+' + '-'*13 + '+'}\n"
    table += f"| {'Metric':<20} | {'Before Opt':<11} | {'After Opt':<11} |\n"
    table += f"{'+' + '-'*22 + '+' + '-'*13 + '+' + '-'*13 + '+'}\n"
    
    table += f"| {'Compile Time':<20} | {metrics_before['Compile Time']:.2f} ms{' ':>4}| {metrics_after['Compile Time']:.2f} ms{' ':>4}|\n"
    table += f"| {'Memory Usage':<20} | {metrics_before['Memory Usage']:.1f} KB{' ':>4}| {metrics_after['Memory Usage']:.1f} KB{' ':>4}|\n"
    table += f"| {'TAC Instructions':<20} | {metrics_before['TAC Instructions']:<11} | {metrics_after['TAC Instructions']:<11} |\n"
    table += f"| {'TAC Size':<20} | {metrics_before['TAC Size']} bytes{' ':>2}| {metrics_after['TAC Size']} bytes{' ':>2}|\n"
    table += f"| {'Runtime Speed':<20} | {metrics_before['Runtime Speed']:.3f} ms{' ':>3}| {metrics_after['Runtime Speed']:.3f} ms{' ':>3}|\n"
    
    table += f"{'+' + '-'*22 + '+' + '-'*13 + '+' + '-'*13 + '+'}\n"
    print(table)
    
    print("\nOPTIMIZATION SUMMARY:")
    print("Constant folding reduced runtime operations and temporary variable generation.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)
        
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()
        
    print("\n=== 1. Source Code ===")
    print(code)
    
    # -----------------------------------------------------------------
    # PIPELINE BEFORE OPTIMIZATION
    # -----------------------------------------------------------------
    tracemalloc.start()
    t0 = time.perf_counter()
    
    try:
        # Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("\n=== 2. Tokens ===")
        for tok in tokens:
            print(tok)
            
        # Parser
        parser = Parser(tokens)
        ast_before = parser.parse()
        
        # Semantic Analysis
        semantic = SemanticAnalyzer()
        semantic.analyze(ast_before)
        
        # TAC Gen Before
        tac_gen_before = TACGenerator()
        tac_gen_before.generate(ast_before)
        
        t1 = time.perf_counter()
        _, peak_mem_before = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Runtime Simulation Before
        sim_before = TACSimulator(debug=False)
        sim_t0 = time.perf_counter()
        sim_before.simulate(tac_gen_before.code)
        sim_t1 = time.perf_counter()
        
        metrics_before = {
            'Compile Time': (t1 - t0) * 1000,
            'Memory Usage': peak_mem_before / 1024,
            'TAC Instructions': len(tac_gen_before.code),
            'TAC Size': sum(len(instr) + 1 for instr in tac_gen_before.code), # rough byte estimate
            'Runtime Speed': (sim_t1 - sim_t0) * 1000
        }
        
        print("\n=== 3. AST Before Optimization ===")
        print(ast_before.print_tree())
        
        print("\n=== 4. TAC Before Optimization ===")
        for instr in tac_gen_before.code:
            print(instr)
            
        # -----------------------------------------------------------------
        # PIPELINE AFTER OPTIMIZATION
        # -----------------------------------------------------------------
        ast_after = copy.deepcopy(ast_before)
        
        tracemalloc.start()
        t2 = time.perf_counter()
        
        optimizer = Optimizer()
        optimized_ast = optimizer.optimize(ast_after)
        
        tac_gen_after = TACGenerator()
        tac_gen_after.generate(optimized_ast)
        
        t3 = time.perf_counter()
        _, peak_mem_after = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Runtime Simulation After
        sim_after = TACSimulator(debug=False)
        sim_t2 = time.perf_counter()
        sim_after.simulate(tac_gen_after.code)
        sim_t3 = time.perf_counter()
        
        # Write Output TAC
        with open("output.tac", "w") as f:
            for instr in tac_gen_after.code:
                f.write(instr + "\n")
        output_size = os.path.getsize("output.tac")
        
        metrics_after = {
            # Add Lex+Parse time to Optimization time to show full compile time
            'Compile Time': ((t1 - t0) + (t3 - t2)) * 1000,
            'Memory Usage': peak_mem_after / 1024,
            'TAC Instructions': len(tac_gen_after.code),
            'TAC Size': sum(len(instr) + 1 for instr in tac_gen_after.code),
            'Runtime Speed': (sim_t3 - sim_t2) * 1000
        }
        
        print("\n=== 5. AST After Optimization ===")
        print(optimized_ast.print_tree())
        
        print("\n=== 6. TAC After Optimization ===")
        for instr in tac_gen_after.code:
            print(instr)
            
        print("\n=== 7. Benchmark Comparison ===")
        print_benchmark_table(metrics_before, metrics_after)
        
    except (LexicalError, SyntaxError, SemanticError) as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
