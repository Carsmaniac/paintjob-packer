import configparser
from library.paintjob import *

print("Reading input file")
input_file = configparser.ConfigParser(allow_no_value = True)
input_file.read("new pack.ini")

game = input_file["pack info"]["game"]

mod_name = input_file["pack info"]["name"]
mod_version = input_file["pack info"]["version"]

list_of_paintjobs = input_file["pack info"]["paintjobs"].split(",")
main_paintjob = input_file["pack info"]["main paintjob"]

related_mods = input_file["pack info"]["related mods"].split(",")
mod_link = input_file["pack info"]["link"]

description = input_file["pack info"]["description"]
more_info = input_file["pack info"]["more info"]
suggested_by = input_file["pack info"]["suggested by"].split(",")

clear_output_folder()

make_manifest_sii(mod_version, mod_name)
copy_mod_manager_image()
make_material_folder()

for pj in list_of_paintjobs:
    if pj == main_paintjob:
        pj_main = True
        pj_all_vehicles = False
    else:
        pj_main = False
    pj_int_name = "cm_"+pj
    pj_name = input_file[pj]["name"]
    pj_price = input_file[pj]["price"]
    pj_colour = input_file[pj]["main colour"]
    if not pj_main:
        pj_all_vehicles = input_file[pj].getboolean("all vehicles")
    pj_list_of_vehicles = []
    if pj_all_vehicles:
        for veh in list(input_file[main_painjob].keys()):
            if veh not in ("name", "price", "main colour", "all vehicles"):
                pj_list_of_vehicles.append(veh)
    else:
        for veh in list(input_file[pj].keys()):
            if veh not in ("name", "price", "main colour", "all vehicles"):
                pj_list_of_vehicles.append(veh)
    copy_paintjob_icon(pj_int_name)
    make_paintjob_icon_tobj(pj_int_name)
    make_paintjob_icon_mat(pj_int_name)
