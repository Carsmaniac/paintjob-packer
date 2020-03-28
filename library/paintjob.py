import os, shutil, binascii, codecs, configparser

class Vehicle:
    def __init__(self, file_name, game):
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("library/vehicles/{}/{}".format(game, file_name))
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
                if acc != "":
                    self.acc_dict[acc] = list(veh_ini[acc].keys())
        if self.trailer:
            self.separate_paintjobs = False
            self.type = "trailer_owned"
        else:
            self.separate_paintjobs = veh_ini["cabins"].getboolean("separate paintjobs")
            self.type = "truck"
            self.cabins = dict(veh_ini["cabins"].items())
            self.cabins.pop("separate paintjobs", None)



def make_folder(output_path, path):
    if not os.path.exists(output_path + "/" + path):
        os.makedirs(output_path + "/" + path)

def convert_string_to_hex(string_input):
    if isinstance(string_input, int):
        string_input = bytes([string_input])
    elif isinstance(string_input, str):
        string_input = string_input.encode()
    string_output = binascii.hexlify(string_input)
    string_output = string_output.decode()
    return string_output

def generate_tobj(path): # TODO: icon tobj?
    tobj_string = "010AB170000000000000000000000000000000000100020002000303030002020001000000010000"
    tobj_string += convert_string_to_hex(len(path))
    tobj_string += "00000000000000"
    tobj_string += convert_string_to_hex(path)
    tobj_file = codecs.decode(tobj_string, "hex_codec")
    return tobj_file



# loose files

