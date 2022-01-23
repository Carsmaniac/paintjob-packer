import sys, os, configparser

def menu():
    print("1. Create nested spreadsheet OR functions")
    print("2. Print list of vehicle paths")
    print("3. Generate mod-links.md")
    choice = input("\nEnter selection, or nothing to quit: ")

    if choice == "":
        sys.exit()
    elif choice == "1":
        menu_1()
    elif choice == "2":
        menu_2()
    elif choice == "3":
        menu_3()
    else:
        cls()
        print("Try again\n")
        menu()

def menu_1():
    cls()
    ats_list = os.listdir("vehicles/ats")
    ets_list = os.listdir("vehicles/ets")
    ats_only_list = []
    ets_only_list = []
    both_list = []
    for veh in ats_list:
        if veh in ets_list:
            both_list.append(veh[:-4])
        else:
            ats_only_list.append(veh[:-4])
    for veh in ets_list:
        if veh not in ats_list:
            ets_only_list.append(veh[:-4])

    cell_name = input("Enter cell to check for ATS vehicles: ")
    nested_function = "="
    nested_function += "OR(" * (len(ats_only_list) - 1)
    nested_function += "ISNUMBER(SEARCH(\"{}\",{}))".format(ats_only_list[0], cell_name)
    for i in range(len(ats_only_list) - 1):
        nested_function += ",ISNUMBER(SEARCH(\"{}\",{})))".format(ats_only_list[i + 1], cell_name)
    print("\n\n"+nested_function+"\n")

    cell_name = input("\nEnter cell to check for ETS 2 vehicles: ")
    nested_function = "="
    nested_function += "OR(" * (len(ets_only_list) - 1)
    nested_function += "ISNUMBER(SEARCH(\"{}\",{}))".format(ets_only_list[0], cell_name)
    for i in range(len(ets_only_list) - 1):
        nested_function += ",ISNUMBER(SEARCH(\"{}\",{})))".format(ets_only_list[i + 1], cell_name)
    print("\n\n"+nested_function+"\n")

    cell_name = input("\nEnter cell to check for both vehicles: ")
    nested_function = "="
    nested_function += "OR(" * (len(both_list) - 1)
    nested_function += "ISNUMBER(SEARCH(\"{}\",{}))".format(both_list[0], cell_name)
    for i in range(len(both_list) - 1):
        nested_function += ",ISNUMBER(SEARCH(\"{}\",{})))".format(both_list[i + 1], cell_name)
    print("\n\n"+nested_function+"\n\n")
    to_exit()

def menu_2():
    cls()
    ats_list = os.listdir("vehicles/ats")
    print("\n================ ATS Vehicles ================\n")
    for file in ats_list:
        print(file[:-4])
    ets_list = os.listdir("vehicles/ets")
    print("\n================ ETS 2 Vehicles ================\n")
    for file in ets_list:
        print(file[:-4])

    print("\n\n")
    to_exit()
