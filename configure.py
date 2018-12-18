import paintjob, configparser, sys, time, re, os

def menu():
    print("\n"*50)
    paintjob.welcome_message()
    print("")
    print("=== Paintjob Packer Configurator ===")
    print("")
    config = configparser.ConfigParser()
    config.read("config.ini")
    truck_list = config["Params"]["truck_list"]
    print("Current paintjob pack: %s" % truck_list)
    print("")
    print("1 - View/edit paintjob pack parameters")
    print("2 - Switch to another paintjob pack")
    print("3 - View/edit manual paintjob parameters")
    print("")
    print("0 - Exit program")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        view_params()
    elif menu_choice == "2":
        switch_truck_list()
    elif menu_choice == "3":
        view_params(manual=True)
    elif menu_choice == "0":
        print("\n"*50)
        sys.exit()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        menu() # what was that? recursion? never heard of it

def view_params(manual=False):
    print("\n"*50)
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini")
    if manual:
        truck_list = "manual"
    else:
        truck_list = config_ini["Params"]["truck_list"]
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    list_type = list_ini["Params"]["list_type"]
    all_truck_lists = config_ini["Params"]["all_truck_lists"].split(",")
    if not manual:
        print("Current paintjob pack: %s" % truck_list)
        print("")
    print("=== Modpack parameters ===")
    print("Mod author:       %s" % list_ini["Params"]["pack_author"])
    print("Mod version:      %s" % list_ini["Params"]["pack_version"])
    print("")
    print("=== In-game paintjob parameters ===")
    print("In-game name:     %s" % list_ini["Params"]["ingame_name"])
    print("Price:            %s" % list_ini["Params"]["price"])
    print("Unlock level:     %s" % list_ini["Params"]["unlock_level"])
    print("")
    print("=== Other parameters ===")
    if list_type == "euro":
        print("Supported game:   Euro Truck Simulator 2")
    else:
        print("Supported game:   American Truck Simulator")
    if manual:
        print("Supported truck:  %s" % list_ini["Params"]["database_name"])
        print("Internal name:    %s" % list_ini["Params"]["internal_name"])
    else:
        print("Supported trucks: %s" % str(len(list_ini.sections())-1))
    print("")
    print("1 - Edit modpack or in-game parameters")
    if manual:
        print("2 - Edit supported truck")
        print("3 - Edit internal name")
        if list_ini["Params"].getboolean("new_truck_format"):
            print("4 - View/edit truck accessories")
        if list_type == "euro":
            print("5 - Switch to ATS support")
        else:
            print("5 - Switch to ETS 2 support")
    else:
        print("2 - View/edit supported trucks")
        print("3 - Rename paintjob pack")
        if len(all_truck_lists) > 1:
            print("4 - Remove paintjob pack")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        edit_params(truck_list)
    elif menu_choice == "2" and manual:
        select_truck()
    elif menu_choice == "3" and manual:
        edit_man_internal_name()
    elif menu_choice == "3" and not manual:
        rename_truck_list(truck_list)
    elif menu_choice == "2" and not manual:
        edit_auto_trucks()
    elif menu_choice == "4" and not manual:
        all_truck_lists.remove(truck_list)
        config_ini["Params"]["all_truck_lists"] = ",".join(all_truck_lists)
        os.remove("truck lists/%s.ini" % truck_list)
        truck_list = all_truck_lists[0]
        config_ini["Params"]["truck_list"] = truck_list
        with open("config.ini", "w") as configfile:
            config_ini.write(configfile)
        print("Pack removed successfully")
        time.sleep(1.5)
        view_params(manual = False)
    elif menu_choice == "4" and manual:
        view_accessories(list_ini["Params"]["internal_name"], "manual")
    elif menu_choice == "5" and manual:
        select_truck(mode="man switch")
    elif menu_choice == "0":
        menu()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        view_params(manual)

