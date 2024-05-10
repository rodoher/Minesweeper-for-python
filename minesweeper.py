from tkinter import *
from functools import partial
import numpy as np
from tkinter import messagebox
from tkinter import simpledialog


class Minesweeper:

    def __init__(self, level="b", rows=10, columns=10, bombs=10):
        # level: beginner, intermediate, advanced, personalized, according to it you get the number of
        # rows, columns and bombs
        self.level = level
        # indicates the location of the bombs
        self.bombs_location = []
        self.bombs = bombs
        self.rows = rows
        self.columns = columns
        self.total_squares = self.rows*self.columns
        # stores the squares that have already been pressed
        self.pressed = []

    def start_game(self):
        options = ["a", "b", "i", "o"]
        lev = None
        while lev not in options:
            lev = simpledialog.askstring("New Game", "Level: (b=beginner, i=intermediate, a=advanced, "
                                                     "o=personalize) ").lower()
        self.level = lev
        match self.level:
            case "b":
                self.rows = 10
                self.columns = 10
                self.bombs = 10
            case "i":
                self.rows = 20
                self.columns = 20
                self.bombs = 50
            case "a":
                self.rows = 20
                self.columns = 30
                self.bombs = 100
            case "o":
                self.rows = simpledialog.askinteger("New Game", "Number of rows: ")
                if self.rows is None:
                    check_play = messagebox.askyesno("Warning", "You have to introduce this information. "
                                                                "Do you want to exit the game?")
                    if check_play:
                        self.root.destroy()
                    else:
                        self.rows = simpledialog.askinteger("New Game", "Number of rows: ")

                self.columns = simpledialog.askinteger("New Game", "Number of columns: ")
                if self.columns is None:
                    check_play = messagebox.askyesno("Warning", "You have to introduce this information. "
                                                                "Do you want to exit the game?")
                    if check_play:
                        self.root.destroy()
                    else:
                        self.columns = simpledialog.askinteger("New Game", "Number of columns: ")
                self.bombs = simpledialog.askinteger("New Game", "Number of bombs: ")
                if self.bombs is None:
                    check_play = messagebox.askyesno("Warning", "You have to introduce this information."
                                                                " Do you want to exit the game?")
                    if check_play:
                        self.root.destroy()
                    else:
                        self.bombs = simpledialog.askinteger("New Game", "Number of bombs: ")

        self.total_squares = self.rows * self.columns
        self.create_board()

    def create_board(self):
        self.pressed = []
        self.choose_bombs()
        self.root = Tk()
        r = 1
        c = 0
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                Button(self.root, text="", command=partial(self.testbomb, c), width=3, height=1).grid(row=r, column=j)
                c += 1

            r += 1
        self.create_menu()
        self.root.mainloop()

    def create_menu(self):
        menu = Menu(self.root)
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label="New game", command=self.restart_game)
        filemenu.add_command(label="Exit", command=self.root.destroy)
        menu.add_cascade(label="Options", menu=filemenu)
        self.root.config(menu=menu)

    def restart_game(self):
        self.root.destroy()
        self.start_game()

    def testbomb(self, c):
        if c in self.bombs_location:
            buttons = self.root.children
            counter = 0
            for k, v in buttons.items():
                if counter == c:
                    buttons[k]['background'] = "red"
                counter += 1
            self.game_over(c)

        elif c not in self.pressed:

            relevant_locations = np.array([c+1, c-1, c+self.columns, c-self.columns, c+self.columns+1, c-self.columns+1,
                                           c+self.columns-1, c-self.columns-1])

            nums = []
            for i in relevant_locations:
                if 0 <= i < self.total_squares:
                    # c es el valor donde hemos pinchado, i es el lugar que puede ser relevante
                    a = True
                    if c % self.columns == 0:
                        if i % self.columns == self.columns-1:
                            a = False
                    elif c % self.columns == self.columns-1:
                        if i % self.columns == 0:
                            a = False
                    if a:
                        nums.append(i)
            bombs_close = 0
            for i in nums:
                if i in self.bombs_location:
                    bombs_close += 1
            counter = 0
            buttons = self.root.children
            for k, v in buttons.items():
                if counter == c:
                    buttons[k]['text'] = bombs_close
                    buttons[k]['font'] = 'Helvetica 8 bold'
                    if bombs_close == 1:
                        buttons[k]['fg'] = "blue"
                    elif bombs_close == 2:
                        buttons[k]['fg'] = "orange"
                    elif bombs_close == 3:
                        buttons[k]['fg'] = "green"
                    elif bombs_close == 4:
                        buttons[k]['fg'] = "purple"
                    elif bombs_close == 5:
                        buttons[k]['fg'] = "red"
                    elif bombs_close == 6:
                        buttons[k]['fg'] = "brown"
                    elif bombs_close == 7:
                        buttons[k]['fg'] = "yellow"
                    elif bombs_close == 8:
                        buttons[k]['fg'] = "black"
                    elif bombs_close == 0:
                        buttons[k]['bg'] = "black"
                counter += 1
            self.pressed.append(c)
            if bombs_close == 0:
                for i in nums:
                    if i not in self.pressed and (i == c+1 or i == c-1 or i == c+self.columns or i == c-self.columns):
                        self.testbomb(i)
            self.test_win()

    def test_win(self):
        if len(self.pressed)+self.bombs == self.total_squares:
            new_game = messagebox.askyesno("You've won!!", "Congratulations! You've won! Do you want to play again?")
            if new_game:
                self.restart_game()
            else:
                self.root.destroy()

    def game_over(self, c):
        new_game = messagebox.askyesno('Game over', f"the bombs were located in the positions "
                                                    f"{self.bombs_location}, {c} was one of those locations. Do you "
                                                    f"want to play again?")
        if new_game:
            self.restart_game()
        else:
            self.root.destroy()

    def choose_bombs(self):
        pick_bombs = np.arange(0, self.total_squares)
        self.bombs_location = np.random.choice(pick_bombs, self.bombs, replace=False)


ms = Minesweeper()
ms.start_game()
