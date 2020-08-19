import os, shutil, binascii, codecs, configparser

class Vehicle:
    def __init__(self, file_name, game):
        veh_ini = configparser.ConfigParser(allow_no_value = True)
        veh_ini.read("library/vehicles/{}/{}".format(game, file_name))
        self.path = veh_ini["vehicle info"]["vehicle path"]
        self.alt_uvset = veh_ini["vehicle info"].getboolean("alt uvset")
        self.name = veh_ini["vehicle info"]["name"]
        self.trailer = veh_ini["vehicle info"].getboolean("trailer")
        self.mod = veh_ini["vehicle info"].getboolean("mod")
        self.mod_author = veh_ini["vehicle info"]["mod author"]
        self.mod_link = veh_ini["vehicle info"]["mod link"]
        self.uses_accessories = veh_ini["vehicle info"].getboolean("uses accessories")
        if self.uses_accessories:
            self.accessories = veh_ini["vehicle info"]["accessories"].split(";")
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
            for cabin in self.cabins:
                self.cabins[cabin] = self.cabins[cabin].split(";")



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
    file.write("\tpackage_version: \"{}\"\n".format(mod_version))
    file.write("\tdisplay_name: \"{}\"\n".format(mod_name))
    file.write("\tauthor: \"{}\"\n".format(mod_author))
    file.write("\n")
    file.write("\tcategory[]: \"paint_job\"\n")
    file.write("\n")
    file.write("\ticon: \"Image.jpg\"\n")
    file.write("\tdescription_file: \"Description.txt\"\n")
    file.write("}\n")
    file.write("}\n")
    file.close()

def copy_mod_manager_image(output_path):
    shutil.copyfile("library/placeholder files/mod_manager_image.jpg", output_path + "/Image.jpg")

def make_description(output_path, truck_list, truck_mod_list, trailer_list, trailer_mod_list, num_of_paintjobs):
    file = open(output_path + "/Description.txt", "w")
    if num_of_paintjobs == "single":
        for veh in truck_list + trailer_list:
            file.write("This paintjob supports the {}\n".format(veh.name))
        for veh in truck_mod_list + trailer_mod_list:
            file.write("This paintjob supports {}'s {}\n".format(veh.mod_author, veh.name))
    else:
        if len(truck_list) + len(truck_mod_list) > 0:
            file.write("Trucks supported:\n")
            for veh in truck_list:
                file.write(veh.name+"\n")
            for veh in truck_mod_list:
                file.write("{}'s {}\n".format(veh.mod_author, veh.name))
            file.write("\n")
        if len(trailer_list) + len(trailer_mod_list) > 0:
            file.write("Trailers supported:\n")
            for veh in trailer_list:
                file.write(veh.name+"\n")
            for veh in trailer_mod_list:
                file.write("{}'s {}\n".format(veh.mod_author, veh.name))
    file.close()

def copy_versions_sii(output_path):
    shutil.copyfile("library/placeholder files/versions.sii", output_path + "/versions.sii")

def copy_workshop_image(output_path):
    shutil.copyfile("library/placeholder files/Workshop image.jpg", output_path + "/Workshop image.jpg")



# material folder

def make_material_folder(output_path):
    make_folder(output_path, "material/ui/accessory/")

def copy_paintjob_icon(output_path, ingame_name):
    shutil.copyfile("library/placeholder files/paintjob_icon.dds", output_path + "/material/ui/accessory/{} Icon.dds".format(ingame_name))

def make_paintjob_icon_tobj(output_path, ingame_name): # TODO: tobj like SCS paintjobs, makes a difference?
    file = open(output_path + "/material/ui/accessory/{} Icon.tobj".format(ingame_name), "wb")
    file.write(generate_tobj("/material/ui/accessory/{} Icon.dds".format(ingame_name)))
    file.close()

def make_paintjob_icon_mat(output_path, internal_name, ingame_name):
    file = open(output_path + "/material/ui/accessory/{}_icon.mat".format(internal_name), "w")
    file.write("material: \"ui\"\n")
    file.write("{\n")
    file.write("\ttexture: \"{} Icon.tobj\"\n".format(ingame_name))
    file.write("\ttexture_name: \"texture\"\n")
    file.write("}\n")
    file.close()



# def folder

def make_def_folder(output_path, veh):
    extra_path = ""
    if veh.uses_accessories:
        extra_path = "/accessory"
    make_folder(output_path, "def/vehicle/{}/{}/paint_job{}".format(veh.type, veh.path, extra_path))

