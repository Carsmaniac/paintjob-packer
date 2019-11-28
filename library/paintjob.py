import os, shutil, binascii, codecs

EMPTY_DDS = "library/placeholder files/empty.dds"

class Vehicle:
    def example_variables():
        make = "scania"
        model = "r"
        vehicle_path = "scania.r"
        alt_uvset = False
        name = "Scania R 2009"
        trailer = False
        mod = False
        mod_author = ""
        mod_link = ""
        accessories = True
        cabins = {"a":"topline","b":"highline","c":"normal","8":"tl_8x4"}
        acc_dict = {"rear_bumper":["r_bumper.arbumpermg01","r_bumper.arbumpermg03"],
                    "chassis_cover":["r_chs_cover.chscmg4x203","r_chs_cover.chscmg6x203","r_chs_cover.chscmg6x2403"]}

class Pack:
    def example_variables():
        name = "XPO Logistics Paintjob Pack"
        version = "v1.0"
        game = "ets"
        paintjobs = ["xpo","xpow","waxpo","waxpow"]
        main_paintjob = "xpo"
        related_mods = {"norbert":"A French logistics company that...","globex":"A totally unrelated mod"}
        link = "http://etcetc"
        suggested_by = ["bobman302","that guy"]
        description = "XPO Logistics is an American company....."
        more_info = "XPO uses many paintjobs...."

def clear_output_folder():
    print("Clearing output folder")
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output")

def make_folder(path):
    if not os.path.exists("output/" + path):
        os.makedirs("output/" + path)

def convert_string_to_hex(string_input):
    if isinstance(string_input, int):
        string_input = bytes([string_input])
    elif isinstance(string_input, str):
        string_input = string_input.encode()
    string_output = binascii.hexlify(string_input)
    string_output = string_output.decode()
    return string_output

def generate_tobj(path):
    tobj_string = "010AB170000000000000000000000000000000000100020002000303030002020001000000010000"
    tobj_string += convert_string_to_hex(len(path))
    tobj_string += "00000000000000"
    tobj_string += convert_string_to_hex(path)
    tobj_file = codecs.decode(tobj_string, "hex_codec")
    return tobj_file

