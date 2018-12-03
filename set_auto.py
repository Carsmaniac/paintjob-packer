# What this file needs to do:
# Open > options
# See current trucks and params
#   Split ATS/ETS/trailers?
# Add truck/trailer
# Modify truck/trailer
# Create file from scratch   *or maybe not the above two, just this one
# Modify other params

import paintjob, configparser, sys, time, os

def menu():
    print("\n"*30)
    print("=== Full Paintjob Pack Configurator ===")
    print("")
    print("1 - View/edit modpack parameters")
    print("2 - View/edit truck list")
    print("3 - Manage truck lists")
    print("")
    print("0 - Exit program")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        view_params()
    elif menu_choice == "2":
        view_list()
    elif menu_choice == "3":
        manage_lists()
    elif menu_choice == "0":
        sys.exit()
    else:
        print("Invalid selection")
        time.sleep(1.5)
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
        time.sleep(1.5)
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
        time.sleep(1.5)
        edit_params()
    print("")
    new_param_value = input("Enter new value for %s: " % param_to_edit[1])
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
    print("\n"*30)
    config = configparser.ConfigParser()
    config.read("config.ini")
    truck_list = config["AutoParams"]["truck_list"]
    print("Current list: %s" % truck_list)
    print("")
    config = []
    config = configparser.ConfigParser()
    config.read("auto lists/%s.ini" % truck_list)
    all_trucks_in_list = config.sections()
    all_trucks_in_list.remove("Params")
    for truck in all_trucks_in_list:
        print(config[truck]["database_name"])
    print("1 - Add truck to list")
    print("2 - Modify truck")
    print("3 - Remove truck from list")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    menu() # TODO: editing lists (add, edit, remove)

def add_to_list(truck_list):
    pass

def edit_list(truck_list):
    pass

def remove_from_list(truck_list):
    pass

def manage_lists():
    print("\n"*30)
    config = configparser.ConfigParser()
    config.read("config.ini")
    truck_list = config["AutoParams"]["truck_list"]
    print("Current list: %s" % truck_list)
    print("")
    other_lists_with_ext = os.listdir("auto lists")
    other_lists = []
    for list in other_lists_with_ext:
        list = list[:-4]
        other_lists.append(list)
    other_lists.remove(truck_list)
    if len(other_lists) == 0:
        print("This is your only truck list")
        menu_num = 0
        print("")
        print("1 - Create a new list")
    else:
        print("Switch to another list:")
        menu_num = 1
        for list in other_lists:
            print("%s - %s" % (menu_num,list))
            menu_num += 1
        print("")
        print("%s - Create a new list" % menu_num)
        print("%s - Remove a list" % menu_num+1)
        print("%s - Modify a list" % menu_num+2)
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_num == 0 and menu_choice == "1":
        create_list()
    elif menu_choice == "0":
        menu()
    elif menu_choice < menu_num: # TODO: Make this work
        switch_to_list(other_lists[menu_num-1])
    else: # TODO: Creating, removing and modifying lists
        print("Invalid selection") # NOTE: list type "euro" = truck types "euro", "euro mod" and "trailer", same for american
        time.sleep(1.5)
        manage_lists()

def create_list(): # TODO: Creating lists
    pass

def switch_to_list(list_to_switch_to):
    print("")
    config = configparser.ConfigParser()
    config.read("config.ini")
    config["AutoParams"]["truck_list"] = list_to_switch_to
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    print("Switched lists successfully")
    time.sleep(1.5)
    manage_lists()

menu()
