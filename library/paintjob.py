import os, shutil, binascii, codecs

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
