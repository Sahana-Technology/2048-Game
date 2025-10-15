import tkinter as tk
import random

# -------------------------------
# Game Logic (Functional Part)
# -------------------------------
class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.reset()

    def reset(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_tiles = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.board[r][c] = random.choice([2, 4])

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return self.compress(row)

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            if merged != row:
                moved = True
            new_board.append(merged)
        self.board = new_board
        if moved:
            self.add_new_tile()
        return moved

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        moved = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return moved

    def move_up(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_left()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def move_down(self):
        self.board = [list(row) for row in zip(*self.board[::-1])]
        moved = self.move_left()
        self.board = [list(row) for row in zip(*self.board)][::-1]
        return moved

    def can_move(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return True
                if r < self.size - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return True
                if c < self.size - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return True
        return False

    def is_win(self):
        return any(2048 in row for row in self.board)


# -------------------------------
# GUI Part
# -------------------------------
class Game2048GUI:
    def __init__(self, master, size=4):
        self.master = master
        self.master.title("2048 Game")
        self.size = size
        self.game = Game2048(size)

        self.grid_cells = []
        self.cell_colors = {
            0: "#ccc0b3", 2: "#eee4da", 4: "#ede0c8",
            8: "#f2b179", 16: "#f59563", 32: "#f67c5f",
            64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }

        self.setup_ui()
        self.update_grid()

        self.master.bind("<Key>", self.key_press)

    def setup_ui(self):
        frame = tk.Frame(self.master, bg="#bbada0", bd=5)
        frame.grid()

        for r in range(self.size):
            row = []
            for c in range(self.size):
                cell = tk.Label(frame, text="", width=6, height=3, font=("Helvetica", 24, "bold"),
                                bg="#ccc0b3", fg="#776e65", borderwidth=2, relief="ridge")
                cell.grid(row=r, column=c, padx=5, pady=5)
                row.append(cell)
            self.grid_cells.append(row)

        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 16, "bold"))
        self.score_label.grid(pady=10)

        restart_button = tk.Button(self.master, text="Restart Game", command=self.restart_game,
                                   font=("Helvetica", 14, "bold"), bg="#8f7a66", fg="white")
        restart_button.grid(pady=10)

    def update_grid(self):
        for r in range(self.size):
            for c in range(self.size):
                value = self.game.board[r][c]
                color = self.cell_colors.get(value, "#3c3a32")
                text = str(value) if value != 0 else ""
                self.grid_cells[r][c].config(text=text, bg=color)
        self.score_label.config(text=f"Score: {self.game.score}")

    def key_press(self, event):
        key = event.keysym
        moved = False
        if key in ("Up", "w", "W"):
            moved = self.game.move_up()
        elif key in ("Down", "s", "S"):
            moved = self.game.move_down()
        elif key in ("Left", "a", "A"):
            moved = self.game.move_left()
        elif key in ("Right", "d", "D"):
            moved = self.game.move_right()

        
        

        if moved:
            self.update_grid()
            if self.game.is_win():
                self.show_message("Congratulations! You reached 2048!")
            elif not self.game.can_move():
                self.show_message("Game Over! No more moves.")

    def show_message(self, message):
        popup = tk.Toplevel()
        popup.title("Game Message")
        tk.Label(popup, text=message, font=("Helvetica", 14, "bold")).pack(padx=20, pady=20)
        tk.Button(popup, text="OK", command=popup.destroy, font=("Helvetica", 12)).pack(pady=10)

    def restart_game(self):
        self.game.reset()
        self.update_grid()


# -------------------------------
# Run the Game
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game_gui = Game2048GUI(root)
    root.mainloop()