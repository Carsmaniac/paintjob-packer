# What this file needs to do:
# Open > options
# See current trucks and params
#   Split ATS/ETS/trailers?
# Add truck/trailer
# Modify truck/trailer
# Create file from scratch   *or maybe not the above two, just this one
# Modify other params

import paintjob

paintjob.welcome_message()
print("")

def menu():
    print("1 - View modpack parameters")
    print("2 - Edit modpack parameters")
    print("3 - View truck list")
    print("4 - Add truck to truck list")
    print("5 - Generate new truck list from scratch")
    print("")
    menu_choice = input("Enter selection: ")
    if menu_choice == "1":
        view_params()
    elif menu_choice == "2":
        edit_params()
    elif menu_choice == "3":
        view_list()
    elif menu_choice == "4":
        append_list()
    elif menu_choice == "5":
        regen_list()
    else:
        print("Invalid value")
        menu() # yeah this isn't a good idea

def view_params():
    paintjob.load_auto_params()
    pass

def edit_params():
    pass

def view_list():
    pass

def append_list():
    pass

def regen_list():
    pass

paintjob.vartest()
print(paintjob.ape)
