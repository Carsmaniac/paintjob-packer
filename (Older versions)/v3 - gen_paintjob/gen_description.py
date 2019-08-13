import time

class DescVehicle():
    def example_variables():
        name = "Scania Streamline"
        mod = False
        trailer = False
        mod_author = None
        mod_link = None

def make_description(workshop):
    if workshop:
        file = open("output/workshop_description.txt", "w")
    else:
        file = open("output/mod_manager_description.txt", "w")
    file.write(brief_desc+"\n")
    file.write("\n")
    if other_pack_link != None:
        other_pack_game = {"ets":"American Truck Simulator", "ats":"Euro Truck Simulator 2"}[game_supported]
        if workshop:
            file.write("%s pack available [url=%s]here[/url].\n" % (other_pack_game, other_pack_link))
        else:
            file.write("%s pack also available.\n" % other_pack_game)
        file.write("\n")
    if len(list_scs_trucks) == 1 and len(list_modded_trucks) == 0:
        file.write("This paintjob supports the %s\n" % list_scs_trucks[0].name)
    elif len(list_modded_trucks) == 1 and len(list_scs_trucks) == 0:
        if workshop:
            file.write("This paintjob supports %s's [url=%s]%s[/url]\n" % (list_modded_trucks[0].mod_author, list_modded_trucks[0].mod_link, list_modded_trucks[0].name))
        else:
            file.write("This paintjob supports %s's %s\n" % (list_modded_trucks[0].mod_author, list_modded_trucks[0].name))
    else:
        file.write("Trucks supported:\n")
        for vehicle in list_scs_trucks:
            file.write(vehicle.name+"\n")
        if len(list_modded_trucks) >= 3 and workshop:
            file.write("\n")
            file.write("Modded trucks supported:\n")
        for vehicle in list_modded_trucks:
            if workshop:
                file.write("%s's [url=%s]%s[/url]\n" % (vehicle.mod_author, vehicle.mod_link, vehicle.name))
            else:
                file.write("%s's %s\n" % (vehicle.mod_author, vehicle.name))
        if workshop:
            if len(list_modded_trucks) == 1:
                file.write("(The %s mod isn't required for the pack to function, but if you do have it it'll be supported)\n" % list_modded_trucks[0].name)
            elif len(list_modded_trucks) > 1:
                file.write("(The modded trucks aren't required for the pack to function, but if you do have them they'll be supported)\n")
    file.write("\n")
    if len(list_trailers) == 1:
        if list_trailers[0].name[:3] == "SCS":
            file.write("Also included is an %s paintjob\n" % list_trailers[0].name)
        else:
            file.write("Also included is a %s paintjob\n" % list_trailers[0].name)
        file.write("\n")
    elif len(list_trailers) > 1:
        file.write("Trailers supported:\n")
        for vehicle in list_trailers:
            file.write(vehicle.name+"\n")
        file.write("\n")
    if more_info != None:
        file.write(more_info+"\n")
        file.write("\n")
    if len(related_mods) > 0 and workshop:
        file.write("Related mods:\n")
        for mod in related_mods:
            file.write("[url=%s]%s[/url] - %s\n" % (mod[2], mod[0], mod[1]))
        file.write("\n")
    file.write("Enjoy! :)\n")
    file.write("\n")
    if workshop:
        if len(requested_by) == 1 and requested_by[0] != "":
            file.write("This paintjob was suggested by [b]%s[/b]!\n" % requested_by[0])
        elif len(requested_by) > 1:
            req_str = "[b]%s[/b]" % requested_by[0]
            for person in requested_by[1:]:
                req_str += " and [b]%s[/b]" % person
            file.write("This paintjob was suggested by %s!\n" % req_str)
        file.write("[h1]Have a suggestion for a paintjob?[/h1]\n")
        file.write("Let me know in my [url=https://steamcommunity.com/groups/carsmaniacspaintjobs/discussions/0/1742229167221776476/]suggestions thread[/url]!\n")
    else:
        file.write("Reminder: My mods are only officially available on Steam Workshop. Be sure to download them there for support and updates!\n")
    file.close()

print("Reading input file")
file = open("input_description.txt", "r")
desc_input = file.read().splitlines()
file.close()

requested_by = desc_input[1].split(";")

brief_desc = desc_input[4]
if desc_input[7] != "":
    more_info = desc_input[7]
else:
    more_info = None

if desc_input[10] != "":
    other_pack_link = desc_input[10]
else:
    other_pack_link = None

related_mods = []
if len(desc_input) > 13:
    if desc_input[13] != "":
        for i in range(13, len(desc_input)):
            related_mods.append(desc_input[i].split(";"))

print("Reading info file")
file = open("database/description_info.txt", "r")
desc_info = file.read().splitlines()
file.close()

game_supported = desc_info[0]
vehicles = []
sorted_list = sorted(desc_info[1:])
scs_box_index = None
if "scs box" in sorted_list:
    scs_box_index = sorted_list.index("scs box")
if scs_box_index != None:
    sorted_list.pop(scs_box_index)
    sorted_list.insert(0, "scs box")

for vehicle in sorted_list:
    file = open("database/%s vehicles/%s.txt" % (game_supported, vehicle), "r")
    veh_db = file.read().splitlines()
    file.close()
    index = len(vehicles)
    vehicles.append(DescVehicle())
    vehicles[index].name = veh_db[0]
    vehicles[index].mod_author = veh_db[1][10:]
    vehicles[index].mod_link = veh_db[2][8:]
    if vehicles[index].mod_author == "":
        vehicles[index].mod = False
    else:
        vehicles[index].mod = True
    if veh_db[3][8:] == "true":
        vehicles[index].trailer = True
    else:
        vehicles[index].trailer = False

list_scs_trucks = []
list_modded_trucks = []
list_trailers = []
for vehicle in vehicles:
    if vehicle.trailer:
        list_trailers.append(vehicle)
    else:
        if vehicle.mod:
            list_modded_trucks.append(vehicle)
        else:
            list_scs_trucks.append(vehicle)

print("Compiling workshop description")
make_description(workshop = True)

print("Compiling manifest description")
make_description(workshop = False)

print("Clearing info file")
file = open("database/description_info.txt", "w")
file.close()

print("Complete!")
time.sleep(1.5)
