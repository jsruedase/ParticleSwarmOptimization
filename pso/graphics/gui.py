
"""
This module defines the GUI class, which represents the graphical user interface for the Particle Swarm Optimization (PSO) application, unifying the different menus and functionalities.

## Classes
- GUI: Represents the main graphical user interface for the PSO application.

### Attributes
- __root: tk.Tk - The root window for the GUI.
- _root_frame: tk.Frame - The main frame within the root window.
- __optimization_history: list[Optimization] - A list to store the optimization history.
- _window_height: int - The height of the window.
- _window_width: int - The width of the window.
- __exit_menu: ExitMenu - The exit menu of the application.
- __main_menu: MainMenu - The main menu of the application.
- __select_menu: SelectMenu - The select menu of the application.
- __menus: dict - A dictionary to store the different menus of the application.

### Methods
- _change_menu(menu_name="") -> None: Changes the current menu to the specified menu.
- _initialize_root(width: int, height: int, title: str = "Particle Swarm Optimization (PSO)") -> None: Initializes the root window with the given parameters.
- run() -> None: Runs the main loop of the GUI.
"""
import os

import numpy as np
import tkinter as tk
from tkinter import font

from pso.graphics.colors import Color
from pso.graphics.exitMenu import ExitMenu
from pso.graphics.mainMenu import MainMenu
from pso.graphics.selectMenu import SelectMenu
from pso.optimization import Optimization
from pso.database.data import Data

class GUI:
    __root: tk.Tk = tk.Tk()
    def __init__(self, optimization_history: list[Optimization], program_version: str = "Error") -> None:
        # TODO1: UPDATE THE CLASS DIAGRAM
        # TODO2: Solve the issue described in select menu: after releasing the back button and then clicking and releasing the select button in the main menu the SelectFrame object is not being displayed. Might have something to do with what is being forgotten in the change_menu function (it may need to forget the canvas or something else instead)
        # ? Future versions could include thread management. Could be an interesting way to start learning about parallelism and concurrency.
        self._root_frame: tk.Frame = tk.Frame(GUI.__root, bg=Color.test2_bg)
        self.__optimization_history: list[Optimization] = [Optimization(1, Data("as"), 1, 1), Optimization(2)]
        self._window_height: int = 0
        self._window_width: int = 0
        print(1)
        self.__exit_menu: ExitMenu = ExitMenu(self._root_frame, self._initialize_root)
        print(2)
        self.__main_menu: MainMenu = MainMenu(self._root_frame, self._initialize_root, self._change_menu, program_version)
        print(3)
        self.__select_menu: SelectMenu = SelectMenu(self._root_frame, self._initialize_root, self._change_menu, self.__optimization_history, window_width=750, window_height=500)
        print(4)
        self.__menus: dict = {"exit": self.__exit_menu, "main": self.__main_menu, "select": self.__select_menu}

    def _change_menu(self, menu_name="") -> None:
        if menu_name in self.__menus:
            for menu in self.__menus.values():
                menu.root.forget()
            self.__menus[menu_name].display()
            self.__menus[menu_name].root.tkraise()
        else:
            raise Exception(f"Menu {menu_name} not found.")

    def _initialize_root(self, width: int, height: int, title: str = "Particle Swarm Optimization (PSO)") -> None:
        GUI.__root.title(title)

        # * Setting initial geometry (dimensions)
        GUI.__root.resizable(False, False)
        screen_width: int = GUI.__root.winfo_screenwidth()
        screen_height: int= GUI.__root.winfo_screenheight()
        self.__window_width: int = width
        self.__window_height: int = height
        top_left_x: int = (screen_width // 2) - (self.__window_width // 2)
        top_left_y: int = (screen_height // 2) - (self.__window_height // 2)
        GUI.__root.geometry(f"{self.__window_width}x{self.__window_height}+{top_left_x}+{top_left_y}")
        self._root_frame.place(x=0, y=0, width=width, height=height)

        # * Setting icon for the application switcher, the dock and the taskbar (Windows)
        small_logo_path: str = "assets/ubuntu-logo.png"
        large_logo_path: str = small_logo_path
        small_logo: tk.PhotoImage = tk.PhotoImage(file=small_logo_path).subsample(10)
        large_logo: tk.PhotoImage = tk.PhotoImage(file=large_logo_path)
        GUI.__root.iconphoto(False, small_logo, large_logo)

        # * Setting background color
        GUI.__root.configure(bg=Color.window_bg)

    def run(self):
        self._change_menu("main")
        GUI.__root.mainloop()

if __name__ == "__main__":
    gui = GUI("0.2.0") # * Version can be obtained from Main's method get_version(). Therefore, when GUI is created inside Main, the method will be called as an argument (?).
    gui.run() # ? Should run be the only public method?