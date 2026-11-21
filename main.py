from collections import deque
from typing import Callable
import heapq
import gc
import random
import time
import tracemalloc
import json

def load_test_cases(filename: str = "test_cases.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["cases"]

class coord:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

class state:
    def __init__(self, step: int, board: list, space: coord, parent: "state" = None):
        self._step = step
        self._parent = parent
        self._board = board
        self._space = space

    def __lt__(self, other):
        return (self._step > other._step)

def check_coord(a: coord) -> bool:
    return (0 <= a._x <= 2 and 0 <= a._y <= 2)

def find_space(board: list) -> coord:
    
    for i in range(3):
        for j in range(3):
            if (board[i][j] == -1):
                return coord(i, j)

    return coord(-1 ,- 1)

def find_goal_pos(board: list) -> list :
    n = len(board)
    res = [coord(0,0) for _ in range(n*n)]

    for i in range(n) :
        for j in range(n) :
            val = board[i][j]
            if (val != -1) :
                res[val - 1] = coord(i,j)

    return res

def distance(a: coord, b: coord) -> int:
    return abs(a._x - b._x) + abs(a._y - b._y)

def matrix_to_state_key(a: list) -> str:
    return "".join(str(cell) for row in a for cell in row)

def heuristic_manhattan(a: state , goal_pos: list) -> int:
    res = 0
    for i in range(3):
        for j in range(3):
            val = a._board[i][j]
            if (val != -1):
                res += distance(coord(i, j), goal_pos[val - 1])
    return res

def heuristic_misplaced(a: state , goal_pos: list) -> int:
    res = 0
    for i in range(3):
        for j in range(3):
            val = a._board[i][j]
            if (val == -1): 
                continue
            if (i != goal_pos[val - 1]._x or j != goal_pos[val - 1]._y) :
                res += 1
    return res

def informed_solve(st_board: list , goal_board: list , heuristic_func: Callable[[state , list] , int], early_exit: bool = False) -> tuple[list[list[int]], int]:
    
    visited_states = set()
    pq = []

    try :
        st_coord = find_space(st_board)
        goal_pos = find_goal_pos(goal_board)
        
        st = state(0, st_board, st_coord)
        f_initial = heuristic_func(st , goal_pos) + st._step
        heapq.heappush(pq, (f_initial, st))

        cnt = 0

        while pq:
            if (cnt == 10**8):
                #print("Run so far")
                break

            cur_f, cur_state = heapq.heappop(pq)
            board_key = matrix_to_state_key(cur_state._board)
            if (board_key in visited_states) :
                continue
            visited_states.add(board_key)
            cnt += 1

            if (cur_state._board == goal_board):
                #print("FOUND")
                
                path = []
                while (cur_state is not None):
                    path.append(cur_state._board)
                    cur_state = cur_state._parent
                
                return (path[::-1] , cnt)


            for i in range(4):
                new_space = coord(cur_state._space._x + dx[i], cur_state._space._y + dy[i])

                if (check_coord(new_space)):
                    new_board = [row[:] for row in cur_state._board]
                    
                    cx, cy = cur_state._space._x, cur_state._space._y
                    nx, ny = new_space._x, new_space._y
                    new_board[cx][cy], new_board[nx][ny] = new_board[nx][ny], new_board[cx][cy]
                    
                    board_key = matrix_to_state_key(new_board)
                    if (board_key in visited_states):
                        continue
                    new_state = state(cur_state._step + 1, new_board, new_space, cur_state)
                    h = heuristic_func(new_state , goal_pos)
                    f = h + new_state._step
                    if (early_exit and h == 0):
                        path = []
                        while (new_state is not None):
                            path.append(new_state._board)
                            new_state = new_state._parent
                        return (path[::-1] , cnt)
                    heapq.heappush(pq, (f, new_state))
    finally: 
        visited_states.clear()
        pq.clear()
        del visited_states
        del pq

def uninformed_solve(st_board: list , goal_board: list, type: str) -> tuple[list[list[int]], int]:
    visited_states = set()
    q = deque()
    st_coord = find_space(st_board)
    goal_pos = find_goal_pos(goal_board)

    st = state(0, st_board, st_coord)
    visited_states.add(matrix_to_state_key(st._board))
    q.append(st)

    cnt = 0

    while q:
        if (cnt == 10**8):
            #print("Run so far")
            break

        cnt += 1
        if (type == "DFS"):
            cur_state = q.pop()
        else:
            cur_state = q.popleft()

        if cur_state._board == goal_board:
            #print("FOUND")

            path = []
            while (cur_state is not None):
                path.append(cur_state._board)
                cur_state = cur_state._parent

            return (path[::-1], cnt)

        for i in range(4):
            new_space = coord(cur_state._space._x + dx[i], cur_state._space._y + dy[i])

            if (check_coord(new_space)):
                new_board = [row[:] for row in cur_state._board]

                cx, cy = cur_state._space._x, cur_state._space._y
                nx, ny = new_space._x, new_space._y
                new_board[cx][cy], new_board[nx][ny] = new_board[nx][ny], new_board[cx][cy]

                board_key = matrix_to_state_key(new_board)

                if board_key not in visited_states:
                    visited_states.add(board_key)

                    new_state = state(cur_state._step + 1, new_board, new_space, cur_state)
                    q.append(new_state)

def create_board():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, -1]
    random.shuffle(nums)
    
    board = [nums[i:i+3] for i in range(0, 9, 3)]
    return board