def make_manifest_sii(output_path, mod_version, mod_name, mod_author):
    file = open(output_path + "/manifest.sii", "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("mod_package: .package_name\n")
    file.write("{\n")
    file.write("    package_version:  \"{}\"\n".format(mod_version))
    file.write("    display_name:     \"{}\"\n".format(mod_name))
    file.write("    author:           \"{}\"\n".format(mod_author))
    file.write("\n")
    file.write("    category[]:       \"paint_job\"\n")
    file.write("\n")
    file.write("    icon:             \"mod_manager_image.jpg\"\n")
    file.write("    description_file: \"mod_manager_description.txt\"\n")
    file.write("}\n")
    file.write("}\n")
    file.close()

def copy_mod_manager_image(output_path):
    shutil.copyfile("library/placeholder files/mod_manager_image.jpg", output_path + "/mod_manager_image.jpg")

def make_description(output_path, truck_list, trailer_list, mod_list):
    file = open(output_path + "/mod_manager_description.txt", "w")
    if len(truck_list) + len(mod_list) > 0:
        file.write("Trucks supported:\n")
        for veh in truck_list:
            file.write(veh.name+"\n")
        for veh in mod_list:
            file.write("{}'s {}\n".format(veh.mod_author, veh.name))
        file.write("\n")
    if len(trailer_list) > 0:
        file.write("Trailers supported:\n")
        for veh in trailer_list:
            file.write(veh.name+"\n")
    file.close()



# material folder

def make_material_folder(output_path):
    make_folder(output_path, "material/ui/accessory/")

def copy_paintjob_icon(output_path, internal_name):
    shutil.copyfile("library/placeholder files/paintjob_icon.dds", output_path + "/material/ui/accessory/{}_icon.dds".format(internal_name))

def make_paintjob_icon_tobj(output_path, internal_name): # TODO: tobj like SCS paintjobs, makes a difference?
    file = open(output_path + "/material/ui/accessory/{}_icon.tobj".format(internal_name), "wb")
    file.write(generate_tobj("/material/ui/accessory/{}_icon.dds".format(internal_name)))
    file.close()

def make_paintjob_icon_mat(output_path, internal_name):
    file = open(output_path + "/material/ui/accessory/{}_icon.mat".format(internal_name), "w")
    file.write("material: \"ui\"\n")
    file.write("{\n")
    file.write("    texture:      \"{}_icon.tobj\"\n".format(internal_name))
    file.write("    texture_name: \"texture\"\n")
    file.write("}\n")
    file.close()



# def folder

def make_def_folder(output_path, veh):
    extra_path = ""
    if veh.uses_accessories:
        extra_path = "/accessory"
    make_folder(output_path, "def/vehicle/{}/{}/paint_job{}".format(veh.type, veh.path, extra_path))

def make_def_sii(output_path, veh, paintjob_name, internal_name, cab_name = None, cab_size = None):
    file = open(output_path + "/def/vehicle/{}/{}/paint_job/{}.sii".format(veh.type, veh.path, paintjob_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: {}.{}.paint_job\n".format(paintjob_name, veh.path))
    file.write("{\n")
    file.write("@include \"{}_settings.sui\"\n".format(internal_name))
    if veh.type == "trailer_owned":
        file.write("    paint_job_mask: \"/vehicle/trailer_owned/upgrade/paintjob/{}/{}_{}/base_colour.tobj\"\n".format(internal_name, veh.make, veh.model))
    elif internal_name != paintjob_name: # cabin handling: separate paintjobs
        file.write("    suitable_for[]: \"{}.{}.cabin\"\n".format(cab_name, veh.path))
        file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin_{}.tobj\"\n".format(internal_name, veh.make, veh.model, cab_size))
    elif veh.type == "truck": # cabin handling: combined paintjobs
        file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin.tobj\"\n".format(internal_name, veh.make, veh.model))
    file.close()

def make_settings_sui(output_path, veh, internal_name, ingame_name, ingame_price, unlock_level):
    file = open(output_path + "/def/vehicle/{}/{}/paint_job/{}_settings.sui".format(veh.type, veh.path, internal_name), "w")
    file.write("    name:     \"{}\"\n".format(ingame_name))
    file.write("    price:    {}\n".format(ingame_price))
    file.write("    unlock:   {}\n".format(unlock_level))
    file.write("    airbrush: true\n")
    file.write("    icon:     \"{}_icon\"\n".format(internal_name))
    if veh.alt_uvset:
        file.write("    alternate_uvset: true\n")
    file.close()

def make_accessory_sii(output_path, veh, internal_name, paintjob_name):
    file = open(output_path + "/def/vehicle/{}/{}/paint_job/accessory/{}.sii".format(veh.type, veh.path, paintjob_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for acc_name in veh.acc_dict:
        file.write("\n")
        file.write("simple_paint_job_data: .ovr{}\n".format(ovr_counter))
        file.write("{\n")
        file.write("    paint_job_mask: \"/vehicle/{}/upgrade/paintjob/{}/{}_{}/{}.tobj\"\n".format(veh.type, internal_name, veh.make, veh.model, acc_name))
        for acc in veh.acc_dict[acc_name]:
            file.write("    acc_list[]: \"{}\"\n".format(acc))
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()



# vehicle folder

def make_vehicle_folder(output_path, veh, internal_name):
    make_folder(output_path, "vehicle/{}/upgrade/paintjob/{}/{}_{}".format(veh.type, internal_name, veh.make, veh.model))

def copy_main_dds(output_path, veh, internal_name, paintjob_name, using_unifier):
    if veh.type == "trailer_owned":
        shutil.copyfile("library/placeholder files/empty.dds", output_path + "/vehicle/trailer_owned/upgrade/paintjob/{}/{}_{}/base_colour.dds".format(internal_name, veh.make, veh.model))
    elif internal_name != paintjob_name:
        if using_unifier:
            shutil.copyfile("library/placeholder files/empty.dds", output_path + "/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin_a.dds".format(internal_name, veh.make, veh.model))
        else:
            for cab_size in veh.cabins:
                shutil.copyfile("library/placeholder files/empty.dds", output_path + "/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin_{}.dds".format(internal_name, veh.make, veh.model, cab_size))
    elif veh.type == "truck":
        shutil.copyfile("library/placeholder files/empty.dds", output_path + "/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin.dds".format(internal_name, veh.make, veh.model))

def copy_accessory_dds(output_path, veh, internal_name):
    for acc_name in veh.acc_dict:
        shutil.copyfile("library/placeholder files/empty.dds", output_path + "/vehicle/{}/upgrade/paintjob/{}/{}_{}/{}.dds".format(veh.type, internal_name, veh.make, veh.model, acc_name))

def make_main_tobj(output_path, veh, internal_name, paintjob_name, using_unifier):
    if veh.type == "trailer_owned":
        file = open(output_path + "/vehicle/trailer_owned/upgrade/paintjob/{}/{}_{}/base_colour.tobj".format(internal_name, veh.make, veh.model), "wb")
        file.write(generate_tobj("/vehicle/trailer_owned/upgrade/paintjob/{}/{}_{}/base_colour.dds".format(internal_name, veh.make, veh.model)))
        file.close()
    elif internal_name != paintjob_name:
        for cab_size in veh.cabins:
            file = open(output_path + "/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin_{}.tobj".format(internal_name, veh.make, veh.model, cab_size), "wb")
            if using_unifier:
                file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin_a.dds".format(internal_name, veh.make, veh.model, cab_size)))
            else:
                file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin_{}.dds".format(internal_name, veh.make, veh.model, cab_size)))
            file.close()
    elif veh.type == "truck":
        file = open(output_path + "/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin.tobj".format(internal_name, veh.make, veh.model), "wb")
        file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/{}/{}_{}/cabin.dds".format(internal_name, veh.make, veh.model)))
        file.close()

def make_accessory_tobj(output_path, veh, internal_name):
    for acc_name in veh.acc_dict:
        file = open(output_path + "/vehicle/{}/upgrade/paintjob/{}/{}_{}/{}.tobj".format(veh.type, internal_name, veh.make, veh.model, acc_name), "wb")
        file.write(generate_tobj("/vehicle/{}/upgrade/paintjob/{}/{}_{}/{}.dds".format(veh.type, internal_name, veh.make, veh.model, acc_name)))
        file.close()



# packer functions

def make_unifier_ini(output_path, internal_name, vehicle_list, unifier_name):
    vehicles_to_add = []
    for veh in vehicle_list:
        if veh.type == "truck" and veh.separate_paintjobs:
            vehicles_to_add.append(veh)

    uni_ini = configparser.ConfigParser()
    uni_ini.add_section("paintjob")
    uni_ini["paintjob"]["internal name"] = internal_name

    for veh in vehicles_to_add:
        veh_name = "{}_{}".format(veh.make, veh.model)
        uni_ini.add_section(veh_name)
        uni_ini[veh_name]["path"] = veh.path
        uni_ini[veh_name]["accessories"] = str(veh.uses_accessories)
        uni_ini[veh_name]["cabins"] = ",".join(veh.cabins)
        for cabin in veh.cabins:
            uni_ini[veh_name][cabin] = veh.cabins[cabin]

    with open(output_path + "/unifier.ini", "w") as config_file:
        uni_ini.write(config_file)

    shutil.copyfile("library/placeholder files/" + unifier_name, output_path + "/" + unifier_name)
