import paintjob, configparser, sys, time

def menu():
    print("\n"*50)
    paintjob.welcome_message()
    print("")
    print("=== Full Paintjob Pack Generator ===")
    print("")
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini")
    truck_list = config_ini["Params"]["truck_list"]
    print("Current truck list: %s" % truck_list)
    print("")
    print("1 - Generate pack from current list")
    print("2 - Change to another list")
    print("")
    print("0 - Exit program")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        make_pack(truck_list)
    elif menu_choice == "2":
        switch_truck_list()
    elif menu_choice == "0":
        print("\n"*50)
        sys.exit()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        menu()

def switch_truck_list():
    print("\n"*50)
    config = configparser.ConfigParser()
    config.read("config.ini")
    truck_list = config["Params"]["truck_list"]
    all_truck_lists = config["Params"]["all_truck_lists"].split(",")
    print("Current truck list: %s" % truck_list)
    print("")
    all_truck_lists.remove(truck_list)
    menu_choice_counter = 1
    if len(all_truck_lists) != 0:
        for other_truck_list in all_truck_lists:
            list_ini = configparser.ConfigParser()
            list_ini.read("truck lists/%s.ini" % other_truck_list)
            print("%s - Switch to %s (%s trucks)" % (menu_choice_counter, other_truck_list, str(len(list_ini.sections())-1)))
            menu_choice_counter += 1
    else:
        print("No other truck lists")
    print("")
    print("0 - Back to previous menu")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice in [str(i+1) for i in range(len(all_truck_lists))]:
        new_truck_list = all_truck_lists[int(menu_choice)-1]
        config["Params"]["truck_list"] = new_truck_list
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        print("Switched to %s successfully" % new_truck_list)
        time.sleep(1.5)
        switch_truck_list()
    elif menu_choice == "0":
        menu()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        switch_truck_list()

def make_pack(truck_list):
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)
    make_pack_files(truck_list)
    list_of_trucks = list_ini.sections()
    list_of_trucks.remove("Params")
    for internal_name in list_of_trucks:
        make_truck_files(internal_name, truck_list)
    finish_up(truck_list)

def make_pack_files(truck_list):
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)

    pack_version = list_ini["Params"]["pack_version"]
    pack_name = list_ini["Params"]["pack_name"]
    pack_author = list_ini["Params"]["pack_author"]

    print("Creating overall mod files...")
    paintjob.Folders.common_mod_folders()
    paintjob.Files.manifest_sii(pack_version=pack_version, pack_name=pack_name, pack_author=pack_author)
    paintjob.Files.copy_mod_package_files(truck_list=truck_list)

def make_truck_files(internal_name, truck_list):
    list_ini = configparser.ConfigParser()
    list_ini.read("truck lists/%s.ini" % truck_list)

    ingame_name = list_ini["Params"]["ingame_name"]
    price = list_ini["Params"]["price"]
    unlock_level = list_ini["Params"]["unlock_level"]

    make = list_ini[internal_name]["make"]
    model = list_ini[internal_name]["model"]
    cabins = list_ini[internal_name]["cabins"]
    cabins = cabins.split(",")

    vehicle_type = list_ini[internal_name]["vehicle_type"]
    database_name = list_ini[internal_name]["database_name"]
    new_truck_format = list_ini[internal_name].getboolean("new_truck_format")

    if new_truck_format:
        accessory_name_list = manual["Params"]["accessory_name_list"].split(",")
        accessory_dict = dict(item.split("=") for item in manual["Params"]["accessory_dict"].split(","))
    else:
        accessory_name_list = None
        accessory_dict = None

    print("Creating files for %s..." % internal_name)
    paintjob.Folders.specific_mod_folders(make=make, model=model, new_truck_format=new_truck_format, internal_name=internal_name)
    paintjob.Files.def_sii(make=make, model=model, cabins=cabins, internal_name=internal_name, ingame_name=ingame_name, price=price, unlock_level=unlock_level, new_truck_format=new_truck_format)
    if new_truck_format:
        paintjob.Files.def_accessory_sii(make=make, model=model, internal_name=internal_name, accessory_name_list=accessory_name_list, accessory_dict=accessory_dict, database_name=database_name)
    paintjob.Files.material_mat(internal_name=internal_name)
    paintjob.Files.generate_tobj_files(internal_name=internal_name, make=make, model=model, new_truck_format=new_truck_format, accessory_name_list=accessory_name_list)
    paintjob.Files.copy_image_files(truck_list=truck_list, internal_name=internal_name, new_truck_format=new_truck_format, make=make, model=model, accessory_name_list=accessory_name_list)

def finish_up(truck_list):
    print("Compiling mod...")
    paintjob.compile_mod_file(truck_list=truck_list)
    print("Cleaning up...")
    paintjob.Folders.clear_output_folder()

menu()
