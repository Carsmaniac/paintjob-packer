import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser, sys, configparser, os, math, re
import library.paintjob as pj

version = "1.0.1"
forum_link = "https://is.gd/CMPackerThread"
github_link = "https://github.com/carsmaniac/paintjob-packer"
mod_link_page_link = "https://github.com/Carsmaniac/paintjob-packer/blob/master/library/mod%20links.md"

# set the path depending on how Paintjob Packer is bundled
try:
    base_path = sys._MEIPASS # packaged into executable
    using_executable = True
except AttributeError:
    base_path = os.path.abspath(".") # loose .py
    using_executable = False
os.chdir(base_path)

output_path = os.path.expanduser("~/Desktop")

class PackerApp:

    def __init__(self, master):
        # container to hold setup/main screen
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.image_packer = tk.PhotoImage(file = "library/packer images/packer.png")
        self.image_ats = tk.PhotoImage(file = "library/packer images/ats.png")
        self.image_ets = tk.PhotoImage(file = "library/packer images/ets.png")
        self.image_single_paintjob = tk.PhotoImage(file = "library/packer images/single paintjob.png")
        self.image_paintjob_pack = tk.PhotoImage(file = "library/packer images/paintjob pack.png")
        self.image_separate_cabins = tk.PhotoImage(file = "library/packer images/separate cabins.png")
        self.image_combined_cabins = tk.PhotoImage(file = "library/packer images/combined cabins.png")
        self.image_spacer_100 = tk.PhotoImage(file = "library/packer images/spacer 100.png")
        self.image_spacer_200 = tk.PhotoImage(file = "library/packer images/spacer 200.png")

        # load appropriate cursor for OS, used when mousing over links
        if sys.platform.startswith("win"):
            self.cursor = "hand2"
        elif sys.platform.startswith("darwin"): # macOS
            self.cursor = "pointinghand"
        elif sys.platform.startswith("linux"):
            self.cursor = "hand2"

        self.seen_unifier_warning = False # controls whether the link to the guide is displayed
        self.total_vehicles = 0 # used in the vehicle selector when making a paintjob pack

        # second window displayed when generating mod, mostly useless as it generates so quickly
        self.loading_window = tk.Toplevel(master)
        self.loading_window.title("Generating Mod")
        self.loading_window.state("withdrawn")
        self.loading_window.resizable(False, False)
        self.loading_label = ttk.Label(self.loading_window, text = "Generating mod, please wait...")
        self.loading_label.grid(row = 0, column = 0, pady = 20)
        self.loading_value = tk.DoubleVar(None, 5.0)
        self.loading_bar = ttk.Progressbar(self.loading_window, orient = "horizontal", length = 200, mode = "determinate", variable = self.loading_value)
        self.loading_bar.grid(row = 1, column = 0, padx = 45)
        self.loading_current = tk.StringVar(None, "DAF XF 105")
        self.loading_current_label = ttk.Label(self.loading_window, textvariable = self.loading_current)
        self.loading_current_label.grid(row = 2, column = 0, pady = 20)

        # setup screen and immediate contents
        self.setup_screen = ttk.Frame(self.container)
        self.tab_selector = ttk.Notebook(self.setup_screen)
        self.tab_selector.pack(fill = "both")
        self.tab_welcome = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_welcome, text = " Welcome ", sticky = "nsew")
        self.tab_game = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_game, text = " Game ")
        self.tab_paintjob = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_paintjob, text = " Paintjobs ")
        self.tab_cabins = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_cabins, text = " Cabin Handling ")

        # Welcome tab
        self.tab_welcome_title = ttk.Label(self.tab_welcome, text = "Welcome to Paintjob Packer")
        self.tab_welcome_title.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        self.tab_welcome_image = ttk.Label(self.tab_welcome, image = self.image_packer)
        self.tab_welcome_image.grid(row = 1, column = 0, columnspan = 2)
        self.tab_welcome_link_forum = ttk.Label(self.tab_welcome, text = "Forum thread", foreground = "blue", cursor = self.cursor)
        self.tab_welcome_link_forum.grid(row = 2, column = 0, pady = 20)
        self.tab_welcome_link_forum.bind("<1>", lambda e: webbrowser.open_new(forum_link))
        self.tab_welcome_link_github = ttk.Label(self.tab_welcome, text = "GitHub page", foreground = "blue", cursor = self.cursor)
        self.tab_welcome_link_github.grid(row = 2, column = 1, pady = 20)
        self.tab_welcome_link_github.bind("<1>", lambda e: webbrowser.open_new(github_link))
        self.tab_welcome_message = ttk.Label(self.tab_welcome, text = "If this is your first time using Paintjob Packer, please read the guide on the GitHub page")
        self.tab_welcome_message.grid(row = 3, column = 0, columnspan = 2, pady = (25, 0))
        self.tab_welcome_button_prev = ttk.Label(self.tab_welcome, text = " ") # to keep everything centred
        self.tab_welcome_button_prev.grid(row = 5, column = 0, sticky = "sw")
        self.tab_welcome_button_next = ttk.Button(self.tab_welcome, text = "Next >", command = lambda : self.tab_selector.select(1))
        self.tab_welcome_button_next.grid(row = 5, column = 1, sticky = "se", pady = 10, padx = 10)
        self.tab_welcome.rowconfigure(5, weight = 1)
        self.tab_welcome.columnconfigure(0, weight = 1)
        self.tab_welcome.columnconfigure(1, weight = 1)

        # Game tab
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
        self.tab_game_button_prev = ttk.Button(self.tab_game, text = "< Prev", command = lambda : self.tab_selector.select(0))
        self.tab_game_button_prev.grid(row = 4, column = 0, sticky = "sw", pady = 10, padx = 10)
        self.tab_game_button_next = ttk.Button(self.tab_game, text = "Next >", command = lambda : self.tab_selector.select(2))
        self.tab_game_button_next.grid(row = 4, column = 1, sticky = "se", pady = 10, padx = 10)

        # Paintjobs tab
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
        self.tab_paintjob_button_prev = ttk.Button(self.tab_paintjob, text = "< Prev", command = lambda : self.tab_selector.select(1))
        self.tab_paintjob_button_prev.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "w")
        self.tab_paintjob_button_next = ttk.Button(self.tab_paintjob, text = "Next >", command = lambda : self.tab_selector.select(3))
        self.tab_paintjob_button_next.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = "e")

        # Cabin Handling tab
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
        self.tab_cabins_desc_combined = ttk.Label(self.tab_cabins, text = "Smaller mod size, but your design might not\nwork perfectly across all the cabin sizes", justify = "center")
        self.tab_cabins_desc_combined.grid(row = 3, column = 0, padx = 10, sticky = "n")
        self.tab_cabins_desc_separate = ttk.Label(self.tab_cabins, text = "Lets you tweak your design for each cabin\nsize, but your mod will be bigger", justify = "center")
        self.tab_cabins_desc_separate.grid(row = 3, column = 1, padx = 10, sticky = "n")
        self.tab_cabins_button_prev = ttk.Button(self.tab_cabins, text = "< Prev", command = lambda : self.tab_selector.select(2))
        self.tab_cabins_button_prev.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "w")
        self.tab_cabins_button_next = ttk.Button(self.tab_cabins, text = "Continue", command = lambda : self.switch_to_main_screen())
        self.tab_cabins_button_next.grid(row = 4, column = 1, padx = 10, pady = 10, stick = "e")

        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        # main screen and immediate contents
        self.main_screen = ttk.Frame(self.container)
        self.panel_mod = ttk.LabelFrame(self.main_screen, text = "Mod Info")
        self.panel_mod.grid(row = 0, column = 0, sticky = "ew")
        self.panel_ingame = ttk.LabelFrame(self.main_screen, text = "In-Game Paintjob Info")
        self.panel_ingame.grid(row = 1, column = 0, sticky = "ew")
        self.panel_internal = ttk.LabelFrame(self.main_screen, text = "Internal (Hidden) Paintjob Info")
        self.panel_internal.grid(row = 2, column = 0, sticky = "new")
        self.panel_vehicles_pack = ttk.LabelFrame(self.main_screen, text = "Vehicles Supported (0)")
        self.panel_vehicles_single = ttk.LabelFrame(self.main_screen, text = "Vehicle Supported")
        self.panel_buttons = ttk.Frame(self.main_screen)
        self.panel_buttons.grid(row = 3, column = 0, columnspan = 2, sticky = "ew")
        self.panel_buttons.columnconfigure(1, weight = 1)
        self.main_screen.rowconfigure(2, weight = 1) # keeps things tidy if too many mods get added

        # Mod Info panel
        self.panel_mod_name_variable = tk.StringVar()
        self.panel_mod_name_label = ttk.Label(self.panel_mod, text = "Name:")
        self.panel_mod_name_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.panel_mod_name_input = ttk.Entry(self.panel_mod, width = 30, textvariable = self.panel_mod_name_variable)
        self.panel_mod_name_input.grid(row = 0, column = 1, padx = 5, sticky = "w")
        self.panel_mod_name_help = ttk.Button(self.panel_mod, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Mod Name", message = "The name of your mod, as it appears in the in-game mod manager\n\ne.g. Transit Co. Paintjob Pack"))
        self.panel_mod_name_help.grid(row = 0, column = 2, padx = (0, 5))
        self.panel_mod_version_variable = tk.StringVar(None, "1.0")
        self.panel_mod_version_label = ttk.Label(self.panel_mod, text = "Version:")
        self.panel_mod_version_label.grid(row = 1, column = 0, padx = 5, sticky = "w")
        self.panel_mod_version_input = ttk.Entry(self.panel_mod, width = 7, textvariable = self.panel_mod_version_variable)
        self.panel_mod_version_input.grid(row = 1, column = 1, padx = 5, sticky = "w")
        self.panel_mod_version_help = ttk.Button(self.panel_mod, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Mod Version", message = "The version of your mod, as it appears in the in-game mod manager\n\ne.g. 1.0"))
        self.panel_mod_version_help.grid(row = 1, column = 2, padx = (0, 5))
        self.panel_mod_author_variable = tk.StringVar()
        self.panel_mod_author_label = ttk.Label(self.panel_mod, text = "Author:")
        self.panel_mod_author_label.grid(row = 2, column = 0, padx = 5, sticky = "w")
        self.panel_mod_author_input = ttk.Entry(self.panel_mod, width = 30, textvariable = self.panel_mod_author_variable)
        self.panel_mod_author_input.grid(row = 2, column = 1, padx = 5, sticky = "w")
        self.panel_mod_author_help = ttk.Button(self.panel_mod, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Author", message = "The author of your mod, as it appears in the in-game mod manager\n\ne.g. Carsmaniac"))
        self.panel_mod_author_help.grid(row = 2, column = 2, padx = (0, 5))
        self.panel_mod_spacer_label = ttk.Label(self.panel_mod, image = self.image_spacer_100)
        self.panel_mod_spacer_label.grid(row = 3, column = 0)
        self.panel_mod_spacer_input = ttk.Label(self.panel_mod, image = self.image_spacer_200)
        self.panel_mod_spacer_input.grid(row = 3, column = 1)

        # In-Game Paintjob Info panel
        self.panel_ingame_name_variable = tk.StringVar()
        self.panel_ingame_name_label = ttk.Label(self.panel_ingame, text = "Name:")
        self.panel_ingame_name_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.panel_ingame_name_input = ttk.Entry(self.panel_ingame, width = 30, textvariable = self.panel_ingame_name_variable)
        self.panel_ingame_name_input.grid(row = 0, column = 1, padx = 5, sticky = "w")
        self.panel_ingame_name_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: In-Game Name", message = "The name of your paintjob as it appears in-game in the vehicle purchase/upgrade screen\n\ne.g. Transit Co. Paintjob"))
        self.panel_ingame_name_help.grid(row = 0, column = 2, padx = (0, 5))
        self.panel_ingame_price_variable = tk.StringVar()
        self.panel_ingame_price_label = ttk.Label(self.panel_ingame, text = "Price:")
        self.panel_ingame_price_label.grid(row = 1, column = 0, padx = 5, sticky = "w")
        self.panel_ingame_price_input = ttk.Entry(self.panel_ingame, width = 7, textvariable = self.panel_ingame_price_variable)
        self.panel_ingame_price_input.grid(row = 1, column = 1, padx = 5, sticky = "w")
        self.panel_ingame_price_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: In-Game Price", message = "How much your paintjob costs in-game, in {}.\n\ne.g. 6000".format(self.currency)))
        self.panel_ingame_price_help.grid(row = 1, column = 2, padx = (0, 5))
        self.panel_ingame_default_variable = tk.BooleanVar(None, True)
        self.panel_ingame_default_checkbox = ttk.Checkbutton(self.panel_ingame, text = "Unlocked by default", variable = self.panel_ingame_default_variable, command = lambda : self.toggle_unlock_level())
        self.panel_ingame_default_checkbox.grid(row = 2, column = 0, columnspan = 2, padx = 5, sticky = "w")
        self.panel_ingame_default_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Unlocked By Default", message = "Whether or not your paintjob can be bought from level 0, for example on a brand new profile"))
        self.panel_ingame_default_help.grid(row = 2, column = 2, padx = (0, 5))
        self.panel_ingame_unlock_variable = tk.StringVar()
        self.panel_ingame_unlock_label = ttk.Label(self.panel_ingame, text = "Unlock level:")
        self.panel_ingame_unlock_label.grid(row = 3, column = 0, padx = 5, sticky = "w")
        self.panel_ingame_unlock_input = ttk.Entry(self.panel_ingame, width = 5, textvariable = self.panel_ingame_unlock_variable)
        self.panel_ingame_unlock_input.grid(row = 3, column = 1, padx = 5, sticky = "w")
        self.panel_ingame_unlock_input.state(["disabled"]) # disabled by default, as the "unlocked by default" checkbox is checked by default
        self.panel_ingame_unlock_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Unlock Level", message = "If not unlocked by default, what level your paintjob is made purchasable at\n\ne.g. 11"))
        self.panel_ingame_unlock_help.grid(row = 3, column = 2, padx = (0, 5))
        self.panel_ingame_spacer_label = ttk.Label(self.panel_ingame, image = self.image_spacer_100)
        self.panel_ingame_spacer_label.grid(row = 4, column = 0)
        self.panel_ingame_spacer_input = ttk.Label(self.panel_ingame, image = self.image_spacer_200)
        self.panel_ingame_spacer_input.grid(row = 4, column = 1)

        # Internal Paintjob Info panel
        self.panel_internal_name_variable = tk.StringVar()
        self.panel_internal_name_label = ttk.Label(self.panel_internal, text = "Internal name:")
        self.panel_internal_name_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.panel_internal_name_input = ttk.Entry(self.panel_internal, width = 15, textvariable = self.panel_internal_name_variable)
        self.panel_internal_name_input.grid(row = 0, column = 1, padx = 5, sticky = "w")
        self.panel_internal_name_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Internal Name", message = "A unique name used by the game to identify your paintjob. Mod users will NOT see this name.\n\nMust be {} characters or fewer, and only contain letters, numbers and underscores.\n\nMust also be unique, if two different mods use the same internal name they will be incompatible with each other.\n\ne.g. transit_co".format(self.internal_name_length)))
        self.panel_internal_name_help.grid(row = 0, column = 2, padx = (0, 5))

        self.panel_internal_unifier_variable = tk.BooleanVar(None, False)
        self.panel_internal_unifier_checkbox = ttk.Checkbutton(self.panel_internal, text = "Use cabin unifier system (advanced users only)", variable = self.panel_internal_unifier_variable, command = lambda : self.show_unifier_warning())
        self.panel_internal_unifier_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Cabin Unifer", message = "Changes all separate cabin paintjobs to point to a single .dds, and adds a separate program that unifies them all into one paintjob\n\nIf some of your textures end up working for multiple cabins (e.g. one for Cabin A, one for Cabin B and Cabin C), this unifies them to a single paintjob to make in-game paintjob switching smoother, and cut down on mod download size\n\nSee the guide on the GitHub page for a more thorough explanation\n\nRequires a hex editor to use"))
        # self.panel_internal_unifier_warning = ttk.Label(self.panel_internal, text = "Please watch the following video before using the unifier:")
        self.panel_internal_unifier_link = ttk.Label(self.panel_internal, text = "Please read the guide here before using the unifier", foreground = "blue", cursor = self.cursor)
        self.panel_internal_unifier_link.bind("<1>", lambda e: webbrowser.open_new(github_link))
        self.panel_internal_spacer_label = ttk.Label(self.panel_internal, image = self.image_spacer_100)
        self.panel_internal_spacer_label.grid(row = 4, column = 0)
        self.panel_internal_spacer_input = ttk.Label(self.panel_internal, image = self.image_spacer_200)
        self.panel_internal_spacer_input.grid(row = 4, column = 1)

        # Vehicle supported panel (single paintjob)
        self.panel_single_type_variable = tk.StringVar(None, "Truck")
        self.panel_single_type_variable.trace("w", self.change_displayed_vehicle_dropdown)
        self.panel_single_type_label = ttk.Label(self.panel_vehicles_single, text = "Type:")
        self.panel_single_type_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.panel_single_type_dropdown = ttk.Combobox(self.panel_vehicles_single, state = "readonly", textvariable = self.panel_single_type_variable, values = ["Truck", "Trailer", "Truck Mod"], width = 12)
        self.panel_single_type_dropdown.grid(row = 1, column = 0, padx = 5, sticky = "w")
        self.panel_single_vehicle_variable = tk.StringVar()
        self.panel_single_vehicle_label = ttk.Label(self.panel_vehicles_single, text = "Vehicle:")
        self.panel_single_vehicle_label.grid(row = 2, column = 0, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_single_vehicle_dropdown = ttk.Combobox(self.panel_vehicles_single, state = "readonly", textvariable = self.panel_single_vehicle_variable, values = [], width = 30)
        self.panel_single_vehicle_dropdown.grid(row = 3, column = 0, padx = 5, sticky = "w")

        # Vehicles supported panel (paintjob pack)
        self.panel_pack_selector = ttk.Notebook(self.panel_vehicles_pack)
        self.panel_pack_selector.grid(row = 0, column = 0, sticky = "nsew", padx = 5, pady = (0, 5))
        self.tab_trucks = ttk.Frame(self.panel_pack_selector)
        self.panel_pack_selector.add(self.tab_trucks, text = "Trucks")
        self.tab_trailers = ttk.Frame(self.panel_pack_selector)
        self.panel_pack_selector.add(self.tab_trailers, text = "Trailers")
        self.tab_mods = ttk.Frame(self.panel_pack_selector)
        self.panel_pack_selector.add(self.tab_mods, text = "Truck Mods")
        self.panel_pack_link_page = ttk.Label(self.tab_mods, text = "Download links for all mods", foreground = "blue", cursor = self.cursor)
        self.panel_pack_link_page.bind("<1>", lambda e: webbrowser.open_new(mod_link_page_link))

        # buttons along the bottom
        self.panel_buttons_setup = ttk.Button(self.panel_buttons, text = "< Back to setup", command = lambda : self.switch_to_setup_screen())
        self.panel_buttons_setup.grid(row = 1, column = 0, pady = (5, 0), sticky = "w")
        self.panel_buttons_feedback = ttk.Label(self.panel_buttons, text = "Leave feedback or get support", foreground = "blue", cursor = self.cursor)
        self.panel_buttons_feedback.grid(row = 1, column = 1, pady = (5, 0), padx = 10, sticky = "e")
        self.panel_buttons_feedback.bind("<1>", lambda e: webbrowser.open_new(forum_link))
        self.panel_buttons_generate = ttk.Button(self.panel_buttons, text = "Generate mod", command = lambda : self.verify_all_inputs())
        self.panel_buttons_generate.grid(row = 1, column = 2, pady = (5, 0), sticky = "e")

    def switch_to_setup_screen(self):
        if self.tab_paintjob_variable.get() == "single":
            self.panel_vehicles_single.grid_forget()
        elif self.tab_paintjob_variable.get() == "pack":
            self.panel_vehicles_pack.grid_forget()
        self.main_screen.grid_forget()
        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        for veh in self.truck_list_1 + self.truck_list_2 + self.trailer_list_1 + self.trailer_list_2 + self.mod_list_1 + self.mod_list_2:
            veh.check.grid_forget()

        self.panel_pack_link_page.grid_forget() # just in case it changes location

        self.panel_internal_unifier_checkbox.grid_forget()
        self.panel_internal_unifier_help.grid_forget()
        # self.panel_internal_unifier_warning.grid_forget()
        self.panel_internal_unifier_link.grid_forget()

    def switch_to_main_screen(self):
        self.setup_screen.grid_forget()
        self.main_screen.grid(row = 0, column = 0, padx = 10, pady = 10)
        if self.tab_paintjob_variable.get() == "single":
            self.panel_vehicles_single.grid(row = 0, column = 1, rowspan = 3, sticky = "ns", padx = (5, 0))
        elif self.tab_paintjob_variable.get() == "pack":
            self.panel_vehicles_pack.grid(row = 0, column = 1, rowspan = 3, sticky = "ns", padx = (5, 0))
        self.load_main_screen_variables()

    def load_main_screen_variables(self): # also grids and ungrids stuff depending on said variables
        if self.tab_game_variable.get() == "ats":
            self.currency = "dollars"
        elif self.tab_game_variable.get() == "ets":
            self.currency = "euro"

        if self.tab_cabins_variable.get() == "separate":
            self.internal_name_length = 10
            self.panel_internal_unifier_checkbox.grid(row = 1, column = 0, columnspan = 2, padx = 5, sticky = "w")
            self.panel_internal_unifier_help.grid(row = 1, column = 2, padx = (0, 5))
            if self.seen_unifier_warning: # these are gridded by show_unifier_warning the first time, then here for all subsequent times (if user goes back to setup, then to main again)
                # self.panel_internal_unifier_warning.grid(row = 2, column = 0, columnspan = 3, padx = 5, sticky = "w")
                self.panel_internal_unifier_link.grid(row = 3, column = 0, columnspan = 3, padx = 5, sticky = "w")
        elif self.tab_cabins_variable.get() == "combined":
            self.internal_name_length = 12

        (self.truck_list, self.trailer_list, self.mod_list) = self.load_list_of_vehicles(self.tab_game_variable.get())
        self.truck_list_1 = self.truck_list[:math.ceil(len(self.truck_list)/2)] # lists need to be split for multiple vehicle selection, it's easier if it's done here
        self.truck_list_2 = self.truck_list[math.ceil(len(self.truck_list)/2):]
        self.trailer_list_1 = self.trailer_list[:math.ceil(len(self.trailer_list)/2)]
        self.trailer_list_2 = self.trailer_list[math.ceil(len(self.trailer_list)/2):]
        self.mod_list_1 = self.mod_list[:math.ceil(len(self.mod_list)/2)]
        self.mod_list_2 = self.mod_list[math.ceil(len(self.mod_list)/2):]

        for i in range(len(self.truck_list_1)):
            self.truck_list_1[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.truck_list_2)):
            self.truck_list_2[i].check.grid(row = i, column = 1, sticky = "w", padx = 5)
        for i in range(len(self.trailer_list_1)):
            self.trailer_list_1[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.trailer_list_2)):
            self.trailer_list_2[i].check.grid(row = i, column = 1, sticky = "w", padx = 5)
        for i in range(len(self.mod_list_1)):
            self.mod_list_1[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.mod_list_2)):
            self.mod_list_2[i].check.grid(row = i, column = 1, sticky = "w", padx = 5)

        self.panel_pack_link_page.grid(row = len(self.mod_list_2), column = 1, sticky = "w", padx = 5)

        self.change_displayed_vehicle_dropdown()
        self.update_total_vehicles_supported()

    def toggle_unlock_level(self):
        if self.panel_ingame_default_variable.get():
            self.panel_ingame_unlock_input.state(["disabled"])
        else:
            self.panel_ingame_unlock_input.state(["!disabled"])

    def load_list_of_vehicles(self, game):
        complete_list = []
        for file_name in os.listdir("library/vehicles/{}".format(game)):
            complete_list.append(VehSelection(game, file_name))
        truck_list = []
        trailer_list = []
        mod_list = []
        for veh in complete_list:
            if veh.mod:
                veh.check = ttk.Checkbutton(self.tab_mods, text = veh.name, command = lambda : self.update_total_vehicles_supported())
                veh.check.state(["!alternate","!selected"])
                mod_list.append(veh)
            elif veh.trailer:
                veh.check = ttk.Checkbutton(self.tab_trailers, text = veh.name, command = lambda : self.update_total_vehicles_supported())
                veh.check.state(["!alternate","!selected"])
                trailer_list.append(veh)
            else:
                veh.check = ttk.Checkbutton(self.tab_trucks, text = veh.name, command = lambda : self.update_total_vehicles_supported())
                veh.check.state(["!alternate","!selected"])
                truck_list.append(veh)
        return (truck_list, trailer_list, mod_list)

    def change_displayed_vehicle_dropdown(self, *args):
        type = self.panel_single_type_variable.get()
        self.panel_single_vehicle_variable.set("")
        new_values = []
        if type == "Truck":
            for veh in self.truck_list: new_values.append(veh.name)
        elif type == "Trailer":
            for veh in self.trailer_list: new_values.append(veh.name)
        elif type == "Truck Mod":
            for veh in self.mod_list: new_values.append(veh.name)
        self.panel_single_vehicle_dropdown.config(values = new_values)

    def show_unifier_warning(self):
        if not self.seen_unifier_warning:
            # messagebox.showwarning(title = "Cabin Unifier", message = "The cabin unifier is for advanced users only, please watch the instructional video before use\n\nA hex editing program is required to use the unifier system")
            self.seen_unifier_warning = True
            self.panel_internal_unifier_link.grid(row = 3, column = 0, columnspan = 3, padx = 5, sticky = "w")
            # self.panel_internal_unifier_warning.grid(row = 2, column = 0, columnspan = 3, padx = 5, sticky = "w")

    def update_total_vehicles_supported(self):
        self.total_vehicles = 0
        for veh in self.truck_list_1 + self.truck_list_2 + self.trailer_list_1 + self.trailer_list_2 + self.mod_list_1 + self.mod_list_2:
            if "selected" in veh.check.state():
                self.total_vehicles += 1
        self.panel_vehicles_pack.configure(text = "Vehicles Supported ({})".format(self.total_vehicles))

    def verify_all_inputs(self):
        inputs_verified = True
        all_errors = []

        # mod info
        if len(self.panel_mod_name_variable.get()) < 1:
            inputs_verified = False
            all_errors.append(["No mod name", "Please enter a mod name"])
        if "\"" in self.panel_mod_name_variable.get():
            inputs_verified = False
            all_errors.append(["Quotation marks in mod name", "Mod names cannot contain \""])
        if len(self.panel_mod_version_variable.get()) < 1:
            inputs_verified = False
            all_errors.append(["No mod version", "Please enter a mod version"])
        if "\"" in self.panel_mod_version_variable.get():
            inputs_verified = False
            all_errors.append(["Quotation marks in mod version", "Mod versions cannot contain \""])
        if len(self.panel_mod_author_variable.get()) < 1:
            inputs_verified = False
            all_errors.append(["No mod author", "Please enter a mod author"])
        if "\"" in self.panel_mod_author_variable.get():
            inputs_verified = False
            all_errors.append(["Quotation marks in mod author", "Mod authors cannot contain \""])

        # in-game paintjob info
        if len(self.panel_ingame_name_variable.get()) < 1:
            inputs_verified = False
            all_errors.append(["No paintjob name", "Please enter a paintjob name"])
        if "\"" in self.panel_ingame_name_variable.get():
            inputs_verified = False
            all_errors.append(["Quotation marks in paintjob name", "Paintjob names cannot contain \""])
        if len(self.panel_ingame_price_variable.get()) < 1:
            inputs_verified = False
            all_errors.append(["No paintjob price", "Please enter a paintjob price"])
        if not re.match("^[0-9]*$", self.panel_ingame_price_variable.get()):
            inputs_verified = False
            all_errors.append(["Invalid paintjob price", "Paintjob price must be a number, with no decimal points, currency signs, spaces or letters"])
        if not self.panel_ingame_default_variable.get():
            if len(self.panel_ingame_unlock_variable.get()) < 1:
                inputs_verified = False
                all_errors.append(["No unlock level", "Please enter an unlock level"])
            if not re.match("^[0-9]*$", self.panel_ingame_unlock_variable.get()):
                inputs_verified = False
                all_errors.append(["Invalid unlock level", "Unlock level must be a number, with no other characters or spaces"])

        # internal paintjob info
        if len(self.panel_internal_name_variable.get()) < 1:
            inputs_verified = False
            all_errors.append(["No internal name", "Please enter an internal name"])
        if len(self.panel_internal_name_variable.get()) > self.internal_name_length:
            inputs_verified = False
            all_errors.append(["Internal name too long", "Internal name too long, it must be {} characters or fewer".format(self.internal_name_length)])
        if not re.match("^[0-9a-z\_]*$", self.panel_internal_name_variable.get()):
            inputs_verified = False
            all_errors.append(["Invalid internal name", "Internal name must only contain lowercase letters, numbers and underscores"]) # I think uppercase letters might work, but no paintjobs in the base game/DLCs use them, so best practice to avoid them

        # vehicle selection
        if self.tab_paintjob_variable.get() == "pack":
            if self.total_vehicles < 1:
                inputs_verified = False
                all_errors.append(["No vehicles selected", "Please select at least one truck, trailer or truck mod"])
        elif self.tab_paintjob_variable.get() == "single":
            if self.panel_single_vehicle_variable.get() == "":
                inputs_verified = False
                all_errors.append(["No vehicle selected", "Please select a vehicle to support"])

        if os.path.exists(output_path+"/Paintjob Packer Output"):
            if len(os.listdir(output_path+"/Paintjob Packer Output")) > 0:
                inputs_verified = False # I don't want to be on the receiving end of an irate user who lost their important report the night before it was due, because they happened to store it in the paintjob packer folder
                messagebox.showerror(title = "Output folder not clear", message = "Output folder contains items, please delete everything within the folder, or delete the folder itself\n\nThe output folder is \"Paintjob Packer Output\", on your desktop")

        if inputs_verified:
            self.make_paintjob()
        else:
            if len(all_errors) == 1:
                messagebox.showerror(title = all_errors[0][0], message = all_errors[0][1])
            elif len(all_errors) > 1:
                total_message = ""
                for error in all_errors:
                    total_message += error[0]+":\n"
                    total_message += error[1]+"\n\n"
                messagebox.showerror(title = "{} errors".format(len(all_errors)), message = total_message)

    def make_paintjob(self):
        truck_list = []
        for veh in self.truck_list_1 + self.truck_list_2:
            if "selected" in veh.check.state():
                truck_list.append(veh)
        trailer_list = []
        for veh in self.trailer_list_1 + self.trailer_list_2:
            if "selected" in veh.check.state():
                trailer_list.append(veh)
        mod_list = []
        for veh in self.mod_list_1 + self.mod_list_2:
            if "selected" in veh.check.state():
                mod_list.append(veh)

        vehicle_list = []
        for veh in truck_list + trailer_list + mod_list:
            vehicle_list.append(pj.Vehicle(veh.file_name, self.tab_game_variable.get()))

        single_veh_name = self.panel_single_vehicle_variable.get()
        for veh in self.truck_list_1 + self.truck_list_2 + self.trailer_list_1 + self.trailer_list_2 + self.mod_list_1 + self.mod_list_2:
            if veh.name == single_veh_name:
                single_veh = pj.Vehicle(veh.file_name, self.tab_game_variable.get())

        game = self.tab_game_variable.get()

        mod_name = self.panel_mod_name_variable.get()
        mod_version = self.panel_mod_version_variable.get()
        mod_author = self.panel_mod_author_variable.get()

        ingame_name = self.panel_ingame_name_variable.get()
        ingame_price = self.panel_ingame_price_variable.get()
        if self.panel_ingame_default_variable.get():
            unlock_level = 0
        else:
            unlock_level = self.panel_ingame_unlock_variable.get()

        internal_name = self.panel_internal_name_variable.get()

        num_of_paintjobs = self.tab_paintjob_variable.get()
        cabin_handling = self.tab_cabins_variable.get()
        using_unifier = self.panel_internal_unifier_variable.get()

        out_path = output_path+"/Paintjob Packer Output"

        if num_of_paintjobs == "single":
            if single_veh.mod:
                mod_list.append(single_veh)
            elif single_veh.trailer:
                trailer_list.append(single_veh)
            else:
                truck_list.append(single_veh)
            vehicle_list.append(single_veh)

        if not os.path.exists(output_path+"/Paintjob Packer Output"):
            os.makedirs(output_path+"/Paintjob Packer Output")

        self.loading_value.set(0.0)
        total_things_to_load = len(vehicle_list) + 1
        if using_unifier:
            total_things_to_load += 1
        self.loading_bar.config(maximum = float(total_things_to_load))
        self.loading_window.state("normal")
        self.loading_window.lift()

        self.loading_value.set(self.loading_value.get()+1.0)
        self.loading_current.set("Loose files")

        pj.make_manifest_sii(out_path, mod_version, mod_name, mod_author)

        pj.copy_mod_manager_image(out_path)

        pj.make_description(out_path, truck_list, trailer_list, mod_list)

        pj.make_material_folder(out_path)

        pj.copy_paintjob_icon(out_path, internal_name)

        pj.make_paintjob_icon_tobj(out_path, internal_name)

        pj.make_paintjob_icon_mat(out_path, internal_name)

        for veh in vehicle_list:
            self.loading_value.set(self.loading_value.get()+1.0)
            self.loading_current.set(veh.name)
            pj.make_def_folder(out_path, veh)
            pj.make_settings_sui(out_path, veh, internal_name, ingame_name, ingame_price, unlock_level)
            pj.make_vehicle_folder(out_path, veh, internal_name)
            if cabin_handling == "combined" or veh.type == "trailer_owned" or not veh.separate_paintjobs:
                paintjob_name = internal_name
                pj.make_def_sii(out_path, veh, paintjob_name, internal_name)
                pj.copy_main_dds(out_path, veh, internal_name, paintjob_name, using_unifier)
                pj.make_main_tobj(out_path, veh, internal_name, paintjob_name, using_unifier)
                if veh.uses_accessories:
                    pj.make_accessory_sii(out_path, veh, internal_name, paintjob_name)
            else:
                for cab_size in veh.cabins:
                    paintjob_name = internal_name + "_" + cab_size
                    pj.make_def_sii(out_path, veh, paintjob_name, internal_name, veh.cabins[cab_size], cab_size)
                    pj.copy_main_dds(out_path, veh, internal_name, paintjob_name, using_unifier)
                    pj.make_main_tobj(out_path, veh, internal_name, paintjob_name, using_unifier)
                    if veh.uses_accessories:
                        pj.make_accessory_sii(out_path, veh, internal_name, paintjob_name)
            if veh.uses_accessories:
                pj.copy_accessory_dds(out_path, veh, internal_name)
                pj.make_accessory_tobj(out_path, veh, internal_name)

        if using_unifier:
            self.loading_value.set(self.loading_value.get()+1.0)
            self.loading_current.set("Cabin unifier")
            if using_executable:
                unifier_name = "Cabin Unifier.exe"
            else:
                unifier_name = "unifier.py"
            pj.make_unifier_ini(out_path, internal_name, vehicle_list, unifier_name)

        self.make_readme_file(internal_name, using_unifier, game)

        self.loading_current.set("Complete!")
        self.loading_window.state("withdrawn")

        exit_now = messagebox.showinfo(title = "Mod generation complete", message = "Your mod has been generated successfully, it's been placed on your desktop.\n\nNext to the output folder is a readme with a list of all of the files you'll need to replace.\n\nNote that your mod is not complete yet, see the guide on the GitHub page for instructions on how to complete it.\n\nThanks for using Paintjob Packer! The program will now quit.")
        sys.exit()

    def make_readme_file(self, internal_name, using_unifier, game):
        file = open(output_path+"/Read Me! - Paintjob Packer.txt", "w")
        file.write("Thanks for using Paintjob Packer!\n")
        file.write("This text file contains a list of all of the placeholder files you'll need to replace.\n")
        file.write("\n")
        file.write("For more info, see the guide on the GitHub page: {}\n".format(github_link))
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("To test your mod, move the output folder (the folder itself, not just the files inside it!) to your mod folder:\n")
        if game == "ets":
            game_name = "Euro Truck Simulator 2"
        elif game == "ats":
            game_name = "American Truck Simulator"
        if sys.platform.startswith("win"):
            mod_folder_location = "C:\\Users\\(username)\\Documents\\{}\\mod\n".format(game_name)
        elif sys.platform.startswith("darwin"):
            mod_folder_location = "/Users/(username)/Library/Application Support/{}/mod\n".format(game_name)
        elif sys.platform.startswith("linux"):
            mod_folder_location = "/home/(username)/.local/share/{}/mod\n".format(game_name)
        file.write(mod_folder_location+"\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== Mod manager image ==\n")
        file.write("mod_manager_image.jpg\n")
        file.write("276 x 162 JPEG image\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== Mod manager description ==\n")
        file.write("mod_manager_description.txt\n")
        file.write("This contains an auto-generated list of vehicles supported by your mod.\n")
        file.write("You may want to add some extra description to it, maybe explaining your mod a bit.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== In-game paintjob icon ==\n")
        file.write("material/ui/accessory/{}_icon.dds\n".format(internal_name))
        file.write("256 x 64 DDS image (saved in DXT5 format with mipmaps), see the placeholder for recommended size/shape\n")
        file.write("This is the icon you see when you go to buy your paintjob in-game.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== Vehicle textures ==\n")
        file.write("vehicle/truck/upgrade/paintjob/{}/<vehicle>/<all the .dds files>\n".format(internal_name))
        file.write("and/or\n")
        file.write("vehicle/trailer_owned/upgrade/paintjob/{}/<vehicle>/<all the .dds files>\n".format(internal_name))
        file.write("DDS images (saved in DXT5 format with mipmaps), height and width need to be powers of 2 (e.g. 16, 64, 1024, 2048, 4096)\n")
        file.write("\n")
        file.write("The \"cabin\" images in the truck folders are the main files of your paintjob,\n")
        file.write("that's where you'll put the designs you make based off templates. All other\n")
        file.write("images refer to accessory parts, which are found on trailers and some newer\n")
        file.write("trucks. You can either create full-on textures for them using templates, or\n")
        file.write("simply re-colour the placeholder files. For example, if you want to make one\n")
        file.write("of the accessories red, you don't have to download a template for that specific\n")
        file.write("part, you can just take the existing 4x4 file and make it red instead of white.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        if using_unifier:
            file.write("Note: you don't have to change any .mat files, or anything in the def folder.\n")
            file.write("\n")
            file.write("\n")
            file.write("\n")
            file.write("Since you're using the cabin unifier, you will need to change cabin .tobj files\n")
            file.write("to add additional textures. If your cabin_a.dds doesn't work on Cabin B of a truck,\n")
            file.write("for example, you'll need to create a second .dds file called cabin_b.dds, then edit\n")
            file.write("cabin_b.tobj to point to it. You can link multiple .tobjs to the same .dds, e.g. you\n")
            file.write("could also point cabin_c.tobj to cabin_b.dds. After you've added all the extra files\n")
            file.write("you need, run the Cabin Unifier. If it completes successfully you can delete it and\n")
            file.write("unifier.ini, if not it will tell you what went wrong.\n")
        else:
            file.write("Note: you don't have to change any .tobj files, any .mat files, or anything in the def folder\n")

class VehSelection:

    def __init__(self, _game, _file_name):
        self.file_name = _file_name
        self.game = _game
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("library/vehicles/{}/{}".format(self.game, self.file_name), encoding="utf-8")
        self.name = veh_ini["vehicle info"]["name"]
        self.trailer = veh_ini["vehicle info"].getboolean("trailer")
        self.mod = veh_ini["vehicle info"].getboolean("mod")
        self.mod_author = veh_ini["vehicle info"]["mod author"]

def main():
    root = tk.Tk()
    root.title("Paintjob Packer v{}".format(version))
    root.iconphoto(True, tk.PhotoImage(file = "library/packer images/icon.png"))
    root.resizable(False, False)
    packer = PackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
