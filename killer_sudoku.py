import json
class KillerSudoku:
    def __init__(self, cages):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.cages = cages
        self.nodes_explored = 0        
        self.cell_to_cage = {}
        for cage in self.cages:
            for r, c in cage['cells']:
                self.cell_to_cage[(r, c)] = cage   
    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cages = []
        for cage in data.get("cages", []):
            cells = [(cell[0], cell[1]) for cell in cage["cells"]]
            cages.append({'sum': cage['sum'], 'cells': cells})
        return cls(cages)
    def is_safe(self, row, col, num):
        if num in self.board[row]:
            return False
        for r in range(9):
            if self.board[r][col] == num:
                return False      
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False 
        return self._check_cage(row, col, num)
    def _check_cage(self, row, col, num):
        cage = self.cell_to_cage.get((row, col))
        if not cage:
            return True   
        current_sum = num
        empty_cells = 0
        for r, c in cage['cells']:
            if (r, c) != (row, col):
                val = self.board[r][c]
                if val == num:
                    return False 
                if val != 0:
                    current_sum += val
                else:
                    empty_cells += 1
        if current_sum > cage['sum']:
            return False
        if empty_cells == 0 and current_sum != cage['sum']:
            return False
        max_possible_addition = 9 * empty_cells
        if current_sum + max_possible_addition < cage['sum']:
            return False
        return True
    def print_board(self):
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("-" * 21)
            row_print = []
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    row_print.append("|")
                val = self.board[r][c]
                row_print.append(str(val) if val != 0 else ".")
            print(" ".join(row_print))