def make_def_sii(output_path, veh, paintjob_name, internal_name, ingame_name, cab_internal_name = None, cab_ingame_name = None, cab_size = None, largest_only = False):
    file = open(output_path + "/def/vehicle/{}/{}/paint_job/{}.sii".format(veh.type, veh.path, paintjob_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: {}.{}.paint_job\n".format(paintjob_name, veh.path))
    file.write("{\n")
    file.write("@include \"{}_settings.sui\"\n".format(internal_name))
    if veh.type == "trailer_owned":
        file.write("\tpaint_job_mask: \"/vehicle/trailer_owned/upgrade/paintjob/{}/{}/Base Colour.tobj\"\n".format(ingame_name, veh.name))
    elif largest_only:
        file.write("\tsuitable_for[]: \"{}.{}.cabin\"\n".format(cab_internal_name, veh.path))
        file.write("\tpaint_job_mask: \"/vehicle/truck/upgrade/paintjob/{}/{}/Cabin.tobj\"\n".format(ingame_name, veh.name))
    elif internal_name != paintjob_name: # cabin handling: separate paintjobs
        file.write("\tsuitable_for[]: \"{}.{}.cabin\"\n".format(cab_internal_name, veh.path))
        file.write("\tpaint_job_mask: \"/vehicle/truck/upgrade/paintjob/{}/{}/{}.tobj\"\n".format(ingame_name, veh.name, cab_ingame_name))
    elif veh.type == "truck": # cabin handling: combined paintjobs
        file.write("\tpaint_job_mask: \"/vehicle/truck/upgrade/paintjob/{}/{}/Cabin.tobj\"\n".format(ingame_name, veh.name))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_settings_sui(output_path, veh, internal_name, ingame_name, ingame_price, unlock_level):
    file = open(output_path + "/def/vehicle/{}/{}/paint_job/{}_settings.sui".format(veh.type, veh.path, internal_name), "w")
    file.write("\tname: \"{}\"\n".format(ingame_name))
    file.write("\tprice: {}\n".format(ingame_price))
    file.write("\tunlock: {}\n".format(unlock_level))
    file.write("\tairbrush: true\n")
    file.write("\ticon: \"{}_icon\"\n".format(internal_name))
    if veh.alt_uvset:
        file.write("\talternate_uvset: true\n")
    file.close()

def make_accessory_sii(output_path, veh, ingame_name, paintjob_name):
    file = open(output_path + "/def/vehicle/{}/{}/paint_job/accessory/{}.sii".format(veh.type, veh.path, paintjob_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for acc_name in veh.acc_dict:
        file.write("\n")
        file.write("simple_paint_job_data: .ovr{}\n".format(ovr_counter))
        file.write("{\n")
        file.write("\tpaint_job_mask: \"/vehicle/{}/upgrade/paintjob/{}/{}/{}.tobj\"\n".format(veh.type, ingame_name, veh.name, acc_name))
        for acc in veh.acc_dict[acc_name]:
            file.write("\tacc_list[]: \"{}\"\n".format(acc))
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()



# vehicle folder

def make_vehicle_folder(output_path, veh, ingame_name):
    make_folder(output_path, "vehicle/{}/upgrade/paintjob/{}/{}".format(veh.type, ingame_name, veh.name))

def copy_main_dds(output_path, veh, internal_name, ingame_name, paintjob_name, game):
    if veh.type == "trailer_owned":
        shutil.copyfile("library/placeholder files/empty.dds", output_path + "/vehicle/trailer_owned/upgrade/paintjob/{}/{}/Base Colour.dds".format(ingame_name, veh.name))
    elif internal_name != paintjob_name:
        for cab_size in veh.cabins:
            shutil.copyfile("library/placeholder files/{} templates/{}/{}.dds".format(game, veh.path, veh.cabins[cab_size][0]), output_path + "/vehicle/truck/upgrade/paintjob/{}/{}/{}.dds".format(ingame_name, veh.name, veh.cabins[cab_size][0]))
    elif veh.type == "truck":
        shutil.copyfile("library/placeholder files/{} templates/{}/{}.dds".format(game, veh.path, veh.cabins["a"][0]), output_path + "/vehicle/truck/upgrade/paintjob/{}/{}/Cabin.dds".format(ingame_name, veh.name))

def copy_accessory_dds(output_path, veh, ingame_name, game):
    for acc_name in veh.acc_dict:
        shutil.copyfile("library/placeholder files/{} templates/{}/{}.dds".format(game, veh.path, acc_name), output_path + "/vehicle/{}/upgrade/paintjob/{}/{}/{}.dds".format(veh.type, ingame_name, veh.name, acc_name))

def make_main_tobj(output_path, veh, internal_name, ingame_name, paintjob_name):
    if veh.type == "trailer_owned":
        file = open(output_path + "/vehicle/trailer_owned/upgrade/paintjob/{}/{}/Base Colour.tobj".format(ingame_name, veh.name), "wb")
        file.write(generate_tobj("/vehicle/trailer_owned/upgrade/paintjob/{}/{}/Base Colour.dds".format(ingame_name, veh.name)))
        file.close()
    elif internal_name != paintjob_name:
        for cab_size in veh.cabins:
            file = open(output_path + "/vehicle/truck/upgrade/paintjob/{}/{}/{}.tobj".format(ingame_name, veh.name, veh.cabins[cab_size][0]), "wb")
            file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/{}/{}/{}.dds".format(ingame_name, veh.name, veh.cabins[cab_size][0])))
            file.close()
    elif veh.type == "truck":
        file = open(output_path + "/vehicle/truck/upgrade/paintjob/{}/{}/Cabin.tobj".format(ingame_name, veh.name), "wb")
        file.write(generate_tobj("/vehicle/truck/upgrade/paintjob/{}/{}/Cabin.dds".format(ingame_name, veh.name)))
        file.close()

def make_accessory_tobj(output_path, veh, ingame_name):
    for acc_name in veh.acc_dict:
        file = open(output_path + "/vehicle/{}/upgrade/paintjob/{}/{}/{}.tobj".format(veh.type, ingame_name, veh.name, acc_name), "wb")
        file.write(generate_tobj("/vehicle/{}/upgrade/paintjob/{}/{}/{}.dds".format(veh.type, ingame_name, veh.name, acc_name)))
        file.close()
