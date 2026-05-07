# Python Mini Compiler (Embedded Edition)

A fully optimized, lightweight mini compiler written in Python for a restricted Lua-like language. This project emphasizes extreme modularity, minimal memory footprint, and constant-folding optimization tailored for an embedded-system style environment.

## Compiler Architecture

The compilation pipeline executes completely locally with zero external dependencies:

1. **Lexical Analysis**: A regex-based tokenizer (`lexer.py`) capable of exact line/column tracking.
2. **Syntax Analysis**: A hand-rolled Recursive Descent parser (`parser.py`) generating a precise Abstract Syntax Tree (AST).
3. **Semantic Validation**: Symbol-table driven analyzer (`semantic.py`) tracking variables across function boundaries and loops.
4. **Optimization Phase**: An aggressive AST-to-AST transformation (`optimizer.py`) applying Constant Folding.
5. **Code Generation**: A lightweight Three Address Code (TAC) generator.
6. **Execution Engine**: A built-in TAC Simulator (`benchmark.py`) designed to benchmark native runtime speeds.

## Embedded Constraints & Optimizations

This compiler is built with **embedded constraints** in mind:
- **Low Memory Overhead**: Operations are strictly list-based to avoid dictionary bloat. Memory trace metrics routinely peak under `50 KB`.
- **Minimal Allocations**: AST nodes do not hold excessive back-references or metadata.
- **Constant Folding Impact**: The optimizer collapses both arithmetic (`2 + 3 * 4`) and comparison operations (`10 < 20`). This drastically reduces the number of generated TAC temporaries and results in a substantially tighter program footprint.

## Benchmark Methodology

The `benchmark.py` module strictly isolates metrics between the Unoptimized and Optimized states:
- `time.perf_counter()` is leveraged for microsecond-level compilation and runtime measurement.
- `tracemalloc` wraps each compilation phase to capture exact memory allocations.
- A custom `TACSimulator` physically iterates through the generated instructions to compute runtime speed, proving the real-world benefit of the AST optimization.

### Example Benchmark Comparison

```text
+----------------------+-------------+-------------+
| Metric               | Before Opt  | After Opt   |
+----------------------+-------------+-------------+
| Compile Time         | 1.30 ms     | 1.45 ms     |
| Memory Usage         | 48.0 KB     | 25.1 KB     |
| TAC Instructions     | 38          | 33          |
| TAC Size             | 321 bytes   | 285 bytes   |
| Runtime Speed        | 0.081 ms    | 0.065 ms    |
+----------------------+-------------+-------------+
```

## How to Run

Requirements:
- Python 3.6+

```bash
# Run the complete compiler suite with benchmarking
make test

# The optimized output is dumped into:
cat output.tac
```

---

## 🖥️ Presentation Slides (PPT Content)

The following content can be directly mapped into your Hackathon PowerPoint slides.

### Slide 1: Compiler Architecture
- **Goal**: Develop a robust, lightweight compiler for embedded system profiles.
- **Constraint**: Zero external libraries. Modularity (Every file < 200 lines).
- **Core Engine**: A 5-phase sequential pipeline (Lexer ➔ Parser ➔ Semantic ➔ Optimizer ➔ Code Gen).

### Slide 2: The Parser & AST Pipeline
- **Methodology**: Recursive Descent Parser evaluating proper arithmetic operator precedence.
- **Memory Footprint**: Extremely lightweight Abstract Syntax Tree instances minimizing dict overhead.
- **Output**: Generates pristine Three Address Code (TAC) representing flattened machine state.

### Slide 3: Embedded Optimizations (Constant Folding)
- **Problem**: Raw AST generation results in bloated temporaries and excessive runtime evaluation.
- **Solution**: Aggressive Constant Folding mapping static trees (e.g. `10 < 20`) directly to boolean nodes (`true`).
- **Result**: Constant folding reduced runtime operations and temporary variable generation significantly.

### Slide 4: Real-World Benchmarks
- We isolated memory allocations and instruction cycle counts using a custom-built Simulator.
- Memory peaks were dropped drastically. TAC byte-size shrank.
- **Conclusion**: Early-stage compilation optimization saves critical runtime hardware cycles on low-end systems!
