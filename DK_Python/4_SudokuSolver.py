def solve_sudoku(board):
    # Repeatedly apply deterministic strategies; if stuck, use backtracking
    while True:
        changed = deterministic_pass(board)
        if not changed:
            break

    if is_solved(board):
        return True

    # Fallback to backtracking when deterministic strategies cannot finish
    return backtrack_solve(board)


def compute_candidates(board):
    """Return dict mapping (r,c) -> set of possible values for empty cells."""
    candidates = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                used = set()
                # row
                used.update(x for x in board[r] if x != 0)
                # column
                used.update(board[i][c] for i in range(9) if board[i][c] != 0)
                # box
                br = (r // 3) * 3
                bc = (c // 3) * 3
                for i in range(br, br + 3):
                    for j in range(bc, bc + 3):
                        if board[i][j] != 0:
                            used.add(board[i][j])
                candidates[(r, c)] = set(range(1, 10)) - used
    return candidates


def deterministic_pass(board):
    """Apply deterministic strategies until no more cells are filled.

    Strategies:
    - Naked single: cell with single candidate
    - Hidden single: in any unit (row/col/box) a digit appears in candidates of only one cell
    Returns True if any cell was filled.
    """
    changed_any = False
    while True:
        changed = False
        candidates = compute_candidates(board)

        # Naked singles
        for (r, c), opts in list(candidates.items()):
            if len(opts) == 1:
                board[r][c] = next(iter(opts))
                changed = True

        if changed:
            changed_any = True
            continue

        # Hidden singles in rows
        for r in range(9):
            # collect candidates for empty cells in row
            row_cells = [(r, c) for c in range(9) if board[r][c] == 0]
            for d in range(1, 10):
                places = [pos for pos in row_cells if d in candidates.get(pos, set())]
                if len(places) == 1:
                    pr, pc = places[0]
                    board[pr][pc] = d
                    changed = True

        if changed:
            changed_any = True
            continue

        # Hidden singles in columns
        for c in range(9):
            col_cells = [(r, c) for r in range(9) if board[r][c] == 0]
            for d in range(1, 10):
                places = [pos for pos in col_cells if d in candidates.get(pos, set())]
                if len(places) == 1:
                    pr, pc = places[0]
                    board[pr][pc] = d
                    changed = True

        if changed:
            changed_any = True
            continue

        # Hidden singles in boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box_cells = [(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3) if board[r][c] == 0]
                for d in range(1, 10):
                    places = [pos for pos in box_cells if d in candidates.get(pos, set())]
                    if len(places) == 1:
                        pr, pc = places[0]
                        board[pr][pc] = d
                        changed = True

        if not changed:
            break
        changed_any = True

    return changed_any


def is_solved(board):
    return all(board[r][c] != 0 for r in range(9) for c in range(9))


def find_best_cell(candidates):
    # choose empty cell with fewest candidates
    if not candidates:
        return None
    return min(candidates.items(), key=lambda item: len(item[1]))[0]


def backtrack_solve(board):
    """Backtracking solver: uses candidates to pick best branch."""
    if is_solved(board):
        return True

    candidates = compute_candidates(board)
    if not candidates:
        return False

    cell = find_best_cell(candidates)
    if cell is None:
        return False
    r, c = cell
    opts = sorted(candidates[cell])
    for val in opts:
        # try value on a copy
        new_board = [row[:] for row in board]
        new_board[r][c] = val
        # apply deterministic strategies first on the branch
        deterministic_pass(new_board)
        if backtrack_solve(new_board):
            # copy solution back
            for i in range(9):
                board[i][:] = new_board[i][:]
            return True

    return False


# Example usage:
if __name__ == '__main__':
    board_string = '''009000865012050004300004000405700090000400000000506700100207000860090002000000000'''
    sudoku_board = [ [0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        sudoku_board[i] = [int(board_string[i * 9 + j]) for j in range(9)]
    solve_sudoku(sudoku_board)
    print(sudoku_board)