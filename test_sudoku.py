import unittest
from killer_sudoku import KillerSudoku
from solver import solve_killer_sudoku, find_empty_location_mrv
class TestKillerSudoku(unittest.TestCase):
    def setUp(self):
        self.basic_cages = [{'sum': 15, 'cells': [(0, 0), (0, 1)]}]
        self.sudoku = KillerSudoku(self.basic_cages)
    def test_find_empty_location(self):
        row, col = find_empty_location_mrv(self.sudoku)
        self.assertIsNotNone(row, "має знайти порожню клітинку")
        for r in range(9):
            for c in range(9):
                self.sudoku.board[r][c] = 1
        row, col = find_empty_location_mrv(self.sudoku)
        self.assertEqual((row, col), (None, None), "повністю заповнена дошка має повертати None")
    def test_is_safe_classic_rules(self):
        self.sudoku.board[0][8] = 5
        self.assertFalse(self.sudoku.is_safe(0, 0, 5), "порушення унікальності в рядку")
        self.sudoku.board[0][8] = 0
        self.sudoku.board[8][0] = 5
        self.assertFalse(self.sudoku.is_safe(0, 0, 5), "порушення унікальності в стовпці")
        self.sudoku.board[8][0] = 0
        self.sudoku.board[1][1] = 5
        self.assertFalse(self.sudoku.is_safe(0, 0, 5), "порушення унікальності в квадраті 3х3")
    def test_cage_sum_exceeded(self):
        self.sudoku.board[0][0] = 9
        self.assertFalse(self.sudoku.is_safe(0, 1, 7), "сума не може перевищувати цільове значення")
    def test_cage_exact_sum(self):
        self.sudoku.board[0][0] = 9
        self.assertFalse(self.sudoku.is_safe(0, 1, 5), "фінальна сума має збігатися з цільовою")
        self.assertTrue(self.sudoku.is_safe(0, 1, 6), "коректна фінальна сума дозволяється")
    def test_cage_duplicates(self):
        cages = [{'sum': 16, 'cells': [(0, 0), (1, 0)]}]
        sudoku = KillerSudoku(cages)
        sudoku.board[0][0] = 8
        self.assertFalse(sudoku.is_safe(1, 0, 8), "дублікати в межах клітки заборонені")
    def test_full_solver_integration(self):
        cages = [
            {'sum': 15, 'cells': [(0, 0), (0, 1)]},
            {'sum': 14, 'cells': [(0, 2), (1, 2), (2, 2)]},
            {'sum': 8,  'cells': [(0, 3), (0, 4)]}
        ]
        sudoku = KillerSudoku(cages)
        self.assertTrue(solve_killer_sudoku(sudoku), "агент повинен знаходити розв'язок валідної дошки")
        self.assertGreater(sudoku.nodes_explored, 0, "лічильник вузлів має працювати")
if __name__ == '__main__':
    unittest.main()