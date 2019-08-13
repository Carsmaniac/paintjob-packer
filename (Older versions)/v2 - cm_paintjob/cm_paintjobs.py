import os, shutil, binascii, codecs, time

def get_accessories(make, model):
    with open("cm_accessories/%s.%s.txt" % (make, model), "r") as file:
        return file.read().splitlines()

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

def make_folder(folder_name):
    if not os.path.exists("cm_output/%s" % folder_name):
        os.makedirs("cm_output/%s" % folder_name)

def make_manifest_file(pack_version, pack_name, pack_author):
    file = open("cm_output/manifest.sii", "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("mod_package: .package_name\n")
    file.write("{\n")
    file.write('    package_version:  "%s"\n' % pack_version)
    file.write('    display_name:     "%s"\n' % pack_name)
    file.write('    author:           "%s"\n' % pack_author)
    file.write("\n")
    file.write('    category[]:       "paint_job"\n')
    file.write("\n")
    file.write('    icon:             "Mod_Manager_Image.jpg"\n')
    file.write('    description_file: "Mod_Manager_Description.txt"\n')
    file.write("}\n")
    file.write("}\n")
    file.close()

def copy_manager_image():
    shutil.copyfile("cm_input/manager_image.jpg", "cm_output/Mod_Manager_Image.jpg")

def copy_manager_description():
    shutil.copyfile("cm_input/manager_description.txt", "cm_output/Mod_Manager_Description.txt")

def make_material_folders():
    make_folder("material/ui/accessory/Carsmaniacs_Paintjobs")

def copy_material_image(icon_name):
    shutil.copyfile("cm_input/material_image.dds", "cm_output/material/ui/accessory/Carsmaniacs_Paintjobs/%s.dds" % icon_name)

def make_material_mat(icon_name):
    file = open("cm_output/material/ui/accessory/Carsmaniacs_Paintjobs/%s.mat" % icon_name, "w")
    file.write('material: "ui"\n')
    file.write("{\n")
    file.write('    texture:      "%s.tobj"\n' % icon_name)
    file.write('    texture_name: "texture"\n')
    file.write("}\n")
    file.close()

def make_material_tobj(icon_name):
    file = open("cm_output/material/ui/accessory/Carsmaniacs_Paintjobs/%s.tobj" % icon_name, "wb")
    file.write(generate_tobj_string("/material/ui/accessory/Carsmaniacs_Paintjobs/%s.dds" % icon_name))
    file.close()

def make_def_folders(make, model, vehicle_type):
    if vehicle_type == "truck":
        make_folder("def/vehicle/truck/%s.%s/paint_job" % (make, model))
    elif vehicle_type == "truck_acc":
        make_folder("def/vehicle/truck/%s.%s/paint_job/accessory" % (make, model))
    elif vehicle_type == "trailer":
        make_folder("def/vehicle/trailer_owned/%s.%s/paint_job/accessory" % (make, model))

def make_def_sii(internal_name, make, model, cabins, ingame_name, price, unlock_level, icon_name, pack_name):
    if vehicle_type == "trailer":
        file = open("cm_output/def/vehicle/trailer_owned/%s.%s/paint_job/%s.sii" % (make, model, internal_name), "w")
    else:
        file = open("cm_output/def/vehicle/truck/%s.%s./paint_job/%s.sii" % (make, model, internal_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("accessory_paint_job_data: %s.%s.%s.paint_job\n" % (internal_name, make, model))
    file.write("{\n")
    file.write('    name:                 "%s"\n' % ingame_name)
    file.write("    price:                %s\n" % price)
    file.write("    unlock:               %s\n" % unlock_level)
    file.write('    icon:                 "Carsmaniacs_Paintjobs/%s"\n' % icon_name)
    file.write("    airbrush:             true\n")
    file.write("\n")
    if vehicle_type != "trailer":
        file.write('    paint_job_mask:       "/vehicle/truck/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s/%s.tobj"\n' % (pack_name, internal_name))
        file.write("\n")
        for each_cabin in cabins:
            file.write('    suitable_for[]: "%s.%s.%s.cabin"\n' % (each_cabin, make, model))
    else:
        file.write('    paint_job_mask:       "/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s/%s.tobj"\n' % (pack_name, internal_name))
    file.write("}\n")
    file.write("}\n")
    file.close()

def make_accessory_sii(internal_name, make, model, vehicle_type, model_accessories, pack_name):
    if vehicle_type == "trailer":
        file = open("cm_output/def/vehicle/trailer_owned/%s.%s/paint_job/accessory/%s.sii" % (make, model, internal_name), "w")
    else:
        file = open("cm_output/def/vehicle/truck/%s.%s/paint_job/accessory/%s.sii" % (make, model, internal_name), "w")
    file.write("SiiNunit\n")
    file.write("{\n")
    file.write("simple_paint_job_data: .ovr0\n")
    file.write("{\n")
    if vehicle_type == "trailer":
        file.write('    paint_job_mask: "/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s/shared_white.tobj"\n' % pack_name)
    else:
        file.write('    paint_job_mask: "/vehicle/truck/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s/shared_white.tobj"\n' % pack_name)
    for accessory in get_accessories(make, model_accessories):
        file.write('    acc_list[]: "%s"\n' % accessory)
    file.write("}\n")
    file.write("\n")
    file.write("}\n")
    file.close()

def make_vehicle_folders(vehicle_type, make, model, internal_name, pack_name):
    if vehicle_type == "trailer":
        make_folder("vehicle/trailer_owned/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s" % pack_name)
    else:
        make_folder("vehicle/truck/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s" % pack_name)

def copy_vehicle_image(vehicle_type, make, model, internal_name, pack_name):
    if vehicle_type == "trailer":
        shutil.copyfile("cm_input/vehicle_image.dds", "cm_output/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s/%s.dds" % (pack_name, internal_name))
    else:
        shutil.copyfile("cm_input/vehicle_image.dds", "cm_output/vehicle/truck/upgrade/paintjob/Carsmaniac\'s Paintjobs/%s/%s.dds" % (pack_name, internal_name))

def make_vehicle_tobj(vehicle_type, make, model, internal_name, pack_name):
    if vehicle_type == "trailer":
        file = open("cm_output/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac's Paintjobs/%s/%s.tobj" % (pack_name, internal_name), "wb")
        file.write(generate_tobj_string("/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac's Paintjobs/%s/%s.dds" % (pack_name, internal_name)))
    else:
        file = open("cm_output/vehicle/truck/upgrade/paintjob/Carsmaniac's Paintjobs/%s/%s.tobj" % (pack_name, internal_name), "wb")
        file.write(generate_tobj_string("/vehicle/truck/upgrade/paintjob/Carsmaniac's Paintjobs/%s/%s.dds" % (pack_name, internal_name)))
    file.close()

def copy_accessory_image(vehicle_type, make, model, internal_name, pack_name):
    if vehicle_type == "trailer":
        shutil.copyfile("cm_input/shared_white.dds", "cm_output/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac's Paintjobs/%s/shared_white.dds" % pack_name)
    else:
        shutil.copyfile("cm_input/shared_white.dds", "cm_output/vehicle/truck/upgrade/paintjob/Carsmaniac's Paintjobs/%s/shared_white.dds" % pack_name)

def make_accessory_tobj(vehicle_type, make, model, internal_name, pack_name):
    if vehicle_type == "trailer":
        file = open("cm_output/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac's Paintjobs/%s/shared_white.tobj" % pack_name, "wb")
        file.write(generate_tobj_string("/vehicle/trailer_owned/upgrade/paintjob/Carsmaniac's Paintjobs/%s/shared_white.dds" % pack_name))
    else:
        file = open("cm_output/vehicle/truck/upgrade/paintjob/Carsmaniac's Paintjobs/%s/shared_white.tobj" % pack_name, "wb")
        file.write(generate_tobj_string("/vehicle/truck/upgrade/paintjob/Carsmaniac's Paintjobs/%s/shared_white.dds" % pack_name))
    file.close()

cmfile = open("cm_paintjobs.txt","r")
params = cmfile.read().splitlines()
cmfile.close()

ingame_name = params[2]
price = params[5]
unlock_level = params[8]

pack_name = params[12]
pack_author = params[15]
pack_version = params[18]

icon_name = params[22]
addon = params[25]
del params[0:33]

shutil.rmtree("cm_output")
os.makedirs("cm_output")

if addon == "false": # who needs booleans when you have strings?
    make_manifest_file(pack_version, pack_name, pack_author)
    copy_manager_image()
    copy_manager_description()
    make_material_folders()
    copy_material_image(icon_name)
    make_material_mat(icon_name)
    make_material_tobj(icon_name)

for each_vehicle in params:
    vehicle = each_vehicle.split(";")
    internal_name = vehicle[0]
    vehicle_type = vehicle[1]
    make = vehicle[2]
    model = vehicle[3]
    if model == "box_ets":
        model = "box"
        model_accessories = "box.ets"
    elif model == "box_ats":
        model = "box"
        model_accessories = "box.ats"
    elif model == "flatbed_ets":
        model = "flatbed"
        model_accessories = "flatbed.ets"
    elif model == "flatbed_ats":
        model = "flatbed"
        model_accessories = "flatbed.ats"
    elif model == "gooseneck_ets":
        model = "gooseneck"
        model_accessories = "gooseneck.ets"
    elif model == "gooseneck_ats":
        model = "gooseneck"
        model_accessories = "gooseneck.ats"
    elif model == "log_ets":
        model = "log"
        model_accessories = "log.ets"
    elif model == "log_ats":
        model = "log"
        model_accessories = "log.ats"
    else:
        model_accessories = model
    if vehicle_type != "trailer":
        cabins = vehicle[4].split(",")
    else:
        cabins = None
    make_def_folders(make, model, vehicle_type)
    make_def_sii(internal_name, make, model, cabins, ingame_name, price, unlock_level, icon_name, pack_name)
    if vehicle_type != "truck":
        make_accessory_sii(internal_name, make, model, vehicle_type, model_accessories, pack_name)
    make_vehicle_folders(vehicle_type, make, model, internal_name, pack_name)
    copy_vehicle_image(vehicle_type, make, model, internal_name, pack_name)
    make_vehicle_tobj(vehicle_type, make, model, internal_name, pack_name)
    if vehicle_type != "truck":
        copy_accessory_image(vehicle_type, make, model, internal_name, pack_name)
        make_accessory_tobj(vehicle_type, make, model, internal_name, pack_name)

print("Success!") # wait to exit
time.sleep(2)
