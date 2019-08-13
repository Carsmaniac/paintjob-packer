import sys, shutil, os, binascii, codecs, time

class Vehicle:
    def example_variables():
        make = "scania"
        model = "streamline"
        name = "Scania Streamline"
        mod_author = None
        mod_link = None
        trailer = False
        cabins = {"a":"topline","b":"highline","c":"normal","8":"tl_8x4"}
        accessories = True
        acc_dict = {"shared_white":["r_bumper.grbumper","r_bumper.arbumper"]}

def add_to_vehicle_list(vehicle, index, chosen_cabins):
    existing_vehicles = []
    for each_veh in vehicle_list:
        existing_vehicles.append(each_veh.make+" "+each_veh.model)
    if vehicle not in existing_vehicles:
        vehicle_list.append(Vehicle())
        file = open("database/%s vehicles/%s.txt" % (supported_game, vehicle), "r")
        veh_info = file.read().splitlines()
        file.close()
        (vehicle_list[index].make, vehicle_list[index].model) = vehicle.split(" ")
        vehicle_list[index].name = veh_info[0]
        mod_author = veh_info[1].split(";")[1]
        mod_link = veh_info[2].split(";")[1]
        if mod_author == "":
            vehicle_list[index].mod_author = None
            vehicle_list[index].mod_link = None
        else:
            vehicle_list[index].mod_author = mod_author
            vehicle_list[index].mod_link = mod_link
        trailer = veh_info[3].split(":")[1]
        if trailer == "true":
            vehicle_list[index].trailer = True
            vehicle_list[index].cabins = {"":""}
        else:
            vehicle_list[index].trailer = False
            vehicle_list[index].cabins = dict(item.split(":") for item in veh_info[4].split(","))
            if len(chosen_cabins) > 0:
                trimmed_cabins = {}
                for cabin in vehicle_list[index].cabins.keys():
                    if cabin in chosen_cabins:
                        trimmed_cabins[cabin] = vehicle_list[index].cabins[cabin]
                vehicle_list[index].cabins = trimmed_cabins
        accessories = veh_info[5].split(":")[1]
        if accessories == "false":
            vehicle_list[index].accessories = False
        else:
            vehicle_list[index].accessories = True
            del veh_info[0:6]
            vehicle_list[index].acc_dict = {}
            for acc_group in veh_info:
                key_val_list = acc_group.split(":")
                vehicle_list[index].acc_dict[key_val_list[0]] = key_val_list[1].split(",")