def get_board_parity(board: list[list[int]]) -> int:
    n = len(board)
    flat = [cell for row in board for cell in row if cell != -1]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if (flat[i] > flat[j]):
                inversions += 1
                
    if (n % 2 == 1):
        return (inversions % 2)

    for i in range(3):
            for j in range(3):
                if (board[i][j] == -1):
                    blank_row = i
                    break

    return (inversions + blank_row) % 2


dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

def benchmark_single_run(func, *args, **kwargs):
    """
    Đo thời gian thực thi (ms) và bộ nhớ (KB)
    Trả về: (steps, states_checked, elapsed_ms, peak_kb)
    """
    gc.collect()
    start_time = time.perf_counter()
    path, states_checked = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    gc.collect()
    tracemalloc.start()
    func(*args, **kwargs)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak_bytes / 1024

    steps = len(path) - 1
    return steps, states_checked, elapsed_ms, peak_kb


def generate_markdown_table(stats: dict, num_trials: int) -> str:
    header = (
        f"### Kết quả thực nghiệm (Trung bình trên {num_trials} bộ test ngẫu nhiên)\n\n"
        "| Thuật toán | Số bước TB (Steps) | Trạng thái duyệt TB | Thời gian TB (ms) | Bộ nhớ TB (KB) |\n"
        "| :--- | :---: | :---: | :---: | :---: |\n"
    )
    rows = []
    for name, data in stats.items():
        avg_steps = data["steps"] / num_trials
        avg_states = data["states"] / num_trials
        avg_time = data["time_ms"] / num_trials
        avg_mem = data["mem_kb"] / num_trials
        rows.append(
            f"| {name} | {avg_steps:.2f} | {avg_states:,.1f} | {avg_time:.3f} | {avg_mem:,.2f} |"
        )
    return header + "\n".join(rows) + "\n"


def main():

    algorithms = {
        "A* (Manhattan)": lambda st, gl: informed_solve(st, gl, heuristic_manhattan, early_exit=False),
        "A* (Manhattan + Early Exit)": lambda st, gl: informed_solve(st, gl, heuristic_manhattan, early_exit=True),
        "A* (Misplaced)": lambda st, gl: informed_solve(st, gl, heuristic_misplaced, early_exit=False),
        "A* (Misplaced + Early Exit)": lambda st, gl: informed_solve(st, gl, heuristic_misplaced, early_exit=True),
        "BFS": lambda st, gl: uninformed_solve(st, gl, "BFS"),
        "DFS": lambda st, gl: uninformed_solve(st, gl, "DFS"),
    }

    stats = {
        name: {"steps": 0, "states": 0, "time_ms": 0.0, "mem_kb": 0.0}
        for name in algorithms
    }

    test_cases = load_test_cases("test_cases.json")
    NUM_TRIALS = len(test_cases)
    
    for i, case in enumerate(test_cases):
        st_board = case["start"]
        goal_board = case["goal"]
    
        for name, solver in algorithms.items():
            steps, states, elapsed_ms, peak_kb = benchmark_single_run(solver, st_board, goal_board)
            stats[name]["steps"] += steps
            stats[name]["states"] += states
            stats[name]["time_ms"] += elapsed_ms
            stats[name]["mem_kb"] += peak_kb

        if (i + 1) % 10 == 0:
            print(f"Đã hoàn thành {i + 1}/{NUM_TRIALS} test...")

    md_table = generate_markdown_table(stats, NUM_TRIALS)
    print("\n" + md_table)

    with open("benchmark_table.md", "w", encoding="utf-8") as f:
        f.write(md_table)


if __name__ == "__main__":
    main()