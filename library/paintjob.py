import os, shutil, binascii, codecs

EMPTY_DDS = "library/placeholder files/empty.dds"

class Pack:
    def __init__(self, file_name, _game = None):
        pack_ini = configparser.ConfigParser(allow_no_value = True)
        if file_name == "new":
            pack_ini.read("new pack.ini")
        else:
            pack_ini.read("library/packs/%s/%s.ini" % (_game, file_name))
        self.game = pack_ini["pack info"]["game"]
        self.name = pack_ini["pack info"]["name"]
        self.version = input_file["pack info"]["version"]
        self.list_of_paintjobs = pack_ini["pack info"]["paintjobs"].split(",")
        self.paintjobs = []
        for pj in self.list_of_paintjobs:
            self.paintjobs.append(Paintjob(pack_ini, pj, self.game))
        self.main_paintjob = pack_ini["pack info"]["main paintjob"]
        self.list_of_related_packs = pack_ini["pack info"]["related packs"].split(",")
        self.related_packs = []
        for rel in self.list_of_related_packs:
            self.related_packs.append(RelatedPack(pack_ini, rel))
        self.link = pack_ini["pack info"]["link"]
        self.brief_desc = pack_ini["pack info"]["description"]
        self.more_info = pack_ini["pack info"]["more info"]

class Paintjob:
    def __init__(self, pack_ini, ini_sec, _game):
        self.int_name = "cm_" + ini_sec
        self.name = pack_ini[ini_sec]["name"]
        self.price = pack_ini[ini_sec]["price"]
        self.colour = pack_ini[ini_sec]["main colour"]
        self.game = _game
        self.list_of_vehicles = []
        for veh in list(pack_ini[ini_sec].keys()):
            if veh not in ("name", "price", "main colour"):
                self.list_of_vehicles.append(veh)
        self.vehicles = []
        for veh in self.list_of_vehicles:
            self.vehicles.append(Vehicle(veh, self.game))

class Vehicle:
    def __init__(self, file_name, game):
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("library/vehicles/%s/%s.ini" % (game, file_name))
        self.make = veh_ini["vehicle info"]["make"]
        self.model = veh_ini["vehicle info"]["model"]
        self.path = veh_ini["vehicle info"]["vehicle path"]
        self.alt_uvset = veh_ini["vehicle info"].getboolean("alt uvset")
        self.name = veh_ini["vehicle info"]["name"]
        self.trailer = veh_ini["vehicle info"].getboolean("trailer")
        self.mod = veh_ini["vehicle info"].getboolean("mod")
        self.mod_author = veh_ini["vehicle info"]["mod author"]
        self.mod_link = veh_ini["vehicle info"]["mod link"]
        self.uses_accessories = veh_ini["vehicle info"].getboolean("uses accessories")
        if self.uses_accessories:
            self.accessories = veh_ini["vehicle info"]["accessories"].split(",")
            self.acc_dict = {}
            for acc in self.accessories:
                self.acc_dict[acc] = list(veh_ini[acc].keys())
        if self.trailer:
            self.separate_paintjobs = False
            self.type = "trailer_owned"
        else:
            self.separate_paintjobs = veh_ini["cabins"].getboolean("separate paintjobs")
            self.type = "truck"
            self.cabins = dict(veh_ini["cabins"].items())
            self.cabins.pop("separate paintjobs", None)

class RelatedPack:
    def __init__(self, pack_ini, ini_sec):
        self.game = pack_ini["pack info"]["game"]
        self.description = pack_ini[ini_sec]["description"]
        rel_ini = configparser.ConfigParser(allow_no_value = True)
        rel_ini.read("library/packs/%s/%s.ini" % (self.game, ini_sec))
        self.name = rel_ini["pack info"]["name"]
        self.link = rel_ini["pack info"]["link"]

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



