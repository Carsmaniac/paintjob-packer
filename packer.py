import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

version = "1.0"

class PackerApp:

    def __init__(self, master):
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.setup_screen = ttk.Frame(self.container)
        self.tab_selector = ttk.Notebook(self.setup_screen)
        self.tab_selector.pack(fill = "both")
        self.tab_game = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_game, text = "Game")
        self.tab_paintjob = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_paintjob, text = "Paintjobs")
        self.tab_cabins = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_cabins, text = "Cabin Handling")

        self.image_ats = tk.PhotoImage(file = "library/packer images/ats.gif")
        self.image_ets = tk.PhotoImage(file = "library/packer images/ets.gif")

        self.tab_game_title = ttk.Label(self.tab_game, text = "Which game are you making a mod for?")
        self.tab_game_title.grid(row = 0, column = 0, columnspan = 2, pady = 10)
        self.tab_game_image_ats = ttk.Label(self.tab_game, image = self.image_ats)
        self.tab_game_image_ats.grid(row = 1, column = 0, padx = 10)
        self.tab_game_image_ets = ttk.Label(self.tab_game, image = self.image_ets)
        self.tab_game_image_ets.grid(row = 1, column = 1, padx = 10)
        self.tab_game_variable = tk.StringVar(None, "ats")
        self.tab_game_option_ats = ttk.Radiobutton(self.tab_game, text = "American Truck Simulator", value = "ats", variable = self.tab_game_variable, state = "selected")
        self.tab_game_option_ats.grid(row = 2, column = 0, pady = 10)
        self.tab_game_image_ats.bind("<1>", lambda e: self.tab_game_variable.set("ats"))
        self.tab_game_option_ets = ttk.Radiobutton(self.tab_game, text = "Euro Truck Simulator 2", value = "ets", variable = self.tab_game_variable)
        self.tab_game_option_ets.grid(row = 2, column = 1, pady = 10)
        self.tab_game_image_ets.bind("<1>", lambda e: self.tab_game_variable.set("ets"))
        self.tab_game_button_next = ttk.Button(self.tab_game, text = "Next >", command = lambda : self.change_tab("paintjob"))
        self.tab_game_button_next.grid(row = 3, column = 1, sticky = "e", pady = 10, padx = 10)

        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.main_screen = ttk.Frame(master)

    def change_tab(self, tab):
        if tab == "game":
            self.tab_selector.select(0)
        if tab == "paintjob":
            self.tab_selector.select(1)
        if tab == "cabins":
            self.tab_selector.select(2)

    def switch_to_setup_screen(self):
        self.main_screen.grid_forget()
        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

    def switch_to_main_screen(self):
        self.setup_screen.grid_forget()
        self.main_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

def main():
    root = tk.Tk()
    root.title("Paintjob Packer v{}".format(version))
    # root.geometry("800x600")
    root.iconphoto(True, tk.PhotoImage(file = "library/packer images/icon.png"))
    packer = PackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