def switch_truck_list():
    print("\n"*50)
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini")
    truck_list = config_ini["Params"]["truck_list"]
    all_truck_lists = config_ini["Params"]["all_truck_lists"].split(",")
    print("Current paintjob pack: %s" % truck_list)
    print("")
    all_truck_lists.remove(truck_list)
    menu_choice_counter = 1
    if len(all_truck_lists) != 0:
        for other_truck_list in all_truck_lists:
            list_ini = configparser.ConfigParser()
            list_ini.read("truck lists/%s.ini" % other_truck_list)
            print("%s - Switch to %s (%s trucks)" % (menu_choice_counter, other_truck_list, str(len(list_ini.sections())-1)))
            menu_choice_counter += 1
        print("%s - Create a new paintjob pack" % menu_choice_counter)
    else:
        print("No other paintjob packs")
        print("")
        print("1 - Create new paintjob pack")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if (menu_choice == "1" and len(all_truck_lists) == 0) or menu_choice == str(menu_choice_counter):
        create_new_list()
    elif menu_choice in [str(i+1) for i in range(len(all_truck_lists))]:
        new_truck_list = all_truck_lists[int(menu_choice)-1]
        config_ini["Params"]["truck_list"] = new_truck_list
        with open("config.ini", "w") as configfile:
            config_ini.write(configfile)
        print("Switched to %s successfully" % new_truck_list)
        time.sleep(1.5)
        switch_truck_list()
    elif menu_choice == "0":
        menu()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        switch_truck_list()

def edit_params(truck_list):
    print("\n"*50)
    if truck_list == "manual":
        manual = True
    else:
        manual = False
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    print("Select parameter to edit:")
    print("")
    print("1 - Edit mod author   (%s)" % list_ini["Params"]["pack_author"])
    print("2 - Edit mod version  (%s)" % list_ini["Params"]["pack_version"])
    print("3 - Edit in-game name (%s)" % list_ini["Params"]["ingame_name"])
    print("4 - Edit price        (%s)" % list_ini["Params"]["price"])
    print("5 - Edit unlock level (%s)" % list_ini["Params"]["unlock_level"])
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        param_to_edit = ("pack_author", "mod author")
    elif menu_choice == "2":
        param_to_edit = ("pack_version", "mod version")
    elif menu_choice == "3":
        param_to_edit = ("ingame_name", "in-game name")
    elif menu_choice == "4":
        param_to_edit = ("price", "price")
    elif menu_choice == "5":
        param_to_edit = ("unlock_level", "Unlock level")
    elif menu_choice == "0":
        param_to_edit = None
        view_params(manual)
    else:
        param_to_edit = None
        print("Invalid selection")
        time.sleep(1.5)
        edit_params(truck_list)
    if param_to_edit != None:
        print("")
        new_param_value = input("Enter new value for %s, or nothing to cancel: " % param_to_edit[1])
        if new_param_value == "":
            edit_params(truck_list)
        else:
            param_to_edit = param_to_edit[0]
            list_ini["Params"][param_to_edit] = new_param_value
            with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                list_ini.write(configfile)
            print("")
            print("Parameter changed successfully")
            time.sleep(1.5)
            edit_params(truck_list)

def select_truck(mode="man"): # mode can be man, man switch or add
    print("\n"*50)
    list_ini = configparser.ConfigParser()
    if mode in ["man", "man switch"]:
        list_ini.read("truck lists/manual.ini")
        print("Current supported truck: %s" % list_ini["Params"]["database_name"])
        database_ini = configparser.ConfigParser()
        database_ini.read("database.ini")
        all_cabin_names = []
        for each_cabin in list_ini["Params"]["cabin_numbers"].split(","):
            all_cabin_names.append(database_ini[list_ini["Params"]["database_name"]]["cabin_%s_name" % each_cabin])
        print("Supported cabins:        %s" % ", ".join(all_cabin_names))
        print("")
        print("Select type of truck to support:")
    else:
        config_ini = configparser.ConfigParser()
        config_ini.read("config.ini")
        list_ini.read("truck lists/%s.ini" % config_ini["Params"]["truck_list"])
        print("Select type of truck to add:")
    print("")
    list_type = list_ini["Params"]["list_type"]
    if mode == "man switch":
        if list_type == "euro":
            list_type = "american"
        else:
            list_type = "euro"
    if list_type == "euro":
        print("1 - Euro Truck Simulator 2")
        print("2 - Euro Truck Simulator 2 truck mod")
        print("3 - Euro Truck Simulator 2 player-owned trailer")
    elif list_type == "american":
        print("1 - American Truck Simulator")
        print("2 - American Truck Simulator truck mod")
        print("3 - American Truck Simulator player-owned trailer")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    vehicle_type = None
    if menu_choice == "1" and list_type == "euro":
        vehicle_type = "euro"
    elif menu_choice == "2" and list_type == "euro":
        vehicle_type = "euro mod"
    elif menu_choice == "3" and list_type == "euro":
        vehicle_type = "euro trailer"
    elif menu_choice == "1" and list_type == "american":
        vehicle_type = "american"
    elif menu_choice == "2" and list_type == "american":
        vehicle_type = "american mod"
    elif menu_choice == "3" and list_type == "american":
        vehicle_type = "american trailer"
    elif menu_choice == "0":
        if mode in ["man", "man switch"]:
            view_params(manual=True)
        else:
            edit_auto_trucks()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        select_truck(mode)
    if vehicle_type != None:
        print("\n"*50)
        if mode in ["man", "man switch"]:
            print("Select truck to support")
        else:
            print("Select truck to add")
        database_ini = configparser.ConfigParser()
        database_ini.read("database.ini")
        vehicles_to_display = []
        for vehicle in database_ini.sections():
            if database_ini[vehicle]["vehicle_type"] == vehicle_type:
                vehicles_to_display.append(vehicle)
        menu_choice_counter = 1
        for vehicle in vehicles_to_display:
            print("%s - %s" % (menu_choice_counter, vehicle))
            menu_choice_counter += 1
        print("")
        menu_choice = input("Enter selection, or nothing to cancel: ")
        database_name = None
        if menu_choice in [str(i+1) for i in range(len(vehicles_to_display))]:
            choose_cabins(vehicles_to_display[int(menu_choice)-1], mode=mode)
        else:
            select_truck(mode)

