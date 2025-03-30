import tkinter as tk
import random
from tkinter import messagebox
import pygame

pygame.mixer.init()  # Initialize the sound mixer

# Load sounds for the game
click_sound = pygame.mixer.Sound('flag.mp3')
win_sound = pygame.mixer.Sound('win.mp3')
mine_sound = pygame.mixer.Sound('lose.mp3')

# Global variable to track which button is being hovered over
hovered_button = None

# Global variables for grid size and number of mines
ROWS = 20
COLS = 20
TOTAL_MINES = 50

# Initialize a global variable to track the number of revealed cells
revealed_cells = 0  # This will count how many non-mine cells have been revealed

# Function to create a grid of buttons
def create_button_grid(root, rows, cols):
    global mines
    mines = set()

    # Randomly assign mine positions
    mine_positions = random.sample(range(rows * cols), TOTAL_MINES)
    mines = set(mine_positions)

    for row in range(rows):
        for col in range(cols):
            # Create a button and bind it to the on_button_click function
            btn = tk.Button(root, text=" ", width=10, height=5, bg="lightpink", fg="black", command=lambda r=row, c=col: on_button_click(root, r, c))
            btn.grid(row=row, column=col, sticky="nsew")

             # Bind the button to mouse enter and leave events, and the spacebar press
            btn.bind("<Enter>", lambda event, r=row, c=col: on_hover(event, r, c))
            btn.bind("<Leave>", on_leave)
            btn.bind_all("<space>", flag_button)  # Bind space key to the entire window


    # Make rows and columns resizable
    for i in range(rows):
        root.rowconfigure(i, weight=1)
    for j in range(cols):
        root.columnconfigure(j, weight=1)

# Function to handle hovering over a button
def on_hover(event, row, col):
    global hovered_button
    hovered_button = (row, col)  # Store the currently hovered button's position

def on_leave(event):
    global hovered_button
    hovered_button = None  # Reset when leaving the button

# Function to flag the button when spacebar is pressed
def flag_button(event):
    if hovered_button:
        row, col = hovered_button
        btn = root.grid_slaves(row=row, column=col)[0]

        # Toggle flagging: if already flagged, remove the flag
        if btn["text"] == "🚩":
            btn.config(text=" ", bg="lightpink", state="normal")  # Remove flag
        else:
            btn.config(text="🚩", bg="lightblue", state="disabled")  # Set flag

# Function to handle button clicks
def on_button_click(root, row, col):
    click_sound.play()  # Play click sound
    button_index = row * COLS + col

    if button_index in mines:
        reveal_mines(root)
        mine_sound.play()  # Play when game over occurs
        messagebox.showerror("Game Over", "You Clicked On A Mine :( Better Luck Next Time :P")
        new_file()
    else:
        # Reveal the clicked button
        reveal_cell(root, row, col)
        
        # Check and reveal the 8 neighboring cells
        for r in range(max(0, row - 1), min(ROWS, row + 2)):  # Loop through rows: row-1 to row+1
            for c in range(max(0, col - 1), min(COLS, col + 2)):  # Loop through columns: col-1 to col+1
                if (r != row or c != col) and (r * COLS + c not in mines):  # Skip the current cell and skip mines
                    reveal_cell(root, r, c)
                   

# Function to check if the player has won
# def check_win():
#    total_cells = ROWS * COLS
#    total_non_mine_cells = total_cells - len(mines)  # Total cells minus the number of mines
#    return revealed_cells == total_non_mine_cells  # Player wins if all non-mine cells are revealed

# Function to reveal a cell and disable the button
def reveal_cell(root, row, col):
    global revealed_cells
    button_index = row * COLS + col
    
    # Skip if this cell is a mine
    if button_index in mines:
        return

    btn = root.grid_slaves(row=row, column=col)[0]

    # If the button is already disabled, skip
    if btn.cget('state') == 'disabled':
        return

    # Count the surrounding mines for this cell
    surrounding_mines = count_surrounding_mines(row, col)

    # Update the button text and disable it
    btn.config(text=str(surrounding_mines) if surrounding_mines > 0 else "", state="disabled",  bg="white", relief="sunken")
    # Increment the count of revealed cells (since this is not a mine)
    revealed_cells += 1

    # Check if the player has won
    #if check_win():
    #    win_sound.play()  # Play click sound
    #    messagebox.showinfo("You Win!", "Congratulations, You Just Won The Game! You Deserve a Cookie :D")
    #    revealed_cells = 0
    #    new_file()  # Start a new game

    # If no mines surround this cell, recursively reveal neighbors (if desired)
    if surrounding_mines == 0:
        for r in range(max(0, row - 1), min(ROWS, row + 2)):
            for c in range(max(0, col - 1), min(COLS, col + 2)):
                if (r != row or c != col) and (r * COLS + c not in mines):  # Skip current cell and mines
                    reveal_cell(root, r, c)
                    

# Function to count how many mines are surrounding a given cell
def count_surrounding_mines(row, col):
    count = 0
    for r in range(max(0, row - 1), min(ROWS, row + 2)):
        for c in range(max(0, col - 1), min(COLS, col + 2)):
            if r == row and c == col:
                continue  # Skip the current button
            if (r * COLS + c) in mines:
                count += 1
    return count

# Function to reveal all mines when the game is over
def reveal_mines(root):
    for mine in mines:
        row, col = divmod(mine, COLS)
        btn = root.grid_slaves(row=row, column=col)[0]
        btn.config(text="Mine", state="disabled", bg="red")

# Function to handle the "New" menu option
def new_file():
    global root
    root.destroy()  # Close the current window
    root = tk.Tk()  # Create a new window
    root.title("Minesweeper Game")
    root.geometry("500x500")  # Set the new window size
    create_menu(root)
    create_button_grid(root, ROWS, COLS)  # Recreate the grid in the new window
    root.mainloop()

# Function to handle the "Open" menu option
def open_file():
    messagebox.showinfo("Open File", "Opening file...")

# Function to handle the "Exit" menu option
def exit_app():
    root.quit()

# Create the menu bar
def create_menu(root):
    menu_bar = tk.Menu(root)

    # Create the "File" menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_separator()
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create the "Help" menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is a simple minesweeper game which is still under constructor with aims to implement unique features compared to the normal minesweeper.\nClick on the pink boxes carefully and avoid mines to win!\nTo flag a box, press the space bar. Enjoy!"))
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

# Initialize the main window
root = tk.Tk()
root.title("Minesweeper Game")
root.geometry("500x500")

# Create the menu and button grid
create_menu(root)
create_button_grid(root, ROWS, COLS)

# Run the main event loop
root.mainloop()

