import tkinter as tk
from tkinter import messagebox
import random

class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Судоку для няш")
        
        self.board = [[0]*9 for _ in range(9)]
        self.entries = [[None]*9 for _ in range(9)]
        
        self.create_board()
        self.generate_puzzle()

    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                self.entries[i][j] = entry

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        solve_button = tk.Button(button_frame, text="Решить", command=self.solve)
        solve_button.pack(side='left', padx=5)
        check_button = tk.Button(button_frame, text="Проверить", command=self.check_solution)
        check_button.pack(side='left', padx=5)

    def generate_puzzle(self):
        self.board = self.solve_board([[0]*9 for _ in range(9)])
        self.remove_numbers()

    def remove_numbers(self):
        # Удаление случайных чисел для создания пазла
        attempts = 5
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            backup = self.board[row][col]
            self.board[row][col] = 0

            board_copy = [row[:] for row in self.board]
            if not self.solve_board(board_copy):
                self.board[row][col] = backup
                attempts -= 1

        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.board[i][j]))
                    self.entries[i][j].config(state='disabled')

    def solve_board(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num

                if self.solve_board(board):
                    return True

                board[row][col] = 0

        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        self.solve_board(self.board)
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(self.board[i][j]))

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.entries[i][j].get() == '':
                    messagebox.showwarning("Ошибка ня", "Заполните все поля ня!")
                    return
                if not self.is_valid(self.board, int(self.entries[i][j].get()), (i, j)):
                    messagebox.showerror("Ошибка", "Решение неправильное!")
                    return
        messagebox.showinfo("Поздравляем!", "Решение правильное!")

if __name__ == '__main__':
    root = tk.Tk()
    Sudoku(root)
    root.mainloop()