def edit_auto_trucks():
    print("\n"*50)
    config = configparser.ConfigParser()
    config.read("config.ini")
    truck_list = config["Params"]["truck_list"]
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    all_trucks_in_list = list_ini.sections()
    all_trucks_in_list.remove("Params")
    if len(all_trucks_in_list) == 0:
        print("This pack is empty")
    else:
        menu_choice_counter = 1
        for truck in all_trucks_in_list:
            print("%s - Edit/remove %s (%s, %s cabins)" % (menu_choice_counter, truck, list_ini[truck]["database_name"], len(list_ini[truck]["cabins"].split(","))))
            menu_choice_counter += 1
    print("%s - Add a new truck" % menu_choice_counter)
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice in [str(i+1) for i in range(len(all_trucks_in_list))]:
        edit_truck(all_trucks_in_list[int(menu_choice)-1])
    elif menu_choice == str(menu_choice_counter):
        select_truck("add")
    elif menu_choice == "0":
        view_params(manual=False)
    else:
        print("Invalid selection")
        time.sleep(1.5)
        edit_auto_trucks()

def edit_truck(selected_truck):
    print("\n"*50)
    config = configparser.ConfigParser()
    config.read("config.ini")
    truck_list = config["Params"]["truck_list"]
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    if len(list_ini.sections()) > 2:
        show_remove_truck = True
    else:
        show_remove_truck = False
    if list_ini[selected_truck].getboolean("new_truck_format"):
        show_edit_accessories = True
    else:
        show_edit_accessories = False
    print("Selected truck: %s (%s)" % (selected_truck, list_ini[selected_truck]["database_name"]))
    print("")
    print("1 - Edit truck")
    print("2 - Rename truck")
    menu_choice_counter = 3
    if show_remove_truck:
        print("%s - Remove truck" % menu_choice_counter)
        menu_choice_counter += 1
    if show_edit_accessories:
        print("%s - View/edit truck accessories" % menu_choice_counter)
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        selected_truck_cabins = list_ini[selected_truck]["cabin_numbers"].split(",")
        if "1" in selected_truck_cabins:
            cabin_1 = True
        else:
            cabin_1 = False
        if "2" in selected_truck_cabins:
            cabin_2 = True
        else:
            cabin_2 = False
        if "3" in selected_truck_cabins:
            cabin_3 = True
        else:
            cabin_3 = False
        if "8x4" in selected_truck_cabins:
            cabin_8x4 = True
        else:
            cabin_8x4 = False
        choose_cabins(database_name=list_ini[selected_truck]["database_name"], cabin_1=cabin_1, cabin_2=cabin_2, cabin_3=cabin_3, cabin_8x4=cabin_8x4, mode="edit", internal_name=selected_truck)
    elif menu_choice == "2":
        print("")
        print("Note: internal name should: - be 12 or fewer characters")
        print("                            - consist of only letters, numbers and underscores")
        print("                            - be unique")
        print("Paintjob Packer will warn you if the name is already in use in this paintjob pack,")
        print("however please take caution when using multiple mods at once")
        print("")
        new_internal_name = input("Enter new internal name, or nothing to cancel: ")
        if new_internal_name == "":
            edit_truck(selected_truck)
        else:
            new_internal_name = re.sub("\W+","",new_internal_name).lower()
            if len(new_internal_name) <= 12:
                if new_internal_name not in list_ini.sections():
                    print("Internal name %s is okay" % new_internal_name)
                    name_is_okay = True
                else:
                    if new_internal_name == selected_truck:
                        print("Internal name %s is okay" % new_internal_name)
                        name_is_okay = None
                    else:
                        print("Internal name %s already exists in %s" % (new_internal_name, truck_list))
                        name_is_okay = False
            else:
                print("Internal name %s is too long" % new_internal_name)
                name_is_okay = False
            if name_is_okay:
                list_ini.add_section(new_internal_name)
                for key in list_ini[selected_truck]:
                    list_ini[new_internal_name][key] = list_ini[selected_truck][key]
                list_ini.remove_section(selected_truck)
                with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                    list_ini.write(configfile)
                print("Internal name changed successfully")
                time.sleep(1.5)
                edit_truck(new_internal_name)
            elif name_is_okay == None:
                edit_truck(selected_truck)
            else:
                time.sleep(1.5)
                edit_truck(selected_truck)
    elif menu_choice == "3":
        if show_remove_truck:
            list_ini.remove_section(selected_truck)
            with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                list_ini.write(configfile)
            print("Removed truck successfully")
            time.sleep(1.5)
            edit_auto_trucks()
        elif show_edit_accessories:
            view_accessories(selected_truck, truck_list)
        else:
            print("Invalid selection")
            time.sleep(1.5)
            edit_truck(selected_truck)
    elif menu_choice == "4":
        if show_edit_accessories and show_remove_truck:
            view_accessories(selected_truck, truck_list)
        else:
            print("Invalid selection")
            time.sleep(1.5)
            edit_truck(selected_truck)
    elif menu_choice == "0":
        edit_auto_trucks()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        edit_truck(selected_truck)

