import tkinter as tk
from tkinter import messagebox
import time
import random
from PIL import Image, ImageTk


# --- Constants and global variables ---

board_size = 8                 # Size of chessboard (8x8)
cell_size = 60                 # Pixel size for each cell
count = 0                      # Move counter (not used globally here)

# Initialize empty 8x8 chessboard grid (all cells empty)
board = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]

# Possible knight moves as (row_change, col_change)
moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),(-2, -1), (-1, -2), (1, -2), (2, -1)]

# Globals for the program state
start_pos = None               # Starting position of knight (row, col)
lookahead_mode = 1             # Lookahead mode: 1-step or 2-step
move_delay = 150               # Delay between moves in milliseconds
buttons = {}                   # Dictionary to hold buttons keyed by (row, col)
stop_tour = False              # Flag to stop knight's tour recursion if needed
knight_labels = {}             # Dictionary to hold knight image labels keyed by (row, col)
backtrack_count = 0            # Tracks how many times we backtrack
max_backtracks = 10            # Set an upper limit (tune this value as needed)


# --- GUI setup ---

# Create main tkinter window and configure appearance
t = tk.Tk()
t.title("Knight's Tour")
t.configure(bg="lavender")

# Load knight PNG image and resize it to fit cell size
knight_img_pil = Image.open("knight.png").resize((cell_size, cell_size), Image.Resampling.LANCZOS)
knight_img = ImageTk.PhotoImage(knight_img_pil)


# --- Helper functions ---

def get_color(row, col):
    """
    Return cell background color based on position to create checkerboard pattern.
    """
    return "plum" if (row + col) % 2 == 0 else "plum1"

def changeVal(btn, row, col):
    """
    Handle click on a cell button: set starting position and reset board.
    """
    global start_pos
    start_pos = (row, col)
    reset_board()
    board[row][col] = 0
    update_buttons()

def update_buttons():
    """
    Update button text and background color for all cells based on board state.
    Also remove any knight image label currently displayed.
    """
    for row in range(board_size):
        for col in range(board_size):
            btn = buttons[(row, col)]
            val = board[row][col]
            btn.config(text=str(val) if val != ' ' else "", bg=get_color(row, col))
            # Clear knight label if it exists on this cell
            lbl = knight_labels.get((row, col))
            if lbl:
                lbl.place_forget()

def reset_board():
    """
    Reset the board to initial empty state and update buttons accordingly.
    """
    global board
    board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]
    update_buttons()

def get_possible_moves(x, y):
    """
    Return a list of valid next moves for the knight from position (x, y).
    Only moves inside the board and to empty cells are allowed.
    """
    valid = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < board_size and 0 <= ny < board_size and board[nx][ny] == ' ':
            valid.append((nx, ny))
    return valid

def onward_moves(x, y):
    """
    Return the number of onward moves from position (x, y).
    """
    return len(get_possible_moves(x, y))

def two_step_score(x, y):
    """
    Compute the sum of onward moves from all possible next moves.
    Used for 2-step lookahead heuristic.
    """
    return sum(onward_moves(nx, ny) for nx, ny in get_possible_moves(x, y))

def place_knight(x, y):
    """
    Display the knight image on the board cell at position (x, y).
    If label already exists, move it; else create a new one.
    """
    if (x, y) not in knight_labels:
        lbl = tk.Label(t, image=knight_img, bg=get_color(x, y))
        knight_labels[(x, y)] = lbl
    else:
        lbl = knight_labels[(x, y)]
    btn = buttons[(x, y)]
    lbl.place(in_=btn, relx=0, rely=0)