def make_manifest_file(pack_name, pack_author, pack_version):
    file = open("output/manifest.sii", "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("mod_package: .package_name\n")
    file.write("{\n")
    file.write("    package_version:   \"%s\"\n" % pack_version)
    file.write("    display_name:      \"%s\"\n" % pack_name)
    file.write("    author:            \"%s\"\n" % pack_author)
    file.write("\n")
    file.write("    category[]:        \"paint_job\"\n")
    file.write("\n")
    file.write("    icon:              \"mod_manager_image.jpg\"\n")
    file.write("    description_file:  \"mod_manager_description.txt\"\n")
    file.write("}\n")
    file.write("}\n")
    file.close()

def copy_manager_image():
    shutil.copyfile("input/manager_image.jpg", "output/mod_manager_image.jpg")

def copy_manager_description():
    shutil.copyfile("input/manager_description.txt", "output/mod_manager_description.txt")

def make_folder(path):
    if not os.path.exists("output/" + path):
        os.makedirs("output/" + path)

def make_material_folders():
    make_folder("material/ui/accessory/paintjob_icons")

def copy_material_image(icon_name):
    shutil.copyfile("input/material_image.dds", "output/material/ui/accessory/paintjob_icons/%s.dds" % icon_name)

def make_material_mat(icon_name):
    file = open("output/material/ui/accessory/paintjob_icons/%s.mat" % icon_name, "w")
    file.write("material: \"ui\"\n")
    file.write("{\n")
    file.write("    texture:      \"%s.tobj\"\n" % icon_name)
    file.write("    texture_name: \"texture\"\n")
    file.write("}\n")
    file.close()

def convert_string_to_hex(string_input):
    if isinstance(string_input, int):
        string_input = bytes([string_input])
    elif isinstance(string_input, str):
        string_input = string_input.encode()
    string_output = binascii.hexlify(string_input)
    string_output = string_output.decode()
    return string_output

def generate_tobj_string(path):
    tobj_string = "010AB170000000000000000000000000000000000100020002000303030002020001000000010000"
    tobj_string += convert_string_to_hex(len(path))
    tobj_string += "00000000000000"
    tobj_string += convert_string_to_hex(path)
    tobj_file = codecs.decode(tobj_string, "hex_codec")
    return tobj_file

def make_material_tobj(icon_name):
    file = open("output/material/ui/accessory/paintjob_icons/%s.tobj" % icon_name, "wb")
    file.write(generate_tobj_string("/material/ui/accessory/paintjob_icons/%s.dds" % icon_name))
    file.close()

def make_def_folders(vehicle):
    if vehicle.make+" "+vehicle.model in unique_name.keys():
        filep = unique_name[vehicle.make+" "+vehicle.model]
    else:
        filep = vehicle.make+"."+vehicle.model
    if vehicle.trailer:
        make_folder("def/vehicle/trailer_owned/%s/paint_job/accessory" % filep)
    else:
        make_folder("def/vehicle/truck/%s/paint_job" % filep)
        if vehicle.accessories:
            make_folder("def/vehicle/truck/%s/paint_job/accessory" % filep)

def make_def_settings_sui(vehicle):
    if vehicle.trailer:
        veh_path = "trailer_owned"
    else:
        veh_path = "truck"
    if vehicle.make+" "+vehicle.model in unique_name.keys():
        filep = unique_name[vehicle.make+" "+vehicle.model]
    else:
        filep = vehicle.make+"."+vehicle.model
    file = open("output/def/vehicle/%s/%s/paint_job/%s_settings.sui" % (veh_path, filep, paintjob_name), "w")
    file.write("    name:     \"%s\"\n" % ingame_name)
    file.write("    price:    %s\n" % price)
    file.write("    unlock:   %s\n" % unlock_level)
    file.write("    airbrush: true\n")
    file.write("    icon:     \"paintjob_icons/%s_icon\"\n" % paintjob_name)
    if vehicle.model in ["t680", "579", "389", "vnl"]:
        file.write("    alternate_uvset: true\n")
    file.close()

def make_def_cabin_sii(vehicle, cabin):
    if vehicle.trailer:
        veh_path = "trailer_owned"
        name = paintjob_name
    else:
        veh_path = "truck"
        name = paintjob_name + "_" + cabin
    if vehicle.make+" "+vehicle.model in unique_name.keys():
        filep = unique_name[vehicle.make+" "+vehicle.model]
    else:
        filep = vehicle.make+"."+vehicle.model
    file = open("output/def/vehicle/%s/%s/paint_job/%s.sii" % (veh_path, filep, name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: %s.%s.paint_job\n" % (name, filep))
    file.write("{\n")
    file.write("@include \"%s_settings.sui\"\n" % paintjob_name)
    if vehicle.trailer:
        file.write("    paint_job_mask: \"/vehicle/trailer_owned/upgrade/paintjob/%s/shared_white.tobj\"\n" % paintjob_name)
    else:
        file.write("    suitable_for[]: \"%s.%s.cabin\"\n" % (vehicle.cabins[cabin], filep))
        file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_%s.tobj\"\n" % (paintjob_name, vehicle.make, vehicle.model, cabin))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_def_accessory_sii(vehicle, cabin):
    if vehicle.trailer:
        veh_path = "trailer_owned"
        name = paintjob_name
    else:
        veh_path = "truck"
        name = paintjob_name + "_" + cabin
    if vehicle.make+" "+vehicle.model in unique_name.keys():
        filep = unique_name[vehicle.make+" "+vehicle.model]
    else:
        filep = vehicle.make+"."+vehicle.model
    file = open("output/def/vehicle/%s/%s/paint_job/accessory/%s.sii" % (veh_path, filep, name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    ovr_counter = 0
    for key in vehicle.acc_dict.keys():
        file.write("\n")
        file.write("simple_paint_job_data: .ovr%s\n" % str(ovr_counter))
        file.write("{\n")
        if key[:12] == "shared_white":
            mask_path = "shared_white.tobj"
        else:
            mask_path = "%s_%s/%s.tobj" % (vehicle.make, vehicle.model, key)
        file.write("    paint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s\"\n" % (veh_path, paintjob_name, mask_path))
        for acc in vehicle.acc_dict[key]:
            file.write("    acc_list[]: \"%s\"\n" % acc)
        file.write("}\n")
        ovr_counter += 1
    file.write("}\n")
    file.close()

def make_vehicle_folders(vehicle):
    veh_path = "truck"
    if vehicle.trailer:
        veh_path = "trailer_owned"
    make_folder("vehicle/%s/upgrade/paintjob/%s/%s_%s" % (veh_path, paintjob_name, vehicle.make, vehicle.model))

def copy_vehicle_images(vehicle):
    if vehicle.trailer:
        veh_path = "trailer_owned"
    else:
        veh_path = "truck"
        shutil.copyfile("input/shared_white.dds", "output/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_a.dds" % (paintjob_name, vehicle.make, vehicle.model))
    shutil.copyfile("input/shared_white.dds", "output/vehicle/%s/upgrade/paintjob/%s/shared_white.dds" % (veh_path, paintjob_name))
    if vehicle.accessories:
        for acc_group in vehicle.acc_dict.keys():
            if acc_group[:12] != "shared_white":
                shutil.copyfile("input/shared_white.dds", "output/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.dds" % (veh_path, paintjob_name, vehicle.make, vehicle.model, acc_group))

def make_vehicle_tobjs(vehicle):
    if vehicle.trailer:
        veh_path = "trailer_owned"
    else:
        veh_path = "truck"
        for cabin in vehicle.cabins:
            file = open("output/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_%s.tobj" % (paintjob_name, vehicle.make, vehicle.model, cabin), "wb")
            file.write(generate_tobj_string("/vehicle/truck/upgrade/paintjob/%s/%s_%s/cabin_a.dds" % (paintjob_name, vehicle.make, vehicle.model)))
            file.close()
    file = open("output/vehicle/%s/upgrade/paintjob/%s/shared_white.tobj" % (veh_path, paintjob_name), "wb")
    file.write(generate_tobj_string("/vehicle/%s/upgrade/paintjob/%s/shared_white.dds" % (veh_path, paintjob_name)))
    file.close()
    if vehicle.accessories:
        for acc_group in vehicle.acc_dict.keys():
            if acc_group != "shared_white":
                file = open("output/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.tobj" % (veh_path, paintjob_name, vehicle.make, vehicle.model, acc_group), "wb")
                file.write(generate_tobj_string("/vehicle/%s/upgrade/paintjob/%s/%s_%s/%s.dds" % (veh_path, paintjob_name, vehicle.make, vehicle.model, acc_group)))
                file.close()

print("Reading input file")
file = open("input_paintjob.txt", "r")
input_paintjob = file.read().splitlines()
file.close()

ingame_name = input_paintjob[2]
price = input_paintjob[5]
unlock_level = input_paintjob[8]

pack_name = input_paintjob[12]
pack_author = input_paintjob[15]
pack_version = input_paintjob[18]

paintjob_name = input_paintjob[23]
supported_game = input_paintjob[26]
addon = input_paintjob[29]

file = open("database/description_info.txt", "r")
desc_info = file.read().splitlines()
file.close()

file = open("database/unique_name.txt", "r")
unique_name = dict(item.split(":") for item in file.read().splitlines())
file.close()

if addon == "false" and len(desc_info) > 0:
    answer = input("Overwrite description info file? (y/n): ")
    if answer == "n":
        sys.exit()
    elif answer == "y":
        desc_info = []

file = open("database/vehicle_packs.txt", "r")
vehicle_packs = dict(item.split(":") for item in file.read().splitlines())
file.close()

vehicle_list = []
for each_line in input_paintjob[65:]:
    if supported_game+" "+each_line in vehicle_packs.keys():
        for pack_veh in vehicle_packs[supported_game+" "+each_line].split(","):
            add_to_vehicle_list(pack_veh, len(vehicle_list), [])
    else:
        vehicle_entry = each_line.split(" ")
        vehicle = vehicle_entry[0]+" "+vehicle_entry[1]
        chosen_cabins = vehicle_entry[2:]
        add_to_vehicle_list(vehicle, len(vehicle_list), chosen_cabins)

print("Clearing output folder")
shutil.rmtree("output")
os.makedirs("output")

print("Making mod files")
if addon == "false": # who needs booleans when you have strings?
    make_manifest_file(pack_name, pack_author, pack_version)
    copy_manager_image()
    copy_manager_description()
    make_material_folders()
    icon_name = paintjob_name + "_icon"
    copy_material_image(icon_name)
    make_material_mat(icon_name)
    make_material_tobj(icon_name)

for vehicle in vehicle_list:
    print("Making paintjob for " + vehicle.name)
    make_def_folders(vehicle)
    make_def_settings_sui(vehicle)
    for cabin in vehicle.cabins.keys():
        make_def_cabin_sii(vehicle, cabin)
        if vehicle.accessories:
            make_def_accessory_sii(vehicle, cabin)
    make_vehicle_folders(vehicle)
    copy_vehicle_images(vehicle)
    make_vehicle_tobjs(vehicle)

print("Updating description file")
if len(desc_info) == 0:
    desc_info.append(supported_game)
for vehicle in vehicle_list:
    new_veh_entry = vehicle.make+" "+vehicle.model
    if new_veh_entry not in desc_info:
        desc_info.append(new_veh_entry)
file = open("database/description_info.txt", "w")
for entry in desc_info:
    file.write(entry+"\n")
file.close()

print("Complete!")
time.sleep(1.5)