def choose_cabins(database_name, cabin_1=False, cabin_2=False, cabin_3=False, cabin_8x4=False, mode="man", internal_name=None): # mode can be man, add or edit
    print("\n"*50)
    database_ini = configparser.ConfigParser()
    database_ini.read("database.ini")
    if mode == "edit":
        print("Select cabin of %s (%s) to toggle support" % (internal_name, database_name))
    else:
        print("Select cabin of %s to toggle support" % database_name)
    print("")
    if "cabin_1" in database_ini[database_name]:
        if not cabin_1:
            print("1 - [ ] - %s" % database_ini[database_name]["cabin_1_name"])
        else:
            print("1 - [X] - %s" % database_ini[database_name]["cabin_1_name"])
    else:
        cabin_1 = None
    if "cabin_2" in database_ini[database_name]:
        if not cabin_2:
            print("2 - [ ] - %s" % database_ini[database_name]["cabin_2_name"])
        else:
            print("2 - [X] - %s" % database_ini[database_name]["cabin_2_name"])
    else:
        cabin_2 = None
    if "cabin_3" in database_ini[database_name]:
        if not cabin_3:
            print("3 - [ ] - %s" % database_ini[database_name]["cabin_3_name"])
        else:
            print("3 - [X] - %s" % database_ini[database_name]["cabin_3_name"])
    else:
        cabin_3 = None
    if "cabin_8x4" in database_ini[database_name]:
        if not cabin_8x4:
            print("4 - [ ] - %s" % database_ini[database_name]["cabin_8x4_name"])
        else:
            print("4 - [X] - %s" % database_ini[database_name]["cabin_8x4_name"])
    else:
        cabin_8x4 = None
    print("")
    print("5 - Confirm")
    print("")
    print("0 - Cancel")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1" and cabin_1 != None:
        cabin_1 = not cabin_1
        choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)
    elif menu_choice == "2" and cabin_2 != None:
        cabin_2 = not cabin_2
        choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)
    elif menu_choice == "3" and cabin_3 != None:
        cabin_3 = not cabin_3
        choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)
    elif menu_choice == "4" and cabin_8x4 != None:
        cabin_8x4 = not cabin_8x4
        choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)
    elif menu_choice == "5" and (cabin_1 or cabin_2 or cabin_3 or cabin_8x4):
        cabins_selected = []
        selected_cabin_numbers = []
        if cabin_1:
            cabins_selected.append(database_ini[database_name]["cabin_1"])
            selected_cabin_numbers.append("1")
        if cabin_2:
            cabins_selected.append(database_ini[database_name]["cabin_2"])
            selected_cabin_numbers.append("2")
        if cabin_3:
            cabins_selected.append(database_ini[database_name]["cabin_3"])
            selected_cabin_numbers.append("3")
        if cabin_8x4:
            cabins_selected.append(database_ini[database_name]["cabin_8x4"])
            selected_cabin_numbers.append("8x4")
        cabins_selected = ",".join(i for i in cabins_selected)
        selected_cabin_numbers = ",".join(i for i in selected_cabin_numbers)
        list_ini = configparser.ConfigParser()
        if mode in ["man", "man switch"]:
            list_ini.read("truck lists/manual.ini")
            list_ini["Params"]["database_name"] = database_name
            list_ini["Params"]["make"] = database_ini[database_name]["make"]
            list_ini["Params"]["model"] = database_ini[database_name]["model"]
            list_ini["Params"]["cabins"] = cabins_selected
            list_ini["Params"]["cabin_numbers"] = selected_cabin_numbers
            if mode == "man switch" and list_ini["Params"]["list_type"] == "euro":
                list_ini["Params"]["list_type"] = "american"
            elif mode == "man switch" and list_ini["Params"]["list_type"] == "american":
                list_ini["Params"]["list_type"] = "euro"
            with open("truck lists/manual.ini", "w") as configfile:
                list_ini.write(configfile)
            print("Supported truck changed successfully")
            time.sleep(1.5)
            select_truck(mode)
        else:
            print("")
            print("Note: internal name should: - be 12 or fewer characters")
            print("                            - consist of only letters, numbers and underscores")
            print("                            - be unique")
            print("Paintjob Packer will warn you if the name is already in use in this paintjob pack,")
            print("however please take caution when using multiple mods at once")
            print("")
            new_internal_name = input("Enter internal name for paintjob, or nothing to cancel: ")
            print("")
            config = configparser.ConfigParser()
            config.read("config.ini")
            truck_list = config["Params"]["truck_list"]
            list_ini.read("truck lists/%s.ini" % truck_list)
            if new_internal_name == "":
                choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)
            else: # TODO: REWRITE THIS MESS
                new_internal_name = re.sub("\W+","",new_internal_name).lower()
                if len(new_internal_name) <= 12:
                    if new_internal_name not in list_ini.sections():
                        print("Internal name %s is okay" % new_internal_name)
                        name_is_okay = True
                    else:
                        if new_internal_name == internal_name and mode == "edit":
                            print("Internal name %s is okay" % new_internal_name)
                            name_is_okay = True
                        else:
                            print("Internal name %s already exists in %s" % (new_internal_name, truck_list))
                            name_is_okay = False
                else:
                    print("Internal name %s is too long" % new_internal_name)
                    name_is_okay = False
                if name_is_okay:
                    time.sleep(1)
                    if mode == "add" or (mode == "edit" and internal_name != new_internal_name):
                        list_ini.add_section(new_internal_name)
                        list_ini[new_internal_name]["database_name"] = database_name
                        list_ini[new_internal_name]["make"] = database_ini[database_name]["make"]
                        list_ini[new_internal_name]["model"] = database_ini[database_name]["model"]
                    list_ini[new_internal_name]["cabins"] = cabins_selected
                    list_ini[new_internal_name]["cabin_numbers"] = selected_cabin_numbers
                    list_ini[new_internal_name]["new_truck_format"] = database_ini[database_name]["new_truck_format"]
                    list_ini[new_internal_name]["vehicle_type"] = database_ini[database_name]["vehicle_type"]
                    if list_ini[new_internal_name].getboolean("new_truck_format"):
                        print("Truck uses the new accessory format! Ensure you edit its accessory textures and assign its accessories")
                        time.sleep(2.5)
                        accessories_ini = configparser.ConfigParser()
                        accessories_ini.read("accessories.ini")
                        list_ini[new_internal_name]["accessory_name_list"] = "default_accessory_texture"
                        all_accessory_types = []
                        for accessory_type in accessories_ini.options(database_name):
                            all_accessory_types.append("%s=0" % accessory_type)
                        list_ini[new_internal_name]["accessory_dict"] = ",".join(all_accessory_types)
                    if mode == "edit" and internal_name != new_internal_name:
                        list_ini.remove_section(internal_name)
                    with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                        list_ini.write(configfile)
                    if mode == "add":
                        print("Truck added successfully")
                        time.sleep(1.5)
                        edit_auto_trucks()
                    else:
                        print("Truck edited successfully")
                        time.sleep(1.5)
                        edit_truck(new_internal_name)
                else:
                    time.sleep(2.5)
                    choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)
    elif menu_choice == "0":
        if mode == "edit":
            edit_truck(internal_name)
        else:
            select_truck(mode)
    else:
        print("Invalid selection")
        time.sleep(1.5)
        choose_cabins(database_name, cabin_1, cabin_2, cabin_3, cabin_8x4, mode, internal_name)

