import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

version = "1.0"

class PackerApp:

    def __init__(self, master):
        # container to hold setup screen
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.setup_screen = ttk.Frame(self.container)
        self.tab_selector = ttk.Notebook(self.setup_screen)
        self.tab_selector.pack(fill = "both")
        self.tab_game = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_game, text = " Game ")
        self.tab_paintjob = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_paintjob, text = " Paintjobs ")
        self.tab_cabins = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_cabins, text = " Cabin Handling ")

        self.image_ats = tk.PhotoImage(file = "library/packer images/ats.gif")
        self.image_ets = tk.PhotoImage(file = "library/packer images/ets.gif")
        self.image_single_paintjob = tk.PhotoImage(file = "library/packer images/single paintjob.gif")
        self.image_paintjob_pack = tk.PhotoImage(file = "library/packer images/paintjob pack.gif")
        self.image_separate_cabins = tk.PhotoImage(file = "library/packer images/separate cabins.gif")
        self.image_combined_cabins = tk.PhotoImage(file = "library/packer images/combined cabins.gif")

        self.tab_game_title = ttk.Label(self.tab_game, text = "Which game are you making a mod for?")
        self.tab_game_title.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        self.tab_game_image_ats = ttk.Label(self.tab_game, image = self.image_ats)
        self.tab_game_image_ats.grid(row = 1, column = 0, padx = 10)
        self.tab_game_image_ets = ttk.Label(self.tab_game, image = self.image_ets)
        self.tab_game_image_ets.grid(row = 1, column = 1, padx = 10)
        self.tab_game_variable = tk.StringVar(None, "ats")
        self.tab_game_option_ats = ttk.Radiobutton(self.tab_game, text = "American Truck Simulator", value = "ats", variable = self.tab_game_variable)
        self.tab_game_option_ats.grid(row = 2, column = 0, pady = 10)
        self.tab_game_image_ats.bind("<1>", lambda e: self.tab_game_variable.set("ats"))
        self.tab_game_option_ets = ttk.Radiobutton(self.tab_game, text = "Euro Truck Simulator 2", value = "ets", variable = self.tab_game_variable)
        self.tab_game_option_ets.grid(row = 2, column = 1, pady = 10)
        self.tab_game_image_ets.bind("<1>", lambda e: self.tab_game_variable.set("ets"))
        self.tab_game_dummy_desc = ttk.Label(self.tab_game, text = "  \n") # to space things out evenly
        self.tab_game_dummy_desc.grid(row = 3, column = 0)
        self.tab_game_button_next = ttk.Button(self.tab_game, text = "Next >", command = lambda : self.tab_selector.select(1))
        self.tab_game_button_next.grid(row = 4, column = 1, sticky = "se", pady = 10, padx = 10)

        self.tab_paintjob_title = ttk.Label(self.tab_paintjob, text = "How many paintjobs are you making?")
        self.tab_paintjob_title.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        self.tab_paintjob_image_single = ttk.Label(self.tab_paintjob, image = self.image_single_paintjob)
        self.tab_paintjob_image_single.grid(row = 1, column = 0, padx = 10)
        self.tab_paintjob_image_pack = ttk.Label(self.tab_paintjob, image = self.image_paintjob_pack)
        self.tab_paintjob_image_pack.grid(row = 1, column = 1, padx = 10)
        self.tab_paintjob_variable = tk.StringVar(None, "pack")
        self.tab_paintjob_option_single = ttk.Radiobutton(self.tab_paintjob, text = "Single paintjob", value = "single", variable = self.tab_paintjob_variable)
        self.tab_paintjob_option_single.grid(row = 2, column = 0, pady = 10)
        self.tab_paintjob_image_single.bind("<1>", lambda e: self.tab_paintjob_variable.set("single"))
        self.tab_paintjob_option_pack = ttk.Radiobutton(self.tab_paintjob, text = "Paintjob pack", value = "pack", variable = self.tab_paintjob_variable)
        self.tab_paintjob_option_pack.grid(row = 2, column = 1, pady = 10)
        self.tab_paintjob_image_pack.bind("<1>", lambda e: self.tab_paintjob_variable.set("pack"))
        self.tab_paintjob_desc_single = ttk.Label(self.tab_paintjob, text = "A single paintjob for a single vehicle\n", wraplength = 300)
        self.tab_paintjob_desc_single.grid(row = 3, column = 0, padx = 10, sticky = "n")
        self.tab_paintjob_desc_pack = ttk.Label(self.tab_paintjob, text = "One paintjob that supports multiple vehicles", wraplength = 300)
        self.tab_paintjob_desc_pack.grid(row = 3, column = 1, padx = 10, sticky = "n")
        self.tab_paintjob_button_prev = ttk.Button(self.tab_paintjob, text = "< Prev", command = lambda : self.tab_selector.select(0))
        self.tab_paintjob_button_prev.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "w")
        self.tab_paintjob_button_next = ttk.Button(self.tab_paintjob, text = "Next >", command = lambda : self.tab_selector.select(2))
        self.tab_paintjob_button_next.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = "e")

        self.tab_cabins_title = ttk.Label(self.tab_cabins, text = "How should separate cabins be handled?")
        self.tab_cabins_title.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        self.tab_cabins_image_combined = ttk.Label(self.tab_cabins, image = self.image_combined_cabins)
        self.tab_cabins_image_combined.grid(row = 1, column = 0, padx = 10)
        self.tab_cabins_image_separate = ttk.Label(self.tab_cabins, image = self.image_separate_cabins)
        self.tab_cabins_image_separate.grid(row = 1, column = 1, padx = 10)
        self.tab_cabins_variable = tk.StringVar(None, "combined")
        self.tab_cabins_option_combined = ttk.Radiobutton(self.tab_cabins, text = "One paintjob per vehicle", value = "combined", variable = self.tab_cabins_variable)
        self.tab_cabins_option_combined.grid(row = 2, column = 0, pady = 10)
        self.tab_cabins_image_combined.bind("<1>", lambda e: self.tab_cabins_variable.set("combined"))
        self.tab_cabins_option_separate = ttk.Radiobutton(self.tab_cabins, text = "Separate paintjobs for each cabin", value = "separate", variable = self.tab_cabins_variable)
        self.tab_cabins_option_separate.grid(row = 2, column = 1, pady = 10)
        self.tab_cabins_image_separate.bind("<1>", lambda e: self.tab_cabins_variable.set("separate"))
        self.tab_cabins_desc_combined = ttk.Label(self.tab_cabins, text = "Simpler to make, but may result in wonky\npaintjobs on differently-sized cabins", justify = "center")
        self.tab_cabins_desc_combined.grid(row = 3, column = 0, padx = 10, sticky = "n")
        self.tab_cabins_desc_separate = ttk.Label(self.tab_cabins, text = "Lets you customise your paintjob for each\ncabin, but is more complex to make", justify = "center")
        self.tab_cabins_desc_separate.grid(row = 3, column = 1, padx = 10, sticky = "n")
        self.tab_cabins_button_prev = ttk.Button(self.tab_cabins, text = "< Prev", command = lambda : self.tab_selector.select(1))
        self.tab_cabins_button_prev.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "w")
        self.tab_cabins_button_next = ttk.Button(self.tab_cabins, text = "Continue", command = lambda : self.switch_to_main_screen())
        self.tab_cabins_button_next.grid(row = 4, column = 1, padx = 10, pady = 10, stick = "e")

        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.main_screen = ttk.Frame(self.container)

    def switch_to_setup_screen(self):
        self.main_screen.grid_forget()
        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

    def switch_to_main_screen(self):
        self.setup_screen.grid_forget()
        self.main_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

def main():
    root = tk.Tk()
    root.title("Paintjob Packer v{}".format(version))
    root.iconphoto(True, tk.PhotoImage(file = "library/packer images/icon.png"))
    root.resizable(False, False)
    packer = PackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
