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
link = input_file["pack info"]["link"]

brief_desc = input_file["pack info"]["description"]
more_info = input_file["pack info"]["more info"]

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

    for veh in pj_list_of_vehicles:
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("vehicles/%s/%s.ini" % (game, veh))
        veh_make = veh_ini["vehicle info"]["make"]
        veh_model = veh_ini["vehicle info"]["model"]
        veh_path = veh_ini["vehicle info"]["vehicle path"]
        veh_alt_uvset = veh_ini["vehicle info"].getboolean("alt uvset")
        veh_name = veh_ini["vehicle info"]["name"]
        veh_trailer = veh_ini["vehicle info"].getboolean("trailer")
        veh_mod = veh_ini["vehicle info"].getboolean("mod")
        if veh_mod:
            veh_mod_author = veh_ini["vehicle info"]["mod author"]
            veh_mod_link = veh_ini["vehicle info"]["mod link"]
        veh_uses_accessories = veh_ini["vehicle info"].getboolean("uses accessories")
        if veh_uses_accessories:
            veh_accessories = veh_ini["vehicle info"]["accessories"].split(",")
            veh_acc_dict = {}
            for acc in veh_accessories:
                veh_acc_dict[acc] = list(veh_ini[acc].keys())
        if veh_trailer:
            veh_separate_paintjobs = False
            veh_type = "trailer_owned"
        else:
            veh_separate_paintjobs = veh_ini["cabins"].getboolean("separate paintjobs")
            veh_type = "truck"
            veh_cabins = dict(veh_ini["cabins"].items())
            veh_cabins.pop("separate paintjobs", None)
        make_def_folder(veh_type, veh_path, veh_uses_accessories)
        make_settings_sui(veh_type, veh_path, pj_int_name, pj_name, pj_price)
        make_vehicle_folder(veh_type, pj_int_name, veh_make, veh_model)
        copy_shared_colour_dds(veh_type, pj_int_name, pj_colour) # runs multiple times, which is okay
        make_shared_colour_tobj(veh_type, pj_int_name, pj_colour)

        if veh_separate_paintjobs: # most trucks
            for cab in veh_cabins:
                cab_size = cab
                cab_name = veh_cabins[cab]
                make_cabin_sii(veh_path, pj_int_name, cab_size, cab_name, veh_make, veh_model)
                make_cabin_tobj(pj_int_name, veh_make, veh_model, cab_size)
                if veh_uses_accessories:
                    make_cabin_acc_sii(veh_path, pj_int_name, cab_size, veh_make, veh_model, veh_acc_dict)
        else: # trailers and some mods
            make_only_sii(veh_trailer, veh_path, pj_int_name, pj_colour, veh_make, veh_model)
            if not veh_trailer:
                make_cabin_tobj(pj_int_name, veh_make, veh_model)
            if veh_uses_accessories:
                make_only_acc_sii(veh_type, veh_path, pj_int_name, veh_make, veh_model, veh_acc_dict)

        if not veh_trailer:
            copy_cabin_dds(pj_int_name, veh_make, veh_model)
        if veh_uses_accessories:
            make_acc_tobj(veh_type, pj_int_name, veh_make, veh_model, veh_acc_dict, pj_colour)
