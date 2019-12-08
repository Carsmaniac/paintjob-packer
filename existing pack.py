import configparser
from library.paintjob import *

existing_ini = configparser.ConfigParser(allow_no_value = True)
existing_ini.read("existing pack.ini")
ini_game = existing_ini["info"]["game"]
ini_pack = existing_ini["info"]["pack"]
pack = Pack(ini_pack, ini_game)

if existing_ini["X to choose"]["add paintjob"] == "X":
    pass

elif existing_ini["X to choose"]["add vehicles"] == "X":
    pass

elif existing_ini["X to choose"]["make description"] == "X":
    if existing_ini["description"].getboolean("workshop desc"):
        make_workshop_description(pack)
    if existing_ini["description"].getboolean("manifest desc"):
        make_manifest_description(pack)

elif existing_ini["X to choose"]["make whole pack"] == "X":
    make_pack(pack)
else:
    print("oops")

clear_existing_ini()

"""to do configparser
allow_no_value
default delimiter :
space after and not before?
default boolean true false (no capital)

"""
