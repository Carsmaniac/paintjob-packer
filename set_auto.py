# What this file needs to do:
# Open > options
# See current trucks and params
#   Split ATS/ETS/trailers?
# Add truck/trailer
# Modify truck/trailer
# Create file from scratch   *or maybe not the above two, just this one
# Modify other params

import paintjob, configparser, sys, time

paintjob.welcome_message()

def menu():
    print("\n"*30)
    print("1 - View/edit modpack parameters")
    print("2 - View truck list")
    print("3 - Add truck to truck list")
    print("4 - Generate new truck list from scratch")
    print("")
    print("0 - Exit program")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        view_params()
    elif menu_choice == "2":
        view_list()
    elif menu_choice == "3":
        append_list()
    elif menu_choice == "4":
        regen_list()
    elif menu_choice == "0":
        sys.exit()
    else:
        print("Invalid selection")
        menu() # yeah this isn't a good idea

def view_params():
    print("\n"*30)
    config = configparser.ConfigParser()
    config.read("config.ini")
    print("=== Mod file parameters ===")
    print("Mod name:     %s" % config["AutoParams"]["pack_name"])
    print("Mod author:   %s" % config["AutoParams"]["pack_author"])
    print("Mod version:  %s" % config["AutoParams"]["pack_version"])
    print("")
    print("=== Ingame paintjob parameters ===")
    print("Ingame name:  %s" % config["AutoParams"]["name"])
    print("Price:        %s" % config["AutoParams"]["price"])
    print("Unlock level: %s" % config["AutoParams"]["unlock_level"])
    print("")
    print("1 - Edit parameters")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        edit_params()
    elif menu_choice == "0":
        menu()
    else:
        print("Invalid selection")
        view_params()

def edit_params():
    print("\n"*30)
    print("Select parameter to edit")
    print("1 - Mod name")
    print("2 - Mod author")
    print("3 - Mod version")
    print("4 - Ingame name")
    print("5 - Price")
    print("6 - Unlock level")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        param_to_edit = ("pack_name", "Mod name")
    elif menu_choice == "2":
        param_to_edit = ("pack_author", "Mod author")
    elif menu_choice == "3":
        param_to_edit = ("pack_version", "Mod version")
    elif menu_choice == "4":
        param_to_edit = ("name", "Ingame name")
    elif menu_choice == "5":
        param_to_edit = ("price", "Price")
    elif menu_choice == "6":
        param_to_edit = ("unlock_level", "Unlock level")
    elif menu_choice == "0":
        view_params()
    else:
        print("Invalid selection")
        edit_params()
    print("")
    new_param_value = input("Enter new value for %s : " % param_to_edit[1])
    param_to_edit = param_to_edit[0]
    config = configparser.ConfigParser()
    config.read("config.ini")
    config["AutoParams"][param_to_edit] = new_param_value
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    print("")
    print("Parameter changed successfully")
    time.sleep(2)
    edit_params()

def view_list():
    pass

def append_list():
    pass

def regen_list():
    pass

menu()
