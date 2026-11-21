import json
import random

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

def save_test_cases(filename: str = "test_cases.json", num_trials: int = 100, seed: int = 42):
    random.seed(seed)
    cases = []

    for i in range(num_trials):
        st_board = create_board()
        while True:
            goal_board = create_board()
            if get_board_parity(st_board) == get_board_parity(goal_board) and st_board != goal_board:
                break
        cases.append({
            "id": i + 1,
            "start": st_board,
            "goal": goal_board
        })

    data = {
        "seed": seed,
        "num_trials": num_trials,
        "cases": cases
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Đã lưu {num_trials} bộ test vào {filename}")

def main():
    save_test_cases("test_cases.json", num_trials=100, seed=42)

if (__name__ == "__main__"):
    main()