def solve_and_animate(x, y, count, lookahead):
    """
    Recursive function to solve knight's tour and animate moves.
    Marks current position, updates GUI, places knight image,
    tries next moves sorted by lookahead heuristic,
    and backtracks if needed.
    """
    global backtrack_count

    if backtrack_count > max_backtracks:
        return False  # Stop recursion if too many backtracks

    board[x][y] = count
    update_buttons()
    place_knight(x, y)

    test_info_label.config(text=f"Start: {start_pos} - Moves: {count + 1}")
    t.update()
    time.sleep(move_delay / 1000)

    if count == board_size * board_size - 1:
        test_info_label.config(text=f"Start: {start_pos} - Moves: {count + 1} ✅ Tour Completed")
        messagebox.showinfo("Tour Success", "The knight's tour has been successfully completed!")
        return True

    next_moves = get_possible_moves(x, y)
    random.shuffle(next_moves)

    if lookahead == 1:
        next_moves.sort(key=lambda move: onward_moves(move[0], move[1]))
    elif lookahead == 2:
        next_moves.sort(key=lambda move: two_step_score(move[0], move[1]))

    for nx, ny in next_moves:
        if solve_and_animate(nx, ny, count + 1, lookahead):
            return True

    # Backtracking
    board[x][y] = ' '
    update_buttons()
    if (x, y) in knight_labels:
        knight_labels[(x, y)].place_forget()
    t.update()
    time.sleep(move_delay / 1000)

    backtrack_count += 1  # Increment backtracking attempts
    return False


def run_tour(mode):
    """
    Start knight's tour animation with given lookahead mode (1 or 2 step).
    Shows error if no starting position is selected.
    """
    global lookahead_mode, backtrack_count
    lookahead_mode = mode
    backtrack_count = 0  # Reset counter before each tour

    if start_pos is None:
        messagebox.showinfo("Select Start", "Please click a starting square on the board.")
        return
    reset_board()
    x, y = start_pos
    board[x][y] = 0
    update_buttons()

    def run():
        success = solve_and_animate(x, y, 0, lookahead_mode)
        if not success:
            if backtrack_count > max_backtracks:
                messagebox.showinfo("Tour Failed", "Backtracking limit reached. Knight's tour could not be completed.")
            else:
                messagebox.showinfo("Tour Failed", "The knight's tour could not be completed from this position.")

    t.after(200, run)

def Quit():
    """
    Close the main application window.
    """
    t.destroy()


# --- UI Layout ---

# Instruction label
label = tk.Label(t, text="Click a square to choose starting position", bg="thistle", font=("COMIC SANS MS", 10, "bold"))
label.grid(row=0, column=0, columnspan=8, pady=10)

# Buttons for lookahead mode selection
btn1 = tk.Button(t, text="1-Step Lookahead", command=lambda: run_tour(1), font=("COMIC SANS MS", 10, "bold"))
btn1.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

btn2 = tk.Button(t, text="2-Step Lookahead", command=lambda: run_tour(2), font=("COMIC SANS MS", 10, "bold"))
btn2.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

# Reset and Quit buttons
reset_btn = tk.Button(t, text="Reset", command=reset_board, font=("COMIC SANS MS", 10, "bold"))
reset_btn.grid(row=1, column=4, columnspan=2, padx=5, pady=5)

exit_btn = tk.Button(t, text="Quit", command=Quit, font=("COMIC SANS MS", 10, "bold"))
exit_btn.grid(row=1, column=6, columnspan=2, padx=5, pady=5)

#Test Info label
test_info_label = tk.Label(t, text="Test info will appear here", bg="thistle", font=("COMIC SANS MS", 10, "bold"))
test_info_label.grid(row=10, column=0, columnspan=8, pady=10)


# Create 8x8 grid of buttons representing chessboard cells
for row in range(board_size):
    for col in range(board_size):
        btn = tk.Button(
            t, text="", height=2, width=6,
            bg=get_color(row, col),
            fg="dark violet", font="Times 15 bold",
            command=lambda r=row, c=col: changeVal(buttons[(r, c)], r, c)
        )
        btn.grid(row=row + 2, column=col, padx=1, pady=1)
        buttons[(row, col)] = btn

# Start the tkinter main event loop
t.mainloop()
