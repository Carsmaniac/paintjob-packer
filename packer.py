import tkinter as tk # GUI system
from tkinter import ttk # Nicer-looking GUI elements
from tkinter import messagebox # Showing popup windows for warnings and errors
from tkinter import filedialog # Choosing save directory
import webbrowser # Opening links in the web browser: forum thread, github page, mod links
import sys # Determining OS, and quitting Paint Job Packer
import configparser # Reading vehicle database files, version info and l10n dictionary
import os # Making folders and getting all vehicle database files
import shutil # Copying files (checking write permission, all actual copying occurs in paintjob.py)
import re # Checking for invalid characters in mod/paint job names
import traceback # Handling unexpected errors
import zipfile # Unzipping templates
import urllib.request # Fetching version info from GitHub
import locale # Determining the default system language
import ssl # Opting out of verification when checking version - see check_new_version()
import threading # Multi-threading the update checking process
from datetime import date # Including date on submitted error reports
try:
    import darkdetect # Detecting whether or not the system is in dark mode
except ModuleNotFoundError:
    print("Darkdetect is not installed (pip install darkdetect), defaulting to light mode")

try:
    import library.paintjob as pj # Copying and generating mod files
    import library.analytics # Simple analytics using RudderStack, see analytics.py for a detailed breakdown
    import library.webhook as webhook # For notifying me of new crash reports
except ModuleNotFoundError:
    print("Paint Job Packer can't find its library files")
    print("Make sure that the \"library\" folder is in the same directory as packer.py, and it contains all of its files")
    input("Press enter to quit")
    sys.exit()

FORUM_LINK = "https://forum.scssoft.com/viewtopic.php?f=33&t=282956"
GITHUB_LINK = "https://github.com/Carsmaniac/paintjob-packer"
KOFI_LINK = "https://ko-fi.com/carsmaniac"
CROWDIN_LINK = "https://crowdin.com/project/paint-job-packer"
MOD_LINK_PAGE_LINK = "https://github.com/Carsmaniac/paintjob-packer/blob/master/library/mod%20links.md"
ETS_TEMPLATE_LINK = "https://forum.scssoft.com/viewtopic.php?f=33&t=272386"
ATS_TEMPLATE_LINK = "https://forum.scssoft.com/viewtopic.php?f=199&t=288778"
VERSION_INFO_LINK = "https://raw.githubusercontent.com/Carsmaniac/paintjob-packer/master/library/version.ini"
LATEST_VERSION_DOWNLOAD_LINK = "https://carsmani.ac/paint-job-packer#downloads"
SUN_VALLEY_LINK = "https://github.com/rdbende/Sun-Valley-ttk-theme"
DARKDETECT_LINK = "https://github.com/albertosottile/darkdetect"
RUDDERSTACK_LINK = "https://github.com/rudderlabs/rudder-sdk-python"
DISCORD_WEBHOOK_LINK = "https://github.com/lovvskillz/python-discord-webhook"
ANALYTICS_SCRIPT_LINK = "https://github.com/Carsmaniac/paintjob-packer/blob/master/library/analytics.py"
MIT_LICENCE_LINK = "https://opensource.org/licenses/MIT"
BSD_LICENCE_LINK = "https://opensource.org/licenses/BSD-3-Clause"

# These will replace the old ones (and the repo will move) a while after v1.9 is released, when the installbase that's ONLY checking the old links is much smaller
NEW_GITHUB_LINK = "https://github.com/Carsmaniac/paint-job-packer"
NEW_MOD_LINK_PAGE_LINK = "https://github.com/Carsmaniac/paint-job-packer/blob/main/library/mod-links.md"
NEW_VERSION_INFO_LINK = "https://raw.githubusercontent.com/Carsmaniac/paint-job-packer/main/library/version.ini"
NEW_ANALYTICS_SCRIPT_LINK = "https://github.com/Carsmaniac/paint-job-packer/blob/main/library/analytics.py"

# Set the path depending on how Paint Job Packer is bundled
try:
    base_path = sys._MEIPASS # Packaged into executable
    using_executable = True
except AttributeError:
    base_path = os.path.abspath(".") # Loose .py
    using_executable = False
os.chdir(base_path)

desktop_path = os.path.expanduser("~/Desktop")

if sys.platform.startswith("darwin") or not using_executable:
    # Set print encoding to UTF-8, in case the system's preferred encoding is ASCII
    sys.stdout.reconfigure(encoding="utf-8")

version_info = configparser.ConfigParser()
version_info.read("library/version.ini")
version = version_info["version info"]["installed version"]