def edit_man_internal_name():
    print("\n"*50)
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/manual.ini")
    internal_name = list_ini["Params"]["internal_name"]
    print("Note: internal name should: - be 12 or fewer characters")
    print("                            - consist of only letters, numbers and underscores")
    print("                            - be unique")
    print("Please take caution when using multiple mods at once")
    print("")
    new_internal_name = input("Enter new internal name: ")
    new_internal_name = re.sub("\W+","",new_internal_name).lower()
    if len(new_internal_name) <= 12:
        print("Internal name %s is okay" % new_internal_name)
        time.sleep(1)
        list_ini["Params"]["internal_name"] = new_internal_name
        with open("truck lists/manual.ini", "w") as configfile:
            list_ini.write(configfile)
        print("Internal name changed successfully")
        time.sleep(1.5)
        view_params(manual=True)
    else:
        print("Internal name %s is too long" % new_internal_name)
        time.sleep(2.5)
        edit_man_internal_name()

def create_new_list(new_truck_list=None):
    print("\n"*50)
    config = configparser.ConfigParser()
    config.read("config.ini")
    all_truck_lists = config["Params"]["all_truck_lists"]
    all_truck_lists = all_truck_lists.split(",")
    print("Current paintjob pack: %s" % config["Params"]["truck_list"])
    if new_truck_list != None:
        print("New paintjob pack: %s" % new_truck_list)
    if len(all_truck_lists) > 1:
        print("")
        print("Other paintjob packs:")
        for other_list in all_truck_lists:
            if other_list != config["Params"]["truck_list"]:
                list_ini = configparser.ConfigParser()
                list_ini.read("truck lists/%s.ini" % other_list)
                print("%s" % other_list)
    print("")
    if new_truck_list == None:
        new_truck_list = input("Enter name for new pack: ")
        print("")
        if new_truck_list in all_truck_lists or new_truck_list in ("manual","defaults_euro","defaults_american"):
            print("Name already exists, choose another")
            time.sleep(1.5)
            new_truck_list = None
        elif "," in new_truck_list:
            print("Name cannot contain any commas")
            time.sleep(1.5)
            new_truck_list = None
        create_new_list(new_truck_list)
    else:
        print("")
        print("Select game to support: ")
        print("")
        print("1 - Euro Truck Simulator 2")
        print("2 - American Truck Simulator")
        print("")
        menu_choice = input("Enter selection: ")
        if menu_choice in ["1","2"]:
            defaults_ini = configparser.ConfigParser()
            list_ini = configparser.ConfigParser()
            list_ini.add_section("Params")
            if menu_choice == "1":
                list_ini["Params"]["list_type"] = "euro"
                defaults_ini.read("truck lists/defaults_euro.ini")
            else:
                list_ini["Params"]["list_type"] = "american"
                defaults_ini.read("truck lists/defaults_american.ini")
            list_ini["Params"]["ingame_name"] = defaults_ini["Params"]["ingame_name"]
            list_ini["Params"]["price"] = defaults_ini["Params"]["price"]
            list_ini["Params"]["unlock_level"] = defaults_ini["Params"]["unlock_level"]
            list_ini["Params"]["pack_version"] = defaults_ini["Params"]["pack_version"]
            list_ini["Params"]["pack_author"] = defaults_ini["Params"]["pack_author"]
            internal_name = defaults_ini["Params"]["internal_name"]
            list_ini.add_section(internal_name)
            list_ini[internal_name]["database_name"] = defaults_ini["Params"]["database_name"]
            list_ini[internal_name]["make"] = defaults_ini["Params"]["make"]
            list_ini[internal_name]["model"] = defaults_ini["Params"]["model"]
            list_ini[internal_name]["cabins"] = defaults_ini["Params"]["cabins"]
            list_ini[internal_name]["cabin_numbers"] = defaults_ini["Params"]["cabin_numbers"]
            with open("truck lists/%s.ini" % new_truck_list, "w") as configfile:
                list_ini.write(configfile)
            print("New pack made successfully")
            print("Default values used, please change them to your liking")
            time.sleep(3)
            config["Params"]["truck_list"] = new_truck_list
            all_truck_lists.append(new_truck_list)
            config["Params"]["all_truck_lists"] = ",".join(i for i in all_truck_lists)
            with open("config.ini", "w") as configfile:
                config.write(configfile)
            view_params()
        else:
            print("Invalid selection")
            time.sleep(1.5)
            create_new_list(new_truck_list)

