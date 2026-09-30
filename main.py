import os
import json
import tkinter as tk
from killer_sudoku import KillerSudoku
from solver import solve_killer_sudoku
def create_sample_puzzle():
    data = {
        "cages": [
            {"sum": 3, "cells": [[0,0], [0,1]]},
            {"sum": 7, "cells": [[0,2], [0,3]]},
            {"sum": 11, "cells": [[0,4], [0,5]]},
            {"sum": 15, "cells": [[0,6], [0,7]]},
            {"sum": 18, "cells": [[0,8], [1,8], [2,8]]},
            {"sum": 9, "cells": [[1,0], [1,1]]},
            {"sum": 13, "cells": [[1,2], [1,3]]},
            {"sum": 17, "cells": [[1,4], [1,5]]},
            {"sum": 3, "cells": [[1,6], [1,7]]},
            {"sum": 15, "cells": [[2,0], [2,1]]},
            {"sum": 10, "cells": [[2,2], [2,3]]},
            {"sum": 5, "cells": [[2,4], [2,5]]},
            {"sum": 9, "cells": [[2,6], [2,7]]}
        ]
    }
    with open("puzzle.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
class SudokuGUI:
    def __init__(self, root, sudoku):
        self.root = root
        self.sudoku = sudoku
        self.cells = {}
        self.create_grid()
        self.create_interface()
    def create_grid(self):
        colors = ["#FFDDC1", "#FFABAB", "#FFC3A0", "#D5AAFF", "#85E3FF", "#B9FFB0", "#F6A6FF", "#FFFFD1", "#E2F0CB"]
        cage_colors = {}
        for i, cage in enumerate(self.sudoku.cages):
            for r, c in cage['cells']:
                cage_colors[(r, c)] = colors[i % len(colors)]   
        grid_frame = tk.Frame(self.root, bd=2, relief="solid")
        grid_frame.pack(padx=20, pady=20)
        for r in range(9):
            for c in range(9):
                color = cage_colors.get((r, c), "white")
                pady = (3, 0) if r % 3 == 0 else (1, 0)
                padx = (3, 0) if c % 3 == 0 else (1, 0)
                frame = tk.Frame(grid_frame, width=50, height=50, bg=color, highlightbackground="black", highlightthickness=1)
                frame.grid(row=r, column=c, padx=padx, pady=pady)
                frame.pack_propagate(False)
                label = tk.Label(frame, text="", bg=color, font=("Arial", 18, "bold"))
                label.pack(expand=True, fill="both")
                self.cells[(r, c)] = label
                for cage in self.sudoku.cages:
                    if cage['cells'][0] == (r, c) or cage['cells'][0] == [r, c]:
                        sum_label = tk.Label(frame, text=str(cage['sum']), bg=color, font=("Arial", 8), fg="#333333")
                        sum_label.place(x=2, y=2)
    def create_interface(self):
        btn = tk.Button(self.root, text="solve", command=self.solve, font=("Times New Roman", 14), bg="#4CAF50", fg="white")
        btn.pack(pady=10)
        self.stats_label = tk.Label(self.root, text="nodes explored: 0", font=("Times New Roman", 12))
        self.stats_label.pack(pady=5)
    def solve(self):
        if solve_killer_sudoku(self.sudoku):
            self.update_grid()
            self.stats_label.config(text=f"solved successfully, nodes explored: {self.sudoku.nodes_explored}", fg="green")
        else:
            self.stats_label.config(text="can't solve", fg="red")
    def update_grid(self):
        for r in range(9):
            for c in range(9):
                val = self.sudoku.board[r][c]
                if val != 0:
                    self.cells[(r, c)].config(text=str(val))
def main():
    if not os.path.exists("puzzle.json"):
        create_sample_puzzle()
    sudoku = KillerSudoku.from_json("puzzle.json")
    root = tk.Tk()
    root.title("killer sudoku solver")
    root.geometry("550x650")
    app = SudokuGUI(root, sudoku)
    root.mainloop()
if __name__ == "__main__":
    main()