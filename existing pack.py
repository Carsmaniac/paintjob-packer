import configparser, time
from library.paintjob import *

existing_ini = configparser.ConfigParser(allow_no_value = True)
existing_ini.read("existing pack.ini")
ini_game = existing_ini["info"]["game"]
ini_pack = existing_ini["info"]["pack"]
pack = Pack(ini_pack, ini_game)

vehicles_to_add = []
for veh in list(existing_ini["add vehicles"].keys()):
    vehicles_to_add.append(Vehicle(veh, ini_game))
if len(vehicles_to_add) > 0:
    print("Pack version: "+pack.version)
    new_version = input("Enter new version, or leave blank to keep the same: ")
    if new_version != "":
        pack.version = new_version
        make_manifest_sii(pack)
    print("")
    make_pack_addon(pack, vehicles_to_add)

if existing_ini["description"].getboolean("workshop desc"):
    make_description(pack, workshop = True)
if existing_ini["description"].getboolean("manifest desc"):
    make_description(pack, workshop = False)

clear_existing_ini()

print("Success!")
time.sleep(2)