def rename_truck_list(truck_list):
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini")
    print("\n"*50)
    print("Current paintjob pack: %s" % truck_list)
    print("")
    new_truck_list = input("Enter new pack name, or nothing to cancel: ")
    all_truck_lists = config_ini["Params"]["all_truck_lists"].split(",")
    if new_truck_list== "":
        view_params(manual=False)
    elif new_truck_list in all_truck_lists or new_truck_list in ["manual", "defaults_euro", "defaults_american"]:
        print("Name already exists")
        time.sleep(1.5)
        rename_truck_list(truck_list)
    elif "," in new_truck_list:
        print("Name cannot contain any commas")
        time.sleep(1.5)
        rename_truck_list(truck_list)
    else:
        os.rename("truck lists/%s.ini" % truck_list, "truck lists/%s.ini" % new_truck_list)
        config_ini["Params"]["truck_list"] = new_truck_list
        all_truck_lists.remove(truck_list)
        all_truck_lists.append(new_truck_list)
        config_ini["Params"]["all_truck_lists"] = ",".join(all_truck_lists)
        with open("config.ini", "w") as configfile:
            config_ini.write(configfile)
        print("Name changed successfully")
        time.sleep(1.5)
        view_params(manual=False)

def view_accessories(internal_name, truck_list):
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    if truck_list == "manual":
        list_key = "Params"
    else:
        list_key = internal_name
    accessory_name_list = list_ini[list_key]["accessory_name_list"].split(",")
    accessory_dict = dict(item.split("=") for item in list_ini[list_key]["accessory_dict"].split(","))
    database_name = list_ini[list_key]["database_name"]
    print("\n"*50)
    if truck_list == "manual":
        print("Current truck: %s (%s accessory textures)" % (database_name, len(accessory_name_list)))
    else:
        print("Current truck: %s (%s, %s accessory textures)" % (internal_name, database_name, len(accessory_name_list)))
    print("")
    accessory_name_counter = 0
    for accessory_name in accessory_name_list:
        assigned_accessories = 0
        for accessory_type in accessory_dict:
            if accessory_dict[accessory_type] == str(accessory_name_counter):
                assigned_accessories += 1
        print("%s - Edit %s (%s accessories assigned)" % (str(accessory_name_counter+1), accessory_name, str(assigned_accessories)))
        accessory_name_counter += 1
    print("%s - Assign accessories" % str(accessory_name_counter+1))
    print("%s - Create new accessory texture" % str(accessory_name_counter+2))
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "0":
        if truck_list == "manual":
            view_params(manual = True)
        else:
            edit_truck(internal_name)
    elif menu_choice in [str(i+1) for i in range(len(accessory_name_list))]:
        edit_accessory_name(internal_name, truck_list, int(menu_choice)-1)
    elif menu_choice == str(accessory_name_counter+1):
        assign_accessories(internal_name, truck_list)
    elif menu_choice == str(accessory_name_counter+2):
        print("")
        new_accessory_name = input("Enter name for new accessory texture, or nothing to cancel: ")
        if new_accessory_name == "":
            view_accessories(internal_name, truck_list)
        elif new_accessory_name in accessory_name_list:
            print("Name already exists, cancelling...")
            time.sleep(1.5)
            view_accessories(internal_name, truck_list)
        else:
            new_accessory_name = re.sub("\W+","",new_accessory_name).lower()
            accessory_name_list.append(new_accessory_name)
            accessory_name_list = ",".join(accessory_name_list)
            list_ini[list_key]["accessory_name_list"] = accessory_name_list
            with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                list_ini.write(configfile)
            print("Created new accessory texture successfully")
            time.sleep(1.5)
            view_accessories(internal_name, truck_list)
    else:
        print("Invalid selection")
        time.sleep(1.5)
        view_accessories(internal_name, truck_list)

