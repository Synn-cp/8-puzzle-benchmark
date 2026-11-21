# 8-Puzzle Solver & Heuristic Search Benchmarking

A Python implementation and empirical benchmark of informed (**A\***) and uninformed (**BFS, DFS**) search algorithms for the 8-puzzle problem. This project evaluates algorithm performance across **solution path length**, **explored states**, **execution time**, and **peak memory usage**, alongside an analysis of **Early Exit goal testing** in unit-cost A\*.

---

## Methodology & Problem Formulation

- **State Representation & Solvability:** Board states are modeled as $3 \times 3$ matrices. All 100 test pairs in `test_cases.json` (`seed=42`) are randomly generated and validated via **inversion parity** to guarantee solvability.
- **Informed Search (A\*):**
  - **Manhattan Distance:** Sum of horizontal and vertical distances of all tiles from their goal coordinates.
  - **Misplaced Tiles:** Count of tiles out of their target positions.
- **Uninformed Search:** Breadth-First Search (**BFS**) and Depth-First Search (**DFS**) as baseline comparisons.
- **Early Exit Strategy:** Evaluates terminating immediately when the goal state is generated in the frontier (`early_exit=True`) versus standard A\* termination when the goal state is popped for expansion (`early_exit=False`).

---

## Experimental Results (Average over 100 Solvable Test Cases)

| Algorithm | Avg. Steps | Avg. Explored States | Avg. Time (ms) | Peak Memory (KB) |
| :--- | :---: | :---: | :---: | :---: |
| **A\* (Manhattan)** | 21.94 | 603.9 | 14.787 | 580.16 |
| **A\* (Manhattan + Early Exit)** | 21.94 | 602.9 | 14.692 | 579.54 |
| **A\* (Misplaced)** | 21.94 | 9,010.0 | 219.169 | 8,212.42 |
| **A\* (Misplaced + Early Exit)** | 21.94 | 9,009.0 | 220.252 | 8,211.88 |
| **BFS (Uninformed)** | 21.94 | 91,539.8 | 1,357.612 | 47,984.23 |
| **DFS (Uninformed)** | 39,301.62 | 94,665.4 | 1,315.321 | 59,055.06 |

---

## Key Findings & Discussion

- **Informed vs. Uninformed Search:** A\* with Manhattan distance explores **~150× fewer states** and uses **~82× less memory** than BFS while achieving the exact same optimal path length (`21.94` steps).
- **Heuristic Dominance:** Both heuristics are *admissible* and *consistent*, guaranteeing optimal paths. However, Manhattan distance **dominates** Misplaced Tiles ($h_{\text{Manhattan}}(n) \ge h_{\text{Misplaced}}(n)$), cutting explored states and memory consumption by **~93.3%** (`603.9` vs. `9,010.0` states).
- **BFS vs. DFS Trade-offs:** BFS guarantees optimal solutions at the cost of heavy memory overhead (`47.98 MB`), whereas DFS fails to guarantee optimality (averaging `39,301.62` steps) while still exploring a massive portion of the state space.
- **Early Exit in Unit-Cost A\*:** In general graph search, stopping upon goal generation risks sub-optimality. However, in the 8-puzzle with uniform step costs ($c = 1$), any neighbor $u$ of the goal state has $h(u) = 1$ under both heuristics, yielding $f(\text{goal}) = g^*(u) + 1 = f^*(u) = f^*$. Thus, `early_exit=True` preserves optimality while saving exactly `1.0` redundant node expansion on average.

---

## Repository Structure & Usage

```text
├── main.py               # Search algorithms (A*, BFS, DFS) & benchmark runner
├── create_test_case.py   # Solvable test-case generator using inversion parity
├── test_cases.json       # 100 pre-generated solvable 8-puzzle instances (seed=42)
├── benchmark_table.md    # Raw benchmark output table
└── README.md             # Project documentation and analysis