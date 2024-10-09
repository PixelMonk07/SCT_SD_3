import tkinter as tk
from tkinter import messagebox

# Sudoku Solver using Backtracking Algorithm
class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        # Add a label to display Sudoku rules
        self.rules_label = tk.Label(
            self.root,
            text=("Sudoku Rules: \n"
                  "1. Each row must contain the numbers 1-9 without repetition.\n"
                  "2. Each column must contain the numbers 1-9 without repetition.\n"
                  "3. Each 3x3 subgrid must contain the numbers 1-9 without repetition.\n"
                  "4. Use blank cells to represent empty spaces."),
            font=("Arial", 12),
            justify="left"
        )
        self.rules_label.grid(row=0, column=0, columnspan=9, padx=5, pady=5)

        # Create a 9x9 grid of Entry widgets
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        # Solve Button
        solve_button = tk.Button(self.root, text="Solve", command=self.validate_and_solve)
        solve_button.grid(row=11, column=4, columnspan=1)

        # Clear Button
        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        clear_button.grid(row=11, column=5, columnspan=1)

    def create_grid(self):
        # Create entry widgets in a 9x9 grid
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=3, font=("Arial", 18), justify="center")
                entry.grid(row=row+1, column=col, padx=5, pady=5)  # Adjusted row index to accommodate rules
                self.entries[row][col] = entry

    def get_grid(self):
        # Retrieve the current grid values from the entry widgets
        grid = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val == '':
                    current_row.append(0)
                else:
                    current_row.append(int(val))
            grid.append(current_row)
        return grid

    def is_valid(self, grid, row, col, num):
        # Check if num is not in the current row
        for i in range(9):
            if grid[row][i] == num:
                return False

        # Check if num is not in the current column
        for i in range(9):
            if grid[i][col] == num:
                return False

        # Check if num is not in the current 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False

        return True

    def solve_sudoku(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:  # Find an empty cell
                    for num in range(1, 10):  # Try numbers 1 to 9
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num  # Place the number
                            if self.solve_sudoku(grid):  # Recur to solve next cells
                                return True
                            grid[row][col] = 0  # Backtrack if no solution found
                    return False  # No valid number found, so return False
        return True  # Puzzle solved

    def solve(self):
        # Get the grid from the GUI
        grid = self.get_grid()

        # Solve the Sudoku puzzle
        if self.solve_sudoku(grid):
            self.update_grid(grid)
        else:
            messagebox.showinfo("Error", "No solution exists")

    def update_grid(self, grid):
        # Update the entry widgets with the solved values
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                # Show blank for empty cells (0) and numbers for filled cells
                if grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(grid[row][col]))

    def clear_grid(self):
        # Clear all the entry widgets
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def validate_and_solve(self):
        # Validate the grid before solving
        grid = self.get_grid()

        # Check for validity and identify the invalid number if present
        validity_result = self.is_valid_grid(grid)

        if validity_result is not True:
            # Show the detailed error message based on the validity result
            invalid_type, index, num = validity_result
            if invalid_type == "row":
                messagebox.showinfo("Error", f"Duplicate number {num} found in row {index + 1}")
            elif invalid_type == "column":
                messagebox.showinfo("Error", f"Duplicate number {num} found in column {index + 1}")
            elif invalid_type == "subgrid":
                messagebox.showinfo("Error", f"Duplicate number {num} found in 3x3 subgrid starting at ({(index // 3) * 3 + 1}, {(index % 3) * 3 + 1})")
            return

        # If valid, proceed to solve the Sudoku
        self.solve()

    def is_valid_grid(self, grid):
        # Check for duplicates in rows, columns, and 3x3 subgrids
        for row in range(9):
            result = self.is_valid_list([grid[row][col] for col in range(9)])
            if result is not True:
                return ("row", row, result)

        for col in range(9):
            result = self.is_valid_list([grid[row][col] for row in range(9)])
            if result is not True:
                return ("column", col, result)

        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                result = self.is_valid_list([grid[row][col]
                                             for row in range(block_row, block_row + 3)
                                             for col in range(block_col, block_col + 3)])
                if result is not True:
                    return ("subgrid", (block_row // 3) * 3 + (block_col // 3), result)
        return True

    def is_valid_list(self, lst):
        # Helper method to check if a list has duplicate numbers (ignores zeros)
        nums = [num for num in lst if num != 0]
        num_set = set()
        for num in nums:
            if num in num_set:
                return num  # Return the duplicate number
            num_set.add(num)
        return True  # No duplicates

# Main function to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    solver = SudokuSolver(root)
    root.mainloop()