def edit_accessory_name(internal_name, truck_list, accessory_name_index):
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    if truck_list == "manual":
        list_key = "Params"
    else:
        list_key = internal_name
    accessory_name_list = list_ini[list_key]["accessory_name_list"].split(",")
    accessory_dict = dict(item.split("=") for item in list_ini[list_key]["accessory_dict"].split(","))
    accessory_name = accessory_name_list[accessory_name_index]
    assigned_accessories = []
    for accessory_type in accessory_dict:
        if accessory_dict[accessory_type] == str(accessory_name_index):
            assigned_accessories.append(accessory_type)
    database_name = list_ini[list_key]["database_name"]
    print("\n"*50)
    print("Current accessory texture: %s" % accessory_name_list[accessory_name_index])
    print("")
    print("Assigned accessories:") # TODO: accessory_type_name
    for accessory_type in assigned_accessories:
        print(accessory_type)
    print("")
    print("1 - Rename %s" % accessory_name)
    if len(accessory_name_list) > 1:
        print("2 - Remove %s (any assigned accessories will be reassigned to a different texture)" % accessory_name)
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        print("")
        new_accessory_name = input("Enter new name, or nothing to cancel: ")
        if new_accessory_name == "":
            edit_accessory_name(internal_name, truck_list, accessory_name_index)
        elif new_accessory_name in accessory_name_list:
            print("Name already exists, cancelling...")
            time.sleep(1.5)
            edit_accessory_name(internal_name, truck_list, accessory_name_index)
        else:
            new_clean_accessory_name = ""
            for character in new_accessory_name:
                if character not in (",", " "):
                    new_clean_accessory_name += character
            new_accessory_name = new_clean_accessory_name
            accessory_name_list.remove(accessory_name)
            accessory_name_list.append(new_accessory_name)
            accessory_name_list = ",".join(accessory_name_list)
            list_ini[list_key]["accessory_name_list"] = accessory_name_list
            with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                list_ini.write(configfile)
            print("Renamed accessory texture successfully")
            time.sleep(1.5)
            view_accessories(internal_name, truck_list)
    elif menu_choice == "2" and len(accessory_name_list) > 1:
        verbose_accessory_dict = {}
        for accessory_type in accessory_dict:
            verbose_accessory_dict[accessory_type] = accessory_name_list[int(accessory_dict[accessory_type])]
        accessory_name_list.remove(accessory_name)
        for accessory_type in verbose_accessory_dict:
            if verbose_accessory_dict[accessory_type] in accessory_name_list:
                verbose_accessory_dict[accessory_type] = accessory_name_list.index(verbose_accessory_dict[accessory_type])
            else:
                verbose_accessory_dict[accessory_type] = 0
        accessory_name_list = ",".join(accessory_name_list)
        list_ini[list_key]["accessory_name_list"] = accessory_name_list
        all_accessory_types = []
        for each_accessory_type in verbose_accessory_dict:
            all_accessory_types.append("%s=%s" % (each_accessory_type, verbose_accessory_dict[each_accessory_type]))
        list_ini[list_key]["accessory_dict"] = ",".join(all_accessory_types)
        with open("truck lists/%s.ini" % truck_list, "w") as configfile:
            list_ini.write(configfile)
        print("Removed accessory texture successfully")
        time.sleep(1.5)
        view_accessories(internal_name, truck_list)
    elif menu_choice == "0":
        view_accessories(internal_name, truck_list)
    else:
        print("Invalid selection")
        time.sleep(1.5)
        edit_accessory_name(internal_name, truck_list, accessory_name_index)