class PackerApp:

    def __init__(self, master, language):
        # new_ver exists between PackerApps so it doesn't need to be re-fetched every time the language is changed
        global new_ver

        # Container to hold setup/main screen
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.image_packer = tk.PhotoImage(file = "library/packer-images/packer.png")
        self.image_ats = tk.PhotoImage(file = "library/packer-images/game-ats.png")
        self.image_ets = tk.PhotoImage(file = "library/packer-images/game-ets.png")
        self.image_single_paintjob = tk.PhotoImage(file = "library/packer-images/paint-job-single.png")
        self.image_paintjob_pack = tk.PhotoImage(file = "library/packer-images/paint-job-pack.png")

        # Load appropriate cursor for OS, used when mousing over links
        if sys.platform.startswith("win"):
            self.os = "Windows"
            self.cursor = "hand2"
        elif sys.platform.startswith("darwin"):
            self.os = "macOS"
            self.cursor = "pointinghand"
        elif sys.platform.startswith("linux"):
            self.os = "Linux"
            self.cursor = "hand2"

        # Choose a shade of blue that works with the light/dark theme
        try:
            if darkdetect.isDark():
                self.blue = "#56C7FE"
                self.red = "#F04040"
            else:
                self.blue = "#006DD3"
                self.red = "#E81000"
        except NameError:
            self.blue = "#006DD3"
            self.red = "#E81000"

        self.total_vehicles = 0 # Used in the vehicle selector when making a paint job pack

        self.language = language
        self.load_language_dictionary(self.language)
        self.load_language_list()
        l = self.get_localised_string # One-letter function name to make all the many calls of it more readable

        # Setup screen and immediate contents
        self.setup_screen = ttk.Frame(self.container)
        self.tab_selector = ttk.Notebook(self.setup_screen)
        self.tab_selector.pack(fill = "both")
        self.tab_welcome = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_welcome, text = l("{TabWelcome}"), sticky = "nsew")
        self.tab_game = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_game, text = l("{TabGame}"))
        self.tab_paintjob = ttk.Frame(self.tab_selector)
        self.tab_selector.add(self.tab_paintjob, text = l("{TabPaintJobs}"))

        # Welcome tab
        self.tab_welcome_title = ttk.Label(self.tab_welcome, text = l("{TabWelcomeMessage}"))
        self.tab_welcome_title.grid(row = 0, column = 0, columnspan = 3, pady = (20, 30))
        self.tab_welcome_language_variable = tk.StringVar(None, l("{LanguageName}"))
        self.tab_welcome_language_variable.trace("w", self.reload_with_language)
        self.tab_welcome_language = ttk.Combobox(self.tab_welcome, state = "readonly", textvariable = self.tab_welcome_language_variable, values = self.language_names_list, width = 18)
        self.tab_welcome_language.grid(row = 0, column = 0, padx = (10, 0), pady = 10, sticky = "nw")
        self.tab_welcome_link_credits = ttk.Button(self.tab_welcome, text = l("{About}"), command = lambda : self.credits_screen())
        self.tab_welcome_link_credits.grid(row = 0, column = 2, padx = (0, 10), pady = 10, sticky = "ne")
        self.tab_welcome_image = ttk.Label(self.tab_welcome, image = self.image_packer)
        self.tab_welcome_image.grid(row = 1, column = 0, columnspan = 3)
        self.tab_welcome_link_forum = ttk.Label(self.tab_welcome, text = l("{LinkForum}"), foreground = self.blue, cursor = self.cursor)
        self.tab_welcome_link_forum.grid(row = 2, column = 0, pady = 20)
        self.tab_welcome_link_forum.bind("<1>", lambda e: webbrowser.open_new(FORUM_LINK))
        self.tab_welcome_link_kofi = ttk.Label(self.tab_welcome, text = l("{LinkKofi}"), foreground = self.blue, cursor = self.cursor)
        self.tab_welcome_link_kofi.grid(row = 2, column = 1, pady = 20)
        self.tab_welcome_link_kofi.bind("<1>", lambda e: webbrowser.open_new(KOFI_LINK))
        self.tab_welcome_link_github = ttk.Label(self.tab_welcome, text = l("{LinkGithub}"), foreground = self.blue, cursor = self.cursor)
        self.tab_welcome_link_github.grid(row = 2, column = 2, pady = 20)
        self.tab_welcome_link_github.bind("<1>", lambda e: webbrowser.open_new(GITHUB_LINK))
        if "new_ver" not in globals():
            # Only on initial startup, not when changing languages
            self.thread_new_version()
            new_ver = [None, None]
        if new_ver[1] != None:
            # Only when changing languages after the version check found a new version
            self.tab_welcome_message = ttk.Label(self.tab_welcome, text = l("{UpdateNotice}").format(version_number = new_ver[0]), foreground = self.red, cursor = self.cursor)
            self.tab_welcome_message.grid(row = 3, column = 0, columnspan = 3, pady = (20, 0))
            self.tab_welcome_message.bind("<1>", lambda e: webbrowser.open_new(LATEST_VERSION_DOWNLOAD_LINK))
            self.tab_welcome_link_forum.configure(foreground = "black")
            self.tab_welcome_link_kofi.configure(foreground = "black")
            self.tab_welcome_link_github.configure(foreground = "black")
            self.tab_welcome_update_info = ttk.Label(self.tab_welcome, text = l("{UpdateDetails}").format(details = new_ver[1]), cursor = self.cursor)
            self.tab_welcome_update_info.grid(row = 4, column = 0, columnspan = 3)
            self.tab_welcome_update_info.bind("<1>", lambda e: webbrowser.open_new(LATEST_VERSION_DOWNLOAD_LINK))
        else:
            # Always on initial startup, and when changing languages after the version check did not find a new version
            self.tab_welcome_message = ttk.Label(self.tab_welcome, text = l("{AcknowledgementNotice}"), cursor = self.cursor, wraplength = 600, justify = tk.CENTER)
            self.tab_welcome_message.bind("<1>", lambda e: messagebox.showinfo(title = "Acknowledgement of Country", message = "Paint Job Packer was developed in Australia, a continent on which Aboriginal and Torres Strait Islander peoples have lived for tens of thousands of years, the oldest continuous culture in the world, spread across hundreds of distinct countries with different languages and customs.\n\nI acknowledge the Darramurragal people, the traditional owners of the land on which this software was created. I pay my respects to Elders past, present and emerging, the Knowledge Holders and caretakers of this Country, and extend that respect to the owners of all the lands on which Paint Job Packer is used.\n\nI acknowledge that this land has been a place of design and creativity for thousands of generations, and that sovereignty was never ceded. This always has been and always will be Aboriginal land."))
            self.tab_welcome_message.grid(row = 3, column = 0, columnspan = 3, pady = (20, 0))
        self.tab_welcome_button_prev = ttk.Label(self.tab_welcome, text = " ") # To keep everything centred
        self.tab_welcome_button_prev.grid(row = 5, column = 0, sticky = "sw")
        self.tab_welcome_button_next = ttk.Button(self.tab_welcome, text = l("{Next} >"), command = lambda : self.tab_selector.select(1))
        self.tab_welcome_button_next.grid(row = 5, column = 2, sticky = "se", pady = 10, padx = 10)
        self.tab_welcome.rowconfigure(5, weight = 1)
        self.tab_welcome.columnconfigure(0, weight = 1)
        self.tab_welcome.columnconfigure(2, weight = 1)

        # Game tab
        self.tab_game_title = ttk.Label(self.tab_game, text = l("{TabGameMessage}"))
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
        self.tab_game_dummy_desc = ttk.Label(self.tab_game, text = "  \n") # To space things out evenly
        self.tab_game_dummy_desc.grid(row = 3, column = 0)
        self.tab_game_button_prev = ttk.Button(self.tab_game, text = l("< {Previous}"), command = lambda : self.tab_selector.select(0))
        self.tab_game_button_prev.grid(row = 4, column = 0, sticky = "sw", pady = 10, padx = 10)
        self.tab_game_button_next = ttk.Button(self.tab_game, text = l("{Next} >"), command = lambda : self.tab_selector.select(2))
        self.tab_game_button_next.grid(row = 4, column = 1, sticky = "se", pady = 10, padx = 10)

        # Paint Jobs tab
        self.tab_paintjob_title = ttk.Label(self.tab_paintjob, text = l("{TabPaintJobsMessage}"))
        self.tab_paintjob_title.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        self.tab_paintjob_image_single = ttk.Label(self.tab_paintjob, image = self.image_single_paintjob)
        self.tab_paintjob_image_single.grid(row = 1, column = 0, padx = 10)
        self.tab_paintjob_image_pack = ttk.Label(self.tab_paintjob, image = self.image_paintjob_pack)
        self.tab_paintjob_image_pack.grid(row = 1, column = 1, padx = 10)
        self.tab_paintjob_variable = tk.StringVar(None, "pack")
        self.tab_paintjob_option_single = ttk.Radiobutton(self.tab_paintjob, text = l("{PaintJobSingle}"), value = "single", variable = self.tab_paintjob_variable)
        self.tab_paintjob_option_single.grid(row = 2, column = 0, pady = 10)
        self.tab_paintjob_image_single.bind("<1>", lambda e: self.tab_paintjob_variable.set("single"))
        self.tab_paintjob_option_pack = ttk.Radiobutton(self.tab_paintjob, text = l("{PaintJobPack}"), value = "pack", variable = self.tab_paintjob_variable)
        self.tab_paintjob_option_pack.grid(row = 2, column = 1, pady = 10)
        self.tab_paintjob_image_pack.bind("<1>", lambda e: self.tab_paintjob_variable.set("pack"))
        self.tab_paintjob_desc_single = ttk.Label(self.tab_paintjob, text = l("{PaintJobSingleDesc}\n"), wraplength = 300, justify = tk.CENTER)
        self.tab_paintjob_desc_single.grid(row = 3, column = 0, padx = 10, sticky = "n")
        self.tab_paintjob_desc_pack = ttk.Label(self.tab_paintjob, text = l("{PaintJobPackDesc}\n"), wraplength = 300, justify = tk.CENTER)
        self.tab_paintjob_desc_pack.grid(row = 3, column = 1, padx = 10, sticky = "n")
        self.tab_paintjob_button_prev = ttk.Button(self.tab_paintjob, text = l("< {Previous}"), command = lambda : self.tab_selector.select(1))
        self.tab_paintjob_button_prev.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "w")
        self.tab_paintjob_button_next = ttk.Button(self.tab_paintjob, text = l("{Continue}"), command = lambda : self.switch_to_main_screen())
        self.tab_paintjob_button_next.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = "e")

        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        # Main screen and immediate contents
        self.main_screen = ttk.Frame(self.container)
        self.panel_mod = ttk.LabelFrame(self.main_screen, text = l("{ModInfoPanelName}"))
        self.panel_mod.grid(row = 0, column = 0, sticky = "ew")
        self.panel_ingame = ttk.LabelFrame(self.main_screen, text = l("{InGamePaintJobInfoPanelName}"))
        self.panel_ingame.grid(row = 1, column = 0, pady = (5, 0), sticky = "ew")
        self.panel_internal = ttk.LabelFrame(self.main_screen, text = l("{InternalInfoPanelName}"))
        self.panel_internal.grid(row = 2, column = 0, pady = (5, 0), sticky = "new")
        self.panel_vehicles_pack = ttk.LabelFrame(self.main_screen, text = l("{VehiclesPanelNamePack}").format(number = "0"))
        self.panel_vehicles_single = ttk.LabelFrame(self.main_screen, text = l("{VehiclesPanelNameSingle}"))
        self.panel_main_buttons = ttk.Frame(self.main_screen)
        self.panel_main_buttons.grid(row = 3, column = 0, columnspan = 2, pady = (5, 0), sticky = "ew")
        self.panel_main_buttons.columnconfigure(1, weight = 1)
        self.main_screen.rowconfigure(2, weight = 1) # Keeps things tidy if too many mods get added

        # Mod Info panel
        self.panel_mod_name_variable = tk.StringVar()
        self.panel_mod_name_label = ttk.Label(self.panel_mod, text = l("{ModName}"))
        self.panel_mod_name_label.grid(row = 0, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_mod_name_input = ttk.Entry(self.panel_mod, width = 37, textvariable = self.panel_mod_name_variable)
        self.panel_mod_name_input.grid(row = 0, column = 1, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_mod_name_help = ttk.Button(self.panel_mod, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{ModName}")), message = l("{ModNameHelp1}\n\n{ModNameExample}")))
        self.panel_mod_name_help.grid(row = 0, column = 2, padx = (0, 10), pady = (5, 0))
        self.panel_mod_version_variable = tk.StringVar(None, "1.0")
        self.panel_mod_version_label = ttk.Label(self.panel_mod, text = l("{ModVersion}"))
        self.panel_mod_version_label.grid(row = 1, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_mod_version_input = ttk.Entry(self.panel_mod, width = 7, textvariable = self.panel_mod_version_variable)
        self.panel_mod_version_input.grid(row = 1, column = 1, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_mod_version_help = ttk.Button(self.panel_mod, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{ModVersion}")), message = l("{ModVersionHelp1}\n\n{ModVersionExample}")))
        self.panel_mod_version_help.grid(row = 1, column = 2, padx = (0, 10), pady = (5, 0))
        self.panel_mod_author_variable = tk.StringVar()
        self.panel_mod_author_label = ttk.Label(self.panel_mod, text = l("{ModAuthor}"))
        self.panel_mod_author_label.grid(row = 2, column = 0, padx = (10, 5), pady = (5, 10), sticky = "w")
        self.panel_mod_author_input = ttk.Entry(self.panel_mod, width = 37, textvariable = self.panel_mod_author_variable)
        self.panel_mod_author_input.grid(row = 2, column = 1, padx = 5, pady = (5, 10), sticky = "w")
        self.panel_mod_author_help = ttk.Button(self.panel_mod, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{ModAuthor}")), message = l("{ModAuthorHelp1}\n\n{ModAuthorExample}")))
        self.panel_mod_author_help.grid(row = 2, column = 2, padx = (0, 10), pady = (5, 10))
        self.panel_mod.columnconfigure(0, minsize = 170)
        self.panel_mod.columnconfigure(1, minsize = 290)

        # In-Game Paint Job Info panel
        self.panel_ingame_name_variable = tk.StringVar()
        self.panel_ingame_name_label = ttk.Label(self.panel_ingame, text = l("{InGameName}"))
        self.panel_ingame_name_label.grid(row = 0, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_ingame_name_input = ttk.Entry(self.panel_ingame, width = 37, textvariable = self.panel_ingame_name_variable)
        self.panel_ingame_name_input.grid(row = 0, column = 1, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_ingame_name_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InGameName}")), message = l("{InGameNameHelp1}\n\n{InGameNameExample}")))
        self.panel_ingame_name_help.grid(row = 0, column = 2, padx = (0, 5), pady = (5, 0))
        self.panel_ingame_price_variable = tk.StringVar()
        self.panel_ingame_price_label = ttk.Label(self.panel_ingame, text = l("{InGamePrice}"))
        self.panel_ingame_price_label.grid(row = 1, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_ingame_price_input = ttk.Entry(self.panel_ingame, width = 7, textvariable = self.panel_ingame_price_variable)
        self.panel_ingame_price_input.grid(row = 1, column = 1, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_ingame_price_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InGamePrice}")), message = l("{InGamePriceHelp1}\n\n{InGamePriceExample}").format(currency = self.currency)))
        self.panel_ingame_price_help.grid(row = 1, column = 2, padx = (0, 5), pady = (5, 0))
        self.panel_ingame_default_variable = tk.BooleanVar(None, True)
        self.panel_ingame_default_checkbox = ttk.Checkbutton(self.panel_ingame, text = l(" {InGameDefault}"), variable = self.panel_ingame_default_variable, command = lambda : self.toggle_unlock_level())
        self.panel_ingame_default_checkbox.grid(row = 2, column = 0, columnspan = 2, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_ingame_default_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InGameDefault}")), message = l("{InGameDefaultHelp1}")))
        self.panel_ingame_default_help.grid(row = 2, column = 2, padx = (0, 5), pady = (5, 0))
        self.panel_ingame_unlock_variable = tk.StringVar()
        self.panel_ingame_unlock_label = ttk.Label(self.panel_ingame, text = l("{InGameUnlock}"))
        self.panel_ingame_unlock_label.grid(row = 3, column = 0, padx = (10, 5), pady = (5, 10), sticky = "w")
        self.panel_ingame_unlock_input = ttk.Entry(self.panel_ingame, width = 7, textvariable = self.panel_ingame_unlock_variable)
        self.panel_ingame_unlock_input.grid(row = 3, column = 1, padx = 5, pady = (5, 10), sticky = "w")
        self.panel_ingame_unlock_input.state(["disabled"]) # Disabled by default, as the "unlocked by default" checkbox is checked by default
        self.panel_ingame_unlock_help = ttk.Button(self.panel_ingame, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InGameUnlock}")), message = l("{InGameUnlockHelp1}\n\n{InGameUnlockExample}")))
        self.panel_ingame_unlock_help.grid(row = 3, column = 2, padx = (0, 5), pady = (5, 10))
        self.panel_ingame.columnconfigure(0, minsize = 170)
        self.panel_ingame.columnconfigure(1, minsize = 290)

        # Internal Paint Job Info panel
        self.panel_internal_name_variable = tk.StringVar()
        self.panel_internal_name_label = ttk.Label(self.panel_internal, text = l("{InternalName}"))
        self.panel_internal_name_label.grid(row = 0, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_internal_name_input = ttk.Entry(self.panel_internal, width = 15, textvariable = self.panel_internal_name_variable)
        self.panel_internal_name_input.grid(row = 0, column = 1, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_internal_name_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InternalName}")), message = l("{InternalNameHelp1}\n\n{InternalNameHelp2}\n\n{InternalNameHelp3}\n\n{InternalNameExample}").format(name_length = self.internal_name_length)))
        self.panel_internal_name_help.grid(row = 0, column = 2, padx = (0, 5), pady = (5, 0))
        self.panel_internal_supported_variable = tk.StringVar(None, l("{InternalSupportedLargest}"))
        self.panel_internal_supported_variable.trace("w", self.update_cabin_dropdowns)
        self.panel_internal_supported_label = ttk.Label(self.panel_internal, text = l("{InternalSupported}"))
        self.panel_internal_supported_label.grid(row = 4, column = 0, padx = (10, 5), pady = (5, 10), sticky = "w")
        self.panel_internal_supported_dropdown = ttk.Combobox(self.panel_internal, state = "readonly", textvariable = self.panel_internal_supported_variable, values = [l("{InternalSupportedLargest}"), l("{InternalSupportedAll}")], width = 34)
        self.panel_internal_supported_dropdown.grid(row = 4, column = 1, padx = 5, pady = (5, 10), sticky = "w")
        self.panel_internal_supported_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InternalSupported}")), message = l("{InternalSupportedHelp1}\n\n{InternalSupportedHelp2}\n\n{InternalSupportedExample}")))
        self.panel_internal_supported_help.grid(row = 4, column = 2, padx = (0, 5), pady = (5, 10))
        self.panel_internal_handling_variable = tk.StringVar(None, l("{InternalHandlingCombined}"))
        self.panel_internal_handling_variable.trace("w", self.update_cabin_dropdowns)
        self.panel_internal_handling_label = ttk.Label(self.panel_internal, text = l("{InternalHandling}"))
        # self.panel_internal_handling_label.grid(row = 5, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_internal_handling_dropdown = ttk.Combobox(self.panel_internal, state = "readonly", textvariable = self.panel_internal_handling_variable, values = [l("{InternalHandlingCombined}"), l("{InternalHandlingSeparate}")], width = 34)
        # self.panel_internal_handling_dropdown.grid(row = 5, column = 1, padx = 5, pady = (5, 0), sticky = "w")
        self.panel_internal_handling_help = ttk.Button(self.panel_internal, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{InternalHandling}")), message = l("{InternalHandlingHelp1}\n\n{InternalHandlingHelp2}\n\n{InternalHandlingHelp3}")))
        # self.panel_internal_handling_help.grid(row = 5, column = 2, padx = (0, 5), pady = (5, 0))
        # All of the handling elements are gridded only when needed, in update_cabin_dropdowns()
        self.panel_internal.columnconfigure(0, minsize = 170)
        self.panel_internal.columnconfigure(1, minsize = 290)

        # Vehicle Supported panel (single paint job)
        self.panel_single_type_variable = tk.StringVar(None, l("{Truck}"))
        self.panel_single_type_variable.trace("w", self.change_displayed_vehicle_dropdown)
        self.panel_single_type_label = ttk.Label(self.panel_vehicles_single, text = l("{VehiclesType}"))
        self.panel_single_type_label.grid(row = 0, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_single_type_dropdown = ttk.Combobox(self.panel_vehicles_single, state = "readonly", textvariable = self.panel_single_type_variable, values = [l("{Truck}"), l("{TruckMod}"), l("{Trailer}"), l("{TrailerMod}")], width = 12)
        self.panel_single_type_dropdown.grid(row = 1, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_single_vehicle_variable = tk.StringVar()
        self.panel_single_vehicle_label = ttk.Label(self.panel_vehicles_single, text = l("{VehiclesVehicle}"))
        self.panel_single_vehicle_label.grid(row = 2, column = 0, padx = (10, 5), pady = (10, 0), sticky = "w")
        self.panel_single_vehicle_dropdown = ttk.Combobox(self.panel_vehicles_single, state = "readonly", textvariable = self.panel_single_vehicle_variable, values = [], width = 45)
        self.panel_single_vehicle_dropdown.grid(row = 3, column = 0, padx = (10, 10), pady = (5, 10), sticky = "w")
        self.panel_single_link = ttk.Label(self.panel_vehicles_single, text = l("{VehiclesDownloadLink}"), foreground = self.blue, cursor = self.cursor)
        self.panel_single_link.bind("<1>", self.open_mod_link_page)
        # self.panel_single_link.grid(row = 4, column = 0, pady = 5, padx = 5, sticky = "w")

        # Vehicles Supported panel (paint job pack)
        self.panel_pack_selector = ttk.Notebook(self.panel_vehicles_pack)
        self.panel_pack_selector.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = (5, 10))
        if self.os in ["Windows", "macOS"]:
            self.panel_pack_selector.bind_all("<MouseWheel>", self.mousewheel_scroll)
        elif self.os == "Linux":
            self.panel_pack_selector.bind_all("<Button-4>", self.mousewheel_scroll)
            self.panel_pack_selector.bind_all("<Button-5>", self.mousewheel_scroll)
        self.tab_trucks = ttk.Frame(self.panel_pack_selector)
        self.tab_trucks.columnconfigure(0, weight = 1)
        self.tab_trucks.rowconfigure(0, weight = 1)
        self.panel_pack_selector.add(self.tab_trucks, text = l("{Trucks}"))
        self.tab_trailers = ttk.Frame(self.panel_pack_selector)
        self.tab_trailers.columnconfigure(0, weight = 1)
        self.tab_trailers.rowconfigure(0, weight = 1)
        self.panel_pack_selector.add(self.tab_trailers, text = l("{Trailers}"))
        self.tab_truck_mods = ttk.Frame(self.panel_pack_selector)
        self.tab_truck_mods.columnconfigure(0, weight = 1)
        self.tab_truck_mods.rowconfigure(0, weight = 1)
        self.panel_pack_selector.add(self.tab_truck_mods, text = l("{TruckMods}"))
        self.tab_bus_mods = ttk.Frame(self.panel_pack_selector)
        self.tab_bus_mods.columnconfigure(0, weight = 1)
        self.tab_bus_mods.rowconfigure(0, weight = 1)
        self.panel_pack_selector.add(self.tab_bus_mods, text = l("{BusMods}"), state = "hidden")
        self.tab_trailer_mods = ttk.Frame(self.panel_pack_selector)
        self.tab_trailer_mods.columnconfigure(0, weight = 1)
        self.tab_trailer_mods.rowconfigure(0, weight = 1)
        self.panel_pack_selector.add(self.tab_trailer_mods, text = l("{TrailerMods}"))
        self.panel_pack_link_truck = ttk.Label(self.tab_truck_mods, text = l("{VehiclesDownloadLink}"), foreground = self.blue, cursor = self.cursor)
        self.panel_pack_link_truck.bind("<1>", self.open_mod_link_page)
        self.panel_pack_link_bus = ttk.Label(self.tab_bus_mods, text = l("{VehiclesDownloadLink}"), foreground = self.blue, cursor = self.cursor)
        self.panel_pack_link_bus.bind("<1>", self.open_mod_link_page)
        self.panel_pack_link_trailer = ttk.Label(self.tab_trailer_mods, text = l("{VehiclesDownloadLink}"), foreground = self.blue, cursor = self.cursor)
        self.panel_pack_link_trailer.bind("<1>", self.open_mod_link_page)
        self.panel_vehicles_pack.rowconfigure(0, weight = 1)

        # Scrollable lists in Vehicles Supported panel
        self.scroll_canvas_trucks = tk.Canvas(self.tab_trucks, highlightthickness = 0)
        self.scroll_bar_trucks = ttk.Scrollbar(self.tab_trucks, orient = "vertical", command = self.scroll_canvas_trucks.yview)
        self.scroll_frame_trucks = ttk.Frame(self.scroll_canvas_trucks)
        self.scroll_frame_trucks.bind("<Configure>", lambda e: self.scroll_canvas_trucks.configure(scrollregion = self.scroll_canvas_trucks.bbox("all")))
        self.scroll_canvas_trucks.create_window((0, 0), window = self.scroll_frame_trucks, anchor = "nw")
        self.scroll_canvas_trucks.configure(yscrollcommand = self.scroll_bar_trucks.set)
        self.scroll_canvas_trucks.grid(row = 0, column = 0, pady = 5, sticky = "nws")
        self.scroll_bar_trucks.grid(row = 0, column = 1, pady = 5, sticky = "nes")

        self.scroll_canvas_trailers = tk.Canvas(self.tab_trailers, highlightthickness = 0)
        self.scroll_bar_trailers = ttk.Scrollbar(self.tab_trailers, orient = "vertical", command = self.scroll_canvas_trailers.yview)
        self.scroll_frame_trailers = ttk.Frame(self.scroll_canvas_trailers)
        self.scroll_frame_trailers.bind("<Configure>", lambda e: self.scroll_canvas_trailers.configure(scrollregion = self.scroll_canvas_trailers.bbox("all")))
        self.scroll_canvas_trailers.create_window((0, 0), window = self.scroll_frame_trailers, anchor = "nw")
        self.scroll_canvas_trailers.configure(yscrollcommand = self.scroll_bar_trailers.set)
        self.scroll_canvas_trailers.grid(row = 0, column = 0, pady = 5, sticky = "nws")
        self.scroll_bar_trailers.grid(row = 0, column = 1, pady = 5, sticky = "nes")

        self.scroll_canvas_truck_mods = tk.Canvas(self.tab_truck_mods, highlightthickness = 0)
        self.scroll_bar_truck_mods = ttk.Scrollbar(self.tab_truck_mods, orient = "vertical", command = self.scroll_canvas_truck_mods.yview)
        self.scroll_frame_truck_mods = ttk.Frame(self.scroll_canvas_truck_mods)
        self.scroll_frame_truck_mods.bind("<Configure>", lambda e: self.scroll_canvas_truck_mods.configure(scrollregion = self.scroll_canvas_truck_mods.bbox("all")))
        self.scroll_canvas_truck_mods.create_window((0, 0), window = self.scroll_frame_truck_mods, anchor = "nw")
        self.scroll_canvas_truck_mods.configure(yscrollcommand = self.scroll_bar_truck_mods.set)
        self.scroll_canvas_truck_mods.grid(row = 0, column = 0, pady = 5, sticky = "nws")
        self.scroll_bar_truck_mods.grid(row = 0, rowspan = 2, column = 1, pady = 5, sticky = "nes")

        self.scroll_canvas_bus_mods = tk.Canvas(self.tab_bus_mods, highlightthickness = 0)
        self.scroll_bar_bus_mods = ttk.Scrollbar(self.tab_bus_mods, orient = "vertical", command = self.scroll_canvas_bus_mods.yview)
        self.scroll_frame_bus_mods = ttk.Frame(self.scroll_canvas_bus_mods)
        self.scroll_frame_bus_mods.bind("<Configure>", lambda e: self.scroll_canvas_bus_mods.configure(scrollregion = self.scroll_canvas_bus_mods.bbox("all")))
        self.scroll_canvas_bus_mods.create_window((0, 0), window = self.scroll_frame_bus_mods, anchor = "nw")
        self.scroll_canvas_bus_mods.configure(yscrollcommand = self.scroll_bar_bus_mods.set)
        self.scroll_canvas_bus_mods.grid(row = 0, column = 0, pady = 5, sticky = "nws")
        self.scroll_bar_bus_mods.grid(row = 0, rowspan = 2, column = 1, pady = 5, sticky = "nes")

        self.scroll_canvas_trailer_mods = tk.Canvas(self.tab_trailer_mods, highlightthickness = 0)
        self.scroll_bar_trailer_mods = ttk.Scrollbar(self.tab_trailer_mods, orient = "vertical", command = self.scroll_canvas_trailer_mods.yview)
        self.scroll_frame_trailer_mods = ttk.Frame(self.scroll_canvas_trailer_mods)
        self.scroll_frame_trailer_mods.bind("<Configure>", lambda e: self.scroll_canvas_trailer_mods.configure(scrollregion = self.scroll_canvas_trailer_mods.bbox("all")))
        self.scroll_canvas_trailer_mods.create_window((0, 0), window = self.scroll_frame_trailer_mods, anchor = "nw")
        self.scroll_canvas_trailer_mods.configure(yscrollcommand = self.scroll_bar_trailer_mods.set)
        self.scroll_canvas_trailer_mods.grid(row = 0, column = 0, pady = 5, sticky = "nws")
        self.scroll_bar_trailer_mods.grid(row = 0, rowspan = 2, column = 1, pady = 5, sticky = "nes")

        # Buttons along the bottom
        self.panel_main_buttons_setup = ttk.Button(self.panel_main_buttons, text = l("< {BackToSetup}"), command = lambda : self.switch_to_setup_screen())
        self.panel_main_buttons_setup.grid(row = 1, column = 0, pady = (5, 0), sticky = "w")
        self.panel_main_buttons_feedback = ttk.Label(self.panel_main_buttons, text = l("{LeaveFeedback}"), foreground = self.blue, cursor = self.cursor)
        self.panel_main_buttons_feedback.grid(row = 1, column = 1, pady = (5, 0), padx = 10, sticky = "e")
        self.panel_main_buttons_feedback.bind("<1>", lambda e: webbrowser.open_new(FORUM_LINK))
        self.panel_main_buttons_generate = ttk.Button(self.panel_main_buttons, text = l("{GenerateSave}"), command = lambda : self.verify_all_inputs())
        self.panel_main_buttons_generate.grid(row = 1, column = 2, pady = (5, 0), sticky = "e")

        # Generate screen
        self.generate_screen = ttk.Frame(self.container)
        self.panel_generating = ttk.LabelFrame(self.generate_screen, text = l("{GeneratingOptions}"))
        self.panel_generating.grid(row = 0, column = 0, pady = (0, 5), sticky = "ew")
        self.panel_directory = ttk.LabelFrame(self.generate_screen, text = l("{SaveDirectory}"))
        self.panel_directory.grid(row = 1, column = 0, pady = (0, 5), sticky = "ew")
        self.panel_progress = ttk.LabelFrame(self.generate_screen, text = l("{GeneratingProgress}"))
        self.panel_progress.grid(row = 2, column = 0, pady = (0, 5), sticky = "ew")
        self.panel_gen_buttons = ttk.Frame(self.generate_screen)
        self.panel_gen_buttons.grid(row = 3, column = 0, sticky = "ew")

        # Generating Options panel
        self.panel_generating_workshop_variable = tk.BooleanVar(None, False)
        self.panel_generating_workshop_checkbox = ttk.Checkbutton(self.panel_generating, text = l("{GenerateWorkshop}"), variable = self.panel_generating_workshop_variable)
        self.panel_generating_workshop_checkbox.grid(row = 0, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_generating_workshop_help = ttk.Button(self.panel_generating, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{GenerateWorkshop}")), message = l("{GenerateWorkshopHelp1}\n\n{GenerateWorkshopHelp2}")))
        self.panel_generating_workshop_help.grid(row = 0, column = 1, padx = (0, 5), pady = (5, 0))
        self.panel_generating_templates_variable = tk.BooleanVar(None, False)
        self.panel_generating_templates_checkbox = ttk.Checkbutton(self.panel_generating, text = l("{GenerateTemplates}"), variable = self.panel_generating_templates_variable)
        self.panel_generating_templates_checkbox.grid(row = 1, column = 0, padx = (10, 20), pady = (5, 0), sticky = "w")
        self.panel_generating_templates_help = ttk.Button(self.panel_generating, text = "?", width = 3, command = lambda : messagebox.showinfo(title = l(l("{HelpTitle}").format(topic = "{GenerateTemplates}")), message = l("{GenerateTemplatesHelp1}\n\n{GenerateTemplatesHelp2}")))
        self.panel_generating_templates_help.grid(row = 1, column = 1, padx = (0, 5), pady = 5)
        self.panel_generating.columnconfigure(0, weight = 1)

        # Save Directory panel
        self.panel_directory_change_label = ttk.Label(self.panel_directory, text = l("{CurrentDirectory}"))
        self.panel_directory_change_label.grid(row = 0, column = 0, columnspan = 2, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_directory_change_button = ttk.Button(self.panel_directory, text = l("{ChangeDirectory}"), command = self.ask_save_location)
        self.panel_directory_change_button.grid(row = 0, column = 2, padx = (0, 5))
        self.panel_directory_current_variable = tk.StringVar(None, desktop_path.replace("\\", "/"))
        self.panel_directory_current_label = ttk.Label(self.panel_directory, textvariable = self.panel_directory_current_variable)
        self.panel_directory_current_label.grid(row = 1, column = 0, columnspan = 3, padx = (10, 5), pady = (5, 0), sticky = "w")
        self.panel_directory_note_label = ttk.Label(self.panel_directory, text = l("{SubfolderCreated}"))
        self.panel_directory_note_label.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 10)
        self.panel_directory.columnconfigure(0, weight = 1)

        # Progress panel
        self.progress_value = tk.DoubleVar(None, 0.0)
        self.panel_progress_bar = ttk.Progressbar(self.panel_progress, orient = "horizontal", mode = "determinate", variable = self.progress_value)
        self.panel_progress_bar.grid(row = 0, column = 0, padx = 10, pady = (15, 10), sticky = "ew")
        self.panel_progress_category_variable = tk.StringVar(None, l("{ProgressReady}"))
        self.panel_progress_category_label = ttk.Label(self.panel_progress, textvariable = self.panel_progress_category_variable)
        self.panel_progress_category_label.grid(row = 1, column = 0, padx = 5, pady = (5, 0))
        self.panel_progress_specific_variable = tk.StringVar(None, l("{ProgressAppearHere}"))
        self.panel_progress_specific_label = ttk.Label(self.panel_progress, textvariable = self.panel_progress_specific_variable)
        self.panel_progress_specific_label.grid(row = 2, column = 0, padx = 5, pady = 5)
        self.panel_progress.columnconfigure(0, weight = 1)

        # Generating buttons
        self.panel_gen_buttons_back = ttk.Button(self.panel_gen_buttons, text = l("< {Back}"), command = self.change_from_generate_to_main)
        self.panel_gen_buttons_back.grid(row = 0, column = 0, pady = (5, 0), sticky = "w")
        self.panel_gen_buttons_generate = ttk.Button(self.panel_gen_buttons, text = l("{Generate}"), command = lambda : self.check_if_folder_clear(self.panel_directory_current_variable.get()))
        self.panel_gen_buttons_generate.grid(row = 0, column = 1, pady = (5, 0), sticky = "e")
        self.panel_gen_buttons.columnconfigure(0, weight = 1)

        # Error popup
        self.error_screen = tk.Frame(self.container)
        self.error_top_text = ttk.Label(self.error_screen, text = l("{FancyTitle}"), justify = "center")
        self.error_top_text.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = (40, 20))
        self.error_text = tk.Text(self.error_screen, height = 10, width = 65)
        self.error_text.grid(row = 1, column = 0, columnspan = 2, padx = 20)
        self.error_please_text = ttk.Label(self.error_screen, text = l("{FancyPlease}"), justify = "center")
        self.error_please_text.grid(row = 2, column = 0, columnspan = 2, padx = 20, pady = (40, 0))
        self.error_send_button = ttk.Button(self.error_screen, text = l("{FancySend}"), command = self.send_error)
        self.error_send_button.grid(row = 3, column = 0, pady = 20, padx = 10, sticky = "ne")
        self.error_dont_send_button = ttk.Button(self.error_screen, text = l("{FancyDontSend}"), command = lambda : sys.exit())
        self.error_dont_send_button.grid(row = 3, column = 1, pady = 20, padx = 10, sticky = "nw")
        self.error_sorry_text = ttk.Label(self.error_screen, text = l("{FancySorry}"))
        self.error_sorry_text.grid(row = 4, column = 0, columnspan = 2, padx = 20, pady = (20, 40))

        master.report_callback_exception = self.show_fancy_error # It's now safe to use the fancy error screen instead of the messagebox

    def load_language_list(self):
        self.language_names_dictionary = {}
        self.language_names_list = []
        for lang_code in os.listdir("lang"):
            lang_code = lang_code[:-4] # Remove .ini from end
            new_lang = configparser.ConfigParser(inline_comment_prefixes=";")
            new_lang.read("lang/{}.ini".format(lang_code), encoding="utf-8")
            self.language_names_dictionary[lang_code] = new_lang["General"]["languagename"]
            self.language_names_list.append(new_lang["General"]["languagename"])
        self.language_names_list.remove(self.language_names_dictionary[self.language])
        self.language_names_list.insert(0, self.language_names_dictionary[self.language])

    def load_language_dictionary(self, language):
        language_ini = configparser.ConfigParser(inline_comment_prefixes=";")
        language_ini.optionxform = str # Maintains capitals in key names
        language_ini.read("lang/{}.ini".format(language), encoding="utf-8")
        language_dict = {}
        for section in language_ini.sections():
            for item in language_ini.items(section):
                language_dict[item[0]] = item[1]
        self.language_dictionary = language_dict

    def reload_with_language(self, *args):
        if self.tab_welcome_language_variable.get() != self.language_names_dictionary[self.language]:
            print("Reloading in " + self.tab_welcome_language_variable.get())
            for language_code in self.language_names_dictionary:
                if self.language_names_dictionary[language_code] == self.tab_welcome_language_variable.get():
                    restart_app(language_code)

    def get_localised_string(self, string):
        # Turn all {placeholder}s into {language_dict[placeholder]}s
        string = string.replace("{", "{lang_dict[").replace("}", "]}")
        return string.format(lang_dict = self.language_dictionary)

    def show_fancy_error(self, error_type, error_message, error_traceback):
        print("\a")
        self.setup_screen.grid_forget()
        self.main_screen.grid_forget()
        self.generate_screen.grid_forget()
        self.error_screen.grid(row = 0, column = 0)
        self.error_text.delete("1.0", "end")
        self.error_text.insert("1.0", "{}: {}\n\nTraceback:\n{}".format(error_type.__name__, str(error_message), "\n".join(traceback.format_list(traceback.extract_tb(error_traceback)))))
        self.error_text.insert("1.0", "Language: {}\n\n".format(self.language))
        self.error_text.insert("1.0", "{}\nVersion {} ({})\n\n".format(date.today(), version, self.os))

    def send_error(self, *args):
        self.error_send_button.configure(text = self.get_localised_string("{FancySending}"))
        self.error_send_button.state(["disabled"])
        self.error_send_button.update()
        self.error_dont_send_button.state(["disabled"])
        self.error_dont_send_button.update()
        print("Sending crash report to Developer...")
        url1 = "https://discord.com/api/webhooks/"
        url2 = 1869225424928931840
        url3 = "/4fZ_MFVq2Hp5WDa1oMR3gaj*3AsgDVp*A8a_c_21TlawqH*t*ksrn90oC2JJ1Ocm-Uq5nJ875O_"
        try:
            if len(self.error_text.get("6.0", "end")) < 600:
                first_line = ""
            else:
                first_line = self.error_text.get("6.0", "end").split("\n")[0] + "\n\n..."
            # This is near-useless obfuscation, but it's better than nothing... right?
            notifier = webhook.DiscordWebhook(url = url1 + str(url2 >> 1) + url3[:-7].replace("*", "P").replace("_", "d").replace("q", "6").replace("a", "I").replace("2", "G"),
                                              content = "New crash report from version {} ({}):\n```{}{}```\n".format(version, self.os, first_line, self.error_text.get("6.0", "end")[-600:]))
            response = notifier.execute()
        except Exception as e:
            # Still try something
            print("Something went wrong, the crash report couldn't be sent")
        sys.exit()

    def credits_screen(self, *args):
        l = self.get_localised_string

        credits = tk.Tk()
        credits.tk.call("source", "sun-valley.tcl")
        try:
            if darkdetect.isDark():
                credits.tk.call("set_theme", "dark")
                credits.blue = "#56C7FE"
            else:
                credits.tk.call("set_theme", "light")
                credits.blue = "#006DD3"
        except NameError:
            credits.tk.call("set_theme", "light")
            credits.blue = "#006DD3"
        if sys.platform.startswith("darwin"):
            credits.cursor = "pointinghand"
        else:
            credits.cursor = "hand2"
        credits.title(l("{About}"))
        credits.resizable(False, False)
        credits.lift()
        credits.columnconfigure(0, weight = 1)
        credits.columnconfigure(1, weight = 1)
        credits.button = ttk.Button(credits, text = l("{Close}"), command = lambda : credits.destroy())
        credits.button.grid(row = 3, column = 0, columnspan = 2, pady = (10, 15))

        credits.tab_selector = ttk.Notebook(credits)
        credits.tab_selector.grid(row = 0, column = 0, padx = 5, pady = 5)
        credits.pjp_frame = ttk.Frame(credits.tab_selector)
        credits.tab_selector.add(credits.pjp_frame, text = "Paint Job Packer")
        credits.sunval_frame = ttk.Frame(credits.tab_selector)
        credits.tab_selector.add(credits.sunval_frame, text = "Sun Valley Theme")
        credits.darkdetect_frame = ttk.Frame(credits.tab_selector)
        credits.tab_selector.add(credits.darkdetect_frame, text = "Darkdetect")
        credits.rudder_frame = ttk.Frame(credits.tab_selector)
        credits.tab_selector.add(credits.rudder_frame, text = "RudderStack Python SDK")
        credits.webhook_frame = ttk.Frame(credits.tab_selector)
        credits.tab_selector.add(credits.webhook_frame, text = "Python Discord Webhook")
        credits.analytics_frame = ttk.Frame(credits.tab_selector)
        credits.tab_selector.add(credits.analytics_frame, text = l("{AnalyticsTitle}"))

        credits.pjp_frame.columnconfigure(0, weight = 1)
        credits.pjp_frame.columnconfigure(2, weight = 1)
        credits.pjp_title = ttk.Label(credits.pjp_frame, text = "Paint Job Packer", justify = "center")
        credits.pjp_title.grid(row = 0, column = 0, columnspan = 3, pady = (20, 0))
        credits.pjp_link = ttk.Label(credits.pjp_frame, text = l("{LinkGithub}"), justify = "center", foreground = credits.blue, cursor = credits.cursor)
        credits.pjp_link.grid(row = 1, column = 0, columnspan = 3, pady = (5, 10))
        credits.pjp_link.bind("<1>", lambda e: webbrowser.open_new(GITHUB_LINK))
        credits.pjp_dev_title = ttk.Label(credits.pjp_frame, text = l("{AboutDeveloper}"))
        credits.pjp_dev_title.grid(row = 2, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.pjp_dev_name = ttk.Label(credits.pjp_frame, text = "Carsmaniac")
        credits.pjp_dev_name.grid(row = 2, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.pjp_contributors_title = ttk.Label(credits.pjp_frame, text = l("{AboutContributors}"))
        credits.pjp_contributors_title.grid(row = 3, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.pjp_contributors_names = ttk.Label(credits.pjp_frame, text = "djbusphotos\nkentuckyfriedmeerkat")
        credits.pjp_contributors_names.grid(row = 3, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.pjp_translators_title = ttk.Label(credits.pjp_frame, text = l("{AboutTranslators}"))
        credits.pjp_translators_title.grid(row = 5, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.pjp_translators_names_1 = ttk.Label(credits.pjp_frame, text = "Angel Praxedis\nCitadis\nEtrusan\ngertjan038\nJ P\nKebas53\nLeving PT\nOle Løvland Stegane")
        credits.pjp_translators_names_1.grid(row = 5, column = 1, padx = (0, 15), pady = 5, sticky = "nw")
        credits.pjp_translators_names_2 = ttk.Label(credits.pjp_frame, text = "Oleg Popenkov\nRasmus Schack\nScrooge62\nSr_GustavoTv")
        credits.pjp_translators_names_2.grid(row = 5, column = 2, padx = 15, pady = 5, sticky = "nw")
        credits.pjp_translators_link = ttk.Label(credits.pjp_frame, text = l("{LinkTranslate}"), foreground = self.blue, cursor = self.cursor)
        credits.pjp_translators_link.grid(row = 6, column = 1, columnspan = 2, padx = (0, 20), sticky = "nw")
        credits.pjp_translators_link.bind("<1>", lambda e: webbrowser.open_new(CROWDIN_LINK))
        credits.pjp_supporters_title = ttk.Label(credits.pjp_frame, text = l("{AboutSupporters}"))
        # credits.pjp_supporters_title.grid(row = 7, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.pjp_supporters_names = ttk.Label(credits.pjp_frame, text = "Name\nName")
        # credits.pjp_supporters_names.grid(row = 7, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.pjp_licence = ttk.Label(credits.pjp_frame, text = l("{AboutMIT}"), foreground = credits.blue, cursor = credits.cursor)
        credits.pjp_licence.grid(row = 8, column = 0, columnspan = 3, padx = 20, pady = 15)
        credits.pjp_licence.bind("<1>", lambda e: webbrowser.open_new(MIT_LICENCE_LINK))

        credits.sunval_frame.columnconfigure(0, weight = 2)
        credits.sunval_frame.columnconfigure(1, weight = 3)
        credits.sunval_title = ttk.Label(credits.sunval_frame, text = "Sun Valley Theme", justify = "center")
        credits.sunval_title.grid(row = 0, column = 0, columnspan = 2, pady = (20, 0))
        credits.sunval_link = ttk.Label(credits.sunval_frame, text = l("{LinkGithub}"), justify = "center", foreground = credits.blue, cursor = credits.cursor)
        credits.sunval_link.grid(row = 1, column = 0, columnspan = 2, pady = (5, 10))
        credits.sunval_link.bind("<1>", lambda e: webbrowser.open_new(SUN_VALLEY_LINK))
        credits.sunval_dev_title = ttk.Label(credits.sunval_frame, text = l("{AboutDeveloper}"))
        credits.sunval_dev_title.grid(row = 2, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.sunval_dev_name = ttk.Label(credits.sunval_frame, text = "rdbende")
        credits.sunval_dev_name.grid(row = 2, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.sunval_contributors_title = ttk.Label(credits.sunval_frame, text = l("{AboutContributors}"))
        credits.sunval_contributors_title.grid(row = 3, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.sunval_contributors_name = ttk.Label(credits.sunval_frame, text = "sumeshir26")
        credits.sunval_contributors_name.grid(row = 3, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.sunval_licence = ttk.Label(credits.sunval_frame, text = l("{AboutMIT}"), foreground = credits.blue, cursor = credits.cursor)
        credits.sunval_licence.grid(row = 4, column = 0, columnspan = 2, padx = 20, pady = 15)
        credits.sunval_licence.bind("<1>", lambda e: webbrowser.open_new(MIT_LICENCE_LINK))

        credits.darkdetect_frame.columnconfigure(0, weight = 2)
        credits.darkdetect_frame.columnconfigure(1, weight = 3)
        credits.darkdetect_title = ttk.Label(credits.darkdetect_frame, text = "Darkdetect", justify = "center")
        credits.darkdetect_title.grid(row = 0, column = 0, columnspan = 2, pady = (20, 0))
        credits.darkdetect_link = ttk.Label(credits.darkdetect_frame, text = l("{LinkGithub}"), justify = "center", foreground = credits.blue, cursor = credits.cursor)
        credits.darkdetect_link.grid(row = 1, column = 0, columnspan = 2, pady = (5, 10))
        credits.darkdetect_link.bind("<1>", lambda e: webbrowser.open_new(DARKDETECT_LINK))
        credits.darkdetect_dev_title = ttk.Label(credits.darkdetect_frame, text = l("{AboutDeveloper}"))
        credits.darkdetect_dev_title.grid(row = 2, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.darkdetect_dev_name = ttk.Label(credits.darkdetect_frame, text = "Alberto Sottile")
        credits.darkdetect_dev_name.grid(row = 2, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.darkdetect_contributors_title = ttk.Label(credits.darkdetect_frame, text = l("{AboutContributors}"))
        credits.darkdetect_contributors_title.grid(row = 3, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.darkdetect_contributors_name = ttk.Label(credits.darkdetect_frame, text = "cboy343\nEric Larson\nHussain\nSayyid\n✨小透明・宸✨")
        credits.darkdetect_contributors_name.grid(row = 3, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.darkdetect_licence = ttk.Label(credits.darkdetect_frame, text = l("{AboutBSD}"), foreground = credits.blue, cursor = credits.cursor)
        credits.darkdetect_licence.grid(row = 4, column = 0, columnspan = 2, padx = 20, pady = 15)
        credits.darkdetect_licence.bind("<1>", lambda e: webbrowser.open_new(BSD_LICENCE_LINK))

        credits.rudder_frame.columnconfigure(0, weight = 1)
        credits.rudder_frame.columnconfigure(3, weight = 1)
        credits.rudder_title = ttk.Label(credits.rudder_frame, text = "RudderStack Python SDK", justify = "center")
        credits.rudder_title.grid(row = 0, column = 0, columnspan = 4, pady = (20, 0))
        credits.rudder_link = ttk.Label(credits.rudder_frame, text = l("{LinkGithub}"), justify = "center", foreground = credits.blue, cursor = credits.cursor)
        credits.rudder_link.grid(row = 1, column = 0, columnspan = 4, pady = (5, 10))
        credits.rudder_link.bind("<1>", lambda e: webbrowser.open_new(RUDDERSTACK_LINK))
        credits.rudder_dev_title = ttk.Label(credits.rudder_frame, text = l("{AboutDeveloper}"))
        credits.rudder_dev_title.grid(row = 2, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.rudder_dev_name = ttk.Label(credits.rudder_frame, text = "RudderStack")
        credits.rudder_dev_name.grid(row = 2, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.rudder_contributors_title = ttk.Label(credits.rudder_frame, text = l("{AboutContributors}"))
        credits.rudder_contributors_title.grid(row = 3, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.rudder_contributors_name_1 = ttk.Label(credits.rudder_frame, text = "Adam Johnson\nAlex Louden\nAmey Varangaonkar\nAmir Abushared\nAndrew Thal\nAndrii Sherepa\nArnab\nBitdeli Chef\nCalvin French-Owen\ndailycoding\nDamian Cirotteau\nDebanjan Chatterjee\nDi Wu")
        credits.rudder_contributors_name_1.grid(row = 3, column = 1, padx = (0, 15), pady = 5, sticky = "nw")
        credits.rudder_contributors_name_2 = ttk.Label(credits.rudder_frame, text = "dsjackins\nEirik Martiniussen Sylliaas\nEmil Sadek\nFathy Boundjadj\nHadrien David\nIan Storm Taylor\nJeff Hu\nJustin Henck\nkehn\nKelly Lu\nNico Esteves\nNhi Nguyen\nPaul Kuruvilla")
        credits.rudder_contributors_name_2.grid(row = 3, column = 2, padx = 15, pady = 5, sticky = "nw")
        credits.rudder_contributors_name_3 = ttk.Label(credits.rudder_frame, text = "Paul Oswald\npberganza\nPrateek Srivastava\nRyan\nSai Kumar B\nStefan Wójcik\nThomas Grainger\nTomasz Kolinko")
        credits.rudder_contributors_name_3.grid(row = 3, column = 3, padx = 15, pady = 5, sticky = "nw")
        credits.rudder_licence = ttk.Label(credits.rudder_frame, text = l("{AboutMIT}"), foreground = credits.blue, cursor = credits.cursor)
        credits.rudder_licence.grid(row = 4, column = 0, columnspan = 4, padx = 20, pady = 15)
        credits.rudder_licence.bind("<1>", lambda e: webbrowser.open_new(MIT_LICENCE_LINK))

        credits.webhook_frame.columnconfigure(0, weight = 2)
        credits.webhook_frame.columnconfigure(1, weight = 3)
        credits.webhook_title = ttk.Label(credits.webhook_frame, text = "Python Discord Webhook", justify = "center")
        credits.webhook_title.grid(row = 0, column = 0, columnspan = 2, pady = (20, 0))
        credits.webhook_link = ttk.Label(credits.webhook_frame, text = l("{LinkGithub}"), justify = "center", foreground = credits.blue, cursor = credits.cursor)
        credits.webhook_link.grid(row = 1, column = 0, columnspan = 2, pady = (5, 10))
        credits.webhook_link.bind("<1>", lambda e: webbrowser.open_new(DISCORD_WEBHOOK_LINK))
        credits.webhook_dev_title = ttk.Label(credits.webhook_frame, text = l("{AboutDeveloper}"))
        credits.webhook_dev_title.grid(row = 2, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.webhook_dev_name = ttk.Label(credits.webhook_frame, text = "lovvskillz")
        credits.webhook_dev_name.grid(row = 2, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.webhook_contributors_title = ttk.Label(credits.webhook_frame, text = l("{AboutContributors}"))
        credits.webhook_contributors_title.grid(row = 3, column = 0, padx = (20, 10), pady = 5, sticky = "ne")
        credits.webhook_contributors_name = ttk.Label(credits.webhook_frame, text = "Almaz\nChaitanya Chinni\nDe La Roche Constantin\nLaird Streak\nMajor Hayden\nnova\nPriyanshu Jindal\nTithen-Firion\nValtteri\nWebTax")
        credits.webhook_contributors_name.grid(row = 3, column = 1, padx = (0, 20), pady = 5, sticky = "nw")
        credits.webhook_licence = ttk.Label(credits.webhook_frame, text = l("{AboutMIT}"), foreground = credits.blue, cursor = credits.cursor)
        credits.webhook_licence.grid(row = 4, column = 0, columnspan = 2, padx = 20, pady = 15)
        credits.webhook_licence.bind("<1>", lambda e: webbrowser.open_new(MIT_LICENCE_LINK))

        credits.analytics_frame.columnconfigure(0, weight = 1)
        credits.analytics_frame.columnconfigure(2, weight = 1)
        credits.analytics_title = ttk.Label(credits.analytics_frame, text = l("{AnalyticsTitle}"), justify = "center")
        credits.analytics_title.grid(row = 0, column = 0, columnspan = 3, pady = (20, 10))
        credits.analytics_1 = ttk.Label(credits.analytics_frame, text = l("{Analytics1}"), justify = "left", wraplength = 500)
        credits.analytics_1.grid(row = 1, column = 1, pady = (5, 15), padx = 20, sticky = "nw")
        credits.analytics_2 = ttk.Label(credits.analytics_frame, text = l("{Analytics2}").format(version = version), justify = "left", wraplength = 500)
        credits.analytics_2.grid(row = 2, column = 1, pady = 2, padx = 20, sticky = "nw")
        credits.analytics_3 = ttk.Label(credits.analytics_frame, text = l("{Analytics3}").format(operating_system = self.os), justify = "left", wraplength = 500)
        credits.analytics_3.grid(row = 3, column = 1, pady = 2, padx = 20, sticky = "nw")
        credits.analytics_4 = ttk.Label(credits.analytics_frame, text = l("{Analytics4}").format(language = system_lang), justify = "left", wraplength = 500)
        credits.analytics_4.grid(row = 4, column = 1, pady = 2, padx = 20, sticky = "nw")
        credits.analytics_5 = ttk.Label(credits.analytics_frame, text = l("{Analytics5}"), justify = "left", wraplength = 500)
        credits.analytics_5.grid(row = 5, column = 1, pady = (2, 15), padx = 20, sticky = "nw")
        credits.analytics_6 = ttk.Label(credits.analytics_frame, text = l("{Analytics6}"), justify = "left", wraplength = 500)
        credits.analytics_6.grid(row = 6, column = 1, pady = (5, 2), padx = 20, sticky = "nw")
        credits.analytics_7 = ttk.Label(credits.analytics_frame, text = l("{Analytics7}"), justify = "left", wraplength = 500)
        credits.analytics_7.grid(row = 7, column = 1, pady = (5, 15), padx = 20, sticky = "nw")
        credits.analytics_8 = ttk.Label(credits.analytics_frame, text = l("{Analytics8}"), justify = "left", wraplength = 500, cursor = credits.cursor)
        credits.analytics_8.grid(row = 8, column = 1, pady = (5, 2), padx = 20, sticky = "nw")
        credits.analytics_8.bind("<1>", lambda e: webbrowser.open_new(ANALYTICS_SCRIPT_LINK))
        credits.analytics_9 = ttk.Label(credits.analytics_frame, text = l("{Analytics9}"), justify = "left", wraplength = 500)
        credits.analytics_9.grid(row = 9, column = 1, pady = (10, 20), padx = 20, sticky = "nw")

    def update_cabin_dropdowns(self, *args):
        l = self.get_localised_string
        self.internal_name_length = 12
        self.panel_internal_supported_label.grid_forget()
        self.panel_internal_supported_dropdown.grid_forget()
        self.panel_internal_supported_help.grid_forget()
        self.panel_internal_handling_label.grid_forget()
        self.panel_internal_handling_dropdown.grid_forget()
        self.panel_internal_handling_help.grid_forget()
        if self.panel_internal_supported_variable.get() == l("{InternalSupportedLargest}"):
            self.panel_internal_supported_label.grid(row = 4, column = 0, padx = (10, 5), pady = (5, 10), sticky = "w")
            self.panel_internal_supported_dropdown.grid(row = 4, column = 1, padx = 5, pady = (5, 10), sticky = "w")
            self.panel_internal_supported_help.grid(row = 4, column = 2, padx = (0, 5), pady = (5, 10))
        elif self.panel_internal_supported_variable.get() == l("{InternalSupportedAll}"):
            self.panel_internal_supported_label.grid(row = 4, column = 0, padx = (10, 5), pady = (5, 0), sticky = "w")
            self.panel_internal_supported_dropdown.grid(row = 4, column = 1, padx = 5, pady = (5, 0), sticky = "w")
            self.panel_internal_supported_help.grid(row = 4, column = 2, padx = (0, 5), pady = (5, 0))
            self.panel_internal_handling_label.grid(row = 5, column = 0, padx = (10, 5), pady = (5, 10), sticky = "w")
            self.panel_internal_handling_dropdown.grid(row = 5, column = 1, padx = 5, pady = (5, 10), sticky = "w")
            self.panel_internal_handling_help.grid(row = 5, column = 2, padx = (0, 5), pady = (5, 10))

            if self.panel_internal_handling_variable.get() == l("{InternalHandlingSeparate}"):
                self.internal_name_length = 10

    def switch_to_setup_screen(self):
        if self.tab_paintjob_variable.get() == "single":
            self.panel_vehicles_single.grid_forget()
        elif self.tab_paintjob_variable.get() == "pack":
            self.panel_vehicles_pack.grid_forget()
        self.main_screen.grid_forget()
        self.setup_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

        for veh in self.truck_list + self.truck_mod_list + self.bus_mod_list + self.trailer_list + self.trailer_mod_list:
            veh.check.grid_forget()

        self.panel_pack_link_truck.grid_forget() # Just in case it changes location
        self.panel_pack_link_bus.grid_forget()
        self.panel_pack_link_trailer.grid_forget()

        self.scroll_bar_trucks.grid_forget()
        self.scroll_bar_trailers.grid_forget()
        self.scroll_bar_truck_mods.grid_forget()
        self.scroll_bar_bus_mods.grid_forget()
        self.scroll_bar_trailer_mods.grid_forget()

    def switch_to_main_screen(self):
        self.setup_screen.grid_forget()
        self.main_screen.grid(row = 0, column = 0, padx = 10, pady = 10)
        if self.tab_paintjob_variable.get() == "single":
            self.panel_vehicles_single.grid(row = 0, column = 1, rowspan = 3, sticky = "ns", padx = (10, 0))
        elif self.tab_paintjob_variable.get() == "pack":
            self.panel_vehicles_pack.grid(row = 0, column = 1, rowspan = 3, sticky = "ns", padx = (10, 0))
        self.load_main_screen_variables()
        self.update_cabin_dropdowns()

    def load_main_screen_variables(self): # Also grids and ungrids elements depending on said variables
        l = self.get_localised_string
        self.scroll_bar_trucks.grid(row = 0, column = 1, pady = 5, sticky = "nes")
        self.scroll_bar_trailers.grid(row = 0, column = 1, pady = 5, sticky = "nes")
        self.scroll_bar_truck_mods.grid(row = 0, rowspan = 2, column = 1, pady = 5, sticky = "nes")
        self.scroll_bar_bus_mods.grid(row = 0, rowspan = 2, column = 1, pady = 5, sticky = "nes")
        self.scroll_bar_trailer_mods.grid(row = 0, rowspan = 2, column = 1, pady = 5, sticky = "nes")

        if self.tab_game_variable.get() == "ats":
            self.currency = l("{InGamePriceDollars}")
            self.panel_pack_selector.tab(3, state = "hidden")
            self.panel_single_type_dropdown.config(values = [l("{Truck}"), l("{TruckMod}"), l("{Trailer}"), l("{TrailerMod}")])
            self.scroll_bar_trucks.grid_forget() # These lists don't need to scroll
            self.scroll_bar_trailers.grid_forget()
            self.scroll_bar_bus_mods.grid_forget()
        elif self.tab_game_variable.get() == "ets":
            self.currency = l("{InGamePriceEuros}")
            self.panel_pack_selector.tab(3, state = "normal")
            self.panel_single_type_dropdown.config(values = [l("{Truck}"), l("{TruckMod}"), l("{BusMod}"), l("{Trailer}"), l("{TrailerMod}")])
            self.scroll_bar_trailers.grid_forget()
            self.scroll_bar_bus_mods.grid_forget()

        self.check_for_outdated_vehicles(self.tab_game_variable.get())

        (self.truck_list, self.truck_mod_list, self.bus_mod_list, self.trailer_list, self.trailer_mod_list) = self.load_list_of_vehicles(self.tab_game_variable.get())

        for i in range(len(self.truck_list)):
            self.truck_list[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.truck_mod_list)):
            self.truck_mod_list[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.bus_mod_list)):
            self.bus_mod_list[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.trailer_list)):
            self.trailer_list[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)
        for i in range(len(self.trailer_mod_list)):
            self.trailer_mod_list[i].check.grid(row = i, column = 0, sticky = "w", padx = 5)

        self.panel_pack_link_truck.grid(row = 1, column = 0, sticky = "w", padx = 8, pady = (0, 5))
        self.panel_pack_link_bus.grid(row = 1, column = 0, sticky = "w", padx = 8, pady = (0, 5))
        self.panel_pack_link_trailer.grid(row = 1, column = 0, sticky = "w", padx = 8, pady = (0, 5))

        self.scroll_canvas_trucks.yview_moveto(0)
        self.scroll_canvas_trailers.yview_moveto(0)
        self.scroll_canvas_truck_mods.yview_moveto(0)
        self.scroll_canvas_bus_mods.yview_moveto(0)
        self.scroll_canvas_trailer_mods.yview_moveto(0)

        self.change_displayed_vehicle_dropdown()
        self.update_total_vehicles_supported()
        self.panel_pack_selector.select(0)

    def toggle_unlock_level(self):
        if self.panel_ingame_default_variable.get():
            self.panel_ingame_unlock_input.state(["disabled"])
        else:
            self.panel_ingame_unlock_input.state(["!disabled"])

    def open_mod_link_page(self, *args):
        if self.tab_game_variable.get() == "ets":
            webbrowser.open_new(MOD_LINK_PAGE_LINK + "#euro-truck-simulator-2")
        else:
            webbrowser.open_new(MOD_LINK_PAGE_LINK + "#american-truck-simulator")

    def mousewheel_scroll(self, event):
        if self.os == "Windows":
            scroll_amount = int(-1 * (event.delta / 120))
        elif self.os == "macOS":
            scroll_amount = int(-1 * event.delta)
        elif self.os == "Linux":
            if event.num == 4:
                scroll_amount = -1
            elif event.num == 5:
                scroll_amount = 1

        current_tab = self.panel_pack_selector.index(self.panel_pack_selector.select())
        if current_tab == 0: # Trucks
            self.scroll_canvas_trucks.yview_scroll(scroll_amount, "units")
            if self.tab_game_variable.get() == "ats":
                self.scroll_canvas_trucks.yview_moveto(0) # Hack to prevent scrolling up past the content
        elif current_tab == 1: # Trailers
            self.scroll_canvas_trailers.yview_scroll(scroll_amount, "units")
            self.scroll_canvas_trailers.yview_moveto(0)
        elif current_tab == 2: # Truck mods
            self.scroll_canvas_truck_mods.yview_scroll(scroll_amount, "units")
        elif current_tab == 3: # Bus mods
            self.scroll_canvas_bus_mods.yview_scroll(scroll_amount, "units")
            self.scroll_canvas_bus_mods.yview_moveto(0)
        elif current_tab == 4: # Trailer mods
            self.scroll_canvas_trailer_mods.yview_scroll(scroll_amount, "units")

    def check_for_outdated_vehicles(self, game):
        outdated_vehicles = []
        for file_name in os.listdir("library/vehicles/{}".format(game)):
            veh_ini = configparser.ConfigParser(allow_no_value = True)
            veh_ini.read("library/vehicles/{}/{}".format(game, file_name), encoding="utf-8")
            if "mod link workshop" not in veh_ini.options("vehicle info"): # 1.7
                outdated_vehicles.append(file_name)
            if "bus mod" not in veh_ini.options("vehicle info"): # 1.8
                outdated_vehicles.append(file_name)
        for file_name in outdated_vehicles:
            os.remove("library/vehicles/{}/{}".format(game, file_name))

    def load_list_of_vehicles(self, game):
        l = self.get_localised_string
        complete_list = []
        for file_name in os.listdir("library/vehicles/{}".format(game)):
            complete_list.append(VehSelection(game, file_name))
        truck_list = []
        truck_mod_list = []
        bus_mod_list = []
        trailer_list = []
        trailer_mod_list = []
        for veh in complete_list:
            if veh.trailer:
                if veh.mod:
                    veh.check = ttk.Checkbutton(self.scroll_frame_trailer_mods, text = "{} ({})".format(veh.display_name, veh.display_author), command = lambda : self.update_total_vehicles_supported())
                    veh.check.state(["!alternate","!selected"])
                    trailer_mod_list.append(veh)
                else:
                    veh.check = ttk.Checkbutton(self.scroll_frame_trailers, text = veh.display_name, command = lambda : self.update_total_vehicles_supported())
                    veh.check.state(["!alternate","!selected"])
                    trailer_list.append(veh)
            else:
                if veh.mod:
                    if veh.bus_mod:
                        veh.check = ttk.Checkbutton(self.scroll_frame_bus_mods, text = "{} ({})".format(veh.display_name, veh.display_author), command = lambda : self.update_total_vehicles_supported())
                        veh.check.state(["!alternate","!selected"])
                        bus_mod_list.append(veh)
                    else:
                        veh.check = ttk.Checkbutton(self.scroll_frame_truck_mods, text = "{} ({})".format(veh.display_name, veh.display_author), command = lambda : self.update_total_vehicles_supported())
                        veh.check.state(["!alternate","!selected"])
                        truck_mod_list.append(veh)
                else:
                    veh.check = ttk.Checkbutton(self.scroll_frame_trucks, text = veh.display_name, command = lambda : self.update_total_vehicles_supported())
                    veh.check.state(["!alternate","!selected"])
                    truck_list.append(veh)
        truck_list.sort(key = lambda veh: veh.name.lower())
        trailer_list.sort(key = lambda veh: veh.name.lower())
        truck_mod_list.sort(key = lambda veh: veh.name.lower())
        bus_mod_list.sort(key = lambda veh: veh.name.lower())
        trailer_mod_list.sort(key = lambda veh: veh.name.lower())
        return (truck_list, truck_mod_list, bus_mod_list, trailer_list, trailer_mod_list)

    def change_displayed_vehicle_dropdown(self, *args):
        l = self.get_localised_string
        type = self.panel_single_type_variable.get()
        self.panel_single_vehicle_variable.set("")
        new_values = []
        if type == l("{Truck}"):
            for veh in self.truck_list: new_values.append(veh.display_name)
        elif type == l("{TruckMod}"):
            for veh in self.truck_mod_list: new_values.append("{} [{}]".format(veh.display_name, veh.display_author))
        elif type == l("{BusMod}"):
            for veh in self.bus_mod_list: new_values.append("{} [{}]".format(veh.display_name, veh.display_author))
        elif type == l("{Trailer}"):
            for veh in self.trailer_list: new_values.append(veh.display_name)
        elif type == l("{TrailerMod}"):
            for veh in self.trailer_mod_list: new_values.append("{} [{}]".format(veh.display_name, veh.display_author))
        self.panel_single_vehicle_dropdown.config(values = new_values)

        if type in [l("{TruckMod}"), l("{BusMod}"), l("{TrailerMod}")]:
            self.panel_single_link.grid(row = 4, column = 0, pady = 5, padx = 5, sticky = "w")
        else:
            self.panel_single_link.grid_forget()

    def update_total_vehicles_supported(self):
        l = self.get_localised_string
        self.total_trucks = 0
        self.total_trailers = 0
        self.total_buses = 0
        for veh in self.truck_list + self.truck_mod_list:
            if "selected" in veh.check.state():
                self.total_trucks += 1
        for veh in self.trailer_list + self.trailer_mod_list:
            if "selected" in veh.check.state():
                self.total_trailers += 1
        for veh in self.bus_mod_list:
            if "selected" in veh.check.state():
                self.total_buses += 1
        self.total_vehicles = self.total_trucks + self.total_trailers + self.total_buses
        self.panel_vehicles_pack.configure(text = l("{VehiclesPanelNamePack}").format(number = self.total_vehicles))
        if self.tab_game_variable.get() == "ets":
            if self.total_trucks + self.total_trailers > 0:
                self.panel_pack_selector.tab(3, state = "disabled")
            else:
                self.panel_pack_selector.tab(3, state = "normal")
            if self.total_buses > 0:
                self.panel_pack_selector.tab(0, state = "disabled")
                self.panel_pack_selector.tab(1, state = "disabled")
                self.panel_pack_selector.tab(2, state = "disabled")
                self.panel_pack_selector.tab(4, state = "disabled")
            else:
                self.panel_pack_selector.tab(0, state = "normal")
                self.panel_pack_selector.tab(1, state = "normal")
                self.panel_pack_selector.tab(2, state = "normal")
                self.panel_pack_selector.tab(4, state = "normal")
        elif self.tab_game_variable.get() == "ats":
            self.panel_pack_selector.tab(0, state = "normal")
            self.panel_pack_selector.tab(1, state = "normal")
            self.panel_pack_selector.tab(2, state = "normal")
            self.panel_pack_selector.tab(4, state = "normal")

    def change_from_generate_to_main(self):
        self.generate_screen.grid_forget()
        self.main_screen.grid(row = 0, column = 0, padx = 10, pady = 10)

    def verify_all_inputs(self):
        l = self.get_localised_string
        inputs_verified = True
        all_errors = []

        # Mod info
        if len(self.panel_mod_name_variable.get()) < 1:
            inputs_verified = False
            all_errors.append([l("{ErrorModNameEmptyTitle}"), l("{ErrorModNameEmpty}")])
        if pj.contains_illegal_characters_file_name(self.panel_mod_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorModNameCharacterTitle}"), l("{ErrorModNameCharacter}") + "\n< > : \" / \\ | ? *"])
        if self.panel_mod_name_variable.get()[-1:] == ".":
            inputs_verified = False
            all_errors.append([l("{ErrorModNameFullStopTitle}"), l("{ErrorModNameFullStop}")])
        if self.panel_mod_name_variable.get()[-1:] == " ":
            inputs_verified = False
            all_errors.append([l("{ErrorModNameSpaceTitle}"), l("{ErrorModNameSpace}")])
        if pj.contains_reserved_file_name(self.panel_mod_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorModNameInvalidTitle}"), l("{ErrorModNameInvalid}") + "\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"])

        for character in ["\0", "\a", "\b", "\t", "\n", "\v", "\f", "\r", "\e"]:
            self.panel_mod_name_variable.set(self.panel_mod_name_variable.get().replace(character, ""))

        if len(self.panel_mod_version_variable.get()) < 1:
            inputs_verified = False
            all_errors.append([l("{ErrorModVersionEmptyTitle}"), l("{ErrorModVersionEmpty}")])
        if pj.contains_illegal_characters_sii(self.panel_mod_version_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorModVersionCharacterTitle}"), l("{ErrorModVersionCharacter}") + "\n\" / \\"])

        if len(self.panel_mod_author_variable.get()) < 1:
            inputs_verified = False
            all_errors.append([l("{ErrorModAuthorEmptyTitle}"), l("{ErrorModAuthorEmpty}")])
        if pj.contains_illegal_characters_sii(self.panel_mod_author_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorModAuthorCharacterTitle}"), l("{ErrorModAuthorCharacter}") + "\n\" / \\"])

        # In-game paint job info
        if len(self.panel_ingame_name_variable.get()) < 1:
            inputs_verified = False
            all_errors.append([l("{ErrorInGameNameEmptyTitle}"), l("{ErrorInGameNameEmpty}")])
        if pj.contains_illegal_characters_file_name(self.panel_ingame_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorInGameNameCharacterTitle}"), l("{ErrorInGameNameCharacter}") + "\n< > : \" / \\ | ? *"])
        if self.panel_ingame_name_variable.get()[-1:] == ".":
            inputs_verified = False
            all_errors.append([l("{ErrorInGameNameFullStopTitle}"), l("{ErrorInGameNameFullStop}")])
        if self.panel_ingame_name_variable.get()[-1:] == " ":
            inputs_verified = False
            all_errors.append([l("{ErrorInGameNameSpaceTitle}"), l("{ErrorInGameNameSpace}")])
        if pj.contains_reserved_file_name(self.panel_ingame_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorInGameNameInvalidTitle}"), l("{ErrorInGameNameInvalid}") + "\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"])
        if not pj.check_if_ascii(self.panel_ingame_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorInGameNameAsciiTitle}"), l("{ErrorInGameNameAscii}") + "\nabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n0123456789\n! @ # $ % ^ & ( ) - _ = + [ ] { } ; ' , ` ~"])

        for character in ["\0", "\a", "\b", "\t", "\n", "\v", "\f", "\r", "\e"]:
            self.panel_ingame_name_variable.set(self.panel_ingame_name_variable.get().replace(character, ""))

        if len(self.panel_ingame_price_variable.get()) < 1:
            inputs_verified = False
            all_errors.append([l("{ErrorInGamePriceEmptyTitle}"), l("{ErrorInGamePriceEmpty}")])
        if not re.match("^[0-9]*$", self.panel_ingame_price_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorInGamePriceCharacterTitle}"), l("{ErrorInGamePriceCharacter}")])

        if not self.panel_ingame_default_variable.get():
            if len(self.panel_ingame_unlock_variable.get()) < 1:
                inputs_verified = False
                all_errors.append([l("{ErrorInGameUnlockEmptyTitle}"), l("{ErrorInGameUnlockEmpty}")])
            if not re.match("^[0-9]*$", self.panel_ingame_unlock_variable.get()):
                inputs_verified = False
                all_errors.append([l("{ErrorInGameUnlockCharacterTitle}"), l("{ErrorInGameUnlockCharacter}")])

        # Internal paint job info
        if len(self.panel_internal_name_variable.get()) < 1:
            inputs_verified = False
            all_errors.append([l("{ErrorInternalNameEmptyTitle}"), l("{ErrorInternalNameEmpty}")])
        if len(self.panel_internal_name_variable.get()) > self.internal_name_length:
            inputs_verified = False
            all_errors.append([l("{ErrorInternalNameLongTitle}"), l("{ErrorInternalNameLong}").format(length = self.internal_name_length)])
        if not re.match("^[0-9a-z\_]*$", self.panel_internal_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorInternalNameCharacterTitle}"), l("{ErrorInternalNameCharacter}")])
            # I think uppercase letters might work, but no paint jobs in the base game/DLCs use them, so best practice to avoid them
        if pj.contains_reserved_file_name(self.panel_internal_name_variable.get()):
            inputs_verified = False
            all_errors.append([l("{ErrorInternalNameInvalidTitle}"), l("{ErrorInternalNameInvalid}") + "\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"])

        # Vehicle selection
        if self.tab_paintjob_variable.get() == "pack":
            if self.total_vehicles < 1:
                inputs_verified = False
                all_errors.append([l("{ErrorSelectVehiclePackTitle}"), l("{ErrorSelectVehiclePack}")])
        elif self.tab_paintjob_variable.get() == "single":
            if self.panel_single_vehicle_variable.get() == "":
                inputs_verified = False
                all_errors.append([l("{ErrorSelectVehicleSingleTitle}"), l("{ErrorSelectVehicleSingle}")])

        # Check for incompatible vehicles
        veh_path_dict = {}
        for veh in self.truck_list + self.truck_mod_list + self.bus_mod_list + self.trailer_list + self.trailer_mod_list:
            if "selected" in veh.check.state():
                if not veh.vehicle_path in veh_path_dict:
                    veh_path_dict[veh.vehicle_path] = []
                veh_path_dict[veh.vehicle_path].append("{} ({})".format(veh.display_name, veh.display_author))
        for veh_path in veh_path_dict.keys():
            if len(veh_path_dict[veh_path]) > 1:
                incompatible_vehicles = "\n".join(veh_path_dict[veh_path])
                inputs_verified = False
                all_errors.append([l("{ErrorIncompatibleTitle}"), l("{ErrorIncompatible}") + "\n" + incompatible_vehicles])

        if inputs_verified:
            # Show warning about bus mods
            warning_vehicles = []
            if self.tab_paintjob_variable.get() == "pack":
                for veh in self.bus_mod_list:
                    if "selected" in veh.check.state() and veh.bus_door_workaround:
                        warning_vehicles.append("{} ({})".format(veh.display_name, veh.display_author))
            elif self.tab_paintjob_variable.get() == "single":
                for veh in self.bus_mod_list:
                    if "{} [{}]".format(veh.display_name, veh.display_author) == self.panel_single_vehicle_variable.get() and veh.bus_door_workaround:
                        warning_vehicles.append("{} ({})".format(veh.display_name, veh.display_author))
            if len(warning_vehicles) > 0:
                if len(warning_vehicles) == 1:
                    quantity_message = l("{ErrorBusSingle}")
                else:
                    quantity_message = l("{ErrorBusMultiple}")
                messagebox.showwarning(title = l("{BusMods}"), message = l("{ErrorBus1}\n\n{ErrorBus2}") + " {quantity}\n\n{bus_list}\n\n".format(quantity = quantity_message, bus_list = "\n".join(warning_vehicles)) + l("{ErrorBus3}"))

            # Disable template checkbox if not installed
            templates_present = False
            if self.tab_paintjob_variable.get() == "pack":
                for veh in self.truck_list + self.truck_mod_list + self.bus_mod_list + self.trailer_list + self.trailer_mod_list:
                    if "selected" in veh.check.state():
                        if os.path.exists("templates/{} templates/{} [{}].zip".format(self.tab_game_variable.get(), veh.vehicle_path, veh.mod_author)):
                            templates_present = True
            elif self.tab_paintjob_variable.get() == "single":
                search_name = self.panel_single_vehicle_variable.get()
                if "[" not in search_name:
                    search_name += " [SCS]" # The single paint job dropdown should probably have a corresponding VehSelection, not just a name that needs to be looked up
                for veh in self.truck_list + self.truck_mod_list + self.bus_mod_list + self.trailer_list + self.trailer_mod_list:
                    if "{} [{}]".format(veh.display_name, veh.display_author) == search_name:
                        if os.path.exists("templates/{} templates/{} [{}].zip".format(self.tab_game_variable.get(), veh.vehicle_path, veh.mod_author)):
                            templates_present = True
            if templates_present:
                self.panel_generating_templates_checkbox.state(["!disabled"])
            else:
                self.panel_generating_templates_variable.set(False)
                self.panel_generating_templates_checkbox.state(["disabled"])

            # Switch screens
            self.main_screen.grid_forget()
            self.generate_screen.grid(row = 0, column = 0, padx = 10, pady = 10)
        else:
            if len(all_errors) == 1:
                messagebox.showerror(title = l("{ErrorSingle}").format(error_name = all_errors[0][0]), message = all_errors[0][1])
            elif len(all_errors) > 1:
                total_message = ""
                for error in all_errors:
                    total_message += error[0]+"\n"
                    total_message += error[1]+"\n\n"
                messagebox.showerror(title = l("{ErrorMultiple}"), message = total_message)

    def ask_save_location(self):
        l = self.get_localised_string
        save_directory = filedialog.askdirectory(title = l("{SaveDialogueTitle}"), initialdir = self.panel_directory_current_variable.get())
        if save_directory != "":
            self.panel_directory_current_variable.set(save_directory)

    def check_if_folder_clear(self, save_directory):
        l = self.get_localised_string
        if save_directory != "":
            output_path = save_directory + "/Paint Job Packer Output"
            folder_clear = True
            if os.path.exists(output_path):
                if len(os.listdir(output_path)) > 0:
                    folder_clear = False
                    # I don't want to be on the receiving end of an irate user who lost their important report the night before it was due, because they happened to store it in the Paint Job Packer folder
                    messagebox.showerror(title = l("{ErrorFolderClearTitle}"), message = l("{ErrorFolderClear1}\n\n{ErrorFolderClear2}").format(folder_name = "\"Paint Job Packer Output\""))
            try:
                shutil.copyfile("library/placeholder-files/empty.dds", save_directory + "/empty.dds")
                os.remove(save_directory + "/empty.dds")
            except (PermissionError, FileNotFoundError):
                folder_clear = False
                messagebox.showerror(title = l("{ErrorFolderAccessTitle}"), message = l("{ErrorFolderAccess1}\n\n{ErrorFolderAccess2}"))
            if folder_clear:
                # Disable the button to stop people clicking it a second time
                self.panel_gen_buttons_generate.state(["disabled"])
                try:
                    self.make_paintjob(output_path)
                except PermissionError:
                    # Caused for some reason by copying the mod manager image
                    try:
                        shutil.rmtree(output_path)
                    except:
                        print("Could not delete output folder, some files may remain")
                    messagebox.showerror(title = l("{ErrorFolderAccessTitle}"), message = l("{ErrorFolderAccess1}\n\n{ErrorFolderAccess2}"))
                    # Reset everything on the generating screen
                    self.panel_gen_buttons_generate.state(["!disabled"])
                    self.progress_value.set(0.0)
                    self.panel_progress_category_variable.set(l("{ProgressReady}"))
                    self.panel_progress_specific_variable.set(l("{ProgressAppearHere}"))
                    self.panel_progress_specific_label.update() # All these update()s ensure the progress bar is updated in real time
                except PathTooLongError:
                    try:
                        shutil.rmtree(output_path)
                    except:
                        print("Could not delete output folder, some files may remain")
                    messagebox.showerror(title = l("{ErrorFolderAccessTitle}"), message = l("TOOO LONG+{ErrorFolderAccess1}\n\n{ErrorFolderAccess2}"))
                    # Reset everything on the generating screen
                    self.panel_gen_buttons_generate.state(["!disabled"])
                    self.progress_value.set(0.0)
                    self.panel_progress_category_variable.set(l("{ProgressReady}"))
                    self.panel_progress_specific_variable.set(l("{ProgressAppearHere}"))
                    self.panel_progress_specific_label.update()
                    self.ask_save_location()



    def make_paintjob(self, output_path):
        try:
            l = self.get_localised_string
            truck_list = []
            for veh in self.truck_list:
                if "selected" in veh.check.state():
                    truck_list.append(veh)
            truck_mod_list = []
            for veh in self.truck_mod_list:
                if "selected" in veh.check.state():
                    truck_mod_list.append(veh)
            bus_mod_list = []
            for veh in self.bus_mod_list:
                if "selected" in veh.check.state():
                    bus_mod_list.append(veh)
            trailer_list = []
            for veh in self.trailer_list:
                if "selected" in veh.check.state():
                    trailer_list.append(veh)
            trailer_mod_list = []
            for veh in self.trailer_mod_list:
                if "selected" in veh.check.state():
                    trailer_mod_list.append(veh)

            vehicle_list = []
            for veh in truck_list + truck_mod_list + bus_mod_list + trailer_list + trailer_mod_list:
                vehicle_list.append(pj.Vehicle(veh.file_name, self.tab_game_variable.get()))

            single_veh_full_name = self.panel_single_vehicle_variable.get()
            single_veh_name = single_veh_full_name.split("[")[0].rstrip()
            if "[" in single_veh_full_name:
                single_veh_author = single_veh_full_name.split("[")[1][:-1]
            else:
                single_veh_author = "SCS"
            for veh in self.truck_list + self.truck_mod_list + self.bus_mod_list + self.trailer_list + self.trailer_mod_list:
                if veh.display_name == single_veh_name and veh.display_author == single_veh_author:
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
            workshop_upload = self.panel_generating_workshop_variable.get()

            # Convert variables to English for behind-the-scenes, to make things smoother
            if self.panel_internal_supported_variable.get() == l("{InternalSupportedLargest}"):
                cabins_supported = "Largest cabin only"
            else:
                cabins_supported = "All cabins"
            if self.panel_internal_handling_variable.get() == l("{InternalHandlingCombined}"):
                cabin_handling = "Combined paint job"
            else:
                cabin_handling = "Separate paint jobs"

            if cabins_supported == "Largest cabin only":
                # This shouldn't be needed, but it might be, so I'm doing it for safe measure
                cabin_handling = "Combined paint job"

            placeholder_templates = self.panel_generating_templates_variable.get()

            out_path = output_path+"/"+mod_name

            if num_of_paintjobs == "single":
                if single_veh.trailer:
                    if single_veh.mod:
                        trailer_mod_list.append(single_veh)
                    else:
                        trailer_list.append(single_veh)
                else:
                    if single_veh.mod:
                        if single_veh.bus_mod:
                            bus_mod_list.append(single_veh)
                        else:
                            truck_mod_list.append(single_veh)
                    else:
                        truck_list.append(single_veh)
                vehicle_list.append(single_veh)

            if not os.path.exists("library/paint-job-tracker.txt"):
                print("Sending data to RudderStack...")
                code_ini = configparser.ConfigParser()
                code_ini.read("library/vehicles/vehicle-codes.ini", encoding="UTF-8")
                vehicle_codes = []
                for veh in vehicle_list:
                    vehicle_codes.append(code_ini[game]["{} [{}]".format(veh.path, veh.mod_author)])
                multi_thread_analytics = threading.Thread(target = library.analytics.send_analytics(",".join(vehicle_codes)))
                multi_thread_analytics.start()

            if not os.path.exists(out_path):
                os.makedirs(out_path)

            if workshop_upload:
                if not os.path.exists(output_path+"/Workshop uploading"):
                    os.makedirs(output_path+"/Workshop uploading")

            self.progress_value.set(0.0)
            things_to_load = len(vehicle_list) + 2 # + general files, complete
            if workshop_upload:
                things_to_load += 1 # Workshop image and description
            self.panel_progress_bar.configure(maximum = float(things_to_load))

            self.progress_value.set(self.progress_value.get()+1.0)
            self.panel_progress_category_variable.set("General mod files")

            self.panel_progress_specific_variable.set("Mod manifest")
            self.panel_progress_specific_label.update() # All these update()s ensure the progress bar is updated in real time
            pj.make_manifest_sii(out_path, mod_version, mod_name, mod_author, workshop_upload)

            self.panel_progress_specific_variable.set("Mod manager image")
            self.panel_progress_specific_label.update()
            pj.copy_mod_manager_image(out_path)

            self.panel_progress_specific_variable.set("Mod manager description")
            self.panel_progress_specific_label.update()
            pj.make_description(out_path, truck_list, truck_mod_list, bus_mod_list, trailer_list, trailer_mod_list, num_of_paintjobs)

            pj.make_material_folder(out_path)

            self.panel_progress_specific_variable.set("Paint job icon")
            self.panel_progress_specific_label.update()
            pj.copy_paintjob_icon(out_path, ingame_name)

            pj.make_paintjob_icon_tobj(out_path, ingame_name)

            pj.make_paintjob_icon_mat(out_path, internal_name, ingame_name)

            for veh in vehicle_list:
                self.progress_value.set(self.progress_value.get()+1.0)
                self.panel_progress_category_variable.set(veh.display_name)

                if placeholder_templates:
                    if os.path.exists("templates/{} templates/{} [{}].zip".format(game, veh.path, veh.mod_author)):
                        template_zip = zipfile.ZipFile("templates/{} templates/{} [{}].zip".format(game, veh.path, veh.mod_author))
                    else:
                        template_zip = None
                else:
                    template_zip = None

                pj.make_def_folder(out_path, veh)
                self.panel_progress_specific_variable.set("Paint job settings")
                self.panel_progress_specific_label.update()
                pj.make_settings_sui(out_path, veh, internal_name, ingame_name, ingame_price, unlock_level)
                pj.make_vehicle_folder(out_path, veh, ingame_name)
                if cabin_handling == "Combined paint job" or veh.type == "trailer_owned" or not veh.separate_paintjobs:
                    one_paintjob = True
                    paintjob_name = internal_name
                    if veh.uses_accessories:
                        if veh.type == "trailer_owned":
                            if veh.name in veh.acc_dict:
                                main_dds_name = veh.name
                                veh.acc_dict.pop(veh.name)
                            else:
                                main_dds_name = "Base Colour"
                        elif veh.type == "truck":
                            main_dds_name = "Cabin"
                    else:
                        main_dds_name = veh.name
                    self.panel_progress_specific_variable.set(main_dds_name)
                    self.panel_progress_specific_label.update()
                    if veh.alt_uvset:
                        main_dds_name = main_dds_name + " (alt uvset)"
                    if veh.type == "truck" and cabins_supported == "Largest cabin only" and veh.separate_paintjobs:
                        one_paintjob = False
                        for cab_size in veh.cabins:
                            if cab_size == "a":
                                cab_internal_name = veh.cabins[cab_size][1]
                                if "/" in cab_internal_name:
                                    cab_internal_name = cab_internal_name.split("/") # For when multiple cabins can use the same template, e.g. Western Star 49X
                                pj.make_def_sii(out_path, veh, paintjob_name, internal_name, one_paintjob, ingame_name, main_dds_name, cab_internal_name)
                    else:
                        pj.make_def_sii(out_path, veh, paintjob_name, internal_name, one_paintjob, ingame_name, main_dds_name)
                    pj.copy_main_dds(out_path, veh, ingame_name, main_dds_name, template_zip)
                    pj.make_main_tobj(out_path, veh, ingame_name, main_dds_name)
                    if veh.uses_accessories:
                        pj.make_accessory_sii(out_path, veh, ingame_name, paintjob_name)
                else:
                    for cab_size in veh.cabins:
                        if cabins_supported == "Largest cabin only" and cab_size != "a":
                            pass
                        else:
                            one_paintjob = False
                            paintjob_name = internal_name + "_" + cab_size
                            main_dds_name = veh.cabins[cab_size][0] # Cabin in-game name
                            self.panel_progress_specific_variable.set(main_dds_name)
                            self.panel_progress_specific_label.update()
                            if veh.alt_uvset:
                                main_dds_name = main_dds_name[:-1] + ", alt uvset)" # Inserts "alt uvset" into the brackets in the cabin name
                            cab_internal_name = veh.cabins[cab_size][1]
                            if "/" in cab_internal_name:
                                cab_internal_name = cab_internal_name.split("/") # For when multiple cabins can use the same template, e.g. Western Star 49X
                            pj.make_def_sii(out_path, veh, paintjob_name, internal_name, one_paintjob, ingame_name, main_dds_name, cab_internal_name)
                            pj.copy_main_dds(out_path, veh, ingame_name, main_dds_name, template_zip)
                            pj.make_main_tobj(out_path, veh, ingame_name, main_dds_name)
                            if veh.uses_accessories:
                                pj.make_accessory_sii(out_path, veh, ingame_name, paintjob_name)
                if veh.uses_accessories:
                    self.panel_progress_specific_variable.set("Accessories")
                    self.panel_progress_specific_label.update()
                    pj.copy_accessory_dds(out_path, veh, ingame_name, game, template_zip)
                    pj.make_accessory_tobj(out_path, veh, ingame_name)

                if template_zip != None:
                    template_zip.close()

            if workshop_upload:
                self.progress_value.set(self.progress_value.get()+1.0)
                self.panel_progress_category_variable.set("Workshop files")
                self.panel_progress_specific_label.update()
                pj.copy_versions_sii(output_path+"/Workshop uploading")
                self.panel_progress_specific_variable.set("Workshop image")
                self.panel_progress_specific_label.update()
                pj.copy_workshop_image(output_path)
                self.panel_progress_specific_variable.set("Workshop readme")
                self.panel_progress_specific_label.update()
                self.make_workshop_readme(output_path, truck_list, truck_mod_list, bus_mod_list, trailer_list, trailer_mod_list, num_of_paintjobs, cabins_supported)

            self.make_readme_file(output_path, ingame_name, game, mod_name, truck_list+truck_mod_list, bus_mod_list, trailer_list+trailer_mod_list)

            self.progress_value.set(self.progress_value.get()+1.0)
            self.panel_progress_category_variable.set(l("{ProgressFinishing}"))
            self.panel_progress_specific_variable.set(l("{ProgressSeconds}"))
            self.panel_progress_specific_label.update()

            if os.path.exists("library/paint-job-tracker.txt") and num_of_paintjobs != "single" and mod_name != "123":
                self.generate_paintjob_tracker_file(game, truck_list, truck_mod_list, bus_mod_list, trailer_list, trailer_mod_list, mod_name)

            exit_now = messagebox.showinfo(title = l("{ProgressCompleteTitle}"), message = l("{ProgressComplete1}\n\n{ProgressComplete2}\n\n{ProgressComplete3}").format(folder_name = "Paint Job Packer Output"))
            sys.exit()
        except FileNotFoundError:
            # If a FileNotFoundError is raised at this point, it is most likely because the path is too long
            # There may be some edge cases where it's caused by a missing library file or some other bizarre error
            raise PathTooLongError

    def make_readme_file(self, output_path, paintjob_name, game, mod_name, truck_list, bus_list, trailer_list):
        file = open(output_path+"/How to complete your mod.txt", "w", encoding="utf-8")
        file.write("Your mod has been generated and placed inside the \"{}\" folder.\n".format(mod_name))
        file.write("There are a few steps left to finish it off. You'll need to replace the files listed in this document.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("To test your mod as you make it, move the \"{}\" folder to your game's mod folder:\n".format(mod_name))
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
        file.write(mod_folder_location)
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== Mod manager image ==\n")
        file.write("Mod_Manager_Image.jpg\n")
        file.write("\n")
        file.write("A 276 x 162 JPEG image that represents your mod in the in-game mod manager.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== Mod manager description ==\n")
        file.write("Mod_Manager_Description.txt\n")
        file.write("\n")
        file.write("Your mod's description in the mod manager.\n")
        file.write("It can be replaced, or you can modify the one that's already there.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== In-game paint job icon ==\n")
        file.write("material/ui/accessory/{} Icon.dds\n".format(paintjob_name))
        file.write("\n")
        file.write("A 256 x 64 DDS image that is shown in-game when you buy your paint job.\n")
        file.write("Stick to the shape in the placeholder for your icon to match the others in-game.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("== Vehicle textures ==\n")
        file.write("All of the .dds files in:\n")
        if len(truck_list) == 1:
            file.write("vehicle/truck/upgrade/paintjob/{}/{}/\n".format(paintjob_name, truck_list[0].name))
        elif len(bus_list) == 1:
            file.write("vehicle/truck/upgrade/paintjob/{}/{}/\n".format(paintjob_name, bus_list[0].name))
        elif len(truck_list) + len(bus_list) > 1:
            file.write("vehicle/truck/upgrade/paintjob/{}/<each vehicle>/\n".format(paintjob_name))
        if len(truck_list + bus_list) > 0 and len(trailer_list) > 0:
            file.write("and\n")
        if len(trailer_list) == 1:
            file.write("vehicle/trailer_owned/upgrade/paintjob/{}/{}/\n".format(paintjob_name, trailer_list[0].name))
        elif len(trailer_list) > 1:
            file.write("vehicle/trailer_owned/upgrade/paintjob/{}/<each vehicle>/\n".format(paintjob_name))
        file.write("\n")
        file.write("These are the main files of your mod, determining what your paint job will actually look like.\n")
        if len(truck_list) + len(bus_list) + len(trailer_list) == 1:
            file.write("Replace or re-colour every DDS image in this folder.\n")
        else:
            file.write("Replace or re-colour every DDS image in these folders.\n")
        file.write("\n")
        file.write("Save each DDS in DXT5 format with mipmaps, if possible.\n")
        file.write("Ensure every file's height and width is a power of 2 (e.g. 16, 64, 2048, 4096 etc).\n")
        file.write("\n")
        if game == "ets":
            file.write("You can grab a complete template pack here: {}\n".format(ETS_TEMPLATE_LINK))
        else:
            file.write("You can grab a complete template pack here: {}\n".format(ATS_TEMPLATE_LINK))
        file.close()

    def make_workshop_readme(self, output_path, truck_list, truck_mod_list, bus_mod_list, trailer_list, trailer_mod_list, num_of_paintjobs, cabins_supported):
        file = open(output_path+"/How to upload your mod to Steam Workshop.txt", "w", encoding="utf-8")
        file.write("In order to upload your mod to Steam Workshop, you'll need to use the SCS Workshop Uploader, which only runs on Windows.\n")
        file.write("To download it, you'll need to own ETS 2 or ATS on Steam. Then go to View > Hidden Games, tick \"Tools\" in the dropdown on\n")
        file.write("the left, then scroll down to find the SCS Workshop Uploader.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("Once your mod is complete, compress all of its files into a zip file. Name it universal.zip, and move it to the \"Workshop\n")
        file.write("uploading\" folder, which should already contain a file called versions.sii.\n")
        file.write("\n")
        file.write("You'll also need to create a workshop image, which is a 640 x 360 JPEG, that will represent your mod when people search\n")
        file.write("for it on the Workshop. There is a placeholder Workshop image.jpg with the correct dimensions.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("Open the SCS Workshop Uploader and select your game. In the Mod data section browse to the \"Workshop uploading\" folder\n")
        file.write("and your workshop image. Enter your mod name, change the visibility to Public if you wish, then enter your description.\n")
        file.write("There's an automatically generated Workshop description at the bottom of this text file that you can copy-paste. On the right,\n")
        file.write("select \"Truck parts\" under Type, then scroll down and check \"Paintjobs\". Select all the brands applicable to your mod, and\n")
        file.write("enter a change note if you wish.\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("Below is a workshop description. It's identical to the mod manager description, but with clickable links for modded vehicles:\n")
        file.write("\n")
        if num_of_paintjobs == "single":
            for veh in truck_list + trailer_list:
                file.write("This paint job supports the {}\n".format(veh.display_name))
            for veh in truck_mod_list + bus_mod_list + trailer_mod_list:
                file.write("This paint job supports {}'s [url={}]{}[/url]\n".format(veh.display_author, veh.mod_link, veh.display_name.split(" [")[0]))
        else:
            if len(truck_list) + len(truck_mod_list) > 0:
                file.write("Trucks supported:\n")
                for veh in truck_list:
                    file.write(veh.display_name+"\n")
                for veh in truck_mod_list:
                    file.write("{}'s [url={}]{}[/url]\n".format(veh.display_author, veh.mod_link, veh.display_name.split(" [")[0]))
                file.write("\n")
            if len(bus_mod_list) > 0:
                file.write("Buses supported:\n")
                for veh in bus_mod_list:
                    file.write("{}'s [url={}]{}[/url]\n".format(veh.display_author, veh.mod_link, veh.display_name.split(" [")[0]))
                file.write("\n")
            if len(trailer_list) + len(trailer_mod_list) > 0:
                file.write("Trailers supported:\n")
                for veh in trailer_list:
                    file.write(veh.display_name+"\n")
                for veh in trailer_mod_list:
                    file.write("{}'s [url={}]{}[/url]\n".format(veh.display_author, veh.mod_link, veh.display_name.split(" [")[0]))
        file.close()

    def generate_paintjob_tracker_file(self, game, truck_list, truck_mod_list, bus_mod_list, trailer_list, trailer_mod_list, mod_name):
        # This function is made to work with Paintjob Tracker, a mod management program I wrote for my own use
        # For more info see my paintjob-tracker repo on GitHub
        file = open("library/paint-job-tracker.txt", "r")
        file_lines = file.readlines()
        file.close()
        tracker_directory = file_lines[0].rstrip() + "/" + game
        tracker = configparser.ConfigParser(allow_no_value = True)
        tracker.optionxform = str # Preserves case
        if os.path.exists("{}/{}.ini".format(tracker_directory, mod_name)):
            tracker.read("{}/{}.ini".format(tracker_directory, mod_name), encoding = "utf-8")
            all_trucks = tracker["pack info"]["trucks"].split(";")
            for veh in truck_list:
                if veh.file_name[:-4] not in all_trucks:
                    all_trucks.append(veh.file_name[:-4])
                    tracker["description"]["changelog"] += "\\n- Added {}".format(veh.display_name)
            tracker["pack info"]["trucks"] = ";".join(all_trucks)
            all_truck_mods = tracker["pack info"]["truck mods"].split(";")
            for veh in truck_mod_list + bus_mod_list:
                if veh.file_name[:-4] not in all_truck_mods:
                    all_truck_mods.append(veh.file_name[:-4])
                    tracker["description"]["changelog"] += "\\n- Added {}'s {}".format(veh.display_author, veh.display_name.replace(" [{}]".format(veh.mod_author), ""))
            tracker["pack info"]["truck mods"] = ";".join(all_truck_mods)
            all_trailers = tracker["pack info"]["trailers"].split(";")
            for veh in trailer_list:
                if veh.file_name[:-4] not in all_trailers:
                    all_trailers.append(veh.file_name[:-4])
                    tracker["description"]["changelog"] += "\\n- Added {}".format(veh.display_name)
            tracker["pack info"]["trailers"] = ";".join(all_trailers)
            all_trailer_mods = tracker["pack info"]["trailer mods"].split(";")
            for veh in trailer_mod_list:
                if veh.file_name[:-4] not in all_trailer_mods:
                    all_trailer_mods.append(veh.file_name[:-4])
                    tracker["description"]["changelog"] += "\\n- Added {}'s {}".format(veh.display_author, veh.display_name.replace(" [{}]".format(veh.mod_author), ""))
            tracker["pack info"]["trailer mods"] = ";".join(all_trailer_mods)

            with open("{}/{}.ini".format(tracker_directory, mod_name), "w", encoding = "utf-8") as configfile:
                tracker.write(configfile)
            print("Paint Job Tracker file at {}/{}.ini updated".format(tracker_directory, mod_name))
        else:
            tracker["pack info"] = {}
            all_trucks = []
            for veh in truck_list:
                all_trucks.append(veh.file_name[:-4])
            tracker["pack info"]["trucks"] = ";".join(all_trucks)
            all_truck_mods = []
            for veh in truck_mod_list + bus_mod_list:
                all_truck_mods.append(veh.file_name[:-4])
            tracker["pack info"]["truck mods"] = ";".join(all_truck_mods)
            all_trailers = []
            for veh in trailer_list:
                all_trailers.append(veh.file_name[:-4])
            tracker["pack info"]["trailers"] = ";".join(all_trailers)
            all_trailer_mods = []
            for veh in trailer_mod_list:
                all_trailer_mods.append(veh.file_name[:-4])
            tracker["pack info"]["trailer mods"] = ";".join(all_trailer_mods)
            if len(bus_mod_list) > 0:
                tracker["pack info"]["bus pack"] = "true"
            else:
                tracker["pack info"]["bus pack"] = "false"
            tracker["pack info"]["paintjobs"] = ""
            tracker["pack info"]["checklist stage"] = 0

            tracker["description"] = {}
            tracker["description"]["short description"] = ""
            tracker["description"]["more info"] = ""
            tracker["description"]["related mods"] = ""
            tracker["description"]["changelog"] = "Version 1.0\\n- Initial release"

            tracker["images"] = {}
            tracker["images"]["header"] = ""
            tracker["images"]["showcase"] = ""
            tracker["images"]["thumbnail"] = ""

            tracker["links"] = {}
            tracker["links"]["steam workshop"] = ""
            tracker["links"]["forums"] = ""
            tracker["links"]["trucky"] = ""
            tracker["links"]["modland"] = ""
            tracker["links"]["sharemods"] = ""
            tracker["links"]["modsbase"] = ""

            with open("{}/{}.ini".format(tracker_directory, mod_name), "w", encoding="utf-8") as configfile:
                tracker.write(configfile)
            print("Paint Job Tracker file written to {}/{}.ini".format(tracker_directory, mod_name))

    def thread_new_version(self):
        multi_thread_version_check = threading.Thread(target = self.check_new_version)
        multi_thread_version_check.start()

    def check_new_version(self):
        global new_ver # Ensures this only runs once
        global GITHUB_LINK, MOD_LINK_PAGE_LINK, VERSION_INFO_LINK, ANALYTICS_SCRIPT_LINK # To update links if the repo has moved
        l = self.get_localised_string
        print("Checking latest version on GitHub...")
        print("Current version: " + version)

        # Fetch version.ini from GitHub
        fetched_new_version = False
        context = ssl._create_unverified_context()
        try:
            # Try Carsmaniac/paintjob-packer/master
            version_info_ini = urllib.request.urlopen(VERSION_INFO_LINK, timeout = 2, context=context)
        except (urllib.error.URLError, urllib.error.HTTPError):
            try:
                # Try Carsmaniac/paint-job-packer/main
                version_info_ini = urllib.request.urlopen(NEW_VERSION_INFO_LINK, timeout = 2, context=context)
            except urllib.error.HTTPError:
                print("Couldn't fetch new version, skipping (HTTPError)")
            except urllib.error.URLError:
                print("Couldn't fetch new version, skipping (URLError)")
            else:
                # The new link worked
                fetched_new_version = True
                # The repo has moved, so update the other links
                GITHUB_LINK = NEW_GITHUB_LINK
                MOD_LINK_PAGE_LINK = NEW_MOD_LINK_PAGE_LINK
                VERSION_INFO_LINK = NEW_VERSION_INFO_LINK
                ANALYTICS_SCRIPT_LINK = NEW_ANALYTICS_SCRIPT_LINK
                # I guess those constants weren't so constant after all
        else:
            # The old link worked
            fetched_new_version = True

        if fetched_new_version:
            try:
                # Get current and latest versions
                version_info = configparser.ConfigParser()
                version_info.read_string(version_info_ini.read().decode())
                installed_version = version.split(".")
                latest_release_string = version_info["version info"]["latest release"]
                latest_release = latest_release_string.split(".")
                print("Latest release: " + latest_release_string)

                # Convert versions to integer lists
                if len(installed_version) < 3:
                    installed_version.append("0")
                if len(latest_release) < 3:
                    latest_release.append("0")
                for i in range(3):
                    installed_version[i] = int(installed_version[i])
                    latest_release[i] = int(latest_release[i])

                # Check if latest release is newer than current install
                update_message = None
                if latest_release[0] > installed_version[0]:
                    update_message = version_info["version info"]["major update"]
                elif latest_release[0] == installed_version[0]:
                    if latest_release[1] > installed_version[1]:
                        update_message = version_info["version info"]["feature update"]
                    elif latest_release[1] == installed_version[1]:
                        if latest_release[2] > installed_version[2]:
                            update_message = version_info["version info"]["patch update"]

                # Update the welcome screen
                if update_message != None:
                    print("New version available! - " + update_message)
                    new_ver = [latest_release_string, update_message]
                    self.tab_welcome_message.configure(text = l("{UpdateNotice}").format(version_number = latest_release_string), foreground = self.red, cursor = self.cursor)
                    self.tab_welcome_message.bind("<1>", lambda e: webbrowser.open_new(LATEST_VERSION_DOWNLOAD_LINK))
                    self.tab_welcome_link_forum.configure(foreground = "black")
                    self.tab_welcome_link_kofi.configure(foreground = "black")
                    self.tab_welcome_link_github.configure(foreground = "black")
                    self.tab_welcome_update_info = ttk.Label(self.tab_welcome, text = l("{UpdateDetails}").format(details = update_message), cursor = self.cursor)
                    self.tab_welcome_update_info.grid(row = 4, column = 0, columnspan = 3)
                    self.tab_welcome_update_info.bind("<1>", lambda e: webbrowser.open_new(LATEST_VERSION_DOWNLOAD_LINK))
                # else: new_ver remains [None, None]
            except ValueError:
                print("Couldn't parse version number, skipping (ValueError)")
            except TypeError:
                print("Couldn't compare version numbers, skipping (TypeError)")

class VehSelection:

    def __init__(self, _game, _file_name):
        self.file_name = _file_name
        self.game = _game
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("library/vehicles/{}/{}".format(self.game, self.file_name), encoding="utf-8")
        self.vehicle_path = veh_ini["vehicle info"]["vehicle path"]
        self.display_name = veh_ini["vehicle info"]["name"]
        self.name = pj.strip_diacritics(self.display_name)
        self.trailer = veh_ini["vehicle info"].getboolean("trailer")
        self.mod = veh_ini["vehicle info"].getboolean("mod")
        if self.mod:
            self.display_author = veh_ini["vehicle info"]["mod author"]
        else:
            self.display_author = "SCS"
        self.mod_author = pj.strip_diacritics(self.display_author)
        if self.mod:
            self.name += " [" + self.mod_author + "]"
        self.mod_link_workshop = veh_ini["vehicle info"]["mod link workshop"]
        self.mod_link_forums = veh_ini["vehicle info"]["mod link forums"]
        self.mod_link_trucky = veh_ini["vehicle info"]["mod link trucky"]
        self.mod_link_author_site = veh_ini["vehicle info"]["mod link author site"]
        # The canonical mod link is chosen with the priority of Steam Workshop > SCS Forums > TruckyMods > Mod author's own site
        if self.mod_link_workshop != "":
            self.mod_link = self.mod_link_workshop
        elif self.mod_link_forums != "":
            self.mod_link = self.mod_link_forums
        elif self.mod_link_trucky != "":
            self.mod_link = self.mod_link_trucky
        else:
            self.mod_link = self.mod_link_author_site
        self.bus_mod = veh_ini["vehicle info"].getboolean("bus mod")
        self.bus_door_workaround = veh_ini["vehicle info"].getboolean("bus door workaround")

class PathTooLongError(Exception):
    # A FileNotFoundError raised when a file path is over Windows' max path length, given this custom name to distinguish it from FileNotFoundErrors caused by different issues
    pass

def show_unhandled_error(error_type, error_message, error_traceback):
    clipboard = tk.Tk()
    clipboard.withdraw()
    clipboard.clipboard_clear()
    clipboard.clipboard_append("{}: {}\n\nTraceback:\n{}".format(error_type.__name__, str(error_message), "\n".join(traceback.format_list(traceback.extract_tb(error_traceback)))))
    clipboard.update()
    clipboard.destroy()
    messagebox.showerror(title = "Unhandled exception", message = "Something went very wrong and Paint Job Packer ran into an unexpected error.\n\nThe full error message has been copied to your clipboard, please send it to the developer on GitHub or the SCS Forums!")

def load_system_language():
    global system_lang
    supported_langs = os.listdir("lang")
    system_lang = locale.getdefaultlocale()[0]
    if system_lang != None:
        if (system_lang + ".ini") in supported_langs:
            # Use exact language
            return system_lang
        else:
            # Use other dialect
            short_lang = None
            for lang in supported_langs:
                if lang.startswith(system_lang[:2]):
                    short_lang = lang[:-4]
            if short_lang != None:
                return short_lang
            else:
                # Default to English
                return "en_US"
    else:
        system_lang = "Not detected"
        return "en_US"

def restart_app(language):
    root.destroy()
    main(language)

def main(language = None):
    global root
    root = tk.Tk()
    root.tk.call("source", "sun-valley.tcl")
    try:
        if darkdetect.isDark():
            root.tk.call("set_theme", "dark")
        else:
            root.tk.call("set_theme", "light")
    except NameError:
        root.tk.call("set_theme", "light")
    root.title("Paint Job Packer v" + version)
    if sys.platform.startswith("darwin"):
        root.iconphoto(True, tk.PhotoImage(file = "library/packer-images/icon-squircle.png"))
    else:
        root.iconphoto(True, tk.PhotoImage(file = "library/packer-images/icon-circle.png"))
    root.resizable(False, False)
    root.report_callback_exception = show_unhandled_error
    if language == None:
        language = load_system_language()
    packer = PackerApp(root, language)
    root.mainloop()

if __name__ == "__main__":
    main()
