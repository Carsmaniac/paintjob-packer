import sys, os, configparser, zipfile
from paintjob import strip_diacritics

def menu():
    print("1. Print list of vehicle paths")
    print("2. Generate mod-links.md")
    print("3. Check vehicle database accessories")
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
    print("\n================ ATS Vehicles ================\n")
    for file in ats_list:
        print(file[:-4])
    ets_list = os.listdir("vehicles/ets")
    print("\n================ ETS 2 Vehicles ================\n")
    for file in ets_list:
        print(file[:-4])

    print("\n\n")
    to_exit()

def menu_2():
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
            if veh["vehicle info"]["mod author"][-1:].lower() == "s":
                links.append("[{}' Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
            else:
                links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** – {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))
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
            if veh["vehicle info"]["mod author"][-1:].lower() == "s":
                links.append("[{}' Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
            else:
                links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** – {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))
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
            if veh["vehicle info"]["mod author"][-1:].lower() == "s":
                links.append("[{}' Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
            else:
                links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** – {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))

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
            if veh["vehicle info"]["mod author"][-1:].lower() == "s":
                links.append("[{}' Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
            else:
                links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** – {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))
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
            if veh["vehicle info"]["mod author"][-1:].lower() == "s":
                links.append("[{}' Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
            else:
                links.append("[{}'s Site]({})".format(veh["vehicle info"]["mod author"], veh["vehicle info"]["mod link author site"]))
        mod_links_text += ("\n* {} by **{}** – {}".format(veh["vehicle info"]["name"], veh["vehicle info"]["mod author"], " / ".join(links)))

    # Print end statement
    mod_links_text += ("\n\n---\n\n* This mod list applies to both Paint Job Packer and my template packs, they support the same list of mods\n")
    mod_links_text += ("* Paint Job Packer only supports mods that are uploaded to reutable sites by their original authors and are freely available to download\n")

    file = open("mod links.md", "w", encoding = "utf-8")
    file.write(mod_links_text)
    file.close()

    print("Saved new mod links.md\n")
    to_exit()

def menu_3():
    cls()
    untextured_accessories = input("List untextured accessories? (y/n) ").lower() == "y"
    ini_name = input("List incorrectly named INIs? (y/n) ").lower() == "y"
    print("\n")
    for game in ["ats", "ets"]:
        for file in os.listdir("vehicles/"+game):
            veh = configparser.ConfigParser(allow_no_value = True)
            veh.read("vehicles/{}/{}".format(game, file), encoding = "utf-8")

            veh_author = veh["vehicle info"]["mod author"]
            if veh_author == "":
                veh_author = "SCS"
            veh_name = "{} [{}]".format(veh["vehicle info"]["name"], veh_author)
            if file[:-4] != "{} [{}]".format(veh["vehicle info"]["vehicle path"], strip_diacritics(veh_author)):
                if ini_name:
                    print("! {} should be named {}".format(file, "{} [{}]".format(veh["vehicle info"]["vehicle path"], strip_diacritics(veh_author))))

            try:
                templates = zipfile.ZipFile("../templates/{} templates/{} [{}].zip".format(game, veh["vehicle info"]["vehicle path"], strip_diacritics(veh_author)))
            except FileNotFoundError:
                print("X Template missing: {} [{}].zip".format(veh["vehicle info"]["vehicle path"], strip_diacritics(veh_author)))
            else:
                for acc in veh["vehicle info"]["accessories"].split(";"):
                    if acc != "":
                        if acc not in veh.sections():
                            print("X Non-existent {} in {} accessories list".format(acc, veh_name))
                        if acc+".dds" not in templates.namelist():
                            if untextured_accessories:
                                print("- {} accessory untextured ({})".format(acc, veh_name))

                for acc in veh.sections():
                    if acc not in ["vehicle info", "cabins", veh["vehicle info"]["name"]]:
                        if acc not in veh["vehicle info"]["accessories"].split(";"):
                            print("X {} not listed in {} accessories list".format(acc, veh_name))

                if veh["vehicle info"].getboolean("trailer"):
                    if not veh["vehicle info"].getboolean("uses accessories"):
                        if veh["vehicle info"]["name"]+".dds" not in templates.namelist():
                            print("X Missing texture: {}".format(veh["vehicle info"]["name"]))
                else:
                    if veh["cabins"].getboolean("separate paintjobs"):
                        if len(veh["cabins"].keys()) < 3:
                            print("X {} should not have separate paint jobs".format(veh_name))
                        for cab in veh["cabins"].keys():
                            if cab != "separate paintjobs":
                                cab_name = veh["cabins"][cab].split(";")[0]
                                if veh["vehicle info"].getboolean("alt uvset"):
                                    cab_name = cab_name.replace(")", ", alt uvset)")
                                if cab_name+".dds" not in templates.namelist():
                                    print("X Missing texture: {} ({})".format(cab_name, veh_name))
                    else:
                        if veh["vehicle info"].getboolean("uses accessories"):
                            if "Cabin.dds" not in templates.namelist():
                                print("X Missing texture: Cabin ({})".format(veh_name))
                        else:
                            if veh["vehicle info"]["name"]+".dds" not in templates.namelist():
                                print("X Missing texture: {}".format(veh["vehicle info"]["name"]))
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