def make_manifest_sii(mod_version, mod_name):
    file = open("output/manifest.sii", "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("mod_package: .package_name\n")
    file.write("{\n")
    file.write("    package_version:  \"%s\"\n" % mod_version)
    file.write("    display_name:     \"%s\"\n" % mod_name)
    file.write("    author:           \"Carsmaniac\"\n")
    file.write("\n")
    file.write("    category[]:       \"paint_job\"\n")
    file.write("\n")
    file.write("    icon:             \"mod_manager_image.jpg\"\n")
    file.write("    description_file: \"mod_manager_description.txt\"\n")
    file.write("}\n")
    file.write("}\n")
    file.close()

def copy_mod_manager_image():
    shutil.copyfile("library/placeholder files/mod_manager_image.jpg", "output/mod_manager_image.jpg")

def make_material_folder():
    make_folder("material/ui/accessory/paintjob_icons")

def copy_paintjob_icon(pj_int_name):
    shutil.copyfile("library/placeholder files/paintjob_icon.dds", "output/material/ui/accessory/paintjob_icons/%s_icon.dds" % pj_int_name)

def make_paintjob_icon_tobj(pj_int_name):
    file = open("output/material/ui/accessory/paintjob_icons/%s_icon.tobj" % pj_int_name, "wb")
    file.write(generate_tobj("/material/ui/acessory/paintjob_icons/%s_icon.dds" % pj_int_name))
    file.close()

def make_paintjob_icon_mat(pj_int_name):
    file = open("output/material/ui/accessory/paintjob_icons/%s_icon.mat" % pj_int_name, "w")
    file.write("material: \"ui\"\n")
    file.write("{\n")
    file.write("    texture:      \"%s_icon.tobj\"\n" % pj_int_name)
    file.write("    texture_name: \"texture\"\n")
    file.write("}\n")
    file.close()

def make_def_folder(veh_type, veh_path, veh_uses_accessories):
    extra_path = ""
    if veh_uses_accessories:
        extra_path = "/accessory"
    make_folder("def/vehicle/%s/%s/paint_job%s" % (veh_type, veh_path, extra_path))

def make_cabin_sii(veh_path, pj_int_name, cab_size, cab_name, veh_make, veh_model):
    cab_pj_name = pj_int_name+"_"+cab_size
    file = open("output/def/vehicle/truck/%s/paint_job/%s.sii" % (veh_path, cab_pj_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: %s.%s.paint_job\n" % (cab_pj_name, veh_path))
    file.write("{\n")
    file.write("@include \"%s_settings.sui\"\n" % pj_int_name)
    file.write("    suitable_for[]: \"%s.%s.cabin\"\n" % (cab_name, veh_path))
    file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_%s.tobj\"\n" % (pj_int_name, veh_make, veh_model, cab_size))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_only_sii(veh_type, veh_path, pj_int_name, pj_colour, veh_make, veh_model):
    if veh_type == "trailer_owned":
        tobj_path = "shared_%s.tobj" % pj_colour
    else:
        tobj_path = "%s_%s/cabin_a.tobj" % (veh_make, veh_model)
    file = open("output/def/vehicle/%s/%s/paint_job/%s.sii" % (veh_type, veh_path, pj_int_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: %s.%s.paint_job\n" % (pj_int_name, veh_path))
    file.write("{\n")
    file.write("@include \"%s_settings.sui\"\n" % pj_int_name)
    file.write("    paint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s\n" % (veh_type, pj_int_name, tobj_path))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_settings_sui(veh_type, veh_path, pj_int_name, pj_name, pj_price):
    file = open("output/def/vehicle/%s/%s/paint_job/%s_settings.sui" % (veh_type, veh_path, pj_int_name), "w")
    file.write("    name:     \"%s\"\n" % pj_name)
    file.write("    price:    %s\n" % pj_price)
    file.write("    unlock:   0\n")
    file.write("    airbrush: true\n")
    file.write("    icon:     \"paintjob_icons/%s_icon\"\n" % pj_int_name)
    file.close()

def make_cabin_acc_sii(veh_path, pj_int_name, cab_size, veh_make, veh_model, veh_acc_dict):
    cab_pj_name = pj_int_name+"_"+cab_size
    file = open("output/def/vehicle/truck/%s/paint_job/accessory/%s.sii" % (veh_path, cab_pj_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for acc_name in veh_acc_dict:
        file.write("\n")
        file.write("simple_paint_job_data: .ovr%s\n" % str(ovr_counter))
        file.write("{\n")
        file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/%s/%s_%s/%s.tobj\"\n" % (pj_int_name, veh_make, veh_model, acc_name))
        for acc in veh_acc_dict[acc_name]:
            file.write("    acc_list[]: \"%s\"\n" % acc)
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()

def make_only_acc_sii(veh_type, veh_path, pj_int_name, veh_make, veh_model, veh_acc_dict):
    file = open("output/def/vehicle/%s/%s/paint_job/accessory/%s.sii" % (veh_type, veh_path, pj_int_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for acc_name in veh_acc_dict:
        file.write("\n")
        file.write("simple_paint_job_data: .ovr%s\n" % str(ovr_counter))
        file.write("{\n")
        file.write("    paint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.tobj\"\n" % (veh_type, pj_int_name, veh_make, veh_model, acc_name))
        for acc in veh_acc_dict[acc_name]:
            file.write("    acc_list[]: \"%s\"\n" % acc)
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()

def make_vehicle_folder(veh_type, pj_int_name, veh_make, veh_model):
    make_folder("vehicle/%s/upgrade/paintjob/%s/%s_%s" % (veh_type, pj_int_name, veh_make, veh_model))

def copy_cabin_dds(pj_int_name, veh_make, veh_model):
    shutil.copyfile(EMPTY_DDS, "output/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_a.dds" % (pj_int_name, veh_make, veh_model))

def copy_shared_colour_dds(veh_type, pj_int_name, pj_colour):
    shutil.copyfile(EMPTY_DDS, "output/vehicle/%s/upgrade/paintjob/%s/shared_%s.dds" % (veh_type, pj_int_name, pj_colour))

def make_cabin_tobj(pj_int_name, veh_make, veh_model, cab_size="a"):
    file = open("output/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_%s.tobj" % (pj_int_name, veh_make, veh_model, cab_size), "wb")
    file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_a.dds" % (pj_int_name, veh_make, veh_model)))
    file.close()

def make_acc_tobj(veh_type, pj_int_name, veh_make, veh_model, veh_acc_dict, pj_colour):
    for acc_name in veh_acc_dict:
        file = open("output/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.tobj" % (veh_type, pj_int_name, veh_make, veh_model, acc_name), "wb")
        file.write(generate_tobj("/vehicle/%s/upgrade/paintjob/%s/shared_%s.dds" % (veh_type, pj_int_name, pj_colour)))
        file.close()

def make_shared_colour_tobj(veh_type, pj_int_name, pj_colour):
    file = open("output/vehicle/%s/upgrade/paintjob/%s/shared_%s.tobj" % (veh_type, pj_int_name, pj_colour), "wb")
    file.write(generate_tobj("/vehicle/%s/upgrade/paintjob/%s/shared_%s.dds" % (veh_type, pj_int_name, pj_colour)))
    file.close()
