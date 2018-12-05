import paintjob, configparser, sys, time

def menu():
    print("\n"*50)
    paintjob.welcome_message()
    print("")
    print("=== Full Paintjob Pack Generator ===")
    print("")
    config = configparser.ConfigParser()
    config.read("config.ini")
    list_name = config["Params"]["list_name"]
    print("Current truck list: %s" % list_name)
    print("")
    print("1 - Generate pack from current list")
    print("2 - Change to another list")
    print("")
    print("0 - Exit program")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        make_pack()
    elif menu_choice == "2":
        switch_truck_list()
    elif menu_choice == "0":
        sys.exit()
    else:
        print("Invalid selection")
        time.sleep(1.5)
        menu()