def menu_3():
    cls()
    mod_links_text = ""

    # Get ETS vehicles
    ets_list = os.listdir("vehicles/ets")
    ets_trucks = []
    ets_buses = []
    ets_trailers = []
    for veh in ets_list:
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("vehicles/ets/" + veh, encoding = "utf-8")
        if veh_ini["vehicle info"].getboolean("mod"):
            if veh_ini["vehicle info"].getboolean("trailer"):
                ets_trailers.append(veh_ini)
            elif veh_ini["vehicle info"].getboolean("bus mod"):
                ets_buses.append(veh_ini)
            else:
                ets_trucks.append(veh_ini)
    ets_trucks.sort(key = lambda veh: veh["vehicle info"]["name"].lower())
    ets_buses.sort(key = lambda veh: veh["vehicle info"]["name"].lower())
    ets_trailers.sort(key = lambda veh: veh["vehicle info"]["name"].lower())

    # Print ETS list
    mod_links_text += ("# Euro Truck Simulator 2\n\n## Trucks\n")
    for veh in ets_trucks:
        links = []
        if veh["vehicle info"]["mod link workshop"] != "":
            links.append("[Steam Workshop]({})".format(veh["vehicle info"]["mod link workshop"]))
        if veh["vehicle info"]["mod link trucky"] != "":
            links.append("[TruckyMods]({})".format(veh["vehicle info"]["mod link trucky"]))
        if veh["vehicle info"]["mod link forums"] != "":
            links.append("[SCS Forums]({})".format(veh["vehicle info"]["mod link forums"]))
        if veh["vehicle info"]["mod link author site"] != "":
            links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** - {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))
    mod_links_text += ("\n\n## Buses\n")
    for veh in ets_buses:
        links = []
        if veh["vehicle info"]["mod link workshop"] != "":
            links.append("[Steam Workshop]({})".format(veh["vehicle info"]["mod link workshop"]))
        if veh["vehicle info"]["mod link trucky"] != "":
            links.append("[TruckyMods]({})".format(veh["vehicle info"]["mod link trucky"]))
        if veh["vehicle info"]["mod link forums"] != "":
            links.append("[SCS Forums]({})".format(veh["vehicle info"]["mod link forums"]))
        if veh["vehicle info"]["mod link author site"] != "":
            links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** - {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))
    mod_links_text += ("\n\n## Trailers\n")
    for veh in ets_trailers:
        links = []
        if veh["vehicle info"]["mod link workshop"] != "":
            links.append("[Steam Workshop]({})".format(veh["vehicle info"]["mod link workshop"]))
        if veh["vehicle info"]["mod link trucky"] != "":
            links.append("[TruckyMods]({})".format(veh["vehicle info"]["mod link trucky"]))
        if veh["vehicle info"]["mod link forums"] != "":
            links.append("[SCS Forums]({})".format(veh["vehicle info"]["mod link forums"]))
        if veh["vehicle info"]["mod link author site"] != "":
            links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** - {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))

    # Get ATS vehicles
    ats_list = os.listdir("vehicles/ats")
    ats_trucks = []
    ats_buses = []
    ats_trailers = []
    for veh in ats_list:
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("vehicles/ats/" + veh, encoding = "utf-8")
        if veh_ini["vehicle info"].getboolean("mod"):
            if veh_ini["vehicle info"].getboolean("trailer"):
                ats_trailers.append(veh_ini)
            else:
                ats_trucks.append(veh_ini)
    ats_trucks.sort(key = lambda veh: veh["vehicle info"]["name"].lower())
    ats_trailers.sort(key = lambda veh: veh["vehicle info"]["name"].lower())

    # Print ATS list
    mod_links_text += ("\n\n# American Truck Simulator \n\n## Trucks\n")
    for veh in ats_trucks:
        links = []
        if veh["vehicle info"]["mod link workshop"] != "":
            links.append("[Steam Workshop]({})".format(veh["vehicle info"]["mod link workshop"]))
        if veh["vehicle info"]["mod link trucky"] != "":
            links.append("[TruckyMods]({})".format(veh["vehicle info"]["mod link trucky"]))
        if veh["vehicle info"]["mod link forums"] != "":
            links.append("[SCS Forums]({})".format(veh["vehicle info"]["mod link forums"]))
        if veh["vehicle info"]["mod link author site"] != "":
            links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** - {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))
    mod_links_text += ("\n\n## Trailers\n")
    for veh in ats_trailers:
        links = []
        if veh["vehicle info"]["mod link workshop"] != "":
            links.append("[Steam Workshop]({})".format(veh["vehicle info"]["mod link workshop"]))
        if veh["vehicle info"]["mod link trucky"] != "":
            links.append("[TruckyMods]({})".format(veh["vehicle info"]["mod link trucky"]))
        if veh["vehicle info"]["mod link forums"] != "":
            links.append("[SCS Forums]({})".format(veh["vehicle info"]["mod link forums"]))
        if veh["vehicle info"]["mod link author site"] != "":
            links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** - {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))

    # Print end statement
    mod_links_text += ("\n\n---\n\n* This mod list applies to both Paint Job Packer and my template packs, they support the same list of mods")
    mod_links_text += ("\n* Paint Job Packer only supports mods that are uploaded to reutable sites by their original authors and are freely available to download")

    file = open("mod links.md", "w", encoding = "utf-8")
    file.write(mod_links_text)
    file.close()

    print("Saved new mod links.md\n")
    to_exit()

def cls():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def to_exit():
    choice = input("Enter 1 to exit, 2 to restart ")
    if choice == "1":
        sys.exit()
    elif choice == "2":
        cls()
        menu()
    else:
        to_exit()

cls()
print("This file is used for miscellaneous functions related to the management of Paint Job Packer")
print("You can run the program itself, and make paint job mods, by running \"packer.py\"\n")
menu()