def assign_accessories(internal_name, truck_list):
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    if truck_list == "manual":
        list_key = "Params"
    else:
        list_key = internal_name
    accessory_name_list = list_ini[list_key]["accessory_name_list"].split(",")
    accessory_dict = dict(item.split("=") for item in list_ini[list_key]["accessory_dict"].split(","))
    database_name = list_ini[list_key]["database_name"]
    print("\n"*50)
    menu_choice_counter = 1
    for accessory_type in accessory_dict:
        print("%s - Reassign %s (currently assigned to %s)" % (menu_choice_counter, accessory_type, accessory_name_list[int(accessory_dict[accessory_type])]))
        menu_choice_counter += 1
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice in [str(i+1) for i in range(len(accessory_dict))]:
        accessory_type = list(accessory_dict.keys())[int(menu_choice)-1]
        print("\n"*50)
        menu_choice_counter = 1
        for accessory_name in accessory_name_list:
            print("%s - Assign %s to %s" % (menu_choice_counter, accessory_type, accessory_name_list[menu_choice_counter-1]))
            menu_choice_counter += 1
        print("")
        menu_choice = input("Enter selection, or nothing to cancel: ")
        if menu_choice in [str(i+1) for i in range(len(accessory_name_list))]:
            accessory_dict[accessory_type] = str(int(menu_choice)-1)
            all_accessory_types = []
            for each_accessory_type in accessory_dict:
                all_accessory_types.append("%s=%s" % (each_accessory_type, accessory_dict[each_accessory_type]))
            list_ini[list_key]["accessory_dict"] = ",".join(all_accessory_types)
            with open("truck lists/%s.ini" % truck_list, "w") as configfile:
                list_ini.write(configfile)
            print("Reassigned %s successfully" % accessory_type)
            time.sleep(1.5)
            assign_accessories(internal_name, truck_list)
        else:
            assign_accessories(internal_name, truck_list)
    elif menu_choice == "0":
        view_accessories(internal_name, truck_list)
    else:
        print("Invalid selection")
        time.sleep(1.5)
        assign_accessories(internal_name, truck_list)

menu()
