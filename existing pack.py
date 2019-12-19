import configparser
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
    if vehicles_to_add[0] != "":
        make_pack_addon(pack, vehicles_to_add)

if existing_ini["description"].getboolean("workshop desc"):
    make_workshop_description(pack)
if existing_ini["description"].getboolean("manifest desc"):
    make_manifest_description(pack)

clear_existing_ini()
