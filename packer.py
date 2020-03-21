import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser, sys, configparser, os, math

# ABANDON ALL HOPE, YE WHO ENTER HERE
# I'm a designer, not a programmer, my code's a mess

version = "1.0"

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
        self.tab_welcome_link_forum.bind("<1>", lambda e: webbrowser.open_new("http://example.com"))
        self.tab_welcome_link_github = ttk.Label(self.tab_welcome, text = "GitHub page", foreground = "blue", cursor = self.cursor)
        self.tab_welcome_link_github.grid(row = 2, column = 1, pady = 20)
        self.tab_welcome_link_github.bind("<1>", lambda e: webbrowser.open_new("http://github.com/carsmaniac/paintjob-packer"))
        self.tab_welcome_message = ttk.Label(self.tab_welcome, text = "If this is your first time using Paintjob Packer, please watch the following instructional video:")
        self.tab_welcome_message.grid(row = 3, column = 0, columnspan = 2, pady = (15, 0))
        self.tab_welcome_link_video = ttk.Label(self.tab_welcome, text = "Instructional video", foreground = "blue", cursor = self.cursor)
        self.tab_welcome_link_video.grid(row = 4, column = 0, columnspan = 2)
        self.tab_welcome_link_video.bind("<1>", lambda e: webbrowser.open_new("http://example.com"))
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
        self.panel_internal.grid(row = 2, column = 0, sticky = "ew")
        self.panel_vehicles_pack = ttk.LabelFrame(self.main_screen, text = "Vehicles Supported")
        self.panel_vehicles_single = ttk.LabelFrame(self.main_screen, text = "Vehicle Supported")
        self.panel_buttons = ttk.Frame(self.main_screen)
        self.panel_buttons.grid(row = 3, column = 0, columnspan = 2, sticky = "ew")
        self.panel_buttons.columnconfigure(1, weight = 1)

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
        self.panel_mod_version_input = ttk.Entry(self.panel_mod, width = 5, textvariable = self.panel_mod_version_variable)
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
        self.panel_internal_colour_variable = tk.StringVar()
        self.panel_internal_colour_label = ttk.Label(self.panel_internal, text = "Main colour:")
        self.panel_internal_colour_label.grid(row = 1, column = 0, padx = 5, sticky = "w")
        self.panel_internal_colour_input = ttk.Entry(self.panel_internal, width = 15, textvariable = self.panel_internal_colour_variable)
        self.panel_internal_colour_input.grid(row = 1, column = 1, padx = 5, sticky = "w")
        self.panel_internal_colour_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = "Help: Main Colour", message = "A name used for accessory files, which are used in trailers and some newer trucks. Mod users will NOT see this.\n\nMust only contain letters, numbers and underscores.\n\ne.g. yellow"))
        self.panel_internal_colour_help.grid(row = 1, column = 2, padx = (0, 5))
        self.panel_internal_spacer_label = ttk.Label(self.panel_internal, image = self.image_spacer_100)
        self.panel_internal_spacer_label.grid(row = 2, column = 0)
        self.panel_internal_spacer_input = ttk.Label(self.panel_internal, image = self.image_spacer_200)
        self.panel_internal_spacer_input.grid(row = 2, column = 1)

        # Vehicle supported panel (single paintjob)
        self.panel_single_type_variable = tk.StringVar(None, "Truck")
        self.panel_single_type_variable.trace("w", self.change_displayed_vehicle_dropdown)
        self.panel_single_type_label = ttk.Label(self.panel_vehicles_single, text = "Type:")
        self.panel_single_type_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.panel_single_type_dropdown = ttk.Combobox(self.panel_vehicles_single, state = "readonly", textvariable = self.panel_single_type_variable, values = ["Truck", "Trailer", "Truck Mod"])
        self.panel_single_type_dropdown.grid(row = 1, column = 0, padx = 5)
        self.panel_single_vehicle_variable = tk.StringVar()
        self.panel_single_vehicle_label = ttk.Label(self.panel_vehicles_single, text = "Vehicle:")
        self.panel_single_vehicle_label.grid(row = 2, column = 0, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_single_vehicle_dropdown = ttk.Combobox(self.panel_vehicles_single, state = "readonly", textvariable = self.panel_single_vehicle_variable, values = ["Truck1", "Truck2", "Truck3"])
        self.panel_single_vehicle_dropdown.grid(row = 3, column = 0, padx = 5)

        # Vehicles supported panel (paintjob pack)
        self.panel_pack_selector = ttk.Notebook(self.panel_vehicles_pack)
        self.panel_pack_selector.grid(row = 0, column = 0, sticky = "nsew", padx = 5, pady = (0, 5))
        self.tab_trucks = ttk.Frame(self.panel_pack_selector)
        self.panel_pack_selector.add(self.tab_trucks, text = "Trucks")
        self.tab_trailers = ttk.Frame(self.panel_pack_selector)
        self.panel_pack_selector.add(self.tab_trailers, text = "Trailers")
        self.tab_mods = ttk.Frame(self.panel_pack_selector)
        self.panel_pack_selector.add(self.tab_mods, text = "Truck Mods")

        # buttons along the bottom
        self.panel_buttons_setup = ttk.Button(self.panel_buttons, text = "< Back to setup", command = lambda : self.switch_to_setup_screen())
        self.panel_buttons_setup.grid(row = 1, column = 0, pady = (5, 0), sticky = "w")
        self.panel_buttons_feedback = ttk.Label(self.panel_buttons, text = "Leave feedback or get support", foreground = "blue", cursor = self.cursor)
        self.panel_buttons_feedback.grid(row = 1, column = 1, pady = (5, 0), padx = 10, sticky = "e")
        self.panel_buttons_feedback.bind("<1>", lambda e: webbrowser.open_new("http://example.com"))
        self.panel_buttons_generate = ttk.Button(self.panel_buttons, text = "Generate mod", command = lambda : messagebox.showinfo(title = "Hi", message = "Yes"))
        self.panel_buttons_generate.grid(row = 1, column = 2, pady = (5, 0), sticky = "e")

    def switch_to_setup_screen(self):
        if self.tab_paintjob_variable.get() == "single":
            self.panel_vehicles_single.grid_forget()
        elif self.tab_paintjob_variable.get() == "pack":
            self.panel_vehicles_pack.grid_forget()
        self.main_screen.grid_forget()
        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        for veh in self.truck_list_1:
            veh.check.grid_forget()
        for veh in self.truck_list_2:
            veh.check.grid_forget()
        for veh in self.trailer_list_1:
            veh.check.grid_forget()
        for veh in self.trailer_list_2:
            veh.check.grid_forget()
        for veh in self.mod_list_1:
            veh.check.grid_forget()
        for veh in self.mod_list_2:
            veh.check.grid_forget()

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
                veh.check = ttk.Checkbutton(self.tab_mods, text = veh.name)
                veh.check.state(["!alternate","!selected"])
                mod_list.append(veh)
            elif veh.trailer:
                veh.check = ttk.Checkbutton(self.tab_trailers, text = veh.name)
                veh.check.state(["!alternate","!selected"])
                trailer_list.append(veh)
            else:
                veh.check = ttk.Checkbutton(self.tab_trucks, text = veh.name)
                veh.check.state(["!alternate","!selected"])
                truck_list.append(veh)
        return (truck_list, trailer_list, mod_list)

    def change_displayed_vehicle_dropdown(self, *args):
        type = self.panel_single_type_variable.get()
        self.panel_single_vehicle_variable.set("")
        new_values = []
        if type == "Truck":
            for veh in self.truck_list: new_values.append()
        elif type == "Trailer":
            self.panel_single_vehicle_dropdown.config(values = ["Trailer"])
        elif type == "Truck Mod":
            self.panel_single_vehicle_dropdown.config(values = ["Truck Mod"])
        self.panel_single_vehicle_dropdown.config(values = new_values)

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