def make_manifest_sii(pack):
    file = open("output/manifest.sii", "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("mod_package: .package_name\n")
    file.write("{\n")
    file.write("    package_version:  \"%s\"\n" % pack.version)
    file.write("    display_name:     \"%s\"\n" % pack.name)
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

def copy_paintjob_icon(pj):
    shutil.copyfile("library/placeholder files/paintjob_icon.dds", "output/material/ui/accessory/paintjob_icons/%s_icon.dds" % pj.int_name)

def make_paintjob_icon_tobj(pj):
    file = open("output/material/ui/accessory/paintjob_icons/%s_icon.tobj" % pj.int_name, "wb")
    file.write(generate_tobj("/material/ui/acessory/paintjob_icons/%s_icon.dds" % pj.int_name))
    file.close()

def make_paintjob_icon_mat(pj):
    file = open("output/material/ui/accessory/paintjob_icons/%s_icon.mat" % pj.int_name, "w")
    file.write("material: \"ui\"\n")
    file.write("{\n")
    file.write("    texture:      \"%s_icon.tobj\"\n" % pj.int_name)
    file.write("    texture_name: \"texture\"\n")
    file.write("}\n")
    file.close()

def make_def_folder(veh):
    extra_path = ""
    if veh.uses_accessories:
        extra_path = "/accessory"
    make_folder("def/vehicle/%s/%s/paint_job%s" % (veh.type, veh.path, extra_path))

def make_cabin_sii(veh, pj, cab_size, cab_name):
    cab_pj_name = pj.int_name+"_"+cab_size
    file = open("output/def/vehicle/truck/%s/paint_job/%s.sii" % (veh.path, cab_pj_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: %s.%s.paint_job\n" % (cab_pj_name, veh.path))
    file.write("{\n")
    file.write("@include \"%s_settings.sui\"\n" % pj.int_name)
    file.write("    suitable_for[]: \"%s.%s.cabin\"\n" % (cab_name, veh.path))
    file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_%s.tobj\"\n" % (pj.int_name, veh.make, veh.model, cab_size))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_only_sii(veh, pj):
    if veh.type == "trailer_owned":
        tobj_path = "shared_%s.tobj" % pj.colour
    else:
        tobj_path = "%s_%s/cabin_a.tobj" % (veh.make, veh.model)
    file = open("output/def/vehicle/%s/%s/paint_job/%s.sii" % (veh.type, veh.path, pj.int_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: %s.%s.paint_job\n" % (pj.int_name, veh.path))
    file.write("{\n")
    file.write("@include \"%s_settings.sui\"\n" % pj.int_name)
    file.write("    paint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s\n" % (veh.type, pj.int_name, tobj_path))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_settings_sui(veh, pj):
    file = open("output/def/vehicle/%s/%s/paint_job/%s_settings.sui" % (veh.type, veh.path, pj.int_name), "w")
    file.write("    name:     \"%s\"\n" % pj.name)
    file.write("    price:    %s\n" % pj.price)
    file.write("    unlock:   0\n")
    file.write("    airbrush: true\n")
    file.write("    icon:     \"paintjob_icons/%s_icon\"\n" % pj.int_name)
    file.close()

def make_cabin_acc_sii(veh, pj, cab_size):
    cab_pj_name = pj.int_name+"_"+cab_size
    file = open("output/def/vehicle/truck/%s/paint_job/accessory/%s.sii" % (veh.path, cab_pj_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for acc_name in veh.acc_dict:
        file.write("\n")
        file.write("simple_paint_job_data: .ovr%s\n" % str(ovr_counter))
        file.write("{\n")
        file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/%s/%s_%s/%s.tobj\"\n" % (pj.int_name, veh.make, veh.model, acc_name))
        for acc in veh.acc_dict[acc_name]:
            file.write("    acc_list[]: \"%s\"\n" % acc)
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()

def make_only_acc_sii(veh, pj):
    file = open("output/def/vehicle/%s/%s/paint_job/accessory/%s.sii" % (veh.type, veh.path, pj.int_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for acc_name in veh.acc_dict:
        file.write("\n")
        file.write("simple_paint_job_data: .ovr%s\n" % str(ovr_counter))
        file.write("{\n")
        file.write("    paint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.tobj\"\n" % (veh.type, pj.int_name, veh.make, veh.model, acc_name))
        for acc in veh.acc_dict[acc_name]:
            file.write("    acc_list[]: \"%s\"\n" % acc)
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()

def make_vehicle_folder(veh, pj):
    make_folder("vehicle/%s/upgrade/paintjob/%s/%s_%s" % (veh.type, pj.int_name, veh.make, veh.model))

def copy_cabin_dds(pj, veh):
    shutil.copyfile(EMPTY_DDS, "output/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_a.dds" % (pj.int_name, veh.make, veh.model))

def copy_shared_colour_dds(veh, pj):
    shutil.copyfile(EMPTY_DDS, "output/vehicle/%s/upgrade/paintjob/%s/shared_%s.dds" % (veh.type, pj.int_name, pj.colour))

def make_cabin_tobj(pj, veh, cab_size = "a"):
    file = open("output/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_%s.tobj" % (pj.int_name, veh.make, veh.model, cab_size), "wb")
    file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_a.dds" % (pj.int_name, veh.make, veh.model)))
    file.close()

def make_acc_tobj(veh, pj):
    for acc_name in veh.acc_dict:
        file = open("output/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.tobj" % (veh.type, pj.int_name, veh.make, veh.model, acc_name), "wb")
        file.write(generate_tobj("/vehicle/%s/upgrade/paintjob/%s/shared_%s.dds" % (veh.type, pj.int_name, pj.colour)))
        file.close()

def make_shared_colour_tobj(veh, pj):
    file = open("output/vehicle/%s/upgrade/paintjob/%s/shared_%s.tobj" % (veh.type, pj.int_name, pj.colour), "wb")
    file.write(generate_tobj("/vehicle/%s/upgrade/paintjob/%s/shared_%s.dds" % (veh.type, pj.int_name, pj.colour)))
    file.close()
