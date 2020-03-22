import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser, sys, configparser, os, math, re
import library.paintjob as pj

# ABANDON ALL HOPE, YE WHO ENTER HERE
# I'm a designer, not a programmer, my code's a mess

version = "1.0"
video_link = "https://google.com"
forum_link = "https://google.com"
github_link = "https://github.com/carsmaniac/paintjob-packer"
mod_link_page_link = "https://github.com/Carsmaniac/paintjob-packer/blob/ui-overhaul/mod%20links.md" # I could replace the %20 with a space to look neater, but it might break compatibility with some browsers (maybe..?)

class PackerApp:

    def __init__(self, master):
        # container to hold setup/main screen
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.image_packer = tk.PhotoImage(file = "library/packer images/packer.gif")
        self.image_ats = tk.PhotoImage(file = "library/packer images/ats.gif")
        self.image_ets = tk.PhotoImage(file = "library/packer images/ets.gif")
        self.image_single_paintjob = tk.PhotoImage(file = "library/packer images/single paintjob.gif")
        self.image_paintjob_pack = tk.PhotoImage(file = "library/packer images/paintjob pack.gif")
        self.image_separate_cabins = tk.PhotoImage(file = "library/packer images/separate cabins.gif")
        self.image_combined_cabins = tk.PhotoImage(file = "library/packer images/combined cabins.gif")
        self.image_spacer_100 = tk.PhotoImage(file = "library/packer images/spacer 100.png")
        self.image_spacer_200 = tk.PhotoImage(file = "library/packer images/spacer 200.png")

        # load appropriate cursor for OS, used when mousing over links
        if sys.platform.startswith("win"):
            self.cursor = "hand2"
        elif sys.platform.startswith("linux"):
            self.cursor = "hand2"
        elif sys.platform.startswith("darwin"): # macOS
            self.cursor = "pointinghand"

        self.seen_unifier_warning = False # will show the warning only once per session
        self.total_vehicles = 0

        # second window displayed when generating mod
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
        self.tab_welcome_message = ttk.Label(self.tab_welcome, text = "If this is your first time using Paintjob Packer, please watch the following instructional video:")
        self.tab_welcome_message.grid(row = 3, column = 0, columnspan = 2, pady = (15, 0))
        self.tab_welcome_link_video = ttk.Label(self.tab_welcome, text = "Instructional video", foreground = "blue", cursor = self.cursor)
        self.tab_welcome_link_video.grid(row = 4, column = 0, columnspan = 2)
        self.tab_welcome_link_video.bind("<1>", lambda e: webbrowser.open_new(video_link))
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
        self.tab_cabins_desc_combined = ttk.Label(self.tab_cabins, text = "Simpler to make, but may result in wonky\npaintjobs on differently-sized cabins", justify = "center")
        self.tab_cabins_desc_combined.grid(row = 3, column = 0, padx = 10, sticky = "n")
        self.tab_cabins_desc_separate = ttk.Label(self.tab_cabins, text = "Lets you customise your paintjob for each\ncabin, but is more complex to make", justify = "center")
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
        self.panel_internal_name_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Internal Name", message = "A unique name used by the game to identify your paintjob. Mod users will NOT see this name.\n\nMust be {} characters or fewer, and only contain letters, numbers and underscores.\n\nMust also be unique, if two different mods use the same internal name they will be incompatible with each other.\n\ne.g. transit_pj".format(self.internal_name_length)))
        self.panel_internal_name_help.grid(row = 0, column = 2, padx = (0, 5))

        self.panel_internal_unifier_variable = tk.BooleanVar(None, False)
        self.panel_internal_unifier_checkbox = ttk.Checkbutton(self.panel_internal, text = "Use cabin unifier system (advanced users only)", variable = self.panel_internal_unifier_variable, command = lambda : self.show_unifier_warning())
        self.panel_internal_unifier_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Cabin Unifer", message = "Changes all separate cabin paintjobs to point to a single .dds, and adds a separate program that unifies them all into one paintjob\n\nIf some of your textures end up working for multiple cabins (e.g. one for Cabin A, one for Cabin B and Cabin C), this unifies them to a single paintjob to make in-game paintjob switching smoother, and cut down on mod download size\n\nSee instructional video for a more thorough explanation\n\nRequires a hex editor and Python 3 to use"))
        self.panel_internal_unifier_warning = ttk.Label(self.panel_internal, text = "Please watch the following video before using the unifier:")
        self.panel_internal_unifier_link = ttk.Label(self.panel_internal, text = "Instructional video", foreground = "blue", cursor = self.cursor)
        self.panel_internal_unifier_link.bind("<1>", lambda e: webbrowser.open_new(video_link))
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
        self.panel_internal_unifier_warning.grid_forget()
        self.panel_internal_unifier_link.grid_forget()

    def switch_to_main_screen(self):
        self.setup_screen.grid_forget()
        self.main_screen.grid(row = 0, column = 0, padx = 10, pady = 10)
        if self.tab_paintjob_variable.get() == "single":
            self.panel_vehicles_single.grid(row = 0, column = 1, rowspan = 3, sticky = "ns", padx = (5, 0))
        elif self.tab_paintjob_variable.get() == "pack":
            self.panel_vehicles_pack.grid(row = 0, column = 1, rowspan = 3, sticky = "ns", padx = (5, 0))
        self.load_main_screen_variables()

    def load_main_screen_variables(self):
        if self.tab_game_variable.get() == "ats":
            self.currency = "dollars"
        elif self.tab_game_variable.get() == "ets":
            self.currency = "euro" # in English, accoring to the EU, the plural of euro is "euro", not "euros"

        if self.tab_cabins_variable.get() == "separate":
            self.internal_name_length = 10
            self.panel_internal_unifier_checkbox.grid(row = 1, column = 0, columnspan = 2, padx = 5, sticky = "w")
            self.panel_internal_unifier_help.grid(row = 1, column = 2, padx = (0, 5))
            if self.seen_unifier_warning: # these are gridded by show_unifier_warning the first time, then here for all subsequent times (if user goes back to setup, then to main again)
                self.panel_internal_unifier_warning.grid(row = 2, column = 0, columnspan = 3, padx = 5, sticky = "w")
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
            messagebox.showwarning(title = "Cabin Unifier", message = "The cabin unifier is for advanced users only, please watch the instructional video before use\n\nA hex editing program and Python 3 are required to use the unifier system")
            self.seen_unifier_warning = True
            self.panel_internal_unifier_link.grid(row = 3, column = 0, columnspan = 3, padx = 5, sticky = "w")
            self.panel_internal_unifier_warning.grid(row = 2, column = 0, columnspan = 3, padx = 5, sticky = "w")

    def update_total_vehicles_supported(self):
        self.total_vehicles = 0
        for veh in self.truck_list_1 + self.truck_list_2 + self.trailer_list_1 + self.trailer_list_2 + self.mod_list_1 + self.mod_list_2:
            if "selected" in veh.check.state():
                self.total_vehicles += 1
        self.panel_vehicles_pack.configure(text = "Vehicles Supported ({})".format(self.total_vehicles))

    def verify_all_inputs(self):
        inputs_verified = True

        # mod info
        if len(self.panel_mod_name_variable.get()) < 1:
            inputs_verified = False
            messagebox.showerror(title = "No mod name", message = "Please enter a mod name")
        if "\"" in self.panel_mod_name_variable.get(): # using if instead of elif, users will see everything wrong with what they've entered
            inputs_verified = False
            messagebox.showerror(title = "Quotation marks in mod name", message = "Mod names cannot contain \"")
        if len(self.panel_mod_version_variable.get()) < 1:
            inputs_verified = False
            messagebox.showerror(title = "No mod version", message = "Please enter a mod version")
        if "\"" in self.panel_mod_version_variable.get():
            inputs_verified = False
            messagebox.showerror(title = "Quotation marks in mod version", message = "Mod versions cannot contain \"")
        if len(self.panel_mod_author_variable.get()) < 1:
            inputs_verified = False
            messagebox.showerror(title = "No mod author", message = "Please enter a mod author")
        if "\"" in self.panel_mod_author_variable.get():
            inputs_verified = False
            messagebox.showerror(title = "Quotation marks in mod author", message = "Mod authors cannot contain \"")

        # in-game paintjob info
        if len(self.panel_ingame_name_variable.get()) < 1:
            inputs_verified = False
            messagebox.showerror(title = "No paintjob name", message = "Please enter a paintjob name")
        if "\"" in self.panel_ingame_name_variable.get():
            inputs_verified = False
            messagebox.showerror(title = "Quotation marks in paintjob name", message = "Paintjob names cannot contain \"")
        if len(self.panel_ingame_price_variable.get()) < 1:
            inputs_verified = False
            messagebox.showerror(title = "No paintjob price", message = "Please enter a paintjob price")
        if not re.match("^[0-9]*$", self.panel_ingame_price_variable.get()):
            inputs_verified = False
            messagebox.showerror(title = "Invalid paintjob price", message = "Paintjob price must be a number, with no decimal points, currency signs, spaces or letters")
        if not self.panel_ingame_default_variable.get():
            if len(self.panel_ingame_unlock_variable.get()) < 1:
                inputs_verified = False
                messagebox.showerror(title = "No unlock level", message = "Please enter an unlock level")
            if not re.match("^[0-9]*$", self.panel_ingame_unlock_variable.get()):
                inputs_verified = False
                messagebox.showerror(title = "Invalid unlock level", message = "Unlock level must be a number, with no other characters or spaces")

        # internal paintjob info
        if len(self.panel_internal_name_variable.get()) < 1:
            inputs_verified = False
            messagebox.showerror(title = "No internal name", message = "Please enter an internal name")
        if len(self.panel_internal_name_variable.get()) > self.internal_name_length:
            inputs_verified = False
            messagebox.showerror(title = "Internal name too long", message = "Internal name too long, it must be {} characters or fewer".format(self.internal_name_length))
        if not re.match("^[0-9a-z\_]*$", self.panel_internal_name_variable.get()):
            inputs_verified = False
            messagebox.showerror(title = "Invalid internal name", message = "Internal name must only contain lowercase letters, numbers and underscores") # I think uppercase letters might work, but no paintjobs in the base game/DLCs use them, so best practice to avoid them

        # vehicle selection
        if self.tab_paintjob_variable.get() == "pack":
            if self.total_vehicles < 1:
                inputs_verified = False
                messagebox.showerror(title = "No vehicles selected", message = "Please select at least one truck, trailer or truck mod")
        elif self.tab_paintjob_variable.get() == "single":
            if self.panel_single_vehicle_variable.get() == "":
                inputs_verified = False
                messagebox.showerror(title = "No vehicle selected", message = "Please select a vehicle to support")

        if inputs_verified:
            print("Success")
            self.make_paintjob()

    def make_paintjob(self):
        pass
        # self.loading_value.set(5.0)
        # self.loading_bar.config(maximum = 10.0)
        # self.loading_current.set("DAF XF 105")
        # self.loading_window.state("normal")

class VehSelection:

    def __init__(self, _game, _file_name):
        self.file_name = _file_name
        self.game = _game
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("library/vehicles/{}/{}".format(self.game, self.file_name))
        self.name = veh_ini["vehicle info"]["name"]
        self.trailer = veh_ini["vehicle info"].getboolean("trailer")
        self.mod = veh_ini["vehicle info"].getboolean("mod")
        self.mod_author = veh_ini["vehicle info"]["mod author"]
        self.mod_link = veh_ini["vehicle info"]["mod link"]

def main():
    root = tk.Tk()
    root.title("Paintjob Packer v{}".format(version))
    root.iconphoto(True, tk.PhotoImage(file = "library/packer images/icon.png"))
    root.resizable(False, False)
    packer = PackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
