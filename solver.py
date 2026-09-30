def find_empty_location_mrv(sudoku):
    min_options = 10
    best_cell = (None, None)
    for row in range(9):
        for col in range(9):
            if sudoku.board[row][col] == 0:
                options = sum(1 for num in range(1, 10) if sudoku.is_safe(row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
                    if options <= 1:
                        return best_cell       
    return best_cell
def solve_killer_sudoku(sudoku):
    row, col = find_empty_location_mrv(sudoku)
    if row is None:
        return True
    for num in range(1, 10):
        sudoku.nodes_explored += 1
        if sudoku.is_safe(row, col, num):
            sudoku.board[row][col] = num
            if solve_killer_sudoku(sudoku):
                return True
            sudoku.board[row][col] = 0
    return False